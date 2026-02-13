# Indian Sign Language (ISL) Gesture Recognition - Project Analysis

## 📋 Project Overview

This is a **Django-based web application** for Indian Sign Language (ISL) translation that provides bidirectional conversion:
- **Audio to Gesture (aud2gest)**: Converts spoken words to ISL gesture images
- **Gesture to Audio (gest2aud)**: Recognizes hand gestures and converts them to speech

### Research Background
The project implements a hierarchical neural network approach that achieved:
- **98.52% accuracy** for one-hand gestures
- **97% accuracy** for two-hand gestures
- Dataset: 150,000+ images of all 26 English alphabets in ISL

---

## 🏗️ Project Structure

```
Indian-Sign-Language-Gesture-Recognition-master/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── db.sqlite3                   # SQLite database
├── README.md                    # Project documentation
│
├── knk/                         # Main Django project folder
│   ├── settings.py              # Django settings
│   ├── urls.py                  # URL routing
│   └── wsgi.py                  # WSGI configuration
│
├── aud2gest/                    # Audio to Gesture app
│   ├── models.py                # AudioDb model
│   ├── views.py                 # Audio processing logic
│   ├── forms.py                 # Upload forms
│   └── migrations/
│
├── gest2aud/                    # Gesture to Audio app
│   ├── models.py                # (Empty - no DB models)
│   ├── views.py                 # Gesture recognition logic
│   └── migrations/
│
├── user/                        # User authentication app
│   ├── models.py                # user_profile model
│   ├── views.py                 # Login/Register logic
│   ├── forms.py                 # UserRegisterationForm
│   └── migrations/
│
├── templates/                   # HTML templates
│   ├── aud2gest/
│   │   ├── home.html
│   │   ├── index.html
│   │   ├── about_project.html
│   │   ├── about_team.html
│   │   └── instructions.html
│   ├── gest2aud/
│   │   ├── Emergency.html
│   │   └── gest_keyboard.html
│   └── user/
│       ├── login.html
│       └── register.html
│
├── static/                      # Static files (CSS, JS, images)
│   ├── aud2gest/
│   ├── gest2aud/               # Contains ML models (HOG, PCA, etc.)
│   └── user/
│
└── media/                       # User-uploaded files
    ├── Alphabets/              # ISL alphabet images
    ├── aud2gest/
    │   ├── audioFiles/
    │   ├── textFiles/
    │   └── imageFiles/
    └── ...
```

---

## 🔧 Technology Stack

### Backend Framework
- **Django 2.2** - Web framework
- **SQLite** - Database

### Machine Learning & Computer Vision
- **TensorFlow 1.8.0** - Deep learning framework
- **Keras 2.2.4** - Neural network API
- **OpenCV 4.0.0.21** - Computer vision
- **scikit-learn 0.20.3** - Machine learning algorithms
- **scikit-image 0.15.0** - Image processing

### Audio Processing
- **SpeechRecognition 3.8.1** - Speech-to-text
- **pyttsx3 2.71** - Text-to-speech
- **pydub 0.23.1** - Audio manipulation
- **win32com** - Windows SAPI for speech synthesis

### Data Science
- **NumPy 1.14.5** - Numerical computing
- **Pandas 0.24.2** - Data manipulation
- **Matplotlib 3.0.3** - Visualization

### Other Dependencies
- **django-crispy-forms 1.7.2** - Form styling
- **Pillow 6.0.0** - Image processing

---

## 📊 Database Models

### 1. AudioDb (aud2gest app)
```python
class AudioDb(models.Model):
    audiofile = FileField(upload_to='aud2gest/audioFiles/')
    textfile = FileField(upload_to='aud2gest/textFiles/')
    imagefile = FileField(upload_to='aud2gest/imageFiles/')
    content = TextField()  # Transcribed text
```

### 2. user_profile (user app)
```python
class user_profile(models.Model):
    user = OneToOneField(User)
    Email1 = EmailField()
    Email2 = EmailField()
    Email3 = EmailField()
    Email4 = EmailField()
    Email5 = EmailField()  # For emergency contacts
```

---

## 🔄 Application Flow

### Audio to Gesture (aud2gest)
1. **User uploads audio** or records via microphone
2. **Speech Recognition** converts audio to text using Google Speech API
3. **Text Processing** splits text into words
4. **Image Generation** creates ISL gesture grid using matplotlib
   - Maps each letter to corresponding ISL alphabet image
   - Arranges in grid format (max 4 words)
5. **Display** shows generated gesture image to user

### Gesture to Audio (gest2aud)
1. **Webcam Capture** records hand gestures (5-second intervals)
2. **Preprocessing** 
   - Crops hand region (50:300, 50:300)
   - Resizes to 144×144 pixels
3. **Classification Pipeline**:
   - **HOG + SVM**: Classifies as one-hand or two-hand gesture
   - **CNN Model 1**: Processes one-hand gestures (7 classes: c,i,j,l,o,u,v)
   - **CNN Model 2**: Processes two-hand gestures (19 classes: a,b,d,e,f,g,h,k,m,n,p,q,r,s,t,w,x,y,z)
4. **Dictionary Correction** 
   - Uses English corpus for spell-checking
   - Binary search through sorted word list
   - Selects highest probability valid word
5. **Text-to-Speech** converts recognized word to audio

---

## 🎯 Key Features

### 1. Bidirectional Translation
- Audio → ISL Gestures
- ISL Gestures → Audio

### 2. User Authentication
- Registration with emergency contacts (5 email addresses)
- Simple login (username only, default password: "qwerty123abc")

### 3. Emergency Messaging
- Quick-send emergency messages to registered contacts
- Pre-defined message templates

### 4. Gesture Keyboard
- Type using hand gestures
- Real-time text-to-speech conversion

### 5. Webcam Integration
- Real-time gesture capture
- Visual feedback with bounding box

---

## 🧠 Machine Learning Models

### Model Architecture

#### 1. Hierarchical Classification
```
Input Image
    ↓
HOG Feature Extraction
    ↓
SVM Classifier (One-hand vs Two-hand)
    ↓
    ├─→ One-hand CNN (VGG-based, 144×144)
    │   └─→ 7 classes
    └─→ Two-hand CNN (VGG16 transfer learning, 64×64)
        └─→ 19 classes
```

#### 2. Model Files (Expected Locations)
- `Z:\style_transfer\asl_dataset\one_hand144.h5` - One-hand gesture model
- `Z:\style_transfer\asl_dataset\fintwo_handVGG.h5` - Two-hand gesture model
- `Z:\BTP\knk\static\gest2aud\HOG_full_newaug.sav` - HOG+SVM classifier
- `Z:\BTP\knk\static\gest2aud\SCfull_newaug.sav` - StandardScaler
- `Z:\BTP\knk\static\gest2aud\PCAfull_newaug.sav` - PCA transformer
- `Z:\BTP\knk\static\gest2aud\my_words_sort.pickle` - English dictionary

### Natural Language Processing
- **Dictionary-based correction** using English corpus
- **Top-3 probability tracking** for each character
- **Permutation search** to find valid words
- **Binary search** for efficient word lookup

---

## 🌐 URL Routes

| URL | View | Description |
|-----|------|-------------|
| `/admin/` | Django Admin | Admin panel |
| `/home/` | `aud_view.home` | Audio upload/recording |
| `/index/` | `aud_view.index` | Main index page |
| `/save_audio/` | `aud_view.ajax` | AJAX audio save endpoint |
| `/about_project/` | `aud_view.about_project` | Project information |
| `/about_team/` | `aud_view.about_team` | Team information |
| `/instruction/` | `aud_view.instruction` | User instructions |
| `/register/` | `user_view.register` | User registration |
| `/login/` | `user_view.login_user` | User login |
| `/logout/` | `user_view.logout_user` | User logout |
| `/webcam/` | `gest_view.take_snaps` | Webcam gesture capture |
| `/gest_keyboard/` | `gest_view.gest_keyboard` | Gesture keyboard |
| `/emergency/` | `gest_view.emergency` | Emergency messaging |

---

## ⚠️ Critical Issues & Platform Dependencies

### 1. **Hardcoded Windows Paths**
Multiple absolute paths that won't work on Mac/Linux:
```python
# In gest2aud/views.py
filename = "Z:\\BTP\\knk\\static\\gest2aud\\HOG_full_newaug.sav"
model1 = load_model('Z:\\style_transfer\\asl_dataset\\one_hand144.h5')

# In aud2gest/views.py
'Z:/BTP/knk/media/aud2gest/audioFiles/'+filename+".bin"
```

### 2. **Windows-Only Dependencies**
```python
from win32com.client import Dispatch  # Windows SAPI
import pythoncom
```

### 3. **Security Issues**
- **Exposed SECRET_KEY** in settings.py
- **Exposed email credentials** (EMAIL_HOST_PASSWORD)
- **Default password** hardcoded: "qwerty123abc"
- **DEBUG = True** in production

### 4. **Missing Model Files**
The ML models are referenced but not included in the repository:
- `one_hand144.h5`
- `fintwo_handVGG.h5`
- `HOG_full_newaug.sav`
- `my_words_sort.pickle`

### 5. **Outdated Dependencies**
- Django 2.2 (released 2019, security vulnerabilities)
- TensorFlow 1.8.0 (very old, incompatible with modern systems)
- Python 2/3 compatibility issues

---

## 🔧 Setup Requirements

### Prerequisites
- **Python 3.6-3.7** (for TensorFlow 1.8 compatibility)
- **Windows OS** (for win32com speech synthesis)
- **Webcam** for gesture recognition
- **GPU** recommended for real-time inference

### Installation Steps
```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. Create superuser
python manage.py createsuperuser

# 5. Run development server
python manage.py runserver
```

### Required Model Files
You need to obtain/train these models and place them in the correct directories:
1. One-hand gesture CNN model
2. Two-hand gesture CNN model
3. HOG+SVM classifier
4. StandardScaler and PCA transformers
5. English dictionary pickle file

---

## 🎨 User Interface

### Pages
1. **Index** - Main landing page
2. **Home** - Audio upload/recording interface
3. **Webcam** - Real-time gesture capture
4. **Gesture Keyboard** - Type with gestures
5. **Emergency** - Quick message sending
6. **About Project** - Research details
7. **About Team** - Team information
8. **Instructions** - User guide

### UI Framework
- **Bootstrap 4** (via crispy-forms)
- Custom CSS in static files
- Responsive design

---

## 📧 Email Configuration

The app sends emergency emails via Gmail SMTP:
```python
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "knk.asilentvoice@gmail.com"
EMAIL_HOST_PASSWORD = "btpgroup1"  # ⚠️ Exposed!
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

**Recommendation**: Use environment variables for credentials!

---

## 🚀 Modernization Recommendations

### 1. **Update Dependencies**
- Upgrade to Django 4.x or 5.x
- Use TensorFlow 2.x with Keras integrated
- Update all security-vulnerable packages

### 2. **Cross-Platform Compatibility**
- Replace `win32com` with `pyttsx3` (already included)
- Use `os.path.join()` for all file paths
- Use environment variables for paths

### 3. **Security Improvements**
- Move SECRET_KEY to environment variables
- Use Django's password validation
- Implement proper authentication
- Remove hardcoded credentials

### 4. **Code Quality**
- Add type hints
- Implement proper error handling
- Add logging
- Write unit tests
- Use Django REST Framework for API endpoints

### 5. **Model Management**
- Store models in project directory or cloud storage
- Use relative paths
- Add model versioning
- Implement model caching

### 6. **Docker Deployment**
```dockerfile
FROM python:3.8
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

---

## 📝 Summary

This is a **research-grade Django application** implementing a sophisticated ISL translation system with:

✅ **Strengths**:
- Novel hierarchical CNN approach
- High accuracy (98%+)
- Bidirectional translation
- Emergency communication features
- Complete web interface

❌ **Weaknesses**:
- Platform-dependent (Windows-only)
- Hardcoded paths and credentials
- Outdated dependencies
- Missing ML model files
- Security vulnerabilities

**Ideal Use Case**: Academic research, proof-of-concept
**Production Readiness**: Requires significant refactoring

---

## 📚 Research Paper Implementation

The project implements the methodology described in the README:
1. **VGG16 with fine-tuning** - 94.52% accuracy
2. **Natural language output networks** - Error correction using English corpus
3. **Hierarchical network** - Best performance (98.52%)

The hierarchical approach uses:
- **SVM + HOG** for one-hand vs two-hand classification (96.79% accuracy)
- **Separate CNNs** for each category
- **Dictionary-based spell checking** for practical error correction

---

## 🎯 Next Steps for You

1. **Fix Path Issues**: Replace all hardcoded Windows paths
2. **Obtain Models**: Train or obtain the required .h5 and .sav files
3. **Update Dependencies**: Migrate to modern versions
4. **Test on Mac**: Resolve platform-specific issues
5. **Add Documentation**: Create setup guide for your system

Would you like me to help with any specific aspect of this project?
