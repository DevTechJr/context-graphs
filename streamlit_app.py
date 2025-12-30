"""
Context Graph System - Streamlit UI

Interactive interface for making AI-powered decisions with full context tracing.
"""

import streamlit as st
import requests
import json
import os
from datetime import datetime

# Configuration - Use environment variable for API URL
API_BASE_URL = os.getenv("API_BASE_URL", "https://context-graph-demo-anidev.onrender.com")

# Page config
st.set_page_config(
    page_title="Context Graph System",
    page_icon="🧠",
    layout="wide"
)

# Initialize theme state
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True

# Custom CSS - Dark mode by default
dark_mode_css = """
<style>
/* Decision Boxes - Dark Mode */
.decision-box {
    background-color: #1e3a4d;
    padding: 20px;
    border-radius: 10px;
    border-left: 5px solid #4CAF50;
    margin: 10px 0;
    color: #e0e0e0;
}
.decision-box-deny {
    background-color: #3a1e1e;
    border-left: 5px solid #f44336;
    color: #e0e0e0;
}
.decision-box h3 {
    color: #ffffff !important;
}
.decision-box p {
    color: #e0e0e0 !important;
}
.decision-box code {
    background-color: #0f2e3d;
    color: #81d4fa;
    padding: 2px 6px;
    border-radius: 3px;
}

/* Metric Cards - Dark Mode */
.metric-card {
    background-color: #1a1a1a;
    padding: 15px;
    border-radius: 8px;
    margin: 5px 0;
    border: 1px solid #333;
    color: #e0e0e0;
}

/* Precedent Cards - Dark Mode */
.precedent-card {
    background-color: #1a2a3a;
    padding: 12px;
    border-radius: 6px;
    margin: 8px 0;
    border-left: 3px solid #2196F3;
    color: #e0e0e0;
}
.precedent-card strong {
    color: #81d4fa;
}

/* Policy Cards - Dark Mode */
.policy-card {
    background-color: #2a2415;
    padding: 12px;
    border-radius: 6px;
    margin: 8px 0;
    border-left: 3px solid #FF9800;
    color: #e0e0e0;
}
.policy-card strong {
    color: #ffb74d;
}
.policy-card em {
    color: #b0bec5;
}

/* Info boxes */
.info-box {
    background-color: #1a2a3a;
    padding: 15px;
    border-radius: 8px;
    border-left: 4px solid #2196F3;
    color: #e0e0e0;
}
</style>
"""

st.markdown(dark_mode_css, unsafe_allow_html=True)

# Sidebar settings
with st.sidebar:
    st.header("⚙️ Settings")
    st.divider()
    
    # Theme toggle
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("**Theme**")
    with col2:
        if st.button("🌙" if st.session_state.dark_mode else "☀️", help="Toggle dark/light mode"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    
    st.caption(f"Mode: {'🌙 Dark' if st.session_state.dark_mode else '☀️ Light'}")
    st.divider()

# Title
st.title("🧠 Context Graph System")
st.markdown("**AI-Powered Decision Making with Full Context Tracing**")

# Apply pending example prefill BEFORE any input widgets are created
if 'pending_example' in st.session_state:
    example = st.session_state.pop('pending_example')
    st.session_state['request_text'] = example.get('request', '')
    ev_list = example.get('evidence', []) or []
    st.session_state['evidence_count'] = len(ev_list)
    for i, v in enumerate(ev_list):
        st.session_state[f"evidence_{i}"] = v
    if 'actor_id' not in st.session_state:
        st.session_state['actor_id'] = 'streamlit_user'

# Create tabs
tab1, tab2, tab3, tab4 = st.tabs(["Make a Decision", "Decision History", "System Info", "About"])

with tab1:
    st.header("Make a New Decision")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        
        # Decision request input
        request_text = st.text_area(
            "Describe the decision request:",
            placeholder="e.g., Customer cust-vip-123 requests full refund for annual subscription due to service outages",
            height=120,
            key="request_text",
            value=st.session_state.get("request_text", "")
        )
        
        # Evidence input
        st.subheader("Evidence (optional)")
        st.caption("Attach concrete facts that justify or inform the decision. Evidence improves trace quality and model confidence.")
        st.caption("Examples: outage logs, support tickets, fraud/risk flags, account tenure, SLA breach reports, prior approvals.")
        evidence_count = st.number_input(
            "Number of evidence items:",
            min_value=0,
            max_value=10,
            value=st.session_state.get("evidence_count", 0),
            key="evidence_count"
        )
        
        evidence_list = []
        if evidence_count > 0:
            for i in range(evidence_count):
                evidence = st.text_input(
                    f"Evidence {i+1}:",
                    key=f"evidence_{i}",
                    value=st.session_state.get(f"evidence_{i}", "")
                )
                if evidence:
                    evidence_list.append(evidence)
        
        # Actor
        actor_id = st.text_input(
            "Actor ID:",
            key="actor_id",
            value=st.session_state.get("actor_id", "streamlit_user")
        )
        
        # Buttons row
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            generate_btn = st.button("Generate Decision", type="primary", use_container_width=True)
        with col_btn2:
            if st.button("Reset Form", use_container_width=True):
                # Clear all form fields
                for key in ['request_text', 'evidence_count', 'actor_id']:
                    if key in st.session_state:
                        del st.session_state[key]
                # Clear evidence fields
                for i in range(10):
                    if f"evidence_{i}" in st.session_state:
                        del st.session_state[f"evidence_{i}"]
                st.rerun()
        
        # Submit logic
        if generate_btn:
            if not request_text:
                st.error("Please provide a decision request!")
            else:
                with st.spinner("Analyzing request and generating decision..."):
                    try:
                        # Call API
                        payload = {
                            "request": request_text,
                            "actor": actor_id
                        }
                        if evidence_list:
                            payload["evidence"] = evidence_list
                        
                        response = requests.post(
                            f"{API_BASE_URL}/decide",
                            json=payload
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            
                            # Store in session state for history
                            if 'decision_history' not in st.session_state:
                                st.session_state.decision_history = []
                            st.session_state.decision_history.insert(0, {
                                'timestamp': datetime.now().isoformat(),
                                'request': request_text,
                                **result
                            })
                            
                            # Display result
                            st.success("✅ Decision generated successfully!")
                            
                            # Decision box
                            box_class = "decision-box" if result['decision'] == "APPROVE" else "decision-box decision-box-deny"
                            st.markdown(f"""
                            <div class="{box_class}">
                                <h3>{'✅ APPROVED' if result['decision'] == 'APPROVE' else '❌ DENIED'}</h3>
                                <p><strong>Confidence:</strong> {result['confidence']}</p>
                                <p><strong>Decision ID:</strong> <code>{result['decision_id']}</code></p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Reasoning
                            st.subheader("🧠 Reasoning")
                            st.write(result['reasoning'])
                            
                            # Metrics
                            col_m1, col_m2, col_m3 = st.columns(3)
                            with col_m1:
                                st.metric("Policies Considered", f"{result['policies_considered']}")
                            with col_m2:
                                st.metric("Precedents Found", f"{result['precedents_found']}")
                            with col_m3:
                                st.metric("Used Precedents", "Yes ✓" if result['used_precedents'] else "No ✗")
                            
                            # Detailed Breakdown
                            st.markdown("---")
                            st.subheader("📊 Decision Process Breakdown")
                            
                            # Policies tab
                            with st.expander(f"📋 Policies Considered ({result['policies_considered']})", expanded=True):
                                if result.get('policies_details') and len(result['policies_details']) > 0:
                                    for idx, policy in enumerate(result['policies_details'], 1):
                                        severity = policy.get('severity', 'moderate')
                                        severity_color = {
                                            'strict': '🔴',
                                            'moderate': '🟡', 
                                            'flexible': '🟢'
                                        }.get(severity, '⚪')
                                        
                                        st.markdown(f"""
                                        <div class="policy-card">
                                            <strong>{idx}. {severity_color} {policy.get('name', 'Unknown Policy')}</strong><br>
                                            <em>Severity: {severity}</em><br>
                                            {policy.get('description', 'No description available')}
                                        </div>
                                        """, unsafe_allow_html=True)
                                else:
                                    st.info(f"📋 {result['policies_considered']} policies were queried from the knowledge base but details are being fetched...")
                            
                            # Precedents tab
                            with st.expander(f"🔍 Precedents Found ({result['precedents_found']})", expanded=True):
                                if result.get('precedents_details') and len(result['precedents_details']) > 0:
                                    for idx, prec in enumerate(result['precedents_details'], 1):
                                        similarity = prec.get('similarity', 0.0)
                                        similarity_pct = f"{similarity * 100:.1f}%"
                                        color = "🟢" if similarity > 0.8 else "🟡" if similarity > 0.6 else "🔵"
                                        
                                        st.markdown(f"""
                                        <div class="precedent-card">
                                            <strong>{idx}. {color} Similarity: {similarity_pct}</strong><br>
                                            <strong>Request:</strong> {prec.get('prompt', 'N/A')[:150]}...<br>
                                            <strong>Decision:</strong> {prec.get('response', 'N/A')}<br>
                                            <strong>Reasoning:</strong> {prec.get('reasoning', 'N/A')[:200]}...
                                        </div>
                                        """, unsafe_allow_html=True)
                                else:
                                    st.info(f"🔍 {result['precedents_found']} precedents were searched but details are being fetched...")
                            
                            # Neo4j Graph Link
                            st.markdown("---")
                            st.subheader("🗂️ Decision Trace in Graph Database")
                            
                            col_neo1, col_neo2 = st.columns([2, 1])
                            with col_neo1:
                                st.success("✅ Decision successfully recorded in Neo4j graph database")
                                st.code(f"Decision ID: {result['decision_id']}", language=None)
                                
                                st.markdown("""
                                **What was recorded:**
                                - Decision node with full context
                                - Links to Actor (who made the decision)
                                - Links to Policies (what rules were considered)
                                - Embeddings for precedent search
                                - Timestamp and reasoning
                                """)
                            
                            with col_neo2:
                                neo4j_url = f"https://browser.neo4j.io/?connectURL={result.get('neo4j_uri', 'neo4j+s://7d50579e.databases.neo4j.io')}"
                                st.markdown(f"""
                                **View in Neo4j Browser:**
                                
                                [Open Neo4j Browser]({neo4j_url})
                                
                                **Query to find this decision:**
                                ```cypher
                                MATCH (d:Decision {{id: '{result['decision_id']}'}})
                                RETURN d
                                ```
                                
                                **Or see full trace:**
                                ```cypher
                                MATCH (d:Decision {{id: '{result['decision_id']}'}})
                                OPTIONAL MATCH (d)-[r]-(n)
                                RETURN d, r, n
                                ```
                                """)
                            
                            
                        else:
                            st.error(f"Error: {response.status_code}")
                            st.error(response.text)
                            
                    except requests.exceptions.ConnectionError:
                        st.error("⚠️ Cannot connect to API server. Make sure FastAPI is running at http://127.0.0.1:8000")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    with col2:
        st.subheader("Quick Examples")
        
        examples = [
            {
                "title": "Enterprise Refund",
                "request": "Customer cust-enterprise-001 requests full refund for non-refundable annual plan due to repeated service outages",
                "evidence": ["Service outage on 2024-12-15 for 6 hours", "Customer has been with us for 3 years"]
            },
            {
                "title": "VIP Discount",
                "request": "VIP customer wants 20% discount on renewal",
                "evidence": []
            },
            {
                "title": "Late Refund",
                "request": "Standard customer requesting refund 45 days after purchase",
                "evidence": []
            }
        ]
        
        for example in examples:
            if st.button(f"Use: {example['title']}", use_container_width=True):
                # Set a pending example and rerun so state is applied before widgets instantiate
                st.session_state['pending_example'] = example
                st.rerun()

with tab2:
    st.header("Decision History")
    
    st.markdown("📊 **Recent decisions from Neo4j database**")
    
    # Fetch decisions from Neo4j
    try:
        # Import here to avoid circular imports
        from services.graph import get_recent_decisions
        
        with st.spinner("Loading decisions from Neo4j..."):
            decisions = get_recent_decisions(limit=50)
        
        if decisions:
            st.caption(f"Showing {len(decisions)} most recent decisions")
            
            for idx, decision in enumerate(decisions):
                # Extract fields from Neo4j node
                decision_id = decision.get('id', 'Unknown')
                response = decision.get('response', decision.get('decision', 'Unknown'))
                prompt = decision.get('prompt', decision.get('request', 'No prompt available'))
                reasoning = decision.get('reasoning', 'No reasoning available')
                confidence = decision.get('confidence', 0.0)
                created_at = decision.get('created_at', 'Unknown time')
                
                # Truncate prompt for display
                prompt_preview = prompt[:80] + "..." if len(prompt) > 80 else prompt
                
                with st.expander(f"{prompt_preview} - {response} ({created_at[:19]})"):
                    st.markdown(f"**Decision ID:** `{decision_id}`")
                    st.markdown(f"**Result:** {'✅ APPROVE' if response == 'APPROVE' else '❌ DENY' if response == 'DENY' else '⚠️ ' + response}")
                    st.markdown(f"**Confidence:** {confidence}")
                    st.markdown(f"**Reasoning:** {reasoning}")
                    
                    # Show full prompt
                    with st.expander("View Full Request"):
                        st.text(prompt)
                    
                    # Neo4j link
                    neo4j_url = f"https://browser.neo4j.io/?connectURL=neo4j+s://7d50579e.databases.neo4j.io"
                    st.markdown(f"[View in Neo4j Browser]({neo4j_url})")
        else:
            st.info("No decisions found in the database. Go to 'Make a Decision' tab to create one!")
            
    except Exception as e:
        st.error(f"Error loading decisions from Neo4j: {str(e)}")
        st.info("Using session history as fallback...")
        
        # Fallback to session state
        if 'decision_history' in st.session_state and st.session_state.decision_history:
            for idx, decision in enumerate(st.session_state.decision_history):
                with st.expander(f"{decision['request'][:80]}... - {decision['decision']} ({decision['timestamp'][:19]})"):
                    st.markdown(f"**Decision ID:** {decision['decision_id']}")
                    st.markdown(f"**Result:** {'✅ APPROVE' if decision['decision'] == 'APPROVE' else '❌ DENY'}")
                    st.markdown(f"**Confidence:** {decision['confidence']}")
                    st.markdown(f"**Reasoning:** {decision['reasoning']}")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Policies", decision['policies_considered'])
                    with col2:
                        st.metric("Precedents", decision['precedents_found'])
                    with col3:
                        st.metric("Used Precedents", "Yes" if decision['used_precedents'] else "No")
        else:
            st.info("No decisions in session history either.")

with tab3:
    st.header("System Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Components")
        st.markdown("""
        - **FastAPI Backend**: REST API for decision orchestration
        - **Neo4j Aura**: Cloud graph database for decision traces
        - **OpenAI GPT-4**: LLM for decision generation
        - **Vector Search**: OpenAI embeddings for precedent matching
        - **LangGraph**: Agent orchestration framework
        """)
    
    with col2:
        st.subheader("API Status")
        try:
            response = requests.get(f"{API_BASE_URL}/decisions/test-connection", timeout=2)
            st.success("✅ API is reachable")
        except:
            st.error("❌ API is not reachable")
            st.info("Start the FastAPI server with: `uvicorn app:app --reload`")
    
    st.subheader("What is a Context Graph?")
    st.markdown("""
    Context Graphs are a "System of Record for Why" - capturing not just **what** decisions were made,
    but **why** they were made, **who** made them, and **what context** informed them.
    
    **Key Features:**
    - 🧠 **AI-Powered Decisions**: LLM analyzes policies, precedents, and evidence
    - 📊 **Full Traceability**: Every decision stored with complete context
    - 🔍 **Precedent Search**: Vector embeddings find similar past decisions
    - 📈 **Organizational Memory**: System learns from every decision
    - 🎯 **Policy-Aware**: Decisions respect organizational rules and exceptions
    """)
    
    st.subheader("Architecture")
    st.markdown("""
    ```
    Streamlit UI → FastAPI → Orchestration Service
                                    ↓
                    ┌───────────────┴───────────────┐
                    ↓                               ↓
                Neo4j Graph                    OpenAI API
            (Policies, Decisions,           (LLM + Embeddings)
             Precedents, Evidence)
    ```
    """)

with tab4:
    st.header("Why This Matters")
    st.markdown("""
    ### Significance & Impact
    
    Modern enterprise systems record transactions but rarely preserve the reasoning behind them. This project creates a living memory of organizational decisions — a Context Graph — enabling:
    
    - **Better Decisions Over Time**: Every new decision embeds context and becomes a precedent. The agent references similar past traces to make more consistent, nuanced choices.
    - **Exception Intelligence**: Overrides to policy (e.g., refunding a non‑refundable ticket) are recorded with evidence and reasoning, turning tribal knowledge into a shared asset.
    - **Auditability & Compliance**: Decisions include who made them, why, and what inputs were considered — essential for reviews, audits, and regulatory requirements.
    - **Faster Onboarding**: New team members learn from real, contextualized decisions rather than static SOPs.
    - **Policy Feedback Loop**: Recurrent exceptions highlight where policies should evolve.
    
    ### How the Agent Improves
    
    The agent’s decision‑making abilities improve as the graph grows:
    - It searches embeddings of prior decisions to find relevant precedents.
    - It integrates applicable policies, evidence, and outcomes.
    - It records each outcome, enriching organizational memory for future cases.
    
    Over time, this builds a robust "System of Record for Why" — not just what was done, but why it was done — enabling more intelligent, consistent, and explainable operations.
    
    ---
    
    ### 🔬 Research & Publication
    
    **For VCs and Researchers:**
    
    This project demonstrates a novel approach to preserving organizational knowledge through graph-structured decision traces. Key innovations:
    
    1. **Hybrid Memory Architecture**: Combines vector embeddings (for semantic search) with graph relationships (for contextual reasoning)
    2. **Policy-Aware Decision Making**: LLM decisions are grounded in organizational rules, with explicit tracking of exceptions
    3. **Compounding Intelligence**: Each decision enriches the system's ability to handle future edge cases
    4. **Full Auditability**: Every decision includes complete provenance (who, what, why, when, which policies, which precedents)
    
    **Potential Applications:**
    - Customer service automation with consistent exception handling
    - Compliance and regulatory decision tracking
    - Medical diagnosis support with precedent awareness
    - Legal reasoning with case law integration
    - Financial approval workflows with risk-aware precedents
    
    ---
    
    ### 📊 Exploring the Graph Database
    
    **This database is open for exploration!**
    
    Connect to the Neo4j Aura instance to see all decision traces:
    
    **Connection Details:**
    - URI: `neo4j+s://7d50579e.databases.neo4j.io`
    - Database: `neo4j` (default)
    - [Open in Neo4j Browser](https://browser.neo4j.io/?connectURL=neo4j+s://7d50579e.databases.neo4j.io)
    
    **Useful Queries:**
    
    ```cypher
    // See all decisions
    MATCH (d:Decision)
    RETURN d
    ORDER BY d.timestamp DESC
    LIMIT 10
    
    // See decision with full context
    MATCH (d:Decision {id: 'your-decision-id'})
    OPTIONAL MATCH (d)-[r]-(n)
    RETURN d, r, n
    
    // Find all APPROVE decisions with high confidence
    MATCH (d:Decision)
    WHERE d.response = 'APPROVE' AND d.confidence > 0.9
    RETURN d.id, d.prompt, d.reasoning, d.confidence
    
    // See which policies are most frequently used
    MATCH (p:Policy)<-[:FOLLOWS]-(d:Decision)
    RETURN p.name, COUNT(d) as usage_count
    ORDER BY usage_count DESC
    
    // Find decisions that referenced precedents
    MATCH (d:Decision)
    WHERE d.precedents_found > 0
    RETURN d.id, d.prompt, d.precedents_found, d.confidence
    ```
    
    **Graph Schema:**
    - **Decision** nodes: The actual decisions made
    - **Policy** nodes: Organizational rules and guidelines
    - **Actor** nodes: Who made each decision
    - **Evidence** nodes: Supporting facts and context
    - **PolicyCategory** nodes: Policy groupings
    - Relationships: MADE, FOLLOWS, OVERRIDES, JUSTIFIED_BY, etc.
    """)
