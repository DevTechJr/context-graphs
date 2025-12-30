"""
Load Knowledge Base (Sample Policies)

This script populates the graph with realistic company policies that the agent
will reference when making decisions.

Policy Categories:
- Refunds: Rules about when/how to issue refunds
- Customer Service: VIP handling, escalation rules
- Service Level: Outage compensation, SLA policies
- Risk Management: High-value transaction approvals
"""

import json
from services.graph import (
    create_policy,
    create_policy_category,
    link_policy_to_category,
    link_policy_supersedes,
)


def load_policy_categories():
    """Create top-level policy categories."""
    print("Creating policy categories...")
    
    categories = [
        {"id": "cat-refunds", "name": "Refunds", "description": "Policies governing refund eligibility and processing"},
        {"id": "cat-customer-service", "name": "Customer Service", "description": "Customer support and VIP handling policies"},
        {"id": "cat-service-level", "name": "Service Level", "description": "SLA and service quality policies"},
        {"id": "cat-risk", "name": "Risk Management", "description": "Approval workflows for high-risk transactions"},
    ]
    
    for cat in categories:
        create_policy_category(cat["id"], cat)
        print(f"  ✓ {cat['name']}")


def load_refund_policies():
    """Create refund-related policies."""
    print("\nCreating refund policies...")
    
    # Policy 1: Non-Refundable Ticket Policy (Strict)
    create_policy("policy-refund-nonrefundable", {
        "name": "Non-Refundable Ticket Policy",
        "description": "Tickets marked as non-refundable cannot be refunded under normal circumstances",
        "severity": "strict",
        "tags": ["refund", "non_refundable"],
        "exception_allowed": True,
        "exception_conditions": "Service failures, VIP customers, or repeated service issues",
        "requires_approval": True,
        "approval_level": "manager",
        "active": True,
    })
    link_policy_to_category("policy-refund-nonrefundable", "cat-refunds")
    print("  ✓ Non-Refundable Ticket Policy (strict, requires manager approval for exceptions)")
    
    # Policy 2: Standard Refund Policy (Moderate)
    create_policy("policy-refund-standard", {
        "name": "Standard Refund Policy",
        "description": "Refundable purchases can be refunded within 30 days",
        "severity": "moderate",
        "tags": ["refund", "standard"],
        "refund_window_days": 30,
        "exception_allowed": False,
        "requires_approval": False,
        "active": True,
    })
    link_policy_to_category("policy-refund-standard", "cat-refunds")
    print("  ✓ Standard Refund Policy (30-day window, no approval needed)")
    
    # Policy 3: Partial Refund Policy (Flexible)
    create_policy("policy-refund-partial", {
        "name": "Partial Refund Policy",
        "description": "Pro-rated refunds based on usage",
        "severity": "flexible",
        "tags": ["refund", "partial", "prorated"],
        "calculation": "Refund = (Days Remaining / Total Days) * Purchase Price",
        "exception_allowed": True,
        "requires_approval": False,
        "active": True,
    })
    link_policy_to_category("policy-refund-partial", "cat-refunds")
    print("  ✓ Partial Refund Policy (pro-rated, no approval)")


def load_customer_service_policies():
    """Create customer service and VIP policies."""
    print("\nCreating customer service policies...")
    
    # Policy 4: VIP Customer Exception Policy
    create_policy("policy-vip-exception", {
        "name": "VIP Customer Exception Policy",
        "description": "VIP and Enterprise customers can override standard policies",
        "severity": "flexible",
        "tags": ["vip", "exception", "customer_service"],
        "applicable_tiers": ["VIP", "Enterprise", "Platinum"],
        "exception_limit_usd": 500,  # Auto-approve up to $500
        "exception_conditions": "Any policy can be overridden for customer retention",
        "requires_approval": True,
        "approval_level": "manager_if_over_500",
        "active": True,
    })
    link_policy_to_category("policy-vip-exception", "cat-customer-service")
    print("  ✓ VIP Exception Policy (auto-approve < $500, manager approval > $500)")
    
    # Policy 5: Customer Retention Policy
    create_policy("policy-retention", {
        "name": "Customer Retention Policy",
        "description": "Agents can offer goodwill gestures to retain at-risk customers",
        "severity": "moderate",
        "tags": ["retention", "customer_service", "churn"],
        "goodwill_options": ["credit", "discount", "refund", "upgrade"],
        "max_value_usd": 250,
        "requires_approval": False,
        "active": True,
    })
    link_policy_to_category("policy-retention", "cat-customer-service")
    print("  ✓ Customer Retention Policy (up to $250 goodwill, no approval)")


def load_service_level_policies():
    """Create SLA and service quality policies."""
    print("\nCreating service level policies...")
    
    # Policy 6: Service Outage Compensation Policy
    create_policy("policy-outage-compensation", {
        "name": "Service Outage Compensation Policy",
        "description": "Customers affected by service outages are eligible for compensation",
        "severity": "moderate",
        "tags": ["outage", "sla", "compensation"],
        "compensation_tiers": json.dumps({
            "minor": "10% credit",
            "major": "25% credit or partial refund",
            "critical": "full refund"
        }),
        "requires_verification": True,
        "verification_source": "support_ticket",
        "requires_approval": False,
        "active": True,
    })
    link_policy_to_category("policy-outage-compensation", "cat-service-level")
    print("  ✓ Outage Compensation Policy (tiered compensation, requires ticket verification)")
    
    # Policy 7: SLA Breach Policy
    create_policy("policy-sla-breach", {
        "name": "SLA Breach Policy",
        "description": "Automatic compensation when SLA commitments are not met",
        "severity": "strict",
        "tags": ["sla", "breach", "enterprise"],
        "applicable_tiers": ["Enterprise", "Platinum"],
        "compensation": "As defined in customer contract",
        "automatic": True,
        "requires_approval": False,
        "active": True,
    })
    link_policy_to_category("policy-sla-breach", "cat-service-level")
    print("  ✓ SLA Breach Policy (automatic compensation for Enterprise customers)")


def load_risk_management_policies():
    """Create approval and escalation policies."""
    print("\nCreating risk management policies...")
    
    # Policy 8: High-Value Transaction Escalation
    create_policy("policy-high-value-escalation", {
        "name": "High-Value Transaction Escalation Policy",
        "description": "Transactions above threshold require executive approval",
        "severity": "strict",
        "tags": ["escalation", "risk", "high_value"],
        "thresholds": json.dumps({
            "manager_approval": 1000,
            "vp_approval": 5000,
            "cfo_approval": 25000
        }),
        "requires_approval": True,
        "approval_level": "tiered",
        "active": True,
    })
    link_policy_to_category("policy-high-value-escalation", "cat-risk")
    print("  ✓ High-Value Escalation Policy (tiered approvals: Manager > $1k, VP > $5k, CFO > $25k)")
    
    # Policy 9: Fraud Prevention Policy
    create_policy("policy-fraud-prevention", {
        "name": "Fraud Prevention Policy",
        "description": "Suspicious transactions must be reviewed before processing",
        "severity": "strict",
        "tags": ["fraud", "security", "risk"],
        "red_flags": ["multiple_refund_requests", "account_age_under_30_days", "high_value_first_purchase"],
        "action": "hold_for_review",
        "requires_approval": True,
        "approval_level": "security_team",
        "active": True,
    })
    link_policy_to_category("policy-fraud-prevention", "cat-risk")
    print("  ✓ Fraud Prevention Policy (hold suspicious transactions for security review)")


def load_all_policies():
    """Load the complete knowledge base."""
    print("=" * 60)
    print("LOADING KNOWLEDGE BASE (Sample Policies)")
    print("=" * 60)
    
    load_policy_categories()
    load_refund_policies()
    load_customer_service_policies()
    load_service_level_policies()
    load_risk_management_policies()
    
    print("\n" + "=" * 60)
    print("✓ Knowledge base loaded successfully!")
    print("=" * 60)
    print("\nPolicies created:")
    print("  - 4 Policy Categories")
    print("  - 9 Policies across different severities (strict, moderate, flexible)")
    print("\nYou can query these in Neo4j Browser:")
    print("  MATCH (p:Policy)-[:PART_OF]->(pc:PolicyCategory) RETURN p, pc")
    print("\nOr via code:")
    print("  query_policies_by_category('Refunds')")
    print("  query_policies_by_tags(['vip', 'exception'])")


if __name__ == "__main__":
    load_all_policies()
