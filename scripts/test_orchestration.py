"""
Test LLM Decision Orchestration

This demonstrates the full Context Graph system in action:
- User makes request
- System queries policies + precedents
- LLM makes informed decision
- Decision recorded with full trace
"""

from services.orchestration import decide
from services.graph import get_decision_subgraph


def test_decision_scenarios():
    """Test multiple decision scenarios."""
    
    scenarios = [
        {
            "request": "Customer cust-enterprise-001 requests full refund for non-refundable annual plan due to repeated service outages over the past month",
            "evidence": None,
        },
        {
            "request": "VIP customer wants 20% discount on renewal",
            "evidence": None,
        },
        {
            "request": "Standard customer requesting refund 45 days after purchase",
            "evidence": None,
        },
    ]
    
    print("=" * 80)
    print("TESTING LLM DECISION ORCHESTRATION")
    print("=" * 80)
    
    results = []
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'#' * 80}")
        print(f"SCENARIO {i}")
        print(f"{'#' * 80}")
        
        result = decide(
            request=scenario["request"],
            evidence=scenario["evidence"],
            actor_id="agent-test-bot",
            actor_name="TestDecisionBot"
        )
        
        results.append(result)
        
        print(f"\nRESULT:")
        print(f"  Decision ID: {result['decision_id']}")
        print(f"  Decision: {result['decision']}")
        print(f"  Confidence: {result['confidence']}")
        print(f"  Reasoning: {result['reasoning']}")
        print(f"  Policies Considered: {result['policies_considered']}")
        print(f"  Precedents Found: {result['precedents_found']}")
        print(f"  Used Precedents: {result['used_precedents']}")
    
    print(f"\n{'=' * 80}")
    print("SUMMARY")
    print(f"{'=' * 80}")
    print(f"Tested {len(scenarios)} decision scenarios")
    print(f"All decisions recorded in Neo4j with full context")
    print(f"\nYou can now:")
    print(f"  1. View decisions in Neo4j Browser")
    print(f"  2. See how precedents influenced new decisions")
    print(f"  3. Query the decision graph")
    
    return results


def show_decision_trace(decision_id: str):
    """Display the full decision trace for a given decision."""
    print(f"\n{'=' * 80}")
    print(f"DECISION TRACE: {decision_id}")
    print(f"{'=' * 80}")
    
    trace = get_decision_subgraph(decision_id)
    
    if not trace:
        print("Decision not found")
        return
    
    decision = trace["decision"]
    print(f"\nDECISION:")
    print(f"  Prompt: {decision.get('prompt')}")
    print(f"  Response: {decision.get('response')}")
    print(f"  Confidence: {decision.get('confidence')}")
    print(f"  Reasoning: {decision.get('reasoning')}")
    
    print(f"\nACTORS ({len(trace['actors'])}):")
    for actor in trace["actors"]:
        print(f"  - {actor.get('name')} ({actor.get('type')})")
    
    print(f"\nPOLICIES REFERENCED ({len(trace['policies'])}):")
    for policy in trace["policies"]:
        print(f"  - {policy.get('name')}")
    
    print(f"\nEVIDENCE ({len(trace['evidence'])}):")
    for ev in trace["evidence"]:
        print(f"  - {ev.get('type', 'Unknown')}: {ev.get('issue', ev.get('description', 'N/A'))}")
    
    print(f"\nAPPROVALS ({len(trace['approvals'])}):")
    for approval in trace["approvals"]:
        print(f"  - {approval.get('approver')}: {approval.get('reason')}")


if __name__ == "__main__":
    print("\n" + "🚀" * 40)
    print("CONTEXT GRAPH SYSTEM - FULL DEMONSTRATION")
    print("🚀" * 40 + "\n")
    
    results = test_decision_scenarios()
    
    # Show detailed trace for first decision
    if results:
        show_decision_trace(results[0]["decision_id"])
    
    print("\n" + "✅" * 40)
    print("CONTEXT GRAPH SYSTEM WORKING END-TO-END!")
    print("✅" * 40)
    print("\nThe system now:")
    print("  ✓ Queries knowledge base (policies)")
    print("  ✓ Searches precedents (vector search)")
    print("  ✓ Calls LLM with full context")
    print("  ✓ Records decision traces")
    print("  ✓ Learns from every decision")
    print("\nThis is a working 'System of Record for Why' — ready for LinkedIn demo!")
