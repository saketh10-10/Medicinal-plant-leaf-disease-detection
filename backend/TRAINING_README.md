# Plant Leaf Disease Classifier Training

This script trains a deep learning model to classify plant leaf diseases using transfer learning.

## Features

- ✅ **Transfer Learning**: Uses pretrained MobileNetV2 for efficient training
- ✅ **Data Augmentation**: Rotation, flip, zoom, shift for better generalization
- ✅ **Automatic Normalization**: Images normalized to 0-1 range
- ✅ **Comprehensive Metrics**: Accuracy, loss, confusion matrix, classification report
- ✅ **Model Checkpointing**: Saves best model during training
- ✅ **Early Stopping**: Prevents overfitting
- ✅ **Learning Rate Scheduling**: Adaptive learning rate reduction

## Requirements

```bash
pip install -r requirements_training.txt
```

**Dependencies:**
- TensorFlow 2.15.0
- scikit-learn
- matplotlib
- seaborn
- pillow

## Prerequisites

1. **Preprocessed Dataset**: Run `preprocess_dataset.py` first to create `dataset_processed/`
2. **Dataset Structure**:
   ```
   dataset_processed/
   ├── train/
   │   ├── class1/
   │   ├── class2/
   │   └── ...
   ├── val/
   │   └── ...
   └── test/
       └── ...
   ```

## Usage

### Basic Training

```bash
python train_model.py
```

### What Happens During Training

1. **Data Loading**: Loads images from `dataset_processed/`
2. **Data Augmentation**: Applies random transformations to training images
3. **Model Building**: Creates MobileNetV2-based classifier
4. **Training**: Trains for up to 50 epochs (with early stopping)
5. **Evaluation**: Tests on test set and generates metrics
6. **Saves**:
   - `plant_disease_model.h5` - Trained model
   - `training_history.png` - Accuracy/loss plots
   - `confusion_matrix.png` - Confusion matrix visualization

## Configuration

Edit these constants in `train_model.py`:

```python
DATASET_DIR = "dataset_processed"   # Dataset directory
MODEL_OUTPUT = "plant_disease_model.h5"  # Output model file
IMAGE_SIZE = (224, 224)             # Image dimensions
BATCH_SIZE = 32                     # Batch size
EPOCHS = 50                         # Maximum epochs
LEARNING_RATE = 0.001               # Initial learning rate
```

## Output Files

### 1. plant_disease_model.h5
Trained Keras model ready for inference.

**Load the model:**
```python
from tensorflow import keras
model = keras.models.load_model('plant_disease_model.h5')
```

### 2. training_history.png
Plots showing training/validation accuracy and loss over epochs.

### 3. confusion_matrix.png
Heatmap showing model predictions vs true labels.

## Example Output

```
============================================================
PLANT LEAF DISEASE CLASSIFIER TRAINING
============================================================

📂 Loading dataset...
✓ Found 3 classes: aloe_healthy, neem_blight, tulsi_healthy
✓ Training samples: 350
✓ Validation samples: 100
✓ Test samples: 50

🏗️  Building model...
✓ Model built with 2,357,984 parameters

============================================================
TRAINING
============================================================

Epoch 1/50
11/11 [==============================] - 15s 1s/step - loss: 1.0234 - accuracy: 0.6571 - val_loss: 0.7234 - val_accuracy: 0.7500
...

============================================================
MODEL EVALUATION
============================================================

📊 Test Accuracy: 0.9200
📊 Test Loss: 0.2341

CLASSIFICATION REPORT
------------------------------------------------------------
              precision    recall  f1-score   support

 aloe_healthy       0.95      0.90      0.92        20
  neem_blight       0.88      0.95      0.91        20
tulsi_healthy       0.93      0.92      0.93        10

     accuracy                           0.92        50
    macro avg       0.92      0.92      0.92        50
 weighted avg       0.92      0.92      0.92        50

============================================================
TRAINING COMPLETE
============================================================
✓ Model saved to: plant_disease_model.h5
✓ Final test accuracy: 0.9200
✓ Final test loss: 0.2341
============================================================
```

## Tips for Better Results

1. **More Data**: Aim for 100+ images per class
2. **Balanced Classes**: Try to have similar numbers of images per class
3. **Quality Images**: Use clear, well-lit images
4. **Fine-tuning**: After initial training, unfreeze some base model layers for better accuracy
5. **Hyperparameter Tuning**: Experiment with learning rate, batch size, and augmentation parameters

## Troubleshooting

### "Dataset directory not found"
Run `python preprocess_dataset.py` first to create the processed dataset.

### Out of Memory Error
Reduce `BATCH_SIZE` (try 16 or 8).

### Low Accuracy
- Check if you have enough training data (100+ images per class)
- Verify images are correctly labeled
- Increase training epochs
- Try different augmentation parameters

## Next Steps

After training, use the model in your FastAPI backend:

```python
from tensorflow import keras
import numpy as np
from PIL import Image

# Load model
model = keras.models.load_model('plant_disease_model.h5')

# Predict
img = Image.open('leaf.jpg').resize((224, 224))
img_array = np.array(img) / 255.0
prediction = model.predict(np.expand_dims(img_array, axis=0))
```
