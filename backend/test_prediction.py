"""
Quick test script to verify prediction is working.
Run this to test if the model loads and can make predictions.
"""

import sys
from pathlib import Path
from predict import predict_image, load_model_and_classes

def test_model_loading():
    """Test if model can be loaded"""
    print("=" * 60)
    print("Testing Model Loading")
    print("=" * 60)
    try:
        model, class_names = load_model_and_classes()
        print(f"[OK] Model loaded successfully!")
        print(f"   - Number of classes: {len(class_names)}")
        print(f"   - Classes: {', '.join(class_names[:5])}...")
        return True
    except Exception as e:
        print(f"[ERROR] Model loading failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_prediction(image_path: str):
    """Test prediction on a single image"""
    print("\n" + "=" * 60)
    print(f"Testing Prediction on: {image_path}")
    print("=" * 60)
    
    if not Path(image_path).exists():
        print(f"[ERROR] Image file not found: {image_path}")
        return False
    
    try:
        result = predict_image(image_path)
        print(f"[OK] Prediction successful!")
        print(f"   - Predicted Class: {result['class_name']}")
        print(f"   - Confidence: {result['confidence']:.2f}%")
        print(f"   - Class Index: {result['class_index']}")
        return True
    except Exception as e:
        print(f"[ERROR] Prediction failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Plant Disease Prediction Test")
    print("=" * 60 + "\n")
    
    # Test 1: Model loading
    model_ok = test_model_loading()
    
    if not model_ok:
        print("\n[ERROR] Model loading failed. Cannot proceed with prediction test.")
        sys.exit(1)
    
    # Test 2: Find a test image
    test_images = [
        "test.jpg",
        "lemon.JPG",
        "neemtest.jpeg",
        "dataset_processed/test/neem_healthy/0001.jpeg",
        "dataset_processed/test/AloeVera_healthy/0001.jpg",
    ]
    
    test_image = None
    for img_path in test_images:
        if Path(img_path).exists():
            test_image = img_path
            break
    
    if test_image:
        prediction_ok = test_prediction(test_image)
        if prediction_ok:
            print("\n[OK] All tests passed!")
            sys.exit(0)
        else:
            print("\n[ERROR] Prediction test failed.")
            sys.exit(1)
    else:
        print("\n[WARNING] No test image found. Model loading test passed.")
        print("   To test prediction, provide an image path:")
        print("   python test_prediction.py <image_path>")
        sys.exit(0)

