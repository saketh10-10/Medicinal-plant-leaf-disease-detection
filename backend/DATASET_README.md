# Plant Leaf Dataset Preprocessing Script

This script preprocesses plant-leaf images for machine learning training.

## Features

- ✅ Automatic image resizing to 224x224
- ✅ Pixel value normalization (0-1 range)
- ✅ Automatic handling of corrupted/unreadable images
- ✅ Train/Val/Test split (70%/20%/10%)
- ✅ Works with any number of classes automatically
- ✅ Detailed progress reporting and statistics

## Requirements

```bash
pip install pillow numpy
```

## Input Structure

```
raw_dataset/
├── aloe_healthy/
│   ├── image1.jpg
│   ├── image2.png
│   └── ...
├── neem_blight/
│   ├── image1.jpg
│   └── ...
└── <other_classes>/
    └── ...
```

## Output Structure

```
dataset_processed/
├── train/
│   ├── aloe_healthy/
│   ├── neem_blight/
│   └── ...
├── val/
│   ├── aloe_healthy/
│   ├── neem_blight/
│   └── ...
└── test/
    ├── aloe_healthy/
    ├── neem_blight/
    └── ...
```

## Usage

1. Place your raw images in `raw_dataset/` with subfolders as class names
2. Run the script:

```bash
python preprocess_dataset.py
```

3. Processed images will be saved to `dataset_processed/`

## Configuration

You can modify these constants in the script:

```python
INPUT_DIR = "raw_dataset"          # Input directory
OUTPUT_DIR = "dataset_processed"   # Output directory
IMAGE_SIZE = (224, 224)            # Target image size
TRAIN_RATIO = 0.7                  # 70% for training
VAL_RATIO = 0.2                    # 20% for validation
TEST_RATIO = 0.1                   # 10% for testing
RANDOM_SEED = 42                   # For reproducibility
```

## Supported Image Formats

- JPG/JPEG
- PNG
- BMP
- TIFF
- WebP

## Example Output

```
============================================================
Plant Leaf Dataset Preprocessing
============================================================

✓ Found 3 classes: aloe_healthy, neem_blight, tulsi_healthy
✓ Created output directory structure in 'dataset_processed'

Processing class: aloe_healthy
----------------------------------------
  Found 150 images
  ✓ Processed: 148 | Skipped: 2
  Split → Train: 105 | Val: 30 | Test: 15

...

============================================================
SUMMARY
============================================================

Total images processed: 442
Total images skipped: 8

Class-wise breakdown:
----------------------------------------

aloe_healthy:
  Total: 150 | Processed: 148 | Skipped: 2
  Train: 105 | Val: 30 | Test: 15

...

============================================================
✓ Dataset preprocessing complete!
✓ Output saved to: dataset_processed/
============================================================
```
