#!/bin/bash

# Start script for LinkedIn Network Intelligence frontend

echo "🚀 Starting LinkedIn Network Intelligence Frontend..."
echo ""

# Change to frontend directory
cd "$(dirname "$0")"

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Start the development server
echo "🌐 Starting Next.js development server"
echo "🔗 Frontend will be available at http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "─────────────────────────────────────────────────────"
echo ""

npm run dev
