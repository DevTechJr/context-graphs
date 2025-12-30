#!/usr/bin/env python3
"""
Direct API test - bypasses terminal issues
"""
import requests
import json
from datetime import datetime

API_URL = "http://127.0.0.1:8000/decide"

def test_decide():
    print("\n" + "="*60)
    print("TESTING /decide ENDPOINT")
    print("="*60)
    
    payload = {
        "request": "Customer wants refund for service outage",
        "evidence": ["Outage 2024-12-15, 6 hours"],
        "actor": "support_agent_1"
    }
    
    print(f"\n📤 Sending request: {payload['request']}")
    print(f"⏱️  Time: {datetime.now()}\n")
    
    try:
        response = requests.post(API_URL, json=payload, timeout=60)
        print(f"✓ Got response: {response.status_code}\n")
        
        data = response.json()
        
        # Check counts
        policies_count = data.get('policies_considered', 0)
        policies_details_len = len(data.get('policies_details', []))
        precedents_count = data.get('precedents_found', 0)
        precedents_details_len = len(data.get('precedents_details', []))
        
        print(f"📋 POLICIES")
        print(f"   Count: {policies_count}")
        print(f"   Details populated: {policies_details_len} items")
        if policies_details_len > 0:
            print(f"   ✅ MATCH!" if policies_count == policies_details_len else f"   ⚠️  MISMATCH!")
        else:
            print(f"   ❌ NO DETAILS!")
        
        print(f"\n🔍 PRECEDENTS")
        print(f"   Count: {precedents_count}")
        print(f"   Details populated: {precedents_details_len} items")
        if precedents_details_len > 0:
            print(f"   ✅ MATCH!" if precedents_count == precedents_details_len else f"   ⚠️  MISMATCH!")
        else:
            print(f"   ❌ NO DETAILS!")
        
        # Show first policy if available
        if data.get('policies_details') and len(data['policies_details']) > 0:
            print(f"\n📌 FIRST POLICY:")
            p = data['policies_details'][0]
            print(f"   Name: {p.get('name', 'N/A')}")
            print(f"   Severity: {p.get('severity', 'N/A')}")
            print(f"   Category: {p.get('category', 'N/A')}")
        
        # Show first precedent if available
        if data.get('precedents_details') and len(data['precedents_details']) > 0:
            print(f"\n📌 FIRST PRECEDENT:")
            prec = data['precedents_details'][0]
            print(f"   Similarity: {prec.get('similarity', 'N/A')}")
            print(f"   Response: {prec.get('response', 'N/A')}")
            print(f"   Confidence: {prec.get('confidence', 'N/A')}")
        
        print(f"\n{'='*60}")
        print("FULL RESPONSE (JSON):")
        print("="*60)
        print(json.dumps(data, indent=2, default=str))
        
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Cannot connect to API at " + API_URL)
        print("   Make sure FastAPI is running: .venv\\Scripts\\python.exe -m uvicorn app:app --reload --port 8000")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_decide()
