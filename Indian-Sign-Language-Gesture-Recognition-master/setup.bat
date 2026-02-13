@echo off
REM Cross-platform setup script for ISL Gesture Recognition
REM Works on Windows

echo =========================================
echo ISL Gesture Recognition - Setup Script
echo =========================================
echo.

REM Check Python version
echo Checking Python version...
python --version

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo Installing dependencies...
echo This may take several minutes...
pip install -r requirements-updated.txt

REM Create necessary directories
echo.
echo Creating project directories...
if not exist "models" mkdir models
if not exist "media\Alphabets" mkdir media\Alphabets
if not exist "media\aud2gest\audioFiles" mkdir media\aud2gest\audioFiles
if not exist "media\aud2gest\textFiles" mkdir media\aud2gest\textFiles
if not exist "media\aud2gest\imageFiles" mkdir media\aud2gest\imageFiles
if not exist "static\gest2aud" mkdir static\gest2aud
if not exist "static\aud2gest" mkdir static\aud2gest
if not exist "static\user" mkdir static\user

REM Copy .env.example to .env if it doesn't exist
if not exist ".env" (
    echo.
    echo Creating .env file from template...
    copy .env.example .env
    echo WARNING: Please edit .env file with your configuration!
)

REM Run migrations
echo.
echo Running database migrations...
python manage.py makemigrations
python manage.py migrate

REM Collect static files
echo.
echo Collecting static files...
python manage.py collectstatic --noinput

echo.
echo =========================================
echo Setup completed successfully!
echo =========================================
echo.
echo Next steps:
echo 1. Edit .env file with your configuration
echo 2. Place ML model files in the 'models/' directory:
echo    - one_hand144.h5
echo    - fintwo_handVGG.h5
echo    - HOG_full_newaug.sav
echo    - SCfull_newaug.sav
echo    - PCAfull_newaug.sav
echo    - my_words_sort.pickle
echo 3. Create a superuser: python manage.py createsuperuser
echo 4. Run the server: python manage.py runserver
echo.
echo To activate the virtual environment later:
echo   venv\Scripts\activate.bat
echo.
pause
