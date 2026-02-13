# ML Models Directory

This directory should contain the trained machine learning models for ISL gesture recognition.

## Required Files

Place the following model files in this directory:

### 1. **one_hand144.h5**
- One-hand gesture CNN model
- Input size: 144×144 pixels
- Classes: c, i, j, l, o, u, v (7 classes)
- Accuracy: ~98.52%

### 2. **fintwo_handVGG.h5**
- Two-hand gesture VGG16-based model
- Input size: 64×64 pixels
- Classes: a, b, d, e, f, g, h, k, m, n, p, q, r, s, t, w, x, y, z (19 classes)
- Accuracy: ~97%

### 3. **HOG_full_newaug.sav**
- HOG + SVM classifier
- Purpose: Classifies gestures as one-hand or two-hand
- Accuracy: ~96.79%

### 4. **SCfull_newaug.sav**
- StandardScaler for feature normalization
- Used with HOG features

### 5. **PCAfull_newaug.sav**
- PCA transformer for dimensionality reduction
- Used with HOG features

### 6. **my_words_sort.pickle**
- Sorted English dictionary for spell correction
- Used to validate and correct predicted words

## How to Obtain Models

These model files are **not included** in the repository due to their large size.

### Option 1: Train Your Own Models
1. Collect/use the ISL dataset (150,000+ images)
2. Train the hierarchical CNN models
3. Train the HOG+SVM classifier
4. Save the models in this directory

### Option 2: Request from Original Authors
Contact the original research team for pre-trained models.

### Option 3: Use Alternative Models
You can train alternative models and update the paths in `.env` file.

## Model Architecture

```
Input Image
    ↓
HOG Feature Extraction
    ↓
SVM Classifier (one-hand vs two-hand)
    ↓
    ├─→ One-hand CNN (one_hand144.h5)
    │   └─→ 7 classes
    └─→ Two-hand CNN (fintwo_handVGG.h5)
        └─→ 19 classes
    ↓
Dictionary Correction (my_words_sort.pickle)
    ↓
Final Prediction
```

## File Size Expectations

- `one_hand144.h5`: ~50-100 MB
- `fintwo_handVGG.h5`: ~50-100 MB
- `HOG_full_newaug.sav`: ~10-50 MB
- `SCfull_newaug.sav`: ~1-10 MB
- `PCAfull_newaug.sav`: ~1-10 MB
- `my_words_sort.pickle`: ~1-5 MB

## Testing Models

After placing the models, run:

```bash
python manage.py runserver
```

Check the console output for model loading messages:
```
✓ Loaded one-hand model from models/one_hand144.h5
✓ Loaded two-hand model from models/fintwo_handVGG.h5
✓ Loaded HOG/SVM models
✓ Loaded dictionary with XXXXX words
```

If you see errors, check:
1. File paths are correct
2. Files are not corrupted
3. TensorFlow/Keras versions are compatible

## Notes

- Models are loaded once at server startup
- Large models may take 10-30 seconds to load
- Ensure sufficient RAM (4GB+ recommended)
- GPU acceleration recommended for real-time inference
