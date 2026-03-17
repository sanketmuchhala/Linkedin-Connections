# Quick Start Guide

## Starting the Application

You need **two terminal windows** running simultaneously.

### Terminal 1: Start Backend (FastAPI)

```bash
cd "/Users/sanketmuchhala/Documents/GitHub/Linkedin Connections/backend"
./start.sh
```

Or manually:
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**Wait until you see:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
Starting LinkedIn Network Intelligence v1.0.0
API Documentation: http://localhost:8000/docs
```

### Terminal 2: Start Frontend (Next.js)

```bash
cd "/Users/sanketmuchhala/Documents/GitHub/Linkedin Connections/frontend"
./start.sh
```

Or manually:
```bash
cd frontend
npm run dev
```

**Wait until you see:**
```
Ready in 2.3s
○ Local:   http://localhost:3000
```

## Access the Application

- **Dashboard**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Your Data

**6,838 connections** imported and analyzed
**3,736 companies** with network intelligence
Database: `data/linkedin_intelligence.db` (8.3 MB)

## What You Can Do

1. **View Network Overview** - http://localhost:3000
   - See total connections, companies, AI/ML matches
   - Top companies by network strength
   - Seniority distribution

2. **Query via API** - http://localhost:8000/docs
   - Get all AI/ML connections: `/api/connections?is_ai_ml=true`
   - Get founders: `/api/connections?is_founder=true`
   - Get high-priority contacts: `/api/connections?min_score=70`

3. **Export Data** - Use the API to export filtered results

## Troubleshooting

**404 Error?**
- Make sure backend is running first (Terminal 1)
- Check http://localhost:8000/health returns `{"status":"healthy"}`

**Connection refused?**
- Backend: Check port 8000 is not in use: `lsof -i :8000`
- Frontend: Check port 3000 is not in use: `lsof -i :3000`

**Database not found?**
- Database is at: `data/linkedin_intelligence.db`
- To re-import: `cd backend && python test_import.py`

## Stop the Servers

Press **Ctrl+C** in each terminal window to stop the servers.

---

**Need help?** Check the main [README.md](README.md) for full documentation.
