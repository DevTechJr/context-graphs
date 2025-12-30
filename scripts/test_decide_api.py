"""
Test the /decide API endpoint.
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"


def test_decide_endpoint():
    """Test the AI decision-making endpoint."""
    
    print("=" * 80)
    print("TESTING /decide ENDPOINT")
    print("=" * 80)
    
    # Test case 1: Enterprise refund with evidence
    print("\n[TEST 1] Enterprise customer refund request\n")
    
    payload = {
        "request": "Customer cust-enterprise-123 requests full refund for $5000 annual subscription due to critical data loss incident",
        "evidence": [
            "Service outage on 2024-12-15 for 6 hours",
            "Customer filed support ticket #789 reporting data loss",
            "Customer has been with us for 3 years"
        ],
        "actor": "support_agent_alice"
    }
    
    response = requests.post(f"{BASE_URL}/decide", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Decision made successfully!")
        print(f"\n  Decision ID: {result['decision_id']}")
        print(f"  Result: {result['decision']}")
        print(f"  Confidence: {result['confidence']}")
        print(f"  Reasoning: {result['reasoning']}")
        print(f"  Policies Considered: {result['policies_considered']}")
        print(f"  Precedents Found: {result['precedents_found']}")
        print(f"  Used Precedents: {result['used_precedents']}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
    
    # Test case 2: Simple discount request
    print("\n" + "=" * 80)
    print("\n[TEST 2] VIP discount request\n")
    
    payload = {
        "request": "VIP customer wants 15% discount on renewal due to billing issues last month"
    }
    
    response = requests.post(f"{BASE_URL}/decide", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Decision made successfully!")
        print(f"\n  Decision ID: {result['decision_id']}")
        print(f"  Result: {result['decision']}")
        print(f"  Confidence: {result['confidence']}")
        print(f"  Reasoning: {result['reasoning'][:200]}...")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
    
    # Test case 3: Denial scenario
    print("\n" + "=" * 80)
    print("\n[TEST 3] Late refund request (should deny)\n")
    
    payload = {
        "request": "Free tier customer requesting refund 60 days after purchase"
    }
    
    response = requests.post(f"{BASE_URL}/decide", json=payload)
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Decision made successfully!")
        print(f"\n  Decision ID: {result['decision_id']}")
        print(f"  Result: {result['decision']}")
        print(f"  Confidence: {result['confidence']}")
        print(f"  Reasoning: {result['reasoning'][:200]}...")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
    
    print("\n" + "=" * 80)
    print("TESTING COMPLETE")
    print("=" * 80)


if __name__ == "__main__":
    test_decide_endpoint()
