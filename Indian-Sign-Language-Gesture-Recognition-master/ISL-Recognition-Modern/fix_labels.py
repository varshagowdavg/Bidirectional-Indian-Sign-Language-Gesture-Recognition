#!/usr/bin/env python3
import numpy as np

# Load the label encoder
labels = np.load('backend/models/label_encoder.npy', allow_pickle=True)
print(f"Original labels ({len(labels)}): {labels}")

# Remove nan values
labels_clean = np.array([x for x in labels if str(x) != 'nan'])
print(f"\nCleaned labels ({len(labels_clean)}): {labels_clean}")

# Save the cleaned version
np.save('backend/models/label_encoder.npy', labels_clean)
print("\n✅ Label encoder cleaned and saved!")
