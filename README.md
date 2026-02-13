## Overview
This project aims to bridge the communication gap between the deaf community and individuals who are unfamiliar with sign language. It provides an intelligent system to convert speech and text into Indian Sign Language (ISL) gestures and vice versa.

The system enables seamless interaction in real-world scenarios such as public announcements, healthcare communication, and mobile-based interpretation, ensuring better accessibility and inclusivity.

## Key Features
- **Speech to ISL Conversion**:
  - Converts spoken language (English/Multiple Indic languages) into ISL gestures using real-time speech recognition and text-to-sign conversion.
  - Ensures accuracy and supports regional ISL variations.
- **Text to ISL Conversion**:
  - Displays ISL gestures corresponding to given text inputs, satisfying use cases like railway announcements.
- **ISL to Text Conversion**:
  - Recognizes ISL gestures captured through a camera and converts them into text. Currently supports letter-based gestures, with word-level gesture recognition under development.

## Technologies Used
- **MediaPipe**: Used for detecting and rendering hand landmarks for text-to-ISL conversion.
- **Sarvam AI**: Enables speech-to-text functionality for spoken language recognition.
- **Python**: Backend implementation for processing inputs and generating outputs.
- **OpenCV**: Used for real-time video feed capture and gesture recognition.
- **Natural Language Processing (NLP)**: Translates recognized speech into text, forming the basis for ISL generation using GenAI.

## Use Cases
1. **Public Announcements**:
   - Converts audio/text announcements at railway stations or other public venues into ISL gestures, ensuring accessibility for the deaf community.
2. **Mobile App for ISL Interpretation**:
   - Enables normal individuals to use their mobile cameras to interpret ISL gestures by deaf individuals.

## Current Status
- **Speech to ISL**:
  - Fully functional, with accurate conversion of spoken content into ISL gestures.
  - Tested and validated for use cases like public announcements.
- **ISL to Text**:
  - Successfully implemented letter-based recognition.
  - Word-level gesture recognition is in progress, with challenges related to complex training on gesture sequences.


## Challenges and Future Work
- **Word-Level Gesture Recognition**:
  - Developing a robust model for recognizing dynamic gesture sequences.
- **Regional ISL Variations**:
  - Incorporating adaptability for regional differences in ISL.

## How to Run the Project
1. git clone https://github.com/your-username/Indian-Sign-Language-Gesture-Recognition.git
2. pip install -r requirements.txt
3. python main.py
   
## Output 
![Output](screenshots/demo.png)

## 👩‍💻 Author
Varsha Gowda

