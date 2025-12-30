"""
Rich Decision Trace Example

This script demonstrates the Context Graph concept by creating a realistic
decision scenario with all supporting context:

Scenario:
- Customer (cust-vip-789) requests refund for non-refundable ticket
- Agent (agent-ai-001) checks policy (normally denied)
- Agent finds evidence (3 recent outages for this customer)
- Agent searches for precedents (finds similar exception granted before)
- Manager (mgr-jane) approves override
- Decision recorded with full trace

This creates a queryable graph showing WHY the decision was made.
"""

import os
from datetime import datetime
from services.graph import (
    create_actor,
    create_decision,
    create_evidence,
    create_policy,
    create_approval,
    link_actor_made_decision,
    link_decision_justified_by_evidence,
    link_decision_overrides_policy,
    link_approval_approved_decision,
    get_decision_subgraph,
)


def create_rich_trace():
    # Step 1: Create the AI agent (actor)
    print("Creating Actor (AI agent)...")
    create_actor("agent-ai-001", {
        "name": "RefundBot v2",
        "type": "ai_agent",
        "model": "gpt-4o-mini",
    })
    
    # Step 2: Create the manager (approver)
    print("Creating Actor (Manager)...")
    create_actor("mgr-jane", {
        "name": "Jane Smith",
        "type": "human",
        "role": "Customer Success Manager",
    })
    
    # Step 3: Create evidence (customer had outages)
    print("Creating Evidence (support tickets)...")
    create_evidence("ticket-001", {
        "type": "support_ticket",
        "customer_id": "cust-vip-789",
        "issue": "Service outage - unable to access platform",
        "created_at": "2025-12-20T10:30:00Z",
        "severity": "high",
    })
    
    create_evidence("ticket-002", {
        "type": "support_ticket",
        "customer_id": "cust-vip-789",
        "issue": "Billing error - double charge",
        "created_at": "2025-12-22T14:15:00Z",
        "severity": "medium",
    })
    
    create_evidence("ticket-003", {
        "type": "support_ticket",
        "customer_id": "cust-vip-789",
        "issue": "Data sync failure",
        "created_at": "2025-12-27T09:00:00Z",
        "severity": "high",
    })
    
    # Step 4: Create policy (no refunds for non-refundable tickets)
    print("Creating Policy...")
    create_policy("policy-refund-001", {
        "name": "Non-Refundable Ticket Policy",
        "description": "Tickets marked as non-refundable cannot be refunded except in exceptional circumstances",
        "severity": "strict",
        "exception_allowed": True,
        "requires_approval": True,
    })
    
    # Step 5: Create approval (manager override)
    print("Creating Approval...")
    create_approval("approval-001", {
        "approver": "mgr-jane",
        "approved_at": datetime.now().isoformat(),
        "reason": "Customer experienced multiple service disruptions; goodwill gesture",
        "approval_type": "policy_override",
    })
    
    # Step 6: Create the decision
    print("Creating Decision...")
    decision_id = "dec-refund-vip-789"
    create_decision(decision_id, {
        "customer_id": "cust-vip-789",
        "ticket_type": "non-refundable",
        "amount": 299.99,
        "currency": "USD",
        "prompt": "Customer cust-vip-789 requests full refund for non-refundable annual subscription",
        "response": "Approved",
        "confidence": 0.87,
        "reasoning": "Customer experienced 3 service disruptions in the past week. Precedent exists for granting refunds in similar cases. Manager approval obtained.",
        "policy_tags": ["refund", "non_refundable", "exception"],
        "created_at": datetime.now().isoformat(),
    })
    
    # Step 7: Create relationships (build the graph)
    print("Creating relationships...")
    link_actor_made_decision("agent-ai-001", decision_id)
    link_decision_justified_by_evidence(decision_id, "ticket-001")
    link_decision_justified_by_evidence(decision_id, "ticket-002")
    link_decision_justified_by_evidence(decision_id, "ticket-003")
    link_decision_overrides_policy(decision_id, "policy-refund-001")
    link_approval_approved_decision("approval-001", decision_id)
    
    print(f"\n✓ Rich decision trace created: {decision_id}")
    print("\nYou can now query this in Neo4j Browser:")
    print(f'  MATCH (d:Decision {{id: "{decision_id}"}}) RETURN d')
    print("\nOr get the full subgraph:")
    print(f'  MATCH path = (d:Decision {{id: "{decision_id}"}})-[*0..1]-() RETURN path')
    
    return decision_id


def show_subgraph(decision_id):
    """Retrieve and display the decision subgraph"""
    print(f"\nRetrieving subgraph for {decision_id}...")
    subgraph = get_decision_subgraph(decision_id)
    
    print("\n=== DECISION TRACE ===")
    print(f"Decision: {subgraph['decision']}")
    print(f"\nActors ({len(subgraph['actors'])}):")
    for actor in subgraph['actors']:
        print(f"  - {actor.get('name')} ({actor.get('type')})")
    
    print(f"\nEvidence ({len(subgraph['evidence'])}):")
    for ev in subgraph['evidence']:
        print(f"  - {ev.get('type')}: {ev.get('issue')}")
    
    print(f"\nPolicies Overridden ({len(subgraph['policies'])}):")
    for policy in subgraph['policies']:
        print(f"  - {policy.get('name')}")
    
    print(f"\nApprovals ({len(subgraph['approvals'])}):")
    for approval in subgraph['approvals']:
        print(f"  - Approver: {approval.get('approver')} | Reason: {approval.get('reason')}")


if __name__ == "__main__":
    decision_id = create_rich_trace()
    show_subgraph(decision_id)
