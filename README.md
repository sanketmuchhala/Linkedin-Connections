# LinkedIn Network Job Hunt Assistant

A production-quality, local-first web application that transforms your LinkedIn connections into an intelligent job-hunt dashboard.

## Features

- **CSV Import**: Upload your LinkedIn Connections.csv file
- **Smart Classification**: Automatically detects recruiters, founders, AI/ML engineers, seniority levels
- **Intelligent Scoring**: Weighted algorithm prioritizes connections for outreach
- **Company Intelligence**: Aggregates network strength and identifies top companies
- **Network Analytics**: Visual dashboards showing your network distribution
- **Local-First**: No external APIs, all data stays on your machine

## Architecture

**Backend**: FastAPI + Python + SQLite
- Data pipeline with CSV parser, normalization, classification, and scoring
- RESTful API with filtering, search, and pagination
- Deterministic heuristics (no LLMs required)

**Frontend**: Next.js 14 + TypeScript + Tailwind CSS
- Server-side rendering for fast page loads
- Clean, minimal UI focused on actionability
- Real-time data from backend API

## What's Been Built

### Backend (Complete)
- SQLAlchemy models for connections, companies, outreach logs
- CSV parser with validation (handles 7,000+ connections)
- Normalization service (cleans names, companies, titles)
- Classification service (detects job functions, seniority, flags)
- Scoring engine (transparent weighted algorithm)
- Company aggregation (network strength calculations)
- FastAPI with 4 API endpoints:
  - `/api/connections` - List/filter/search connections
  - `/api/companies` - Company intelligence
  - `/api/analytics/overview` - Dashboard statistics
  - `/api/import/csv` - Upload CSV files

### Frontend (Basic Implementation)
- Next.js 14 with App Router
- Overview dashboard with stats cards
- Sidebar navigation
- API client for backend communication
- TypeScript types

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the backend server
uvicorn app.main:app --reload

# Backend will be available at http://localhost:8000
# API docs at http://localhost:8000/docs
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev

# Frontend will be available at http://localhost:3000
```

### Import Your LinkedIn Data

**Option 1: Using the backend directly**

```bash
cd backend
source venv/bin/activate
python test_import.py
```

**Option 2: Using the API** (coming soon - UI for CSV upload)

```bash
curl -X POST http://localhost:8000/api/import/csv \
  -F "file=@../Connections.csv"
```

## Project Structure

```
linkedin-intelligence/
├── backend/                     # FastAPI backend
│   ├── app/
│   │   ├── models/             # SQLAlchemy ORM models
│   │   ├── services/           # Business logic
│   │   │   ├── csv_parser.py
│   │   │   ├── normalization.py
│   │   │   ├── classification.py
│   │   │   ├── scoring.py
│   │   │   └── data_pipeline.py
│   │   ├── api/                # API endpoints
│   │   ├── core/               # Enums and rules
│   │   ├── main.py             # FastAPI app
│   │   └── database.py         # Database config
│   └── requirements.txt
│
├── frontend/                    # Next.js frontend
│   ├── app/
│   │   ├── layout.tsx          # Root layout with sidebar
│   │   ├── page.tsx            # Overview dashboard
│   │   └── globals.css
│   ├── lib/
│   │   ├── api-client.ts       # Backend API wrapper
│   │   └── types.ts            # TypeScript interfaces
│   └── package.json
│
├── data/                        # Database and uploads
│   ├── linkedin_intelligence.db # SQLite database
│   └── uploads/                # Temporary file storage
│
└── README.md
```

## Scoring Algorithm

Connections are scored using a transparent weighted algorithm:

**Base Score (0-100):**
- Seniority (30%): Founder=100, C-level=95, VP=90, Director=85, etc.
- Job Function (25%): Data Science=85, Engineering=80, Executive=90
- Recency (20%): ≤30 days=100, ≤90 days=80, ≤180 days=60
- Company (15%): Based on company reputation
- Email Available (10%): +5 if email provided

**Bonuses:**
- AI/ML relevant: +15
- Founder: +20
- C-level executive: +15
- Dense company (5+ connections): +5
- Recruiter: -10 (penalty)

**Result:** Each connection gets a score 0-100 with a human-readable explanation.

## Database Stats (Current)

Based on the test import:
- **6,838 connections** successfully imported
- **3,737 unique companies**
- **98.4%** have company and position data
- **170 invalid rows** skipped (empty names, bad URLs)

## Roadmap (V2)

- [ ] Connections table with advanced filtering
- [ ] Priority Outreach view (score ≥ 70)
- [ ] Recruiters and Founders specialized views
- [ ] Outreach tracker (mini CRM)
- [ ] CSV export functionality
- [ ] Scoring configuration UI
- [ ] Charts with Recharts (network growth, seniority distribution)
- [ ] Company detail pages
- [ ] Dark mode support

## Development

### Running Tests

```bash
cd backend
pytest tests/
```

### Linting

```bash
# Backend
black backend/app/

# Frontend
cd frontend
npm run lint
```

## Environment Variables

**Backend (`backend/.env`):**
```
DATABASE_URL=sqlite:///data/linkedin_intelligence.db
CORS_ORIGINS=http://localhost:3000
LOG_LEVEL=INFO
```

**Frontend (`frontend/.env.local`):**
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Contributing

This is a personal project, but suggestions are welcome! Open an issue or submit a pull request.

## License

MIT License - Feel free to use this for your own job search!

## Key Success Metric

**Can you answer "Who should I contact this week for AI/ML roles?" in under 10 seconds?**

With this tool: YES! Filter by `is_ai_ml=true`, sort by `total_score desc`, and you're done.

---

Built with ❤️ to help you land your dream job faster.
