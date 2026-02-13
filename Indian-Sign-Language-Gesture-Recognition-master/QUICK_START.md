# 🚀 Quick Start Guide

## For Mac/Linux Users

```bash
# 1. Run setup script
chmod +x setup.sh
./setup.sh

# 2. Activate virtual environment
source venv/bin/activate

# 3. Copy and edit .env file
cp .env.example .env
# Edit .env with your settings

# 4. Create superuser
python manage.py createsuperuser

# 5. Run server
python manage.py runserver
```

Visit: http://localhost:8000/index/

## For Windows Users

```cmd
# 1. Run setup script
setup.bat

# 2. Activate virtual environment
venv\Scripts\activate.bat

# 3. Copy and edit .env file
copy .env.example .env
# Edit .env with your settings

# 4. Create superuser
python manage.py createsuperuser

# 5. Run server
python manage.py runserver
```

Visit: http://localhost:8000/index/

## ⚠️ Important: Model Files Required

Place these files in the `models/` directory:
- `one_hand144.h5`
- `fintwo_handVGG.h5`
- `HOG_full_newaug.sav`
- `SCfull_newaug.sav`
- `PCAfull_newaug.sav`
- `my_words_sort.pickle`

Without these files, gesture recognition won't work!

## 📧 Email Configuration

Edit `.env` file:
```env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

Get Gmail app password: https://myaccount.google.com/apppasswords

## 🎥 Webcam Access

Grant camera permissions when prompted.

## 📚 Full Documentation

See `CROSS_PLATFORM_GUIDE.md` for detailed instructions.
