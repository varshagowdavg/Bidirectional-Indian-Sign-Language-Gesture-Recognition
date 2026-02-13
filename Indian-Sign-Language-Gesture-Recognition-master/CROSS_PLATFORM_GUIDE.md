# Cross-Platform Setup Guide

This guide explains how to run the ISL Gesture Recognition project on **both Windows and Mac/Linux**.

## 🎯 What Changed?

We've made the following cross-platform improvements:

### ✅ **1. Removed Windows-Only Dependencies**
- **Before**: Used `win32com` (Windows-only) for text-to-speech
- **After**: Using `pyttsx3` (works on Windows, Mac, Linux)

### ✅ **2. Fixed Hardcoded Paths**
- **Before**: `Z:\\BTP\\knk\\static\\...` (Windows absolute paths)
- **After**: `os.path.join(BASE_DIR, 'models', ...)` (cross-platform)

### ✅ **3. Environment Variables**
- **Before**: Hardcoded secrets in `settings.py`
- **After**: Using `.env` file with `python-decouple`

### ✅ **4. Updated Dependencies**
- **Before**: Django 2.2, TensorFlow 1.8 (outdated, incompatible)
- **After**: Django 3.2, TensorFlow 2.13 (modern, compatible)

---

## 📦 Installation

### **For Mac/Linux:**

```bash
# 1. Make setup script executable
chmod +x setup.sh

# 2. Run setup script
./setup.sh

# 3. Activate virtual environment
source venv/bin/activate

# 4. Create superuser
python manage.py createsuperuser

# 5. Run server
python manage.py runserver
```

### **For Windows:**

```cmd
# 1. Run setup script
setup.bat

# 2. Activate virtual environment
venv\Scripts\activate.bat

# 3. Create superuser
python manage.py createsuperuser

# 4. Run server
python manage.py runserver
```

---

## ⚙️ Configuration

### **1. Edit `.env` File**

Copy `.env.example` to `.env` and update:

```env
# Django Settings
SECRET_KEY=your-unique-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email Configuration
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Model Paths (relative to project root)
ONE_HAND_MODEL_PATH=models/one_hand144.h5
TWO_HAND_MODEL_PATH=models/fintwo_handVGG.h5
HOG_MODEL_PATH=models/HOG_full_newaug.sav
SCALER_MODEL_PATH=models/SCfull_newaug.sav
PCA_MODEL_PATH=models/PCAfull_newaug.sav
DICTIONARY_PATH=models/my_words_sort.pickle
```

### **2. Place Model Files**

Create a `models/` directory and place these files:
- `one_hand144.h5` - One-hand gesture CNN model
- `fintwo_handVGG.h5` - Two-hand gesture CNN model
- `HOG_full_newaug.sav` - HOG+SVM classifier
- `SCfull_newaug.sav` - StandardScaler
- `PCAfull_newaug.sav` - PCA transformer
- `my_words_sort.pickle` - English dictionary

**Note**: These model files are not included in the repository. You need to:
- Train them yourself using the dataset
- Or obtain them from the original researchers

---

## 🔧 Platform-Specific Notes

### **Mac (M1/M2 Chips)**

For better performance on Apple Silicon:

```bash
# Install TensorFlow Metal plugin
pip install tensorflow-metal
```

### **Windows**

Text-to-speech works out of the box with `pyttsx3`.

### **Linux**

Install espeak for text-to-speech:

```bash
# Ubuntu/Debian
sudo apt-get install espeak

# Fedora
sudo dnf install espeak

# Arch
sudo pacman -S espeak
```

---

## 🚀 Running the Application

### **Development Server**

```bash
# Activate virtual environment first
# Mac/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate.bat

# Run server
python manage.py runserver
```

Visit: `http://localhost:8000/index/`

### **Create Superuser**

```bash
python manage.py createsuperuser
```

Access admin panel: `http://localhost:8000/admin/`

---

## 📁 Project Structure

```
ISL-Gesture-Recognition/
├── .env                    # Environment variables (create from .env.example)
├── .env.example            # Template for environment variables
├── requirements-updated.txt # Modern, cross-platform dependencies
├── setup.sh                # Mac/Linux setup script
├── setup.bat               # Windows setup script
│
├── models/                 # ML model files (you need to add these)
│   ├── one_hand144.h5
│   ├── fintwo_handVGG.h5
│   ├── HOG_full_newaug.sav
│   ├── SCfull_newaug.sav
│   ├── PCAfull_newaug.sav
│   └── my_words_sort.pickle
│
├── knk/                    # Django project
│   ├── settings.py         # ✓ Updated for cross-platform
│   └── urls.py
│
├── gest2aud/               # Gesture to Audio
│   └── views.py            # ✓ Updated: pyttsx3, dynamic paths
│
├── aud2gest/               # Audio to Gesture
│   └── views.py            # ✓ Updated: dynamic paths
│
└── user/                   # User authentication
    └── views.py
```

---

## 🔍 Troubleshooting

### **Issue: "No module named 'decouple'"**

```bash
pip install python-decouple
```

### **Issue: "Model file not found"**

Make sure model files are in the `models/` directory and paths in `.env` are correct.

### **Issue: Text-to-speech not working**

**Mac**: Should work out of the box
**Linux**: Install espeak (`sudo apt-get install espeak`)
**Windows**: Should work out of the box

### **Issue: TensorFlow errors on Mac M1/M2**

```bash
pip install tensorflow-metal
```

### **Issue: Webcam not accessible**

Make sure you grant camera permissions to your terminal/IDE.

---

## 🔐 Security Notes

1. **Never commit `.env` file** to version control
2. **Change SECRET_KEY** in production
3. **Use app-specific passwords** for Gmail (not your main password)
4. **Set DEBUG=False** in production
5. **Update ALLOWED_HOSTS** for production deployment

---

## 📊 Dependency Comparison

| Package | Old Version | New Version | Notes |
|---------|-------------|-------------|-------|
| Django | 2.2 | 3.2.23 | LTS, security updates |
| TensorFlow | 1.8.0 | 2.13.0 | Modern, compatible |
| OpenCV | 4.0.0.21 | 4.8.1.78 | Latest stable |
| scikit-learn | 0.20.3 | 1.3.2 | Latest |
| pyttsx3 | 2.71 | 2.90 | Cross-platform TTS |

---

## 🎯 Key Improvements

1. ✅ **Cross-platform compatibility** (Windows, Mac, Linux)
2. ✅ **Modern dependencies** (no deprecated packages)
3. ✅ **Secure configuration** (environment variables)
4. ✅ **Dynamic paths** (no hardcoded Windows paths)
5. ✅ **Better error handling** (try-except blocks)
6. ✅ **Setup automation** (setup scripts for both platforms)

---

## 📝 Next Steps

1. **Get Model Files**: Train or obtain the ML models
2. **Configure Email**: Set up Gmail app password
3. **Test Features**: Try audio-to-gesture and gesture-to-audio
4. **Deploy**: Consider Docker for production deployment

---

## 🐛 Known Limitations

1. **Model files not included**: You need to train/obtain them separately
2. **Webcam required**: For gesture recognition features
3. **Internet required**: For Google Speech Recognition API
4. **Email setup**: Requires Gmail account with app password

---

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [TensorFlow Guide](https://www.tensorflow.org/guide)
- [pyttsx3 Documentation](https://pyttsx3.readthedocs.io/)
- [python-decouple](https://github.com/henriquebastos/python-decouple)

---

## 🤝 Contributing

If you encounter platform-specific issues, please:
1. Check this guide first
2. Review error messages carefully
3. Ensure all dependencies are installed
4. Verify model files are in place

---

**Happy Coding! 🚀**
