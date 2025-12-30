# 🧠 Context Graph System

**A "System of Record for Why"** - Capturing not just _what_ decisions were made, but _why_ they were made, _who_ made them, and _what context_ informed them.

> 🎯 **Live Demo Database:** This project uses a live Neo4j Aura database that you can explore! See the [Viewing the Graph Database](#viewing-the-graph-database) section below.

## Overview

Context Graphs solve a critical gap in enterprise software: traditional systems store objects (customers, invoices, prices) but lose the **decision traces** - the reasoning, exceptions, and "tribal knowledge" that led to specific actions.

This proof-of-concept demonstrates:

- 🧠 **AI-Powered Decision Making** with full context awareness
- 📊 **Complete Traceability** of every decision with evidence and reasoning
- 🔍 **Precedent Search** using vector embeddings to find similar past decisions
- 📈 **Organizational Memory** that learns from every decision
- 🎯 **Policy-Aware Reasoning** that respects rules and handles exceptions

## Architecture

```
┌─────────────────┐
│  Streamlit UI   │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│    FastAPI      │
└────────┬────────┘
         │
         ↓
┌─────────────────────────────┐
│  Orchestration Service      │
│  (Decision Engine)          │
└────┬───────────────────┬────┘
     │                   │
     ↓                   ↓
┌──────────────┐   ┌─────────────┐
│  Neo4j Aura  │   │  OpenAI API │
│  (Graph DB)  │   │  (LLM +     │
│              │   │  Embeddings)│
└──────────────┘   └─────────────┘
```

## Features

### 1. Decision Orchestration Flow

The system follows a 6-step process for every decision:

```
[1/6] Query Knowledge Base → Find relevant policies
[2/6] Search Precedents → Vector search for similar decisions
[3/6] Build Context → Combine policies + precedents + evidence
[4/6] Call LLM → GPT-4 generates decision with reasoning
[5/6] Parse Response → Extract decision, confidence, reasoning
[6/6] Record Trace → Save to Neo4j with full context
```

### 2. Graph Schema

**Node Types:**

- `Decision`: The actual decision made (APPROVE/DENY)
- `Policy`: Organizational rules and guidelines
- `Actor`: Who made the decision (human or AI agent)
- `Evidence`: Supporting information (logs, tickets, customer data)
- `Approval`: Approval workflows and thresholds
- `ProductTier`: Customer tier definitions (Free, Pro, VIP, Enterprise)
- `PolicyCategory`: Policy groupings (Refunds, Billing, Compliance, etc.)

**Relationships:**

- `MADE`: Actor → Decision
- `JUSTIFIED_BY`: Decision → Evidence
- `FOLLOWS`: Decision → Policy
- `OVERRIDES`: Decision → Policy (for exceptions)
- `APPROVED`: Approval → Decision
- `PART_OF`: Policy → PolicyCategory

### 3. Knowledge Base

The system includes 16 pre-loaded policies across 7 categories:

- **Refunds**: Standard refund windows, non-refundable policies, partial refunds
- **Customer Service**: VIP exceptions, customer retention, service outages
- **Risk Management**: Fraud detection, high-value transactions
- **Billing**: Grace periods, payment plans, auto-renewals
- **Compliance**: GDPR data handling, data deletion, account security
- **Product**: Tier-based features and limits

### 4. Vector Search

- Uses OpenAI `text-embedding-3-small` (1536 dimensions)
- Cosine similarity matching for precedent search
- Automatically embeds every decision for future searches

## Installation

### Prerequisites

- Python 3.13+
- Neo4j Aura account (free tier works)
- OpenAI API key

### Setup

1. **Clone and navigate to project:**

```bash
cd context-graphs
```

2. **Create virtual environment:**

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Create `.env` file:**

```env
NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-password
OPENAI_API_KEY=sk-your-key-here
```

5. **Load knowledge base:**

```bash
python -m scripts.load_knowledge_base
python -m scripts.enrich_knowledge_base
```

## Usage

### Option 1: Streamlit UI (Recommended)

1. **Start FastAPI backend:**

```bash
uvicorn app:app --reload
```

2. **Start Streamlit UI (in new terminal):**

```bash
streamlit run streamlit_app.py
```

3. **Open browser:** http://localhost:8501

### Option 2: API Direct

1. **Start FastAPI:**

```bash
uvicorn app:app --reload
```

2. **Make decision via API:**

```bash
curl -X POST "http://127.0.0.1:8000/decide" \
  -H "Content-Type: application/json" \
  -d '{
    "request": "VIP customer wants 20% discount on renewal",
    "actor": "support_agent_alice"
  }'
```

### Option 3: Python Script

```bash
python -m scripts.test_orchestration
```

## Example Scenarios

### Scenario 1: Enterprise Refund Exception

**Request:** "Customer cust-enterprise-001 requests full refund for non-refundable annual plan due to repeated service outages"

**System Response:**

- ✅ **Decision:** APPROVE
- 🎯 **Confidence:** 0.95
- 📋 **Policies Considered:** 6 (including Service Outage Compensation, SLA Breach)
- 🔍 **Precedents Found:** 5 similar cases
- 💡 **Reasoning:** Service outages meet exception criteria, enterprise status supports override

### Scenario 2: VIP Discount

**Request:** "VIP customer wants 20% discount on renewal"

**System Response:**

- ✅ **Decision:** APPROVE
- 🎯 **Confidence:** 0.90
- 📋 **Policies Considered:** 5 (including VIP Exception Policy, Retention Policy)
- 🔍 **Precedents Found:** 5 similar approvals
- 💡 **Reasoning:** VIP status + retention precedents support approval

### Scenario 3: Late Refund Denial

**Request:** "Standard customer requesting refund 45 days after purchase"

**System Response:**

- ❌ **Decision:** DENY
- 🎯 **Confidence:** 0.90
- 📋 **Policies Considered:** 3 (Standard Refund Policy: 30-day window)
- 🔍 **Precedents Found:** Similar denials
- 💡 **Reasoning:** Exceeds 30-day window, no exceptional circumstances

## API Reference

### POST `/decide`

Generate an AI-powered decision with full context tracing.

**Request:**

```json
{
  "request": "Customer wants refund...",
  "evidence": ["Support ticket #123", "Customer since 2020"],
  "actor": "support_agent_alice"
}
```

**Response:**

```json
{
  "status": "ok",
  "decision_id": "dec-abc123",
  "decision": "APPROVE",
  "confidence": 0.9,
  "reasoning": "Based on VIP status and precedents...",
  "policies_considered": 5,
  "precedents_found": 3,
  "used_precedents": true
}
```

### POST `/decisions`

Create a decision node manually (low-level API).

### GET `/decisions/{decision_id}`

Retrieve a decision by ID.

## Testing

### Run All Tests

```bash
# Test Neo4j connection
python -m scripts.test_neo4j

# Test orchestration (3 scenarios)
python -m scripts.test_orchestration

# Test vector search
python -m scripts.test_vector_search

# Test API endpoints
python -m scripts.test_decide_api
```

## Tech Stack

| Component         | Technology                    | Purpose                           |
| ----------------- | ----------------------------- | --------------------------------- |
| **Backend**       | FastAPI 0.115.6               | REST API endpoints                |
| **Database**      | Neo4j Aura (Cloud)            | Graph storage for decision traces |
| **LLM**           | OpenAI gpt-4.1-nano           | Decision generation               |
| **Embeddings**    | OpenAI text-embedding-3-small | Vector search                     |
| **Orchestration** | LangGraph 0.3.31              | Agent framework                   |
| **UI**            | Streamlit 1.40.2              | Interactive web interface         |
| **Language**      | Python 3.13.5                 | Core implementation               |

## Visual Logging

The system includes beautiful colored terminal output for decision tracing:

```
════════════════════════════════════════════════════════════════
                    DECISION ORCHESTRATION FLOW
════════════════════════════════════════════════════════════════

ℹ Request: Customer cust-vip-789 requests refund...

[1/6] Querying knowledge base for relevant policies...
  Tags extracted: vip, refund, exception
  Policies found: 6
    1. Non-Refundable Ticket Policy (strict)
    2. VIP Customer Exception Policy (flexible)
    ...

[2/6] Searching for similar past decisions (precedents)...
  Precedents found: 5
    1. Similarity: 0.743 | ID: dec-refund-vip-789 | APPROVE
    ...

[4/6] Calling LLM for decision (gpt-4.1-nano)...
  ✓ LLM response received

┌────────────────────────────────────────────────────────────┐
│ DECISION RESULT                                            │
├────────────────────────────────────────────────────────────┤
│   Result: APPROVE                                          │
│   Confidence: 0.95                                         │
├────────────────────────────────────────────────────────────┤
│   Reasoning: Given VIP status and precedents...            │
└────────────────────────────────────────────────────────────┘
```

## Project Structure

```
context-graphs/
├── app.py                      # FastAPI application
├── streamlit_app.py            # Streamlit UI
├── requirements.txt            # Python dependencies
├── .env                        # Configuration (gitignored)
├── Config/
│   ├── llm.py                 # OpenAI LLM config
│   └── neo4j.py               # Neo4j connection
├── services/
│   ├── graph.py               # Graph operations (280+ lines)
│   └── orchestration.py       # Decision orchestration engine
├── utils/
│   └── visual_logging.py      # Colored terminal output
└── scripts/
    ├── load_knowledge_base.py
    ├── enrich_knowledge_base.py
    ├── test_orchestration.py
    ├── test_vector_search.py
    └── test_decide_api.py
```

## Viewing the Graph Database

**This project uses a live, publicly viewable Neo4j Aura database!**

Anyone can explore the decision traces and see how the system builds organizational memory:

### Quick Access

🔗 **[Open Neo4j Browser](https://browser.neo4j.io/?connectURL=neo4j+s://7d50579e.databases.neo4j.io)**

**Connection Details:**

- URI: `neo4j+s://7d50579e.databases.neo4j.io`
- Username: `neo4j`
- Password: `SvHj-D4sLeJdgtgebGSoOAhqVnYESzqTF5nP7tqyVKU`
- Database: `neo4j` (default)

### Example Queries

Once connected, try these queries to explore the decision graph:

**See all recent decisions:**

```cypher
MATCH (d:Decision)
RETURN d
ORDER BY d.timestamp DESC
LIMIT 10
```

**View a decision with full context:**

```cypher
MATCH (d:Decision {id: 'your-decision-id'})
OPTIONAL MATCH (d)-[r]-(n)
RETURN d, r, n
```

**Find high-confidence approvals:**

```cypher
MATCH (d:Decision)
WHERE d.response = 'APPROVE' AND d.confidence > 0.9
RETURN d.id, d.prompt, d.reasoning, d.confidence
ORDER BY d.confidence DESC
```

**See which policies are most referenced:**

```cypher
MATCH (p:Policy)<-[:FOLLOWS]-(d:Decision)
RETURN p.name, COUNT(d) as usage_count
ORDER BY usage_count DESC
```

**Find decisions that used precedents:**

```cypher
MATCH (d:Decision)
WHERE d.precedents_found > 0
RETURN d.id, d.prompt, d.precedents_found, d.confidence
ORDER BY d.timestamp DESC
```

**Visualize decision flow:**

```cypher
MATCH path = (a:Actor)-[:MADE]->(d:Decision)-[:FOLLOWS]->(p:Policy)
RETURN path
LIMIT 25
```

### Graph Schema

The database contains these node types and relationships:

**Nodes:**

- `Decision`: AI-generated decisions with reasoning
- `Policy`: Organizational rules and guidelines
- `PolicyCategory`: Policy groupings
- `Actor`: Who made each decision (human or AI)
- `Evidence`: Supporting facts and context
- `ProductTier`: Customer tier definitions
- `ApprovalWorkflow`: Approval routing rules

**Relationships:**

- `MADE`: Actor → Decision
- `FOLLOWS`: Decision → Policy
- `OVERRIDES`: Decision → Policy (for exceptions)
- `JUSTIFIED_BY`: Decision → Evidence
- `PART_OF`: Policy → PolicyCategory
- `APPROVED`: Approval → Decision

## Inspiration

This project is inspired by the concept of "Context Graphs" as a missing layer in enterprise software - a system that preserves organizational memory by recording not just transactions, but the reasoning and context behind every decision.

**Key Insight:** When an exception is made (e.g., refunding a non-refundable ticket), traditional systems lose the "why." Context Graphs preserve this tribal knowledge, enabling:

- Consistent exception handling
- Precedent-based reasoning
- Onboarding new team members with decision history
- Auditing and compliance
- Continuous learning from organizational decisions

## Future Enhancements

- [ ] Graph visualization (pyvis integration)
- [ ] Decision replay and "what-if" analysis
- [ ] Multi-agent collaboration
- [ ] Real-time decision monitoring dashboard
- [ ] Export decision traces to markdown/PDF
- [ ] Advanced policy conflict detection
- [ ] Human-in-the-loop approval workflows

## License

MIT License - feel free to use this for learning, demos, or as a starting point for production systems!

## Contributing

This is a proof-of-concept for demonstration purposes. If you want to extend it:

1. Fork the repo
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

---

**Built with ❤️ to demonstrate the power of Context Graphs**

Questions? Reach out or open an issue!
