import os
import uuid
from services.graph import create_decision, get_decision


def main():
    # Ensure env vars are set (you can also export them in your shell)
    required = ["NEO4J_URI", "NEO4J_USERNAME", "NEO4J_PASSWORD"]
    for r in required:
        if not os.getenv(r):
            print(f"Environment variable {r} is not set. Aborting.")
            return 2

    decision_id = f"dec-{uuid.uuid4().hex[:8]}"
    payload = {
        "prompt": "Customer requested refund for non-refundable ticket",
        "response": "Denied",
        "confidence": 0.12,
        "policy_tags": ["refund", "non_refundable"],
        "note": "Example smoke test",
    }

    print("Creating decision", decision_id)
    create_decision(decision_id, payload, database=os.getenv("NEO4J_DATABASE") or None)
    print("Read back decision:")
    node = get_decision(decision_id, database=os.getenv("NEO4J_DATABASE") or None)
    print(node)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
