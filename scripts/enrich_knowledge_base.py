"""
Enrich Knowledge Base

This adds more realistic organizational knowledge:
- Product Tiers (Free, Pro, VIP, Enterprise)
- Customer Segments
- Approval Workflows
- Additional policies (security, billing, compliance)
"""

import json
from services.graph import (
    create_policy,
    create_policy_category,
    link_policy_to_category,
    link_policy_supersedes,
)


def create_product_tiers():
    """Create product tier nodes with benefits and rules."""
    print("\nCreating product tiers...")
    
    from services.graph import _get_driver
    driver = _get_driver()
    
    tiers = [
        {
            "id": "tier-free",
            "name": "Free",
            "price_monthly": 0,
            "refund_eligible": False,
            "support_level": "community",
            "exception_priority": "low",
        },
        {
            "id": "tier-pro",
            "name": "Professional",
            "price_monthly": 49,
            "refund_eligible": True,
            "refund_window_days": 30,
            "support_level": "email",
            "exception_priority": "medium",
        },
        {
            "id": "tier-vip",
            "name": "VIP",
            "price_monthly": 199,
            "refund_eligible": True,
            "refund_window_days": 60,
            "support_level": "priority",
            "exception_priority": "high",
            "auto_approve_exceptions_under": 500,
        },
        {
            "id": "tier-enterprise",
            "name": "Enterprise",
            "price_monthly": "custom",
            "refund_eligible": True,
            "refund_window_days": 90,
            "support_level": "dedicated",
            "exception_priority": "highest",
            "auto_approve_exceptions_under": 2000,
            "sla_guaranteed": True,
        },
    ]
    
    with driver:
        session = driver.session()
        with session:
            for tier in tiers:
                cypher = "MERGE (t:ProductTier {id: $id}) SET t += $props"
                session.run(cypher, id=tier["id"], props=tier)
                print(f"  ✓ {tier['name']} tier")


def create_approval_workflows():
    """Create approval workflow nodes."""
    print("\nCreating approval workflows...")
    
    from services.graph import _get_driver
    driver = _get_driver()
    
    workflows = [
        {
            "id": "workflow-standard",
            "name": "Standard Approval",
            "description": "Agent → Manager",
            "steps": json.dumps(["agent_review", "manager_approval"]),
            "max_amount": 1000,
        },
        {
            "id": "workflow-high-value",
            "name": "High Value Approval",
            "description": "Agent → Manager → VP",
            "steps": json.dumps(["agent_review", "manager_approval", "vp_approval"]),
            "max_amount": 10000,
        },
        {
            "id": "workflow-executive",
            "name": "Executive Approval",
            "description": "Agent → Manager → VP → CFO",
            "steps": json.dumps(["agent_review", "manager_approval", "vp_approval", "cfo_approval"]),
            "max_amount": None,
        },
        {
            "id": "workflow-auto",
            "name": "Automatic Approval",
            "description": "Auto-approved by policy",
            "steps": json.dumps(["auto_approve"]),
            "max_amount": 250,
        },
    ]
    
    with driver:
        session = driver.session()
        with session:
            for wf in workflows:
                cypher = "MERGE (w:ApprovalWorkflow {id: $id}) SET w += $props"
                session.run(cypher, id=wf["id"], props=wf)
                print(f"  ✓ {wf['name']}")


def add_billing_policies():
    """Add billing and payment policies."""
    print("\nAdding billing policies...")
    
    # Policy: Late Payment Grace Period
    create_policy("policy-billing-grace", {
        "name": "Late Payment Grace Period",
        "description": "Customers have 7-day grace period before service suspension",
        "severity": "moderate",
        "tags": ["billing", "payment", "grace_period"],
        "grace_period_days": 7,
        "suspension_after_days": 7,
        "requires_approval": False,
        "active": True,
    })
    link_policy_to_category("policy-billing-grace", "cat-billing")
    print("  ✓ Late Payment Grace Period")
    
    # Policy: Payment Plan Eligibility
    create_policy("policy-payment-plan", {
        "name": "Payment Plan Eligibility",
        "description": "Customers can request payment plans for amounts over $500",
        "severity": "flexible",
        "tags": ["billing", "payment_plan"],
        "minimum_amount": 500,
        "max_installments": 6,
        "requires_approval": True,
        "approval_level": "manager",
        "active": True,
    })
    link_policy_to_category("policy-payment-plan", "cat-billing")
    print("  ✓ Payment Plan Eligibility")


def add_security_policies():
    """Add security and compliance policies."""
    print("\nAdding security policies...")
    
    # Policy: Data Access Request
    create_policy("policy-data-access", {
        "name": "Customer Data Access Request Policy",
        "description": "GDPR/CCPA data access requests must be fulfilled within 30 days",
        "severity": "strict",
        "tags": ["security", "gdpr", "compliance", "data"],
        "response_deadline_days": 30,
        "requires_approval": True,
        "approval_level": "compliance_team",
        "active": True,
    })
    link_policy_to_category("policy-data-access", "cat-compliance")
    print("  ✓ Data Access Request Policy (GDPR)")
    
    # Policy: Account Deletion
    create_policy("policy-account-deletion", {
        "name": "Account Deletion Policy",
        "description": "Account deletions processed within 48 hours with data retention as per policy",
        "severity": "strict",
        "tags": ["security", "account", "deletion", "gdpr"],
        "processing_time_hours": 48,
        "data_retention_days": 90,
        "requires_approval": False,
        "active": True,
    })
    link_policy_to_category("policy-account-deletion", "cat-compliance")
    print("  ✓ Account Deletion Policy")
    
    # Policy: Suspicious Activity
    create_policy("policy-suspicious-activity", {
        "name": "Suspicious Activity Policy",
        "description": "Accounts flagged for suspicious activity require security review",
        "severity": "strict",
        "tags": ["security", "fraud", "risk"],
        "auto_suspend": True,
        "review_required": True,
        "requires_approval": True,
        "approval_level": "security_team",
        "active": True,
    })
    link_policy_to_category("policy-suspicious-activity", "cat-risk")
    print("  ✓ Suspicious Activity Policy")


def add_upgrade_downgrade_policies():
    """Add subscription change policies."""
    print("\nAdding subscription change policies...")
    
    # Policy: Pro-rated Upgrades
    create_policy("policy-upgrade-prorated", {
        "name": "Pro-rated Upgrade Policy",
        "description": "Upgrades are pro-rated and effective immediately",
        "severity": "flexible",
        "tags": ["upgrade", "billing", "prorated"],
        "immediate_effect": True,
        "prorated_charge": True,
        "requires_approval": False,
        "active": True,
    })
    link_policy_to_category("policy-upgrade-prorated", "cat-billing")
    print("  ✓ Pro-rated Upgrade Policy")
    
    # Policy: Downgrade Restrictions
    create_policy("policy-downgrade-restrictions", {
        "name": "Downgrade Restriction Policy",
        "description": "Downgrades effective at end of billing cycle; annual plans require manager approval",
        "severity": "moderate",
        "tags": ["downgrade", "billing"],
        "effective_date": "end_of_cycle",
        "annual_plan_approval_required": True,
        "requires_approval": False,
        "active": True,
    })
    link_policy_to_category("policy-downgrade-restrictions", "cat-billing")
    print("  ✓ Downgrade Restriction Policy")


def add_additional_categories():
    """Add new policy categories."""
    print("\nAdding additional policy categories...")
    
    categories = [
        {"id": "cat-billing", "name": "Billing & Payments", "description": "Policies for billing, payments, and subscriptions"},
        {"id": "cat-compliance", "name": "Compliance & Legal", "description": "GDPR, CCPA, and legal compliance policies"},
        {"id": "cat-product", "name": "Product & Features", "description": "Feature access and product usage policies"},
    ]
    
    for cat in categories:
        create_policy_category(cat["id"], cat)
        print(f"  ✓ {cat['name']}")


def enrich_knowledge_base():
    """Load all enriched knowledge base content."""
    print("=" * 80)
    print("ENRICHING KNOWLEDGE BASE")
    print("=" * 80)
    
    add_additional_categories()
    create_product_tiers()
    create_approval_workflows()
    add_billing_policies()
    add_security_policies()
    add_upgrade_downgrade_policies()
    
    print("\n" + "=" * 80)
    print("✓ Knowledge base enriched successfully!")
    print("=" * 80)
    print("\nAdded:")
    print("  - 3 new policy categories (Billing, Compliance, Product)")
    print("  - 4 product tiers (Free, Pro, VIP, Enterprise)")
    print("  - 4 approval workflows (Auto, Standard, High-Value, Executive)")
    print("  - 7 new policies (billing, security, compliance, upgrades)")
    print("\nTotal knowledge base now contains:")
    print("  - 7 policy categories")
    print("  - 16 policies")
    print("  - 4 product tiers")
    print("  - 4 approval workflows")


if __name__ == "__main__":
    enrich_knowledge_base()
