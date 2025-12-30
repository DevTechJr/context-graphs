# Quick Start Commands

## Local Development

### Start FastAPI (backend)

```bash
uvicorn app:app --reload --port 8000
```

### Start Streamlit (frontend)

```bash
streamlit run streamlit_app.py --server.port 8501
```

### Access locally

- FastAPI: http://localhost:8000
- FastAPI Docs: http://localhost:8000/docs
- Streamlit: http://localhost:8501

---

## First Time Setup

1. Create virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create .env file (copy from .env.example):

```bash
cp .env.example .env
# Then edit .env with your actual credentials
```

4. Test connection:

```bash
python -c "from Config.neo4j import load_neo4j_graph; g = load_neo4j_graph(); print('Connected!')"
```

---

## Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for full deployment guide to Render + Streamlit Cloud.

**Quick version:**

1. Push to GitHub
2. Deploy FastAPI to Render
3. Deploy Streamlit to Streamlit Cloud
4. Update API_BASE_URL environment variable
