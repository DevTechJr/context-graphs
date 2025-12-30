import os
from typing import Optional, Dict, Any, List
from neo4j import GraphDatabase
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Initialize OpenAI client for embeddings
_openai_client = None

def _get_openai_client():
    global _openai_client
    if _openai_client is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY must be set in .env for vector search")
        _openai_client = OpenAI(api_key=api_key)
    return _openai_client


def _get_driver():
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USERNAME")
    pwd = os.getenv("NEO4J_PASSWORD")
    if not uri or not user or not pwd:
        raise RuntimeError("NEO4J_URI, NEO4J_USERNAME and NEO4J_PASSWORD must be set")
    return GraphDatabase.driver(uri, auth=(user, pwd))


def create_decision(decision_id: str, payload: Dict[str, Any], database: Optional[str] = None) -> None:
    """Create a Decision node with provided payload (stored as properties).

    payload should be a flat JSON-serializable dict (prompt, response, tags, timestamp, etc.).
    """
    driver = _get_driver()
    with driver:
        if database:
            session = driver.session(database=database)
        else:
            session = driver.session()

        with session:
            # Create Decision node with an id and properties
            props = {k: v for k, v in payload.items()}
            cypher = (
                "MERGE (d:Decision {id: $id})\n"
                "SET d += $props\n"
                "RETURN d.id AS id"
            )
            session.run(cypher, id=decision_id, props=props)


def get_decision(decision_id: str, database: Optional[str] = None) -> Optional[Dict[str, Any]]:
    driver = _get_driver()
    with driver:
        if database:
            session = driver.session(database=database)
        else:
            session = driver.session()

        with session:
            cypher = "MATCH (d:Decision {id: $id}) RETURN d LIMIT 1"
            rec = session.run(cypher, id=decision_id).single()
            if not rec:
                return None
            node = rec["d"]
            return dict(node)


# --- Context Graph: Extended Schema Helpers ---

def create_actor(actor_id: str, payload: Dict[str, Any], database: Optional[str] = None) -> None:
    """Create an Actor node (human or agent)."""
    driver = _get_driver()
    with driver:
        session = driver.session(database=database) if database else driver.session()
        with session:
            cypher = "MERGE (a:Actor {id: $id}) SET a += $props"
            session.run(cypher, id=actor_id, props=payload)


def create_evidence(evidence_id: str, payload: Dict[str, Any], database: Optional[str] = None) -> None:
    """Create an Evidence node (support ticket, outage record, customer history)."""
    driver = _get_driver()
    with driver:
        session = driver.session(database=database) if database else driver.session()
        with session:
            cypher = "MERGE (e:Evidence {id: $id}) SET e += $props"
            session.run(cypher, id=evidence_id, props=payload)


def create_policy(policy_id: str, payload: Dict[str, Any], database: Optional[str] = None) -> None:
    """Create a Policy node (company rule or guideline)."""
    driver = _get_driver()
    with driver:
        session = driver.session(database=database) if database else driver.session()
        with session:
            cypher = "MERGE (p:Policy {id: $id}) SET p += $props"
            session.run(cypher, id=policy_id, props=payload)


def create_approval(approval_id: str, payload: Dict[str, Any], database: Optional[str] = None) -> None:
    """Create an Approval node (manager override or exception grant)."""
    driver = _get_driver()
    with driver:
        session = driver.session(database=database) if database else driver.session()
        with session:
            cypher = "MERGE (a:Approval {id: $id}) SET a += $props"
            session.run(cypher, id=approval_id, props=payload)


# --- Relationships ---

def link_actor_made_decision(actor_id: str, decision_id: str, database: Optional[str] = None) -> None:
    """Create (Actor)-[:MADE]->(Decision)."""
    driver = _get_driver()
    with driver:
        session = driver.session(database=database) if database else driver.session()
        with session:
            cypher = """
            MATCH (a:Actor {id: $actor_id}), (d:Decision {id: $decision_id})
            MERGE (a)-[:MADE]->(d)
            """
            session.run(cypher, actor_id=actor_id, decision_id=decision_id)


def link_decision_justified_by_evidence(decision_id: str, evidence_id: str, database: Optional[str] = None) -> None:
    """Create (Decision)-[:JUSTIFIED_BY]->(Evidence)."""
    driver = _get_driver()
    with driver:
        session = driver.session(database=database) if database else driver.session()
        with session:
            cypher = """
            MATCH (d:Decision {id: $decision_id}), (e:Evidence {id: $evidence_id})
            MERGE (d)-[:JUSTIFIED_BY]->(e)
            """
            session.run(cypher, decision_id=decision_id, evidence_id=evidence_id)


def link_decision_overrides_policy(decision_id: str, policy_id: str, database: Optional[str] = None) -> None:
    """Create (Decision)-[:OVERRIDES]->(Policy)."""
    driver = _get_driver()
    with driver:
        session = driver.session(database=database) if database else driver.session()
        with session:
            cypher = """
            MATCH (d:Decision {id: $decision_id}), (p:Policy {id: $policy_id})
            MERGE (d)-[:OVERRIDES]->(p)
            """
            session.run(cypher, decision_id=decision_id, policy_id=policy_id)


def link_approval_approved_decision(approval_id: str, decision_id: str, database: Optional[str] = None) -> None:
    """Create (Approval)-[:APPROVED]->(Decision)."""
    driver = _get_driver()
    with driver:
        session = driver.session(database=database) if database else driver.session()
        with session:
            cypher = """
            MATCH (a:Approval {id: $approval_id}), (d:Decision {id: $decision_id})
            MERGE (a)-[:APPROVED]->(d)
            """
            session.run(cypher, approval_id=approval_id, decision_id=decision_id)


def get_decision_subgraph(decision_id: str, database: Optional[str] = None) -> Dict[str, Any]:
    """Get a decision and all its connected nodes (Actor, Evidence, Policy, Approval)."""
    driver = _get_driver()
    with driver:
        session = driver.session(database=database) if database else driver.session()
        with session:
            cypher = """
            MATCH (d:Decision {id: $id})
            OPTIONAL MATCH (a:Actor)-[:MADE]->(d)
            OPTIONAL MATCH (d)-[:JUSTIFIED_BY]->(e:Evidence)
            OPTIONAL MATCH (d)-[:OVERRIDES]->(p:Policy)
            OPTIONAL MATCH (ap:Approval)-[:APPROVED]->(d)
            RETURN d, collect(DISTINCT a) as actors, collect(DISTINCT e) as evidence, 
                   collect(DISTINCT p) as policies, collect(DISTINCT ap) as approvals
            """
            rec = session.run(cypher, id=decision_id).single()
            if not rec:
                return {}
            
            return {
                "decision": dict(rec["d"]),
                "actors": [dict(n) for n in rec["actors"] if n],
                "evidence": [dict(n) for n in rec["evidence"] if n],
                "policies": [dict(n) for n in rec["policies"] if n],
                "approvals": [dict(n) for n in rec["approvals"] if n],
            }


# --- Knowledge Base: Policy Management ---

def create_policy_category(category_id: str, payload: Dict[str, Any], database: Optional[str] = None) -> None:
    """Create a PolicyCategory node (e.g., 'Refunds', 'Customer Service')."""
    driver = _get_driver()
    with driver:
        session = driver.session(database=database) if database else driver.session()
        with session:
            cypher = "MERGE (pc:PolicyCategory {id: $id}) SET pc += $props"
            session.run(cypher, id=category_id, props=payload)


def link_policy_to_category(policy_id: str, category_id: str, database: Optional[str] = None) -> None:
    """Create (Policy)-[:PART_OF]->(PolicyCategory)."""
    driver = _get_driver()
    with driver:
        session = driver.session(database=database) if database else driver.session()
        with session:
            cypher = """
            MATCH (p:Policy {id: $policy_id}), (pc:PolicyCategory {id: $category_id})
            MERGE (p)-[:PART_OF]->(pc)
            """
            session.run(cypher, policy_id=policy_id, category_id=category_id)


def link_policy_supersedes(new_policy_id: str, old_policy_id: str, database: Optional[str] = None) -> None:
    """Create (NewPolicy)-[:SUPERSEDES]->(OldPolicy) for policy versioning."""
    driver = _get_driver()
    with driver:
        session = driver.session(database=database) if database else driver.session()
        with session:
            cypher = """
            MATCH (new:Policy {id: $new_id}), (old:Policy {id: $old_id})
            MERGE (new)-[:SUPERSEDES]->(old)
            """
            session.run(cypher, new_id=new_policy_id, old_id=old_policy_id)


def query_policies_by_category(category: str, database: Optional[str] = None) -> list[Dict[str, Any]]:
    """Query all active policies in a category (e.g., 'refund')."""
    driver = _get_driver()
    with driver:
        session = driver.session(database=database) if database else driver.session()
        with session:
            cypher = """
            MATCH (p:Policy)-[:PART_OF]->(pc:PolicyCategory)
            WHERE pc.name = $category OR pc.id = $category
            AND (p.active IS NULL OR p.active = true)
            RETURN p
            ORDER BY p.severity DESC
            """
            result = session.run(cypher, category=category)
            return [dict(rec["p"]) for rec in result]


def query_policies_by_tags(tags: list[str], database: Optional[str] = None) -> list[Dict[str, Any]]:
    """Query policies matching any of the provided tags."""
    driver = _get_driver()
    with driver:
        session = driver.session(database=database) if database else driver.session()
        with session:
            cypher = """
            MATCH (p:Policy)
            WHERE ANY(tag IN $tags WHERE tag IN p.tags)
            AND (p.active IS NULL OR p.active = true)
            RETURN p
            ORDER BY p.severity DESC
            """
            result = session.run(cypher, tags=tags)
            return [dict(rec["p"]) for rec in result]


def link_decision_follows_policy(decision_id: str, policy_id: str, database: Optional[str] = None) -> None:
    """Create (Decision)-[:FOLLOWS]->(Policy) when decision adheres to a policy."""
    driver = _get_driver()
    with driver:
        session = driver.session(database=database) if database else driver.session()
        with session:
            cypher = """
            MATCH (d:Decision {id: $decision_id}), (p:Policy {id: $policy_id})
            MERGE (d)-[:FOLLOWS]->(p)
            """
            session.run(cypher, decision_id=decision_id, policy_id=policy_id)


# --- Vector Search: Precedent Matching ---

def generate_embedding(text: str) -> List[float]:
    """Generate OpenAI embedding for text (used for similarity search)."""
    client = _get_openai_client()
    response = client.embeddings.create(
        model="text-embedding-3-small",  # 1536 dimensions, fast & cheap
        input=text
    )
    return response.data[0].embedding


def add_embedding_to_decision(decision_id: str, database: Optional[str] = None) -> None:
    """Generate and store embedding for a decision's prompt."""
    driver = _get_driver()
    with driver:
        session = driver.session(database=database) if database else driver.session()
        with session:
            # Get the decision prompt
            cypher_get = "MATCH (d:Decision {id: $id}) RETURN d.prompt AS prompt"
            rec = session.run(cypher_get, id=decision_id).single()
            if not rec or not rec["prompt"]:
                return
            
            # Generate embedding
            prompt = rec["prompt"]
            embedding = generate_embedding(prompt)
            
            # Store embedding
            cypher_update = """
            MATCH (d:Decision {id: $id})
            SET d.embedding = $embedding
            """
            session.run(cypher_update, id=decision_id, embedding=embedding)


def search_similar_decisions(query: str, top_k: int = 5, database: Optional[str] = None) -> List[Dict[str, Any]]:
    """Find similar decisions using cosine similarity of embeddings.
    
    Returns list of {decision: dict, similarity: float} sorted by similarity (highest first).
    """
    # Generate query embedding
    query_embedding = generate_embedding(query)
    
    driver = _get_driver()
    with driver:
        session = driver.session(database=database) if database else driver.session()
        with session:
            # Get all decisions with embeddings
            cypher = """
            MATCH (d:Decision)
            WHERE d.embedding IS NOT NULL
            RETURN d, d.embedding AS embedding
            """
            results = session.run(cypher)
            
            # Calculate cosine similarity in Python (Neo4j Aura may not have vector index)
            similarities = []
            for rec in results:
                decision = dict(rec["d"])
                stored_embedding = rec["embedding"]
                
                # Cosine similarity
                dot_product = sum(a * b for a, b in zip(query_embedding, stored_embedding))
                norm_a = sum(a * a for a in query_embedding) ** 0.5
                norm_b = sum(b * b for b in stored_embedding) ** 0.5
                similarity = dot_product / (norm_a * norm_b) if norm_a > 0 and norm_b > 0 else 0.0
                
                similarities.append({
                    "decision": decision,
                    "similarity": similarity
                })
            
            # Sort by similarity descending
            similarities.sort(key=lambda x: x["similarity"], reverse=True)
            
            return similarities[:top_k]



