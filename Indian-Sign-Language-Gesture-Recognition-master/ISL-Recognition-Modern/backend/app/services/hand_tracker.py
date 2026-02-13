"""
Hand tracking and gesture recognition service using MediaPipe.
"""
import cv2
import numpy as np
import mediapipe as mp
from typing import Optional, Tuple, List, Dict
import logging

logger = logging.getLogger(__name__)


class HandTracker:
    """
    Real-time hand tracking using MediaPipe Hands.
    Provides hand landmark detection and preprocessing for gesture recognition.
    """
    
    def __init__(
        self,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
        max_num_hands: int = 2
    ):
        """
        Initialize MediaPipe Hands.
        
        Args:
            min_detection_confidence: Minimum confidence for hand detection
            min_tracking_confidence: Minimum confidence for hand tracking
            max_num_hands: Maximum number of hands to detect
        """
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
    
    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, Optional[List[Dict]]]:
        """
        Process a single frame to detect hands and extract landmarks.
        
        Args:
            frame: Input image frame (BGR format from OpenCV)
            
        Returns:
            Tuple of (annotated_frame, hand_landmarks_list)
        """
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = self.hands.process(rgb_frame)
        
        # Annotate the frame
        annotated_frame = frame.copy()
        hand_landmarks_list = []
        
        if results.multi_hand_landmarks:
            for hand_idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                # Draw landmarks on frame
                self.mp_drawing.draw_landmarks(
                    annotated_frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style()
                )
                
                # Extract landmark coordinates
                landmarks = []
                for landmark in hand_landmarks.landmark:
                    landmarks.append({
                        'x': landmark.x,
                        'y': landmark.y,
                        'z': landmark.z
                    })
                
                # Get handedness (left or right)
                handedness = "Unknown"
                if results.multi_handedness:
                    handedness = results.multi_handedness[hand_idx].classification[0].label
                
                hand_landmarks_list.append({
                    'landmarks': landmarks,
                    'handedness': handedness
                })
        
        return annotated_frame, hand_landmarks_list if hand_landmarks_list else None
    
    def extract_hand_region(
        self,
        frame: np.ndarray,
        landmarks: List[Dict],
        padding: int = 20
    ) -> Optional[np.ndarray]:
        """
        Extract hand region from frame using landmarks.
        
        Args:
            frame: Input image frame
            landmarks: List of hand landmarks
            padding: Padding around hand region in pixels
            
        Returns:
            Cropped hand region or None if extraction fails
        """
        if not landmarks:
            return None
        
        h, w, _ = frame.shape
        
        # Get bounding box coordinates
        x_coords = [lm['x'] * w for lm in landmarks]
        y_coords = [lm['y'] * h for lm in landmarks]
        
        x_min = max(0, int(min(x_coords)) - padding)
        x_max = min(w, int(max(x_coords)) + padding)
        y_min = max(0, int(min(y_coords)) - padding)
        y_max = min(h, int(max(y_coords)) + padding)
        
        # Extract region
        hand_region = frame[y_min:y_max, x_min:x_max]
        
        return hand_region if hand_region.size > 0 else None
    
    def preprocess_for_classification(
        self,
        hand_region: np.ndarray,
        target_size: Tuple[int, int] = (144, 144)
    ) -> np.ndarray:
        """
        Preprocess hand region for gesture classification.
        
        Args:
            hand_region: Cropped hand region
            target_size: Target size for resizing
            
        Returns:
            Preprocessed image ready for model input
        """
        # Resize to target size
        resized = cv2.resize(hand_region, target_size, interpolation=cv2.INTER_AREA)
        
        # Normalize pixel values to [-1, 1]
        normalized = (resized.astype(np.float32) / 127.5) - 1.0
        
        # Add batch dimension
        preprocessed = np.expand_dims(normalized, axis=0)
        
        return preprocessed
    
    def get_hand_features(self, landmarks: List[Dict]) -> np.ndarray:
        """
        Extract feature vector from hand landmarks for classification.
        
        Args:
            landmarks: List of hand landmarks
            
        Returns:
            Feature vector (flattened coordinates)
        """
        # Flatten all landmark coordinates
        features = []
        for lm in landmarks:
            features.extend([lm['x'], lm['y'], lm['z']])
        
        return np.array(features, dtype=np.float32)
    
    def classify_hand_type(self, landmarks: List[Dict]) -> str:
        """
        Classify whether gesture is one-hand or two-hand.
        Simple heuristic based on landmark spread.
        
        Args:
            landmarks: List of hand landmarks
            
        Returns:
            "one_hand" or "two_hand"
        """
        # Calculate spread of landmarks
        x_coords = [lm['x'] for lm in landmarks]
        y_coords = [lm['y'] for lm in landmarks]
        
        x_spread = max(x_coords) - min(x_coords)
        y_spread = max(y_coords) - min(y_coords)
        
        # Simple threshold-based classification
        # Two-hand gestures typically have larger spread
        if x_spread > 0.5 or y_spread > 0.5:
            return "two_hand"
        return "one_hand"
    
    def close(self):
        """Release resources."""
        self.hands.close()
    
    def __del__(self):
        """Cleanup on deletion."""
        self.close()
