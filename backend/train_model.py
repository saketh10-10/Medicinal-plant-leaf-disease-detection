"""
Plant Leaf Disease Classifier Training Script (PyTorch)

This script trains a deep learning model to classify plant leaf diseases using:
- PyTorch with EfficientNet_B0 or MobileNetV2 pretrained models
- Transfer learning for efficient training
- Data augmentation for better generalization
- Early stopping to prevent overfitting
- Comprehensive evaluation metrics

Input: dataset_processed/ with train/val/test splits
Output: plant_disease_model.pth (trained model)

Configuration:
- Model: EfficientNet_B0 or MobileNet_V2 (configurable)
- Input size: 224x224
- Training: 10-25 epochs with early stopping
- Optimizer: Adam with learning rate scheduling
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime
import json

# PyTorch imports
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms, models
from tqdm import tqdm

# Scikit-learn for metrics
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import seaborn as sns

# Configuration
DATASET_DIR = "dataset_processed"
MODEL_OUTPUT = "plant_disease_model.pth"
IMAGE_SIZE = 224
BATCH_SIZE = 32
EPOCHS = 15  # Adjusted to be in 10-25 range as requested
LEARNING_RATE = 0.0001
# Options: "efficientnet_b0", "efficientnet_b3", "mobilenet_v2", "resnet50"
MODEL_TYPE = "resnet50"
EARLY_STOPPING_PATIENCE = 7  # Stop training if no improvement for this many epochs
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Set random seeds for reproducibility
torch.manual_seed(42)
np.random.seed(42)

def check_dataset_exists(dataset_dir: str) -> bool:
    """Check if the processed dataset exists."""
    dataset_path = Path(dataset_dir)
    
    if not dataset_path.exists():
        print(f"\n❌ Error: Dataset directory '{dataset_dir}' not found!")
        print("\n📋 Please run the preprocessing script first:")
        print("   python preprocess_dataset.py")
        return False
    
    # Check for train/val/test folders
    required_splits = ['train', 'val', 'test']
    for split in required_splits:
        split_path = dataset_path / split
        if not split_path.exists():
            print(f"\n❌ Error: '{split}' folder not found in {dataset_dir}")
            return False
    
    return True

def get_data_transforms():
    """Create data transforms with augmentation for training."""
    
    # Training transforms
    train_transform = transforms.Compose([
        transforms.RandomResizedCrop(IMAGE_SIZE, scale=(0.6, 1.0)),
        transforms.RandomRotation(30),
        transforms.RandomHorizontalFlip(),
        transforms.RandomVerticalFlip(),
        transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.2, hue=0.02),
        transforms.RandomAffine(degrees=20, translate=(0.1, 0.1)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])
    
    # Validation/Test transforms
    val_test_transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(IMAGE_SIZE),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    return train_transform, val_test_transform

def create_dataloaders(dataset_dir: str, batch_size: int):
    """Create PyTorch dataloaders."""
    
    train_transform, val_test_transform = get_data_transforms()
    
    # Create datasets
    train_dataset = datasets.ImageFolder(
        os.path.join(dataset_dir, 'train'),
        transform=train_transform
    )
    
    val_dataset = datasets.ImageFolder(
        os.path.join(dataset_dir, 'val'),
        transform=val_test_transform
    )
    
    test_dataset = datasets.ImageFolder(
        os.path.join(dataset_dir, 'test'),
        transform=val_test_transform
    )
    
    # Create dataloaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=0)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=0)
    
    return train_loader, val_loader, test_loader, train_dataset.classes

def build_model(num_classes: int, model_type: str = MODEL_TYPE):
    """Build transfer learning model using EfficientNet_B0 or MobileNetV2."""

    if model_type == "efficientnet_b0":
        # Load pretrained EfficientNet_B0
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
        # Load pretrained EfficientNet_B3 (larger backbone for better features)
        model = models.efficientnet_b3(weights=models.EfficientNet_B3_Weights.IMAGENET1K_V1)
        num_features = model.classifier[1].in_features
        model.classifier = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(num_features, num_classes)
        )
    elif model_type == "mobilenet_v2":
        # Load pretrained MobileNetV2
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
        # Load pretrained ResNet50
        model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
        num_features = model.fc.in_features
        model.fc = nn.Sequential(
            nn.Dropout(0.3),
            nn.Linear(num_features, num_classes)
        )
    else:
        raise ValueError(
            f"Unsupported model type: {model_type}. "
            "Choose 'efficientnet_b0', 'efficientnet_b3', 'mobilenet_v2', or 'resnet50'"
        )

    # Freeze base layers and only train classifier head
    for name, param in model.named_parameters():
        param.requires_grad = False

    # Unfreeze classifier / final block depending on architecture
    if hasattr(model, "classifier"):
        for param in model.classifier.parameters():
            param.requires_grad = True
    elif hasattr(model, "fc"):
        for param in model.fc.parameters():
            param.requires_grad = True

    return model.to(DEVICE)

def train_epoch(model, train_loader, criterion, optimizer):
    """Train for one epoch."""
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    pbar = tqdm(train_loader, desc='Training')
    for inputs, labels in pbar:
        inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
        
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()
        
        pbar.set_postfix({'loss': running_loss/len(train_loader), 'acc': 100.*correct/total})
    
    epoch_loss = running_loss / len(train_loader)
    epoch_acc = 100. * correct / total
    return epoch_loss, epoch_acc

def validate(model, val_loader, criterion):
    """Validate the model."""
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    
    with torch.no_grad():
        for inputs, labels in tqdm(val_loader, desc='Validation'):
            inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            
            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
    
    epoch_loss = running_loss / len(val_loader)
    epoch_acc = 100. * correct / total
    return epoch_loss, epoch_acc

def plot_training_history(history, output_path='training_history.png'):
    """Plot training and validation accuracy/loss."""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    epochs = range(1, len(history['train_loss']) + 1)
    
    # Accuracy plot
    ax1.plot(epochs, history['train_acc'], 'b-', label='Train Accuracy')
    ax1.plot(epochs, history['val_acc'], 'r-', label='Val Accuracy')
    ax1.set_title('Model Accuracy')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy (%)')
    ax1.legend()
    ax1.grid(True)
    
    # Loss plot
    ax2.plot(epochs, history['train_loss'], 'b-', label='Train Loss')
    ax2.plot(epochs, history['val_loss'], 'r-', label='Val Loss')
    ax2.set_title('Model Loss')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✓ Training history plot saved to: {output_path}")
    plt.close()

def plot_confusion_matrix(cm, class_names, output_path='confusion_matrix.png'):
    """Plot confusion matrix."""
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=class_names, yticklabels=class_names)
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✓ Confusion matrix saved to: {output_path}")
    plt.close()

def evaluate_model(model, test_loader, class_names):
    """Evaluate model and print metrics."""
    
    print("\n" + "="*60)
    print("MODEL EVALUATION")
    print("="*60)
    
    model.eval()
    all_preds = []
    all_labels = []
    
    with torch.no_grad():
        for inputs, labels in tqdm(test_loader, desc='Testing'):
            inputs = inputs.to(DEVICE)
            outputs = model(inputs)
            _, predicted = outputs.max(1)
            
            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.numpy())
    
    # Calculate metrics
    test_accuracy = accuracy_score(all_labels, all_preds) * 100
    
    print(f"\n📊 Test Accuracy: {test_accuracy:.2f}%")
    
    # Classification report
    print("\n" + "-"*60)
    print("CLASSIFICATION REPORT")
    print("-"*60)
    print(classification_report(all_labels, all_preds, target_names=class_names, digits=4))
    
    # Confusion matrix
    cm = confusion_matrix(all_labels, all_preds)
    plot_confusion_matrix(cm, class_names)
    
    return test_accuracy

def train_model():
    """Main training function."""
    
    print("\n" + "="*60)
    print("PLANT LEAF DISEASE CLASSIFIER TRAINING (PyTorch)")
    print("="*60)
    print(f"Device: {DEVICE}")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Check if dataset exists
    if not check_dataset_exists(DATASET_DIR):
        return
    
    # Create dataloaders
    print("📂 Loading dataset...")
    train_loader, val_loader, test_loader, class_names = create_dataloaders(DATASET_DIR, BATCH_SIZE)
    
    num_classes = len(class_names)
    
    print(f"✓ Found {num_classes} classes: {', '.join(class_names)}")
    print(f"✓ Training samples: {len(train_loader.dataset)}")
    print(f"✓ Validation samples: {len(val_loader.dataset)}")
    print(f"✓ Test samples: {len(test_loader.dataset)}")
    
    # Build model
    print(f"\n🏗️  Building {MODEL_TYPE} model...")
    model = build_model(num_classes, MODEL_TYPE)
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"✓ {MODEL_TYPE.upper()} model built with {total_params:,} total parameters")
    print(f"✓ Trainable parameters: {trainable_params:,}")
    
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', factor=0.5, patience=3)
    
    # Training history
    history = {
        'train_loss': [],
        'train_acc': [],
        'val_loss': [],
        'val_acc': []
    }

    best_val_acc = 0.0
    best_val_loss = float('inf')
    patience_counter = 0
    early_stopping_triggered = False
    
    # Train model
    print("\n" + "="*60)
    print("TRAINING")
    print("="*60 + "\n")
    
    for epoch in range(EPOCHS):
        print(f"\nEpoch {epoch+1}/{EPOCHS}")
        print("-" * 40)
        
        train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer)
        val_loss, val_acc = validate(model, val_loader, criterion)
        
        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)
        
        print(f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}%")
        print(f"Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.2f}%")

        # Save best model (based on validation accuracy)
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_acc': val_acc,
                'class_names': class_names,
                'model_type': MODEL_TYPE
            }, MODEL_OUTPUT)
            print(f"✓ Saved best model (Val Acc: {val_acc:.2f}%)")

        # Early stopping check (based on validation loss)
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            patience_counter = 0
        else:
            patience_counter += 1
            print(f"Early stopping counter: {patience_counter}/{EARLY_STOPPING_PATIENCE}")

        if patience_counter >= EARLY_STOPPING_PATIENCE:
            print(f"\n🛑 Early stopping triggered at epoch {epoch+1} (no improvement for {EARLY_STOPPING_PATIENCE} epochs)")
            early_stopping_triggered = True
            break

        scheduler.step(val_loss)

        # Log current learning rate
        current_lr = optimizer.param_groups[0]['lr']
        print(f"Learning Rate: {current_lr:.6f}")

    # Plot training history
    plot_training_history(history)
    
    # Load best model for evaluation
    print("\n📥 Loading best model for evaluation...")
    checkpoint = torch.load(MODEL_OUTPUT)
    model.load_state_dict(checkpoint['model_state_dict'])
    
    # Evaluate on test set
    test_accuracy = evaluate_model(model, test_loader, class_names)
    
    # Save class names
    with open('class_names.json', 'w') as f:
        json.dump(class_names, f, indent=2)
    print(f"✓ Class names saved to: class_names.json")
    
    # Final summary
    print("\n" + "="*60)
    print("TRAINING COMPLETE")
    print("="*60)
    print(f"✓ Model saved to: {MODEL_OUTPUT}")
    print(f"✓ Model type: {MODEL_TYPE}")
    print(f"✓ Best validation accuracy: {best_val_acc:.2f}%")
    print(f"✓ Final test accuracy: {test_accuracy:.2f}%")
    if early_stopping_triggered:
        print(f"✓ Early stopping triggered after {len(history['train_loss'])} epochs")
    else:
        print(f"✓ Training completed all {EPOCHS} epochs")
    print(f"✓ Training completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        train_model()
    except KeyboardInterrupt:
        print("\n\n⚠️  Training interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error during training: {str(e)}")
        raise
