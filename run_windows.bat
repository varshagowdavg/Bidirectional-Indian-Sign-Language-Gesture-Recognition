@echo off
echo Starting SignSetu on Windows...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH. Please install Python 3.8+.
    pause
    exit /b
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
pip install flask opencv-python mediapipe scikit-learn speechrecognition gTTS pydub matplotlib

REM Check for FFmpeg (optional but recommended check)
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: FFmpeg is not installed or not in PATH.
    echo Audio processing features might fail.
    echo Please download FFmpeg from https://ffmpeg.org/download.html and add it to your PATH.
    pause
)

REM Run the application
echo Starting the server...
python web_app/app.py

pause
