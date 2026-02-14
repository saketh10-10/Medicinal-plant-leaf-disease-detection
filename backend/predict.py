"""
Plant Disease Prediction Script

This script loads a trained PyTorch model and performs inference on individual plant leaf images.

Usage:
    python predict.py path/to/image.jpg

Or import and use the predict_image function:
    from predict import predict_image
    result = predict_image("path/to/image.jpg")
    print(f"Predicted: {result['class_name']} with {result['confidence']:.2f}% confidence")
"""

import os
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import json
from pathlib import Path
import sys
import traceback

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent.absolute()

# Configuration (must match training script)
IMAGE_SIZE = 224
MODEL_PATH = SCRIPT_DIR / "plant_disease_model.pth"
DATASET_DIR = SCRIPT_DIR / "dataset_processed"
CLASS_NAMES_PATH = SCRIPT_DIR / "class_names.json"
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Global model cache to avoid reloading
_model_cache = None
_class_names_cache = None

def get_image_transforms():
    """Create image transforms matching those used during training validation/testing."""
    # Match training script: Resize(256) then CenterCrop(224) for validation/test
    return transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(IMAGE_SIZE),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

def build_model(num_classes: int, model_type: str):
    """Build model architecture matching the training script."""
    try:
        if model_type == "efficientnet_b0":
            model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.IMAGENET1K_V1)
            num_features = model.classifier[1].in_features
            model.classifier = nn.Sequential(
                nn.Dropout(0.5),
                nn.Linear(num_features, 256),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(256, num_classes)
            )
        elif model_type == "efficientnet_b3":
            model = models.efficientnet_b3(weights=models.EfficientNet_B3_Weights.IMAGENET1K_V1)
            num_features = model.classifier[1].in_features
            model.classifier = nn.Sequential(
                nn.Dropout(0.5),
                nn.Linear(num_features, 512),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(512, num_classes)
            )
        elif model_type == "mobilenet_v2":
            model = models.mobilenet_v2(weights=models.MobileNet_V2_Weights.IMAGENET1K_V1)
            num_features = model.classifier[1].in_features
            model.classifier = nn.Sequential(
                nn.Dropout(0.5),
                nn.Linear(num_features, 256),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(256, num_classes)
            )
        elif model_type == "resnet50":
            model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
            num_features = model.fc.in_features
            # Match training script architecture: direct connection with dropout
            model.fc = nn.Sequential(
                nn.Dropout(0.3),
                nn.Linear(num_features, num_classes)
            )
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
        
        return model.to(DEVICE)
    except Exception as e:
        raise RuntimeError(f"Failed to build model architecture '{model_type}': {str(e)}")

def get_class_names_from_dataset():
    """Extract class names from the dataset directory structure."""
    train_dir = DATASET_DIR / 'train'
    if not train_dir.exists():
        raise FileNotFoundError(f"Training directory not found: {train_dir}")

    class_names = []
    for item in sorted(train_dir.iterdir()):
        if item.is_dir():
            class_names.append(item.name)

    if not class_names:
        raise ValueError(f"No class directories found in {train_dir}")

    return class_names

def load_model_and_classes(force_reload=False):
    """
    Load the trained model and class names.
    Uses caching to avoid reloading on every prediction.
    """
    global _model_cache, _class_names_cache
    
    # Return cached model if available and not forcing reload
    if not force_reload and _model_cache is not None and _class_names_cache is not None:
        return _model_cache, _class_names_cache
    
    try:
        # Check if model file exists
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Model file not found: {MODEL_PATH}\n"
                f"Current working directory: {os.getcwd()}\n"
                f"Script directory: {SCRIPT_DIR}\n"
                f"Please train the model first or ensure the model file exists."
            )

        # Load checkpoint
        try:
            checkpoint = torch.load(str(MODEL_PATH), map_location=DEVICE)
        except Exception as e:
            raise RuntimeError(f"Failed to load model checkpoint from {MODEL_PATH}: {str(e)}")

        # Get class names from checkpoint, JSON file, or dataset
        class_names = None
        
        # Try checkpoint first
        if 'class_names' in checkpoint:
            class_names = checkpoint['class_names']
            print(f"[OK] Loaded {len(class_names)} class names from checkpoint")
        
        # Try JSON file
        elif CLASS_NAMES_PATH.exists():
            try:
                with open(CLASS_NAMES_PATH, 'r', encoding='utf-8') as f:
                    class_names = json.load(f)
                print(f"[OK] Loaded {len(class_names)} class names from {CLASS_NAMES_PATH}")
            except Exception as e:
                print(f"[WARNING] Could not load class names from JSON: {e}")
        
        # Fallback to dataset directory
        if class_names is None:
            try:
                class_names = get_class_names_from_dataset()
                print(f"[OK] Loaded {len(class_names)} class names from dataset directory")
            except Exception as e:
                raise RuntimeError(f"Could not determine class names: {e}")

        if not class_names:
            raise ValueError("Class names list is empty")

        num_classes = len(class_names)
        model_type = checkpoint.get('model_type', 'efficientnet_b0')
        
        print(f"[OK] Model type: {model_type}, Number of classes: {num_classes}")

        # Build model
        try:
            model = build_model(num_classes, model_type)
        except Exception as e:
            raise RuntimeError(f"Failed to build model: {str(e)}")

        # Load model state
        try:
            if 'model_state_dict' in checkpoint:
                model.load_state_dict(checkpoint['model_state_dict'], strict=False)
                print("[OK] Model state dict loaded successfully")
            else:
                raise KeyError("'model_state_dict' not found in checkpoint")
        except Exception as e:
            # Try loading without strict mode if there's a mismatch
            try:
                model.load_state_dict(checkpoint['model_state_dict'], strict=False)
                print(f"[WARNING] Model loaded with some mismatches: {e}")
            except Exception as e2:
                raise RuntimeError(f"Failed to load model state dict: {str(e2)}")

        model.eval()
        
        # Cache the model and class names
        _model_cache = model
        _class_names_cache = class_names
        
        print(f"[OK] Model loaded successfully on {DEVICE}")
        return model, class_names

    except Exception as e:
        error_msg = f"Error loading model: {str(e)}\n{traceback.format_exc()}"
        print(f"[ERROR] {error_msg}")
        raise RuntimeError(error_msg)

def predict_image(image_path: str, top_k: int = 3):
    """
    Predict plant disease from a single image.

    Args:
        image_path (str): Path to the image file
        top_k (int): Number of top predictions to return (default: 3)

    Returns:
        dict: {
            'class_name': str,
            'confidence': float (0-100),
            'class_index': int,
            'top_predictions': list of (class_name, confidence) tuples
        }
    """
    try:
        # Load model and classes (will use cache if already loaded)
        model, class_names = load_model_and_classes()

        # Get transforms
        transform = get_image_transforms()

        # Load and preprocess image
        try:
            image_path_obj = Path(image_path)
            if not image_path_obj.exists():
                raise FileNotFoundError(f"Image file not found: {image_path}")
            
            image = Image.open(str(image_path_obj)).convert('RGB')
        except Exception as e:
            raise ValueError(f"Could not load image {image_path}: {e}")
        
        # Ensure image is valid
        if image.size[0] < 1 or image.size[1] < 1:
            raise ValueError(f"Invalid image dimensions: {image.size}")

        # Apply transforms
        try:
            input_tensor = transform(image).unsqueeze(0).to(DEVICE)
        except Exception as e:
            raise RuntimeError(f"Failed to preprocess image: {e}")

        # Run inference
        try:
            with torch.no_grad():
                outputs = model(input_tensor)
                probabilities = torch.softmax(outputs, dim=1)
                confidence, predicted_idx = torch.max(probabilities, 1)
                
                # Get top-k predictions for debugging
                top_probs, top_indices = torch.topk(probabilities, min(top_k, len(class_names)), dim=1)
        except Exception as e:
            raise RuntimeError(f"Model inference failed: {e}")

        predicted_idx_value = predicted_idx.item()
        
        # Validate index
        if predicted_idx_value < 0 or predicted_idx_value >= len(class_names):
            raise IndexError(f"Predicted index {predicted_idx_value} is out of range for {len(class_names)} classes")

        predicted_class = class_names[predicted_idx_value]
        confidence_score = confidence.item() * 100
        
        # Build top predictions list
        top_predictions = []
        for i in range(top_probs.size(1)):
            idx = top_indices[0][i].item()
            prob = top_probs[0][i].item() * 100
            top_predictions.append((class_names[idx], prob))

        return {
            'class_name': predicted_class,
            'confidence': confidence_score,
            'class_index': predicted_idx_value,
            'top_predictions': top_predictions
        }

    except Exception as e:
        error_msg = f"Prediction failed: {str(e)}"
        print(f"[ERROR] {error_msg}")
        print(traceback.format_exc())
        raise RuntimeError(error_msg)

def main():
    """Command line interface for prediction."""
    if len(sys.argv) != 2:
        print("Usage: python predict.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]

    try:
        result = predict_image(image_path)
        print(f"\n🖼️  Image: {image_path}")
        print(f"🌿 Predicted Class: {result['class_name']}")
        print(f"📊 Confidence: {result['confidence']:.2f}%")
        print(f"🔢 Class Index: {result['class_index']}\n")

    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
