# 🚀 Deployment Checklist

## Pre-Deployment Setup

### ✅ 1. GitHub Repository
- [ ] Create new GitHub repo
- [ ] Initialize git: `git init`
- [ ] Add remote: `git remote add origin <your-repo-url>`
- [ ] Stage files: `git add .`
- [ ] Commit: `git commit -m "Initial commit - Context Graph PoC"`
- [ ] Push: `git push -u origin main`

**⚠️ VERIFY .gitignore worked:** Check GitHub - `.env` should NOT be visible!

---

## Deploy FastAPI Backend (Render)

### ✅ 2. Create Render Web Service (FastAPI)
1. Go to: https://dashboard.render.com
2. Click **New** → **Web Service**
3. Connect your GitHub repo
4. Configure:
   - **Name:** `context-graph-api`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Instance Type:** `Free`

### ✅ 3. Add Environment Variables (Render Dashboard)
Go to **Environment** tab and add:
```
NEO4J_URI=neo4j+s://7d50579e.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=SvHj-D4sLeJdgtgebGSoOAhqVnYESzqTF5nP7tqyVKU
NEO4J_DATABASE=neo4j
OPENAI_API_KEY=<your-openai-key>
```

### ✅ 4. Deploy & Get URL
- Click **Create Web Service**
- Wait for build (~3 min)
- Copy your URL: `https://context-graph-api.onrender.com`

### ✅ 5. Test API
```bash
curl https://context-graph-api.onrender.com/decide -X POST \
  -H "Content-Type: application/json" \
  -d '{"request":"test","actor":"test"}'
```

---

## Deploy Streamlit Frontend (Streamlit Cloud)

### ✅ 6. Update API_BASE_URL
In Render dashboard, add one more environment variable:
```
API_BASE_URL=https://context-graph-api.onrender.com
```
(Or update locally and push to GitHub)

### ✅ 7. Deploy to Streamlit Cloud
1. Go to: https://share.streamlit.io
2. Sign in with GitHub
3. Click **New app**
4. Select:
   - **Repository:** your repo
   - **Branch:** `main`
   - **Main file path:** `streamlit_app.py`

### ✅ 8. Add Secrets (Streamlit Cloud)
In **Advanced Settings** → **Secrets**, add:
```toml
API_BASE_URL = "https://context-graph-api.onrender.com"
```

### ✅ 9. Deploy
- Click **Deploy!**
- Wait ~2 min
- Get URL: `https://your-app.streamlit.app`

---

## Post-Deployment Verification

### ✅ 10. Test End-to-End
1. Open Streamlit app URL
2. Use one of the sample requests
3. Click "Generate Decision"
4. Verify:
   - [ ] Decision appears
   - [ ] Policies show (6 items)
   - [ ] Precedents show (5 items)
   - [ ] Neo4j link works
   - [ ] Decision recorded in Neo4j Browser

### ✅ 11. Check Logs
- **FastAPI:** Render dashboard → Logs
- **Streamlit:** Streamlit Cloud → Manage app → Logs

---

## Common Issues & Fixes

### ❌ "Connection refused" in Streamlit
**Fix:** Update `API_BASE_URL` in Streamlit secrets to your Render URL

### ❌ "CORS error"
**Fix:** Already added CORS middleware to app.py ✅

### ❌ "ModuleNotFoundError"
**Fix:** Ensure requirements.txt is complete and committed

### ❌ FastAPI sleeping/slow
**Render Free tier sleeps after 15min. First request takes ~30s.**
**Fix:** Upgrade to paid tier or accept cold starts

### ❌ Neo4j connection timeout
**Fix:** Verify environment variables in Render dashboard match your .env

---

## Final URLs to Share

After deployment, update README.md with:
```markdown
## Live Demo

- **Streamlit App:** https://your-app.streamlit.app
- **FastAPI Docs:** https://context-graph-api.onrender.com/docs
- **Neo4j Browser:** https://browser.neo4j.io (credentials in app)
```

---

## Security Notes

✅ Credentials are in environment variables (not code)  
✅ .env is gitignored  
✅ Neo4j password visible in UI is intentional (demo access)  
⚠️ For production: Add authentication, rate limiting, input validation
