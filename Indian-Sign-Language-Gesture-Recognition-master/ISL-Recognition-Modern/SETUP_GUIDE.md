# ISL Recognition System - Complete Setup Guide

## 🚀 Quick Start (Windows & Mac)

### Prerequisites
- Python 3.11 or higher
- Node.js 18 or higher
- Git

### Step 1: Clone and Setup Backend

```bash
# Navigate to the project
cd ISL-Recognition-Modern/backend

# Create virtual environment
# On Windows:
python -m venv venv
venv\Scripts\activate

# On Mac/Linux:
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and set your SECRET_KEY (generate one using):
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Initialize database
python -c "from app.database import init_db; import asyncio; asyncio.run(init_db())"
```

### Step 2: Setup Frontend

```bash
# Navigate to frontend
cd ../frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### Step 3: Run Backend

```bash
# In a new terminal, navigate to backend
cd backend

# Activate virtual environment (if not already activated)
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Run the server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 4: Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📦 Docker Setup (Recommended for Production)

### Using Docker Compose

```bash
# Build and run all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000

## 🔧 Configuration

### Environment Variables

Edit `backend/.env`:

```env
# Required
SECRET_KEY=your-secret-key-here

# Optional - Email for emergency messaging
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Optional - Database (default: SQLite)
DATABASE_URL=sqlite+aiosqlite:///./isl_recognition.db
```

## 🎯 Features Overview

### 1. Audio to Gesture Translation
- Upload audio files or record via microphone
- Automatic speech-to-text conversion
- Generate ISL gesture image grids
- Support for multiple words

### 2. Gesture to Audio Translation
- Real-time webcam hand tracking
- MediaPipe-based hand detection
- Hierarchical gesture classification
- Text-to-speech synthesis
- Dictionary-based spell correction

### 3. Gesture Keyboard
- Type using hand gestures
- Real-time character recognition
- Visual feedback
- Text-to-speech output

### 4. Emergency Messaging
- Quick-send emergency messages
- Multiple contact support
- Pre-defined message templates

## 🧪 Testing the Application

### 1. Register a New User
1. Go to http://localhost:5173/register
2. Fill in the registration form
3. Click "Register"

### 2. Test Audio to Gesture
1. Login and navigate to "Audio → Gesture"
2. Either upload an audio file or use text input
3. View the generated ISL gesture images

### 3. Test Gesture Recognition
1. Navigate to "Gesture → Audio"
2. Allow webcam access
3. Show hand gestures to the camera
4. View recognized characters

## 🔐 Security Notes

### For Development:
- The default SECRET_KEY in .env.example is for development only
- Generate a new secret key for production

### For Production:
1. Set `DEBUG=False` in .env
2. Use a strong SECRET_KEY
3. Use environment variables for sensitive data
4. Enable HTTPS
5. Use a production database (PostgreSQL recommended)

## 📊 Database

### SQLite (Default)
- Perfect for development and small deployments
- No additional setup required
- Database file: `isl_recognition.db`

### PostgreSQL (Production)
Update DATABASE_URL in .env:
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost/isl_recognition
```

## 🎨 Customization

### Adding ISL Alphabet Images
1. Create folder: `data/alphabets/`
2. Add images named: `a.png`, `b.png`, ..., `z.png`
3. Images should be clear ISL hand gestures
4. Recommended size: 200x200 pixels

### Training Custom Models
1. Prepare your ISL gesture dataset
2. Train models using TensorFlow/Keras
3. Save models to `models/` directory
4. Update model paths in `backend/app/config.py`

## 🐛 Troubleshooting

### Backend Issues

**Error: "No module named 'app'"**
```bash
# Make sure you're in the backend directory
cd backend
python -m uvicorn app.main:app --reload
```

**Error: "Could not connect to database"**
```bash
# Initialize the database
python -c "from app.database import init_db; import asyncio; asyncio.run(init_db())"
```

**Error: "TTS engine not initialized"**
- On Mac: Install espeak `brew install espeak`
- On Windows: pyttsx3 should work out of the box
- On Linux: Install espeak `sudo apt-get install espeak`

### Frontend Issues

**Error: "Cannot connect to backend"**
- Ensure backend is running on port 8000
- Check CORS settings in backend/.env

**Webcam not working**
- Allow browser permission for camera access
- Check if another application is using the camera

### Cross-Platform Issues

**Windows Path Issues**
- All paths are now relative and cross-platform compatible
- No hardcoded Windows paths

**Mac Permission Issues**
- Allow terminal/Python to access camera in System Preferences
- Allow microphone access for speech recognition

## 📱 Browser Compatibility

- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support (may need permissions)
- Mobile browsers: ⚠️ Limited (webcam features may not work)

## 🚀 Deployment

### Deploy to Production Server

1. **Build Frontend**:
```bash
cd frontend
npm run build
```

2. **Setup Backend**:
```bash
cd backend
pip install -r requirements.txt
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

3. **Serve Frontend**:
Use Nginx or Apache to serve the `frontend/dist` directory

### Deploy with Docker

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly on both Windows and Mac
5. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- MediaPipe for hand tracking
- FastAPI for the modern Python framework
- React and Vite for the frontend
- Original ISL research team

## 📞 Support

For issues and questions:
- Check the troubleshooting section above
- Review API documentation at /docs
- Open an issue on GitHub

---

**Built with ❤️ for accessibility and inclusion**
