"""
Debug script to test predictions and see top-k results.
Helps diagnose why predictions might be incorrect.
"""

import sys
from pathlib import Path
from predict import predict_image, load_model_and_classes

def debug_prediction(image_path: str, expected_class: str = None):
    """Debug a prediction with detailed output."""
    print("=" * 70)
    print(f"DEBUGGING PREDICTION: {image_path}")
    print("=" * 70)
    
    if not Path(image_path).exists():
        print(f"[ERROR] Image file not found: {image_path}")
        return
    
    try:
        # Load model info
        model, class_names = load_model_and_classes()
        print(f"\n[INFO] Model loaded with {len(class_names)} classes")
        print(f"[INFO] Classes: {', '.join(class_names)}\n")
        
        # Make prediction
        result = predict_image(image_path, top_k=5)
        
        print(f"\n{'='*70}")
        print("PREDICTION RESULTS")
        print(f"{'='*70}")
        print(f"Top Prediction: {result['class_name']}")
        print(f"Confidence: {result['confidence']:.2f}%")
        print(f"Class Index: {result['class_index']}")
        
        if expected_class:
            is_correct = result['class_name'].lower() == expected_class.lower()
            print(f"\nExpected: {expected_class}")
            print(f"Match: {'[OK] CORRECT' if is_correct else '[ERROR] INCORRECT'}")
        
        print(f"\n{'='*70}")
        print("TOP 5 PREDICTIONS:")
        print(f"{'='*70}")
        for i, (class_name, confidence) in enumerate(result['top_predictions'], 1):
            marker = ">>>" if i == 1 else "   "
            print(f"{marker} {i}. {class_name:30s} {confidence:6.2f}%")
        
        print(f"\n{'='*70}\n")
        
    except Exception as e:
        print(f"[ERROR] Prediction failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python debug_prediction.py <image_path> [expected_class]")
        print("\nExample:")
        print("  python debug_prediction.py test.jpg AloeVera_healthy")
        print("  python debug_prediction.py dataset_processed/test/neem_healthy/0001.jpeg neem_healthy")
        sys.exit(1)
    
    image_path = sys.argv[1]
    expected_class = sys.argv[2] if len(sys.argv) > 2 else None
    
    debug_prediction(image_path, expected_class)

