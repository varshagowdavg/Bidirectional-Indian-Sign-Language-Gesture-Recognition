#!/usr/bin/env python3
import sys
sys.path.insert(0, 'backend')

from app.services.gesture_classifier import GestureClassifier
from app.services.hand_tracker import HandTracker
import cv2
import numpy as np

# Test if models load
print("Testing model loading...")
classifier = GestureClassifier()
print(f"Models loaded: {classifier.models_loaded}")
print(f"Classes: {classifier.classes}")

# Test hand tracker
print("\nTesting hand tracker...")
tracker = HandTracker()

# Create a simple test
print("\nTest complete!")
