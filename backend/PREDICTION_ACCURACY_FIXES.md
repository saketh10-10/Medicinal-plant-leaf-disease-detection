# Prediction Accuracy Fixes

## Issues Fixed

### 1. **Image Preprocessing Mismatch** ✅ FIXED
- **Problem**: Prediction used `Resize(224, 224)` but training used `Resize(256) + CenterCrop(224)`
- **Impact**: Different preprocessing can cause significant accuracy drops
- **Fix**: Updated prediction preprocessing to match training exactly:
  ```python
  transforms.Resize(256),
  transforms.CenterCrop(224),
  transforms.ToTensor(),
  transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
  ```

### 2. **Model Architecture Mismatch** ✅ FIXED
- **Problem**: ResNet50 architecture didn't match training script
- **Impact**: Model couldn't load weights correctly
- **Fix**: Updated to match training: `Dropout(0.3) → Linear(2048, 18)`

## Current Status

✅ Model loads successfully  
✅ Predictions are working  
✅ Preprocessing matches training  

## Debugging Tools

### 1. Debug Prediction Script
Test a single image with detailed output:
```bash
cd backend
python debug_prediction.py <image_path> [expected_class]
```

Example:
```bash
python debug_prediction.py test.jpg AloeVera_healthy
python debug_prediction.py dataset_processed/test/neem_healthy/0001.jpeg neem_healthy
```

### 2. Test Prediction Script
Quick test of model loading and prediction:
```bash
python test_prediction.py
```

## Potential Issues & Solutions

### Issue 1: Low Confidence Scores
**Symptoms**: Predictions have low confidence (< 60%)

**Possible Causes**:
- Model might need retraining with more data
- Image quality might be poor
- Class imbalance in training data

**Solutions**:
1. Check model accuracy on test set:
   ```bash
   # Check if you have evaluation metrics from training
   # Look for accuracy in training logs
   ```

2. Retrain with more balanced data
3. Use data augmentation during training
4. Try different model architectures

### Issue 2: Wrong Predictions
**Symptoms**: Model predicts wrong class consistently

**Possible Causes**:
- Model not trained well enough
- Training data quality issues
- Class confusion (similar classes)

**Solutions**:
1. Check training accuracy:
   - Look at `confusion_matrix.png` if available
   - Review training logs for validation accuracy

2. Test on known good images:
   ```bash
   python debug_prediction.py dataset_processed/test/neem_healthy/0001.jpeg neem_healthy
   ```

3. Check if specific classes are confused:
   - Use debug script to see top-5 predictions
   - Identify which classes are being confused

### Issue 3: Inconsistent Predictions
**Symptoms**: Same image gives different predictions

**Possible Causes**:
- Model not in eval mode (should be fixed)
- Image preprocessing variations

**Solutions**:
1. Ensure model is in eval mode (already done)
2. Verify preprocessing is consistent
3. Check for image corruption

## Improving Accuracy

### 1. Retrain the Model
If accuracy is low, consider retraining:
```bash
python train_model.py
```

**Training Tips**:
- Use more epochs if validation loss is still decreasing
- Increase data augmentation
- Try different model architectures
- Balance the dataset classes

### 2. Data Quality
- Ensure training images are high quality
- Remove corrupted images
- Balance classes (similar number of images per class)
- Use diverse images (different angles, lighting, etc.)

### 3. Model Architecture
- Try different architectures: EfficientNet, MobileNet, ResNet
- Adjust dropout rates
- Experiment with learning rates

## Testing Your Model

### Test on Known Images
```bash
# Test on images from test set (should be accurate)
python debug_prediction.py dataset_processed/test/neem_healthy/0001.jpeg neem_healthy
python debug_prediction.py dataset_processed/test/AloeVera_healthy/0001.jpg AloeVera_healthy
```

### Check Top Predictions
The debug script shows top-5 predictions. If the correct class is in top-3, the model is learning but might need:
- More training
- Better data
- Different architecture

## Next Steps

1. **Test on multiple images**:
   ```bash
   python debug_prediction.py <image1> <expected_class1>
   python debug_prediction.py <image2> <expected_class2>
   ```

2. **Check training metrics**:
   - Review training logs
   - Check confusion matrix
   - Look at validation accuracy

3. **If accuracy is still low**:
   - Consider retraining with more data
   - Try different model architectures
   - Improve data quality

## Files Modified

1. **backend/predict.py**:
   - Fixed image preprocessing to match training
   - Fixed ResNet50 architecture
   - Added top-k predictions for debugging

2. **backend/debug_prediction.py** (NEW):
   - Debug script to test predictions
   - Shows top-5 predictions
   - Compares with expected class

## Verification

Run these commands to verify everything works:
```bash
# 1. Test model loading
python test_prediction.py

# 2. Debug a prediction
python debug_prediction.py test.jpg

# 3. Test on known good image
python debug_prediction.py dataset_processed/test/neem_healthy/0001.jpeg neem_healthy
```

If all tests pass, the prediction system is working correctly. If predictions are still wrong, the issue is likely with:
- Model training quality
- Data quality
- Need for retraining

