"""
Gesture classification service using TensorFlow/Keras models.
"""
import numpy as np
import os
from typing import Tuple, Optional, List, Dict
import logging
from pathlib import Path
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import load_model, Sequential
from tensorflow.keras.layers import Dense

logger = logging.getLogger(__name__)


class GestureClassifier:
    """
    Gesture classifier using pre-trained KeyPoint Classifier.
    """
    
    def __init__(self, model_path: str = "models"):
        """
        Initialize gesture classifier.
        
        Args:
            model_path: Path to directory containing model files
        """
        # Resolve path relative to backend root
        base_path = Path(__file__).parent.parent.parent # backend/
        self.model_path = base_path / model_path
        
        self.model = None
        self.classes = None
        self.models_loaded = False
        
        # Try to load models if they exist
        self._load_models()
    
    def _load_models(self):
        """Load pre-trained models if available."""
        try:
            model_file = self.model_path / 'keypoint_classifier.hdf5'
            label_file = self.model_path / 'label_encoder.npy'
            
            if model_file.exists() and label_file.exists():
                logger.info(f"Loading model from {model_file}")
                
                # Load classes first
                self.classes = np.load(str(label_file), allow_pickle=True)
                logger.info(f"Loaded {len(self.classes)} classes")
                
                # Load the full model directly
                self.model = keras.models.load_model(str(model_file))
                self.models_loaded = True
                logger.info("Models loaded successfully")
            else:
                logger.warning(f"Model files not found at {self.model_path}")
                self.models_loaded = False
                
        except Exception as e:
            import traceback
            logger.error(f"Error loading models: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            self.models_loaded = False
    
    def _preprocess_landmarks(self, landmarks: List[Dict], image_shape: Tuple[int, int]) -> np.ndarray:
        """
        Convert normalized landmarks to pixel coordinates (flattened).
        Matches the logic in the training script, INCLUDING the horizontal flip.
        
        CRITICAL: The model was trained on 1280x720 images.
        We must scale the normalized landmarks to this specific resolution,
        regardless of the actual input image size, to ensure the pixel coordinates
        match the range the model expects.
        """
        # Validate input
        if landmarks is None:
            raise ValueError("Landmarks cannot be None")
        if len(landmarks) != 21:
            raise ValueError(f"Expected 21 landmarks, got {len(landmarks)}")
        
        # Force target resolution to match training data
        w = 1280
        h = 720
        
        pts = []
        for lm in landmarks:
            # The training script flips the frame horizontally: frame = cv2.flip(frame, 1)
            # This means the x-coordinates are inverted relative to the original frame.
            
            x_norm = lm['x']
            y_norm = lm['y']
            
            # Flip x to match training data mirroring
            x_norm = 1.0 - x_norm
            
            x = min(int(x_norm * w), w - 1)
            y = min(int(y_norm * h), h - 1)
            pts.extend([x, y])
        return np.array(pts)

    def classify_gesture(
        self,
        image: np.ndarray,
        hand_type: str,
        landmarks: Optional[List[Dict]] = None,
        confidence_threshold: float = 0.7
    ) -> Tuple[str, float]:
        """
        Classify a gesture. Prioritizes landmark-based classification if landmarks are provided.
        """
        if landmarks and self.models_loaded:
            return self.classify_from_landmarks(landmarks, image.shape[:2])
            
        # Fallback to placeholder if model not loaded or no landmarks
        import random
        char = random.choice(['A', 'B', 'C'])
        return char, 0.0

    def classify_from_landmarks(
        self,
        landmarks: List[Dict],
        image_shape: Tuple[int, int]
    ) -> Tuple[str, float]:
        """
        Classify gesture from hand landmarks using the loaded model.
        """
        if not self.models_loaded:
            logger.warning("Models not loaded, returning default")
            return "?", 0.0
            
        try:
            # Preprocess landmarks
            pts = self._preprocess_landmarks(landmarks, image_shape)
            logger.info(f"Preprocessed landmarks shape: {pts.shape}, values: {pts[:10]}...")
            
            # Predict
            # Model expects shape (1, 42)
            input_data = pts.reshape(1, -1)
            logger.info(f"Input data shape: {input_data.shape}")
            preds = self.model.predict(input_data, verbose=0)[0]
            
            # Get top prediction
            class_idx = np.argmax(preds)
            confidence = float(preds[class_idx]) * 100 # Convert to percentage
            predicted_char = self.classes[class_idx]
            
            logger.info(f"Predicted: {predicted_char} with confidence: {confidence}%")
            return predicted_char, confidence
            
        except Exception as e:
            import traceback
            logger.error(f"Prediction error: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return "Error", 0.0


class SpellCorrector:
    """
    Dictionary-based spell correction for recognized gestures.
    """
    
    def __init__(self, dictionary_path: Optional[str] = None):
        """
        Initialize spell corrector.
        
        Args:
            dictionary_path: Path to dictionary file (pickle or text)
        """
        self.dictionary = self._load_dictionary(dictionary_path)
    
    def _load_dictionary(self, path: Optional[str]) -> set:
        """Load English dictionary."""
        # Basic English words for demonstration
        # In production, load from comprehensive dictionary file
        basic_words = {
            'hello', 'world', 'help', 'emergency', 'yes', 'no', 'please',
            'thank', 'you', 'sorry', 'water', 'food', 'bathroom', 'doctor',
            'family', 'friend', 'home', 'work', 'school', 'hospital'
        }
        
        if path and os.path.exists(path):
            try:
                # Load from file
                with open(path, 'r') as f:
                    words = {line.strip().lower() for line in f}
                return words
            except Exception as e:
                logger.error(f"Error loading dictionary: {e}")
                return basic_words
        
        return basic_words
    
    def correct_word(
        self,
        word: str,
        top_predictions: list = None
    ) -> str:
        """
        Correct a word using dictionary lookup.
        
        Args:
            word: Input word to correct
            top_predictions: List of alternative character predictions
            
        Returns:
            Corrected word or original if no correction found
        """
        word_lower = word.lower()
        
        # If word is in dictionary, return it
        if word_lower in self.dictionary:
            return word_lower
        
        # Try simple corrections (one character off)
        for i in range(len(word)):
            # Try replacing each character
            for c in 'abcdefghijklmnopqrstuvwxyz':
                candidate = word_lower[:i] + c + word_lower[i+1:]
                if candidate in self.dictionary:
                    return candidate
        
        # If no correction found, return original
        return word_lower
    
    def correct_sentence(self, sentence: str) -> str:
        """
        Correct all words in a sentence.
        
        Args:
            sentence: Input sentence
            
        Returns:
            Corrected sentence
        """
        words = sentence.split()
        corrected_words = [self.correct_word(word) for word in words]
        return ' '.join(corrected_words)
