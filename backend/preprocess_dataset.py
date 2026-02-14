"""
Plant Leaf Image Dataset Preprocessing Script (NumPy-free version)

This script preprocesses plant-leaf images for machine learning by:
1. Resizing images to 224x224
2. Normalizing pixel values to 0-1 range
3. Automatically skipping corrupted/unreadable images
4. Splitting data into train (70%), val (20%), and test (10%) sets

Input: raw_dataset/ with subfolders as class names
Output: dataset_processed/ with train/val/test splits
"""

import os
import shutil
from pathlib import Path
from PIL import Image, ImageOps
from typing import List, Tuple, Dict
import random

# Configuration
INPUT_DIR = "raw_dataset"
OUTPUT_DIR = "dataset_processed"
IMAGE_SIZE = (224, 224)
TRAIN_RATIO = 0.7
VAL_RATIO = 0.2
TEST_RATIO = 0.1
RANDOM_SEED = 42
MIN_SIZE = 50  # Minimum width/height (less strict)

# Supported image formats
SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}

def create_output_structure(output_dir: str, classes: List[str]) -> None:
    """Create output directory structure for train/val/test splits."""
    for split in ['train', 'val', 'test']:
        for class_name in classes:
            split_dir = Path(output_dir) / split / class_name
            split_dir.mkdir(parents=True, exist_ok=True)
    print(f"✓ Created output directory structure in '{output_dir}'")

def get_classes(input_dir: str) -> List[str]:
    """Get list of class names from input directory subfolders."""
    input_path = Path(input_dir)
    
    # Check if input directory exists
    if not input_path.exists():
        print(f"⚠ Input directory '{input_dir}' not found!")
        print(f"✓ Creating '{input_dir}' with example class folders...\n")
        
        # Create raw_dataset directory
        input_path.mkdir(parents=True, exist_ok=True)
        
        # Create example class folders
        example_classes = ['example_class_1', 'example_class_2', 'example_class_3']
        for class_name in example_classes:
            class_dir = input_path / class_name
            class_dir.mkdir(exist_ok=True)
        
        # Print instructions
        print("=" * 60)
        print("📁 SETUP REQUIRED")
        print("=" * 60)
        print(f"\nI've created the '{input_dir}/' folder with example class folders:")
        for class_name in example_classes:
            print(f"  - {input_dir}/{class_name}/")
        
        print("\n📋 NEXT STEPS:")
        print("-" * 60)
        print("1. Delete or rename the example class folders")
        print("2. Create your own class folders (e.g., 'aloe_healthy', 'neem_blight')")
        print("3. Put your raw plant images inside each class folder")
        print("4. Run this script again: python preprocess_dataset.py")
        
        print("\n💡 EXAMPLE STRUCTURE:")
        print("-" * 60)
        print(f"{input_dir}/")
        print("├── aloe_healthy/")
        print("│   ├── image1.jpg")
        print("│   ├── image2.png")
        print("│   └── ...")
        print("├── neem_blight/")
        print("│   └── ...")
        print("└── tulsi_healthy/")
        print("    └── ...")
        
        print("\n" + "=" * 60)
        print("✓ Setup complete! Add your images and run again.")
        print("=" * 60 + "\n")
        exit(0)
    
    classes = [d.name for d in input_path.iterdir() if d.is_dir()]
    if not classes:
        raise ValueError(f"No class folders found in '{input_dir}'")
    
    print(f"✓ Found {len(classes)} classes: {', '.join(classes)}")
    return classes

def is_valid_image(file_path: Path) -> bool:
    """Check if file is a valid image format."""
    return file_path.suffix.lower() in SUPPORTED_FORMATS

def preprocess_image(image_path: Path, output_path: Path) -> Tuple[bool, str]:
    """
    Preprocess a single image: validate, resize, and normalize.
    
    Args:
        image_path: Path to input image
        output_path: Path to save processed image
        
    Returns:
        (success, status_message)
    """
    try:
        # Open and convert to RGB (handles grayscale, RGBA, etc.)
        img = Image.open(image_path).convert("RGB")

        # Only enforce a very small minimum size check
        if min(img.size) < MIN_SIZE:
            return False, f"Too small {img.size}"

        # Resize and center crop to target size
        # ImageOps.fit resizes maintaining aspect ratio, then crops center
        img_processed = ImageOps.fit(img, IMAGE_SIZE, method=Image.Resampling.LANCZOS)
        
        # Save processed image
        img_processed.save(output_path, quality=95)
        return True, "Processed"
        
    except Exception as e:
        return False, f"Corrupted/Error: {str(e)}"

def split_files(files: List[Path], train_ratio: float, val_ratio: float, test_ratio: float) -> Tuple[List[Path], List[Path], List[Path]]:
    """Split files into train, validation, and test sets."""
    random.shuffle(files)
    
    total = len(files)
    train_end = int(total * train_ratio)
    val_end = train_end + int(total * val_ratio)
    
    train_files = files[:train_end]
    val_files = files[train_end:val_end]
    test_files = files[val_end:]
    
    return train_files, val_files, test_files

def process_dataset(input_dir: str, output_dir: str) -> None:
    """Main function to process the entire dataset."""
    print("\n" + "="*60)
    print("Plant Leaf Dataset Preprocessing")
    print("="*60 + "\n")
    
    # Set random seed for reproducibility
    random.seed(RANDOM_SEED)
    
    # Get classes from input directory
    classes = get_classes(input_dir)
    
    # Create output directory structure
    create_output_structure(output_dir, classes)
    
    # Statistics
    total_processed = 0
    total_skipped = 0
    class_stats = {}
    
    # Process each class
    for class_name in classes:
        print(f"\nProcessing class: {class_name}")
        print("-" * 40)
        
        class_input_dir = Path(input_dir) / class_name
        
        # Get all valid image files
        all_files = [f for f in class_input_dir.iterdir() if f.is_file() and is_valid_image(f)]
        
        if not all_files:
            print(f"  ⚠ No valid images found in {class_name}")
            continue
        
        print(f"  Found {len(all_files)} images")
        
        # Split into train/val/test
        train_files, val_files, test_files = split_files(all_files, TRAIN_RATIO, VAL_RATIO, TEST_RATIO)
        
        splits = {
            'train': train_files,
            'val': val_files,
            'test': test_files
        }
        
        class_processed = 0
        class_skipped = 0
        
        # Process each split
        for split_name, files in splits.items():
            output_class_dir = Path(output_dir) / split_name / class_name
            
            for img_file in files:
                output_path = output_class_dir / img_file.name
                
                success, reason = preprocess_image(img_file, output_path)
                
                if success:
                    class_processed += 1
                else:
                    class_skipped += 1
                    # print(f"    Skipped {img_file.name}: {reason}") # Optional: verbose logging
        
        total_processed += class_processed
        total_skipped += class_skipped
        
        class_stats[class_name] = {
            'total': len(all_files),
            'train': len(train_files),
            'val': len(val_files),
            'test': len(test_files),
            'processed': class_processed,
            'skipped': class_skipped,
            'success_rate': (class_processed / len(all_files) * 100) if all_files else 0
        }
        
        print(f"  ✓ Processed: {class_processed} | Skipped: {class_skipped}")
        if class_skipped > 0:
            print(f"    (Removed {class_skipped} low quality/corrupted images)")
        print(f"  Split → Train: {len(train_files)} | Val: {len(val_files)} | Test: {len(test_files)}")
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"\nTotal images processed: {total_processed}")
    print(f"Total images skipped: {total_skipped}")
    print(f"\nClass-wise breakdown:")
    print("-" * 40)
    
    for class_name, stats in class_stats.items():
        print(f"\n{class_name}:")
        print(f"  Total: {stats['total']} | Kept: {stats['processed']} | Removed: {stats['skipped']} ({100-stats['success_rate']:.1f}%)")
        print(f"  Train: {stats['train']} | Val: {stats['val']} | Test: {stats['test']}")
    
    print("\n" + "="*60)
    print(f"✓ Dataset preprocessing complete!")
    print(f"✓ Output saved to: {output_dir}/")
    print(f"✓ Images are resized to 224x224")
    print(f"✓ To normalize: divide pixel values by 255.0 in your training code")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        process_dataset(INPUT_DIR, OUTPUT_DIR)
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        exit(1)
