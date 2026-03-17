#!/bin/bash

# Start script for LinkedIn Network Intelligence backend

echo "Starting LinkedIn Network Intelligence Backend..."
echo ""

# Change to backend directory
cd "$(dirname "$0")"

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Virtual environment not found! Please run:"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Check if database exists
DB_PATH="../data/linkedin_intelligence.db"
if [ ! -f "$DB_PATH" ]; then
    echo "Database not found at $DB_PATH"
    echo "Run python test_import.py to import your LinkedIn data first"
    echo ""
fi

# Start the server
echo "Starting FastAPI server on http://localhost:8000"
echo "API documentation available at http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo "─────────────────────────────────────────────────────"
echo ""

uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
