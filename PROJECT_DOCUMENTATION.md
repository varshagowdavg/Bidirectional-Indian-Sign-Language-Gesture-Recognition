# SignSetu - Bridging Communication Gaps

**SignSetu** is a comprehensive Indian Sign Language (ISL) translation and recognition system designed to bridge the communication gap between the hearing and the deaf-mute community. By leveraging advanced computer vision and machine learning technologies, SignSetu offers a two-way communication interface that is intuitive, accessible, and efficient.

---

## 🌟 Project Overview

Communication is a fundamental human right, yet millions of people with hearing and speech impairments face daily challenges in expressing themselves to those who do not understand sign language. Conversely, the general population often struggles to understand sign language gestures.

**SignSetu** addresses this problem by providing a multi-modal translation platform:
1.  **ISL to Text/Voice**: Recognizes hand gestures in real-time and converts them into spoken language and text.
2.  **Audio/Text to ISL**: Converts spoken words or written text into corresponding ISL gestures (images/video).

This project was developed by a dedicated team of students from **Acharya Institute of Technology**.

---

## 🚀 Key Features

### 1. Live ISL Recognition
*   **Functionality**: Uses the device's webcam to detect hand gestures in real-time.
*   **Technology**: MediaPipe for hand tracking and a custom-trained Machine Learning model (Random Forest/SVC) for gesture classification.
*   **Output**: Displays the recognized character or word on the screen.

### 2. Audio to ISL
*   **Functionality**: Converts spoken language into ISL gestures.
*   **How it works**:
    *   Users can record audio directly in the browser or upload an audio file.
    *   The system converts speech to text using Google Speech Recognition.
    *   The text is processed to find corresponding ISL gesture images from the database and displayed as a sequence.

### 3. Text to ISL
*   **Functionality**: Converts written text into ISL gestures.
*   **How it works**:
    *   Users type a word or sentence.
    *   The system maps each character/word to its corresponding ISL sign image and displays them.

### 4. Text to Voice
*   **Functionality**: Converts written text into spoken audio.
*   **How it works**:
    *   Users type text.
    *   The system uses Google Text-to-Speech (gTTS) to generate an MP3 audio file, which is played back to the user.

### 5. Sign to Voice
*   **Functionality**: A dual-mode feature to convert signs into speech.
    *   **Live Camera Mode**: Detects signs from the webcam. Users click "Speak Sign" to hear the detected sign spoken out loud.
    *   **Image Upload Mode**: Users upload an image of a hand sign. The system detects the sign and converts the predicted text into speech.

---

## 🛠️ Technology Stack

*   **Frontend**: HTML5, CSS3 (Glassmorphism Design), JavaScript
*   **Backend**: Python, Flask
*   **Computer Vision**: OpenCV, MediaPipe
*   **Machine Learning**: Scikit-learn (Random Forest, SVC)
*   **Audio Processing**: SpeechRecognition, gTTS (Google Text-to-Speech), Pydub
*   **Visualization**: Matplotlib

---

## 👥 The Team

**Varsha M**
*   USN: 1AY23IS410
*   Email: varsham.23.beis@acharya.ac.in

**Khushi J Dhongadi**
*   USN: 1AY23IS402
*   Email: khushij.23.beis@acharya.ac.in

**Manoj M B**
*   USN: 1AY23IS404
*   Email: manojb.23.beis@acharya.ac.in

**Yuvaraj**
*   USN: 1AY22IS132
*   Email: yuvaraja.22.beis@acharya.ac.in

---

## 📖 User Guide

### Prerequisites
Ensure you have Python 3.8+ installed. You will need the following libraries:
```bash
pip install flask opencv-python mediapipe scikit-learn speechrecognition gTTS pydub matplotlib
```

#### ⚠️ Important for Windows Users
For audio processing features to work correctly, you **must** install **FFmpeg**:
1.  Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html).
2.  Extract the files.
3.  Add the `bin` folder to your System Environment Variables (PATH).

### How to Run

#### On macOS/Linux
1.  Navigate to the project directory.
2.  Run:
    ```bash
    python3 web_app/app.py
    ```

#### On Windows
1.  Navigate to the project directory.
2.  Double-click `run_windows.bat` OR run in command prompt:
    ```cmd
    run_windows.bat
    ```

3.  Open your web browser and go to:
    **http://127.0.0.1:5001**

### Navigation
*   **Home**: The landing page with the live ISL recognition feed.
*   **Audio to ISL**: Record or upload audio to see sign language translations.
*   **Text to ISL**: Type text to see sign language translations.
*   **Text to Voice**: Type text to hear it spoken.
*   **Sign to Voice**: Use camera or upload images to hear signs spoken.
*   **About**: View team details and project mission.

---

## 🔧 Troubleshooting

*   **Camera not working?**
    *   Ensure you have granted camera permissions to your terminal/browser.
    *   Check if another app is using the camera.
*   **"Address already in use" error?**
    *   This means the app is already running. Stop it by pressing `Ctrl+C` in the terminal.
    *   If that fails, run `lsof -i :5001` to find the PID and `kill -9 <PID>` to stop it forcefully.
