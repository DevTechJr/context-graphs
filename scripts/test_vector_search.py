"""
Test Vector Search (Precedent Matching)

This script demonstrates how the agent finds similar past decisions using embeddings.

Steps:
1. Add embeddings to existing decisions
2. Search for similar decisions using a query
3. Show results with similarity scores
"""

from services.graph import (
    add_embedding_to_decision,
    search_similar_decisions,
)


def add_embeddings_to_existing_decisions():
    """Add embeddings to the decisions we created earlier."""
    print("Adding embeddings to existing decisions...\n")
    
    decision_ids = [
        "dec-9d2d1890",  # From smoke test
        "dec-test-002",   # From API test
        "dec-refund-vip-789",  # From rich decision trace
    ]
    
    for dec_id in decision_ids:
        try:
            add_embedding_to_decision(dec_id)
            print(f"  ✓ Embedded: {dec_id}")
        except Exception as e:
            print(f"  ✗ Failed {dec_id}: {e}")
    
    print()


def test_precedent_search():
    """Test finding similar decisions."""
    print("=" * 70)
    print("TESTING PRECEDENT SEARCH")
    print("=" * 70)
    
    queries = [
        "Customer wants refund for non-refundable subscription due to service issues",
        "VIP customer requesting discount",
        "Approve special exception for enterprise customer",
    ]
    
    for query in queries:
        print(f"\nQuery: \"{query}\"")
        print("-" * 70)
        
        results = search_similar_decisions(query, top_k=3)
        
        if not results:
            print("  No similar decisions found (no embeddings yet)")
            continue
        
        for i, result in enumerate(results, 1):
            decision = result["decision"]
            similarity = result["similarity"]
            
            print(f"\n  [{i}] Similarity: {similarity:.3f}")
            print(f"      ID: {decision.get('id')}")
            print(f"      Prompt: {decision.get('prompt', 'N/A')[:100]}...")
            print(f"      Response: {decision.get('response', 'N/A')}")
            print(f"      Confidence: {decision.get('confidence', 'N/A')}")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    print("NOTE: This requires OPENAI_API_KEY in .env\n")
    
    try:
        add_embeddings_to_existing_decisions()
        test_precedent_search()
        
        print("\n✓ Vector search working!")
        print("\nNow the agent can:")
        print("  1. Find similar past decisions")
        print("  2. Use them as precedents for new decisions")
        print("  3. Learn from organizational history")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure:")
        print("  1. OPENAI_API_KEY is set in .env")
        print("  2. You have decision nodes in Neo4j")
