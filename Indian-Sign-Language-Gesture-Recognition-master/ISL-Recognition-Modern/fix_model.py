#!/usr/bin/env python3
import numpy as np
import tensorflow as tf
from tensorflow import keras

# Load the model
model = keras.models.load_model('backend/models/keypoint_classifier.hdf5')
print("Model summary:")
model.summary()

# Get the weights
weights = model.get_weights()
print(f"\nNumber of weight arrays: {len(weights)}")
for i, w in enumerate(weights):
    print(f"Weight {i}: shape {w.shape}")

# The last layer should have 48 outputs (including nan)
# We need to remove the last column (nan class)
print("\nRemoving nan class from output layer...")

# Rebuild model with 47 outputs
new_model = keras.Sequential([
    keras.layers.Dense(128, activation='relu', input_shape=(42,)),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(64, activation='relu'),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(47, activation='softmax')  # 47 instead of 48
])

# Copy weights, excluding the last column of the final layer
new_weights = []
for i, w in enumerate(weights):
    if i == len(weights) - 2:  # Last Dense layer weights
        # Remove the last column (nan class)
        new_weights.append(w[:, :-1])
        print(f"Trimmed weight {i} from {w.shape} to {w[:, :-1].shape}")
    elif i == len(weights) - 1:  # Last Dense layer bias
        # Remove the last bias (nan class)
        new_weights.append(w[:-1])
        print(f"Trimmed bias {i} from {w.shape} to {w[:-1].shape}")
    else:
        new_weights.append(w)

new_model.set_weights(new_weights)

# Save the new model
new_model.save('backend/models/keypoint_classifier.hdf5')
print("\n✅ Model updated and saved with 47 classes!")
