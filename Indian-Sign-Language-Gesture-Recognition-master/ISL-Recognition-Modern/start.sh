#!/bin/bash

# ISL Recognition System - Quick Start Script
# This script sets up and runs the application on Mac/Linux

echo "🚀 ISL Recognition System - Quick Start"
echo "========================================"
echo ""

# Check Python version
echo "📋 Checking Python version..."
python3 --version || { echo "❌ Python 3 not found. Please install Python 3.11+"; exit 1; }

# Check Node version
echo "📋 Checking Node.js version..."
node --version || { echo "❌ Node.js not found. Please install Node.js 18+"; exit 1; }

echo ""
echo "✅ Prerequisites check passed!"
echo ""

# Setup Backend
echo "🔧 Setting up Backend..."
cd backend || exit 1

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    
    # Generate secret key
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    
    # Update .env with generated secret key
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s/your-secret-key-change-this-in-production/$SECRET_KEY/" .env
    else
        # Linux
        sed -i "s/your-secret-key-change-this-in-production/$SECRET_KEY/" .env
    fi
    
    echo "✅ Generated SECRET_KEY in .env"
fi

# Initialize database
echo "Initializing database..."
python3 -c "from app.database import init_db; import asyncio; asyncio.run(init_db())" 2>/dev/null || echo "Database already initialized"

echo "✅ Backend setup complete!"
echo ""

# Setup Frontend
echo "🔧 Setting up Frontend..."
cd ../frontend || exit 1

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
else
    echo "Node modules already installed"
fi

echo "✅ Frontend setup complete!"
echo ""

# Start services
echo "🚀 Starting services..."
echo ""
echo "Starting Backend on http://localhost:8000..."
cd ../backend
source venv/bin/activate
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

echo "Waiting for backend to start..."
sleep 3

echo "Starting Frontend on http://localhost:5173..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ Services started successfully!"
echo ""
echo "📍 Access the application:"
echo "   Frontend: http://localhost:5173"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for Ctrl+C
trap "echo ''; echo '🛑 Stopping services...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo '✅ Services stopped'; exit 0" INT

# Keep script running
wait
