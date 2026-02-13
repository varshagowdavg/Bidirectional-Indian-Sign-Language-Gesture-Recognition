#!/bin/bash
# Cross-platform setup script for ISL Gesture Recognition
# Works on Mac and Linux

echo "========================================="
echo "ISL Gesture Recognition - Setup Script"
echo "========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
echo "This may take several minutes..."
pip install -r requirements-updated.txt

# Create necessary directories
echo ""
echo "Creating project directories..."
mkdir -p models
mkdir -p media/Alphabets
mkdir -p media/aud2gest/audioFiles
mkdir -p media/aud2gest/textFiles
mkdir -p media/aud2gest/imageFiles
mkdir -p static/gest2aud
mkdir -p static/aud2gest
mkdir -p static/user

# Copy .env.example to .env if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration!"
fi

# Run migrations
echo ""
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Collect static files
echo ""
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "========================================="
echo "✓ Setup completed successfully!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Place ML model files in the 'models/' directory:"
echo "   - one_hand144.h5"
echo "   - fintwo_handVGG.h5"
echo "   - HOG_full_newaug.sav"
echo "   - SCfull_newaug.sav"
echo "   - PCAfull_newaug.sav"
echo "   - my_words_sort.pickle"
echo "3. Create a superuser: python manage.py createsuperuser"
echo "4. Run the server: python manage.py runserver"
echo ""
echo "To activate the virtual environment later:"
echo "  source venv/bin/activate"
echo ""
