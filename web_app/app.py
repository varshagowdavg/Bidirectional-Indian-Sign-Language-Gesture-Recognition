from flask import Flask, render_template, Response, request, redirect, url_for
import cv2
import pickle
import mediapipe as mp
import numpy as np
import os
import speech_recognition as sr
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import uuid
from pydub import AudioSegment
from gtts import gTTS

app = Flask(__name__)

# Load the models
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
STATIC_DIR = os.path.join(BASE_DIR, 'static')
ALPHABETS_DIR = os.path.join(STATIC_DIR, 'Alphabets')
GENERATED_IMAGES_DIR = os.path.join(STATIC_DIR, 'generated_images')

os.makedirs(GENERATED_IMAGES_DIR, exist_ok=True)

try:
    single_hand_model_dict = pickle.load(open(os.path.join(PROJECT_ROOT, 'saved_models/single_hand_model_word_seq(scikit-upgraded).p'), 'rb'))
    single_hand_model = single_hand_model_dict['model']

    double_hand_model_dict = pickle.load(open(os.path.join(PROJECT_ROOT, 'saved_models/double_hand_model_word(scikit-upgraded).p'), 'rb'))
    double_hand_model = double_hand_model_dict['model']
except Exception as e:
    print(f"Error loading models: {e}")
    single_hand_model = None
    double_hand_model = None

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3, max_num_hands=2)

# Labels for single and double hand signs
double_hand_labels_dict = {0: 'A', 1: 'B', 2: 'D', 3: 'E', 4: 'F', 5: 'G', 6: 'H', 7: 'J', 8: 'K', 9: 'M', 10: 'N',
                           11: 'P', 12: 'Q', 13: 'R', 14: 'S', 15: 'T', 16: 'W', 17: 'X', 18: 'Y', 19: 'Z',20:'ACCIDENT',21:'HELP'}

single_hand_labels_dict = {0: '1', 1: '2', 2: '3', 3: '4', 4: '5', 5: '6', 6: '7', 7: '8', 8: '9', 9: 'C', 10: 'I',
                           11: 'L', 12: 'O', 13: 'U', 14: 'V',15:'PAIN',16:'CALL',17:'NEXT',18:'BACKSPACE',19:'SPACE'}

camera = None

def get_camera():
    global camera
    if camera is None:
        print("Initializing camera...")
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            print("Error: Could not open camera.")
    return camera

def gen_frames():
    global current_prediction
    cap = get_camera()
    if not cap.isOpened():
        print("Camera is not open, yielding empty frame.")
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + b'' + b'\r\n')
        return

    print("Starting frame generation loop...")
    while True:
        success, frame = cap.read()
        if not success:
            print("Failed to read frame from camera.")
            # Try to re-initialize camera if read fails
            cap.release()
            global camera
            camera = None
            cap = get_camera()
            if not cap.isOpened():
                 break
            continue
        
        data_aux = []
        x_ = []
        y_ = []

        H, W, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame with MediaPipe
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            num_hands = len(results.multi_hand_landmarks)
            
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )

                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    x_.append(x)
                    y_.append(y)

                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    data_aux.append(x - min(x_))
                    data_aux.append(y - min(y_))

            x1 = int(min(x_) * W) - 10
            y1 = int(min(y_) * H) - 10
            x2 = int(max(x_) * W) - 10
            y2 = int(max(y_) * H) - 10

            try:
                if single_hand_model and double_hand_model:
                    if num_hands == 1:
                        prediction = single_hand_model.predict([np.asarray(data_aux)])
                        predicted_character = single_hand_labels_dict[int(prediction[0])]
                    else:
                        prediction = double_hand_model.predict([np.asarray(data_aux)])
                        predicted_character = double_hand_labels_dict[int(prediction[0])]
                    
                    current_prediction = predicted_character

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
                    cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3, cv2.LINE_AA)
            except Exception as e:
                pass # Prediction error
        else:
            current_prediction = "Waiting..."

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def audio_to_text(audio_path):
    print(f"Processing audio file: {audio_path}")
    r = sr.Recognizer()
    text = ""
    try:
        with sr.AudioFile(audio_path) as source:
            audio = r.record(source)
        print("Audio recorded, recognizing...")
        text = r.recognize_google(audio)
        print(f"Recognized text: {text}")
    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio")
        text = "Could not understand audio"
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        text = "Service unavailable"
    except Exception as e:
        print(f"Error in audio_to_text: {e}")
        text = f"Error: {str(e)}"
    return text

def text_to_image(text):
    print(f"Generating image for text: {text}")
    Alp = {}
    for code in range(ord('A'), ord('Z') + 1):
        Alp[chr(code)] = os.path.join(ALPHABETS_DIR, chr(code) + ".jpg")
    
    # Filter text to only include alphabets and spaces
    clean_text = ''.join([c.upper() for c in text if c.isalpha() or c.isspace()])
    words = clean_text.split(' ')
    
    # Remove empty strings
    words = [w for w in words if w]
    
    if not words:
        print("No valid words found to generate image.")
        return None

    print(f"Words to process: {words}")

    max_len = max(len(w) for w in words) if words else 0
    if len(words) < 4:
        words += [''] * (4 - len(words)) # Pad with empty strings for layout consistency if needed

    # Create a figure
    fig = plt.figure(figsize=(15, 15))
    
    j = 0
    for word in words:
        if not word:
            j += 1
            continue
        i = 1 + j * max_len
        for key in word:
            if key in Alp and os.path.exists(Alp[key]):
                image = mpimg.imread(Alp[key])
                plt.subplot(len(words), max_len, i)
                plt.axis('off')
                plt.imshow(image, aspect='auto')
                plt.subplots_adjust(left=0, right=1, top=1, bottom=0, hspace=0, wspace=0)
            else:
                print(f"Image not found for character: {key}")
            i += 1
        j += 1
    
    image_filename = f"{uuid.uuid4()}.png"
    image_path = os.path.join(GENERATED_IMAGES_DIR, image_filename)
    print(f"Saving generated image to: {image_path}")
    plt.savefig(image_path, bbox_inches='tight')
    plt.close(fig)
    
    return f"generated_images/{image_filename}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/audio_to_isl', methods=['GET', 'POST'])
def audio_to_isl():
    if request.method == 'POST':
        if 'audio_file' not in request.files:
             return render_template('audio_to_isl.html', error="No file part")
        
        file = request.files['audio_file']
        if file.filename == '':
            return render_template('audio_to_isl.html', error="No selected file")
        
        if file:
            # Generate unique filename
            original_filename = f"{uuid.uuid4()}_{file.filename}"
            filepath = os.path.join(GENERATED_IMAGES_DIR, original_filename)
            file.save(filepath)
            
            # Convert to wav if necessary (SpeechRecognition prefers wav)
            wav_filename = f"{uuid.uuid4()}.wav"
            wav_filepath = os.path.join(GENERATED_IMAGES_DIR, wav_filename)
            
            try:
                # Load audio file (pydub handles various formats like mp3, ogg, flv, wav, etc.)
                audio = AudioSegment.from_file(filepath)
                # Export as wav
                audio.export(wav_filepath, format="wav")
                
                # Process the wav file
                text = audio_to_text(wav_filepath)
                image_url = text_to_image(text)
            except Exception as e:
                print(f"Error converting/processing audio: {e}")
                return render_template('audio_to_isl.html', error=f"Error processing audio: {str(e)}")
            finally:
                # Clean up temporary files
                try:
                    if os.path.exists(filepath):
                        os.remove(filepath)
                    if os.path.exists(wav_filepath):
                        os.remove(wav_filepath)
                except Exception as cleanup_error:
                    print(f"Error cleaning up files: {cleanup_error}")
                
            return render_template('audio_to_isl.html', text=text, image_url=image_url)

    return render_template('audio_to_isl.html')

@app.route('/text_to_isl', methods=['GET', 'POST'])
def text_to_isl():
    if request.method == 'POST':
        text = request.form.get('text_input')
        if not text:
            return render_template('text_to_isl.html', error="Please enter some text")
        
        image_url = text_to_image(text)
        if not image_url:
             return render_template('text_to_isl.html', error="Could not generate ISL for the given text. Try simple alphabets.")

        return render_template('text_to_isl.html', text=text, image_url=image_url)

    return render_template('text_to_isl.html')

@app.route('/text_to_voice', methods=['GET', 'POST'])
def text_to_voice():
    if request.method == 'POST':
        text = request.form.get('text_input')
        if not text:
            return render_template('text_to_voice.html', error="Please enter some text")
        
        try:
            # Generate audio using gTTS
            tts = gTTS(text=text, lang='en')
            filename = f"{uuid.uuid4()}.mp3"
            filepath = os.path.join(GENERATED_IMAGES_DIR, filename) # Saving in same dir for convenience
            tts.save(filepath)
            
            audio_url = f"generated_images/{filename}"
            return render_template('text_to_voice.html', text=text, audio_url=audio_url)
            
        except Exception as e:
            print(f"Error generating voice: {e}")
            return render_template('text_to_voice.html', error=f"Error generating voice: {str(e)}")

    return render_template('text_to_voice.html')

    return render_template('text_to_voice.html')

current_prediction = "Waiting..."

def predict_from_image_file(image_path):
    try:
        image = cv2.imread(image_path)
        if image is None:
            return None
        
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)
        
        data_aux = []
        x_ = []
        y_ = []
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    x_.append(x)
                    y_.append(y)

                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    data_aux.append(x - min(x_))
                    data_aux.append(y - min(y_))
            
            # Prediction logic
            num_hands = len(results.multi_hand_landmarks)
            if single_hand_model and double_hand_model:
                if num_hands == 1:
                    prediction = single_hand_model.predict([np.asarray(data_aux)])
                    return single_hand_labels_dict[int(prediction[0])]
                else:
                    prediction = double_hand_model.predict([np.asarray(data_aux)])
                    return double_hand_labels_dict[int(prediction[0])]
        return None
    except Exception as e:
        print(f"Error in predict_from_image_file: {e}")
        return None

@app.route('/sign_to_voice')
def sign_to_voice():
    return render_template('sign_to_voice.html')

@app.route('/sign_image_to_voice', methods=['POST'])
def sign_image_to_voice():
    if 'sign_image' not in request.files:
        return render_template('sign_to_voice.html', error="No file part")
    
    file = request.files['sign_image']
    if file.filename == '':
        return render_template('sign_to_voice.html', error="No selected file")
    
    if file:
        filename = f"{uuid.uuid4()}_{file.filename}"
        filepath = os.path.join(GENERATED_IMAGES_DIR, filename)
        file.save(filepath)
        
        predicted_text = predict_from_image_file(filepath)
        
        if predicted_text:
            # Generate Audio
            try:
                tts = gTTS(text=predicted_text, lang='en')
                audio_filename = f"{uuid.uuid4()}.mp3"
                audio_filepath = os.path.join(GENERATED_IMAGES_DIR, audio_filename)
                tts.save(audio_filepath)
                
                return render_template('sign_to_voice.html', 
                                     predicted_text=predicted_text, 
                                     uploaded_image_url=f"generated_images/{filename}",
                                     audio_url=f"generated_images/{audio_filename}")
            except Exception as e:
                return render_template('sign_to_voice.html', error=f"Error generating audio: {e}")
        else:
            return render_template('sign_to_voice.html', error="Could not detect any sign in the image.", uploaded_image_url=f"generated_images/{filename}")

    return render_template('sign_to_voice.html')

@app.route('/speak_current_sign', methods=['POST'])
def speak_current_sign():
    global current_prediction
    if not current_prediction or current_prediction == "Waiting...":
        return {"error": "No sign detected yet."}
    
    try:
        tts = gTTS(text=current_prediction, lang='en')
        audio_filename = f"{uuid.uuid4()}.mp3"
        audio_filepath = os.path.join(GENERATED_IMAGES_DIR, audio_filename)
        tts.save(audio_filepath)
        
        return {"text": current_prediction, "audio_url": f"generated_images/{audio_filename}"}
    except Exception as e:
        return {"error": str(e)}

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
