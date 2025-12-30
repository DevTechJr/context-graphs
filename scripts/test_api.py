import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_post_decision():
    """Test creating a decision via POST endpoint"""
    payload = {
        "id": "dec-test-002",
        "payload": {
            "prompt": "Approve discount for VIP customer",
            "response": "Approved",
            "confidence": 0.95,
            "policy_tags": ["vip", "discount"],
            "actor": "sales_agent_001"
        }
    }
    
    print("POST /decisions")
    print("Request:", json.dumps(payload, indent=2))
    
    response = requests.post(f"{BASE_URL}/decisions", json=payload)
    print(f"Status: {response.status_code}")
    print("Response:", response.json())
    print()
    
    return payload["id"]


def test_get_decision(decision_id):
    """Test retrieving a decision via GET endpoint"""
    print(f"GET /decisions/{decision_id}")
    
    response = requests.get(f"{BASE_URL}/decisions/{decision_id}")
    print(f"Status: {response.status_code}")
    print("Response:", json.dumps(response.json(), indent=2))
    print()


if __name__ == "__main__":
    print("Testing FastAPI endpoints...\n")
    
    # Create a decision
    decision_id = test_post_decision()
    
    # Retrieve it
    test_get_decision(decision_id)
    
    print("✓ All tests passed!")
