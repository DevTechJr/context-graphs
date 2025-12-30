"""
Decision Orchestration Service

This is the "brain" of the Context Graph system. It orchestrates the full
decision-making flow:

1. User submits request (e.g., "Customer wants refund")
2. Query knowledge base for relevant policies
3. Search for similar past decisions (precedents)
4. Gather evidence (customer history, tickets)
5. LLM synthesizes all context → decision + reasoning
6. Record decision trace in Neo4j

This demonstrates the core thesis: AI agents making decisions informed by
organizational memory (policies + precedents + evidence).
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from Config.llm import llm
from services.graph import (
    query_policies_by_tags,
    search_similar_decisions,
    create_decision,
    create_actor,
    link_actor_made_decision,
    link_decision_justified_by_evidence,
    link_decision_overrides_policy,
    link_decision_follows_policy,
    add_embedding_to_decision,
)
from utils.visual_logging import (
    print_header,
    print_step,
    print_success,
    print_info,
    print_metric,
    print_policies,
    print_precedents,
    print_decision_box,
    print_trace_summary,
)


def extract_tags_from_request(request: str) -> List[str]:
    """Extract relevant tags from user request for policy matching.
    
    In production, this would use NER or a small classifier.
    For now, simple keyword matching.
    """
    keywords = {
        "refund": ["refund"],
        "discount": ["discount", "vip", "exception"],
        "vip": ["vip", "exception", "customer_service"],
        "outage": ["outage", "sla", "compensation"],
        "enterprise": ["vip", "exception"],
        "exception": ["exception"],
        "escalation": ["escalation", "high_value"],
    }
    
    tags = set()
    request_lower = request.lower()
    
    for keyword, tag_list in keywords.items():
        if keyword in request_lower:
            tags.update(tag_list)
    
    # Always include basic tags
    tags.add("refund")  # Most common case
    
    return list(tags)


def build_decision_prompt(
    request: str,
    policies: List[Dict[str, Any]],
    precedents: List[Dict[str, Any]],
    evidence: Optional[List[Dict[str, Any]]] = None
) -> str:
    """Build the LLM prompt with all context."""
    
    prompt = f"""You are an AI decision agent for a SaaS company. A customer has made a request that requires a decision.

CUSTOMER REQUEST:
{request}

"""
    
    # Add policies
    if policies:
        prompt += "RELEVANT COMPANY POLICIES:\n"
        for i, policy in enumerate(policies, 1):
            prompt += f"{i}. {policy.get('name', 'Unknown Policy')}\n"
            prompt += f"   Description: {policy.get('description', 'N/A')}\n"
            prompt += f"   Severity: {policy.get('severity', 'N/A')}\n"
            if policy.get('requires_approval'):
                prompt += f"   Requires Approval: {policy.get('approval_level', 'Yes')}\n"
            if policy.get('exception_conditions'):
                prompt += f"   Exceptions: {policy.get('exception_conditions')}\n"
            prompt += "\n"
    
    # Add precedents
    if precedents:
        prompt += "SIMILAR PAST DECISIONS (Precedents):\n"
        for i, prec in enumerate(precedents, 1):
            decision = prec["decision"]
            similarity = prec["similarity"]
            prompt += f"{i}. (Similarity: {similarity:.2f}) {decision.get('prompt', 'N/A')}\n"
            prompt += f"   Decision: {decision.get('response', 'N/A')}\n"
            prompt += f"   Reasoning: {decision.get('reasoning', 'N/A')}\n"
            prompt += "\n"
    
    # Add evidence
    if evidence:
        prompt += "EVIDENCE (Customer Context):\n"
        for i, ev in enumerate(evidence, 1):
            # Handle both string evidence and dict evidence
            if isinstance(ev, str):
                prompt += f"{i}. {ev}\n"
            else:
                prompt += f"{i}. {ev.get('type', 'Unknown')}: {ev.get('description', ev.get('issue', 'N/A'))}\n"
        prompt += "\n"
    
    prompt += """INSTRUCTIONS:
Based on the above context, make a decision. You must:

1. DECISION: State clearly "APPROVE" or "DENY" or "ESCALATE"
2. CONFIDENCE: Provide a confidence score (0.0 to 1.0)
3. REASONING: Explain your reasoning in 2-3 sentences
4. POLICIES: List which policies you followed or overrode
5. PRECEDENTS: Mention if precedents influenced your decision

Format your response as:
DECISION: [APPROVE/DENY/ESCALATE]
CONFIDENCE: [0.0-1.0]
REASONING: [Your explanation]
POLICIES: [Policy names you considered]
PRECEDENTS: [Yes/No - did precedents influence this?]
"""
    
    return prompt


def parse_llm_response(response: str) -> Dict[str, Any]:
    """Parse the structured LLM response."""
    lines = response.strip().split("\n")
    result = {
        "decision": "UNKNOWN",
        "confidence": 0.5,
        "reasoning": "",
        "policies_mentioned": [],
        "used_precedents": False
    }
    
    for line in lines:
        if line.startswith("DECISION:"):
            result["decision"] = line.split(":", 1)[1].strip()
        elif line.startswith("CONFIDENCE:"):
            try:
                result["confidence"] = float(line.split(":", 1)[1].strip())
            except:
                pass
        elif line.startswith("REASONING:"):
            result["reasoning"] = line.split(":", 1)[1].strip()
        elif line.startswith("POLICIES:"):
            result["policies_mentioned"] = line.split(":", 1)[1].strip()
        elif line.startswith("PRECEDENTS:"):
            val = line.split(":", 1)[1].strip().lower()
            result["used_precedents"] = "yes" in val
    
    return result


def decide(
    request: str,
    evidence: Optional[List[Dict[str, Any]]] = None,
    actor_id: str = "agent-ai-001",
    actor_name: str = "DecisionBot",
    database: Optional[str] = None
) -> Dict[str, Any]:
    """
    Main decision orchestration function.
    
    This is the core of the Context Graph system. It:
    1. Queries policies from knowledge base
    2. Searches for similar precedents
    3. Calls LLM with full context
    4. Records decision trace in Neo4j
    
    Args:
        request: User's decision request
        evidence: Optional list of evidence dicts
        actor_id: ID of the agent making the decision
        actor_name: Display name of the agent
        database: Neo4j database name
    
    Returns:
        Dict with decision, reasoning, and trace metadata
    """
    print_header("DECISION ORCHESTRATION FLOW")
    print_info(f"Request: {request}", indent=0)
    
    # Step 1: Extract tags and query policies
    print_step(1, 6, "Querying knowledge base for relevant policies...")
    tags = extract_tags_from_request(request)
    print_metric("Tags extracted", ", ".join(tags))
    policies = query_policies_by_tags(tags, database=database)
    print_metric("Policies found", len(policies))
    if policies:
        print_policies(policies, max_display=5)
    
    # Step 2: Search for precedents
    print_step(2, 6, "Searching for similar past decisions (precedents)...")
    precedents = search_similar_decisions(request, top_k=5, database=database)
    print_metric("Precedents found", len(precedents))
    if precedents:
        print_precedents(precedents, max_display=3)
    
    # Step 3: Build LLM prompt
    print_step(3, 6, "Building LLM prompt with full context...")
    prompt = build_decision_prompt(request, policies, precedents, evidence)
    print_success(f"Prompt built ({len(prompt)} characters)")
    
    # Step 4: Call LLM
    print_step(4, 6, "Calling LLM for decision (gpt-4.1-nano)...")
    llm_response = llm.invoke(prompt)
    response_text = llm_response.content
    print_success("LLM response received")
    
    # Step 5: Parse response
    print_step(5, 6, "Parsing LLM response...")
    parsed = parse_llm_response(response_text)
    print_decision_box(parsed['decision'], parsed['confidence'], parsed['reasoning'])
    
    # Step 6: Record decision trace
    print_step(6, 6, "Recording decision trace in Neo4j...")
    decision_id = f"dec-{uuid.uuid4().hex[:12]}"
    
    # Create decision node
    create_decision(decision_id, {
        "prompt": request,
        "response": parsed["decision"],
        "confidence": parsed["confidence"],
        "reasoning": parsed["reasoning"],
        "policies_mentioned": parsed["policies_mentioned"],
        "used_precedents": parsed["used_precedents"],
        "created_at": datetime.now().isoformat(),
        "llm_model": "gpt-4.1-nano",
    }, database=database)
    
    # Add embedding for future precedent searches
    add_embedding_to_decision(decision_id, database=database)
    
    # Create actor if not exists
    create_actor(actor_id, {
        "name": actor_name,
        "type": "ai_agent",
        "model": "gpt-4.1-nano",
    }, database=database)
    
    # Link actor to decision
    link_actor_made_decision(actor_id, decision_id, database=database)
    
    # Link evidence if provided
    if evidence:
        for ev in evidence:
            # Handle both string evidence and dict evidence
            if isinstance(ev, dict):
                ev_id = ev.get("id")
                if ev_id:
                    link_decision_justified_by_evidence(decision_id, ev_id, database=database)
            # If evidence is a string, we could create an evidence node here
            # For now, we'll just skip linking (evidence is embedded in the prompt)
    
    # Link policies (simplified: link to first policy as example)
    if policies:
        # In production, would parse which policies were actually used
        link_decision_follows_policy(decision_id, policies[0]["id"], database=database)
    
    print_success(f"Decision recorded: {decision_id}")
    print_trace_summary(
        decision_id=decision_id,
        policies_count=len(policies),
        precedents_count=len(precedents),
        used_precedents=parsed["used_precedents"]
    )
    
    # Convert Neo4j objects to dictionaries for JSON serialization
    policies_dict = []
    if policies:
        for p in policies:
            if isinstance(p, dict):
                policies_dict.append(p)
            else:
                # Neo4j node object - convert to dict
                policies_dict.append(dict(p))
    
    precedents_dict = []
    if precedents:
        for prec in precedents:
            # precedents from search_similar_decisions() have structure: {"decision": {...}, "similarity": score}
            if isinstance(prec, dict):
                # If it has a "decision" key, it's from search_similar_decisions - unwrap it
                if "decision" in prec:
                    decision_data = prec["decision"]
                    if isinstance(decision_data, dict):
                        decision_data["similarity"] = prec.get("similarity", 0.0)
                        precedents_dict.append(decision_data)
                    else:
                        # Convert Neo4j node to dict
                        decision_dict = dict(decision_data)
                        decision_dict["similarity"] = prec.get("similarity", 0.0)
                        precedents_dict.append(decision_dict)
                else:
                    # Already a flat dict, just add it
                    precedents_dict.append(prec)
            else:
                # Neo4j node object
                precedents_dict.append(dict(prec))
    
    # DEBUG: Verify data is populated
    print_success(f"Data serialization complete: {len(policies_dict)} policies, {len(precedents_dict)} precedents")
    
    return {
        "decision_id": decision_id,
        "decision": parsed["decision"],
        "confidence": parsed["confidence"],
        "reasoning": parsed["reasoning"],
        "policies_considered": len(policies),
        "precedents_found": len(precedents),
        "used_precedents": parsed["used_precedents"],
        # Include full details for UI display
        "policies_details": policies_dict,
        "precedents_details": precedents_dict,
        "neo4j_uri": "neo4j+s://7d50579e.databases.neo4j.io",
        "llm_response": response_text,
    }


