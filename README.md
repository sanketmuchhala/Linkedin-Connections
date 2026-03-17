# LinkedIn Network Intelligence

A local-first web application that transforms your LinkedIn connections export into an intelligent job-hunt dashboard. Score, classify, and prioritize your network for outreach — all on your machine, no external APIs needed.

---

## Table of Contents

- [Getting Your LinkedIn Data](#getting-your-linkedin-data)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Importing Your Data](#importing-your-data)
- [Using the Dashboard](#using-the-dashboard)
- [Scoring Algorithm](#scoring-algorithm)
- [Project Structure](#project-structure)
- [Environment Variables](#environment-variables)
- [Development](#development)
- [License](#license)

---

## Getting Your LinkedIn Data

Before you can use this tool, you need to export your connections from LinkedIn.

### Step 1: Request Your Data from LinkedIn

1. Log in to [linkedin.com](https://www.linkedin.com)
2. Click your **profile picture** (top right) and go to **Settings & Privacy**
3. In the left sidebar, click **Data privacy**
4. Under "Get a copy of your data", click **Get a copy of your data**
5. Select **Connections** (you only need this one — deselect everything else for a faster export)
6. Click **Request archive**

### Step 2: Download the Export

1. LinkedIn will send you an email when your data is ready (usually within 10 minutes, sometimes up to 24 hours)
2. Click the download link in the email, or go back to **Settings & Privacy > Data privacy > Get a copy of your data** and click **Download**
3. You'll get a `.zip` file — extract it
4. Inside, find the file named **`Connections.csv`** — this is what you need

### Step 3: Place the File

Copy `Connections.csv` to the root of this project directory:

```
Linkedin Connections/
├── Connections.csv    <-- place it here
├── backend/
├── frontend/
└── ...
```

> **Note**: The CSV file contains: First Name, Last Name, URL, Email Address, Company, Position, and Connected On date. LinkedIn does not export location data.

---

## Prerequisites

Make sure you have the following installed:

- **Python 3.9+** — [Download Python](https://www.python.org/downloads/)
- **Node.js 18+** — [Download Node.js](https://nodejs.org/)
- **npm** (comes with Node.js)

To verify your installations:

```bash
python3 --version   # Should show 3.9 or higher
node --version       # Should show 18 or higher
npm --version        # Should show 8 or higher
```

---

## Setup

### 1. Backend Setup

```bash
# Navigate to the backend directory
cd backend

# Create a Python virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate        # macOS / Linux
# venv\Scripts\activate         # Windows

# Install Python dependencies
pip install -r requirements.txt
```

### 2. Frontend Setup

```bash
# Navigate to the frontend directory
cd frontend

# Install Node.js dependencies
npm install
```

---

## Importing Your Data

Once your backend is set up and you have your `Connections.csv` file in place, import your connections into the database.

### Option A: Using the Import Script

```bash
cd backend
source venv/bin/activate
python test_import.py
```

This will:
- Parse the CSV file
- Normalize names, companies, and titles
- Classify each connection (recruiter, founder, AI/ML, seniority level, etc.)
- Score each connection based on the weighted algorithm
- Aggregate company-level intelligence
- Store everything in the SQLite database at `data/linkedin_intelligence.db`

You'll see output showing how many connections were imported and any rows that were skipped.

### Option B: Using the API

Start the backend server first (see [Running the App](#running-the-app) below), then:

```bash
curl -X POST http://localhost:8000/api/import/csv \
  -F "file=@Connections.csv"
```

### Re-importing Data

If you export a fresh CSV from LinkedIn later, just run the import again. The pipeline will process and update your database with the new data.

---

## Running the App

You need two terminal windows — one for the backend, one for the frontend.

### Terminal 1: Start the Backend

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

The API will be available at **http://localhost:8000**. You can browse the interactive API docs at **http://localhost:8000/docs**.

### Terminal 2: Start the Frontend

```bash
cd frontend
npm run dev
```

The dashboard will be available at **http://localhost:3000**.

### Using the Start Scripts

Alternatively, use the included start scripts:

```bash
# Terminal 1
cd backend && ./start.sh

# Terminal 2
cd frontend && ./start.sh
```

---

## Using the Dashboard

Once both servers are running, open **http://localhost:3000** in your browser.

### Overview (`/`)
The main dashboard showing:
- Total connections, companies, AI/ML connections, and founders
- Connections growth over time chart
- Top companies ranked by network strength (click any company to see its connections)
- Seniority distribution breakdown

### Connections (`/connections`)
A searchable, filterable table of all your connections:
- Search by name, company, or title
- Filter by: AI/ML, Founders, Recruiters
- Set a minimum priority score
- Paginated results (50 per page)

### Companies (`/companies`)
Companies in your network ranked by network strength, showing connection counts by type (engineers, recruiters, founders, AI/ML).

### Priority Outreach (`/priority-outreach`)
Your highest-value contacts (score 70+), automatically grouped into:
- **Referral Asks** — high-scoring technical contacts
- **Startup Networking** — founders and executives
- **Recruiter Messages** — recruiters at relevant companies
- **Informational Chats** — other high-value connections

### Recruiters (`/recruiters`)
All recruiters in your network, grouped by company and sorted by priority score.

### Founders (`/founders`)
Founders and co-founders in your network, with a dedicated section for AI/ML founders.

### AI/ML Matches (`/ai-ml`)
All connections relevant to AI/ML roles, with stats on high-priority contacts and senior-level connections.

> **Tip**: Connection names are clickable links that open their LinkedIn profile in a new tab.

---

## Scoring Algorithm

Each connection gets a priority score (0-100) using a transparent, weighted algorithm:

### Base Score Components

| Component | Weight | How It Works |
|-----------|--------|--------------|
| Seniority | 30% | Founder=100, C-level=95, VP=90, Director=85, down to Intern=20 |
| Job Function | 25% | Data Science=85, Engineering=80, Executive=90, etc. |
| Recency | 20% | Connected in last 30 days=100, 90 days=80, 180 days=60 |
| Company | 15% | Based on company reputation signals |
| Email Available | 10% | Bonus if LinkedIn includes their email |

### Score Bonuses

| Flag | Bonus |
|------|-------|
| AI/ML relevant | +15 |
| Founder | +20 |
| C-level executive | +15 |
| Dense company (5+ connections) | +5 |
| Recruiter | -10 (penalty) |

Each connection also gets a human-readable explanation of why it received its score.

---

## Project Structure

```
Linkedin Connections/
├── backend/                      # FastAPI Backend
│   ├── app/
│   │   ├── api/                  # API route handlers
│   │   │   ├── connections.py    # /api/connections endpoints
│   │   │   ├── companies.py      # /api/companies endpoints
│   │   │   ├── analytics.py      # /api/analytics endpoints
│   │   │   └── import_data.py    # /api/import endpoints
│   │   ├── models/               # SQLAlchemy ORM models
│   │   ├── services/             # Business logic
│   │   │   ├── csv_parser.py     # CSV parsing and validation
│   │   │   ├── normalization.py  # Name/company/title cleaning
│   │   │   ├── classification.py # Job function and seniority detection
│   │   │   ├── scoring.py        # Priority scoring engine
│   │   │   └── data_pipeline.py  # End-to-end import orchestrator
│   │   ├── core/                 # Enums and classification rules
│   │   ├── schemas/              # Pydantic request/response schemas
│   │   ├── main.py               # FastAPI app entry point
│   │   ├── database.py           # Database configuration
│   │   └── config.py             # App settings
│   ├── requirements.txt
│   └── start.sh
│
├── frontend/                     # Next.js Frontend
│   ├── app/
│   │   ├── layout.tsx            # Root layout with sidebar
│   │   ├── page.tsx              # Overview dashboard
│   │   ├── connections/page.tsx  # Connections table
│   │   ├── companies/page.tsx    # Companies view
│   │   ├── priority-outreach/    # Priority outreach view
│   │   ├── recruiters/page.tsx   # Recruiters view
│   │   ├── founders/page.tsx     # Founders view
│   │   ├── ai-ml/page.tsx        # AI/ML matches view
│   │   ├── sidebar-nav.tsx       # Navigation component
│   │   └── globals.css           # Tailwind styles
│   ├── lib/
│   │   ├── api-client.ts         # Backend API wrapper
│   │   └── types.ts              # TypeScript interfaces
│   ├── package.json
│   └── start.sh
│
├── data/
│   ├── linkedin_intelligence.db  # SQLite database (created after import)
│   └── uploads/                  # Temporary CSV uploads
│
├── Connections.csv               # Your LinkedIn export (you provide this)
├── README.md
├── PROJECT_STATUS.md
└── START_HERE.md
```

---

## Environment Variables

### Backend (`backend/.env`)

```
DATABASE_URL=sqlite:///data/linkedin_intelligence.db
CORS_ORIGINS=http://localhost:3000
LOG_LEVEL=INFO
```

### Frontend (`frontend/.env.local`)

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

These files are already configured with sensible defaults. You shouldn't need to change them for local use.

---

## Development

### Running Tests

```bash
cd backend
source venv/bin/activate
pytest tests/
```

### Linting

```bash
# Backend
black backend/app/

# Frontend
cd frontend && npm run lint
```

### API Documentation

With the backend running, visit **http://localhost:8000/docs** for interactive Swagger API documentation. You can test all endpoints directly from the browser.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI, SQLAlchemy, pandas |
| Frontend | Next.js 14, TypeScript, Tailwind CSS, Recharts |
| Database | SQLite |
| Data Processing | Deterministic heuristics (no LLMs required) |

---

## Troubleshooting

### Backend won't start
- Make sure you activated the virtual environment: `source venv/bin/activate`
- Make sure dependencies are installed: `pip install -r requirements.txt`
- Check that port 8000 is not in use

### Frontend shows "Loading..." forever
- Make sure the backend is running on port 8000
- Check the browser console for CORS errors
- Verify `frontend/.env.local` has `NEXT_PUBLIC_API_URL=http://localhost:8000`

### Import fails or skips many rows
- Make sure you're using the `Connections.csv` file directly from LinkedIn's export
- The file should have headers: First Name, Last Name, URL, Email Address, Company, Position, Connected On
- Rows missing a first name or last name will be skipped (this is normal — LinkedIn sometimes includes blank rows)

### No data showing on dashboard
- Run the import step first (see [Importing Your Data](#importing-your-data))
- Check that `data/linkedin_intelligence.db` exists and is not empty

---

## License

MIT License — Feel free to use this for your own job search.

---

Built with ❤️ to help you land your dream job faster.