@echo off
REM ISL Recognition System - Quick Start Script for Windows

echo ========================================
echo ISL Recognition System - Quick Start
echo ========================================
echo.

REM Check Python
echo Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found. Please install Python 3.11+
    pause
    exit /b 1
)

REM Check Node
echo Checking Node.js version...
node --version >nul 2>&1
if errorlevel 1 (
    echo Node.js not found. Please install Node.js 18+
    pause
    exit /b 1
)

echo.
echo Prerequisites check passed!
echo.

REM Setup Backend
echo Setting up Backend...
cd backend

REM Create virtual environment
if not exist "venv" (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
pip install -q --upgrade pip
pip install -q -r requirements.txt

REM Create .env
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
    echo Please edit backend\.env and set your SECRET_KEY
)

REM Initialize database
echo Initializing database...
python -c "from app.database import init_db; import asyncio; asyncio.run(init_db())" 2>nul

echo Backend setup complete!
echo.

REM Setup Frontend
echo Setting up Frontend...
cd ..\frontend

REM Install dependencies
if not exist "node_modules" (
    echo Installing Node.js dependencies...
    call npm install
)

echo Frontend setup complete!
echo.

REM Start services
echo Starting services...
echo.

echo Starting Backend on http://localhost:8000...
cd ..\backend
call venv\Scripts\activate.bat
start "ISL Backend" cmd /k "python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 3 /nobreak >nul

echo Starting Frontend on http://localhost:5173...
cd ..\frontend
start "ISL Frontend" cmd /k "npm run dev"

echo.
echo ========================================
echo Services started successfully!
echo ========================================
echo.
echo Access the application:
echo   Frontend: http://localhost:5173
echo   Backend:  http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo.
echo Close the terminal windows to stop services
echo.
pause
