# ☁️ CloudClassification

A Python deep learning project that classifies cloud images into the 11 standard meteorological cloud genera using a custom Xception-inspired CNN built with TensorFlow/Keras. Includes a purpose-built web scraper for dataset collection, a dataset merging utility, and separate CLI scripts for model creation, training, and single-image inference.

---

## Cloud Classes

The model classifies images into all 11 WMO cloud genera:

| Abbreviation | Cloud Type |
|---|---|
| Ac | Altocumulus |
| As | Altostratus |
| Cb | Cumulonimbus |
| Cc | Cirrocumulus |
| Ci | Cirrus |
| Cs | Cirrostratus |
| Ct | Contrail |
| Cu | Cumulus |
| Ns | Nimbostratus |
| Sc | Stratocumulus |
| St | Stratus |

---

## Dataset Pipeline

The dataset was built from scratch using a two-step scraping and merging pipeline:

### 1. `imageScraper/imageScraper.py` — Web scraper

Crawls a German meteorological photo gallery website, automatically categorising and downloading cloud images:

- Traverses all gallery pages discovered via a `<select>` dropdown on the index page
- For each image entry, fetches the detail page and extracts the cloud type by parsing the `<b>` tag with a regex
- Creates a local folder per cloud type and downloads all `.jpg` images into it

```bash
python imageScraper.py <gallery-url>
```

### 2. `imageScraper/copy.py` — Dataset merger

After scraping, cloud type folder names may contain comma-separated multi-label categories (e.g. `"Cu, Cb"`). `copy.py` resolves these by checking whether all labels share the same 2-letter prefix, and if so copies the images into the corresponding class folder in `mergedDataset/`. Single-label folders are copied directly. The final merged dataset contains **2,543 images** across **11 classes**.

---

## Model Architecture

A custom Xception-style CNN built from scratch with Keras:

- **Input** — 180×180 RGB images
- **Data augmentation** — Random horizontal flip and random rotation applied during training
- **Entry block** — Two Conv2D layers (32 and 64 filters) with batch normalisation and ReLU
- **Residual blocks** — Four blocks with depthwise separable convolutions at sizes 128 → 256 → 512 → 728, each with MaxPooling and a projected residual connection
- **Top block** — SeparableConv2D (1024 filters), GlobalAveragePooling, Dropout (0.5)
- **Output** — Softmax over N classes (or sigmoid for binary); trained with categorical crossentropy and the Adam optimiser
- **Checkpointing** — Model saved after each epoch via `ModelCheckpoint`

---

## Project Structure

```
CloudClassification/
├── createModel.py              # Build and save a fresh untrained model
├── trainModel.py               # Load and train a model on a dataset
├── classifyImage.py            # Run inference on a single image
├── image_classification_01.py  # Original all-in-one prototype script
└── imageScraper/
    ├── imageScraper.py         # Web scraper for cloud image collection
    └── copy.py                 # Merge scraped folders into clean dataset
```

---

## Usage

### 1. Scrape dataset

```bash
cd imageScraper
python imageScraper.py <gallery-url>
python copy.py
```

### 2. Create a model

Builds and saves an untrained model whose output size matches the number of class folders in the dataset:

```bash
python createModel.py <modelfile.h5> <datasetPath>
```

### 3. Train the model

Loads an existing model and trains it for a given number of epochs, saving a checkpoint after each:

```bash
python trainModel.py <model.h5> <datasetPath> <epochs>
```

The dataset directory should contain one subfolder per class (e.g. `Ac/`, `Cu/`, `Cb/`, etc.) with JPEG images inside.

### 4. Classify an image

Runs inference on a single image, printing the confidence score for each class and the winner:

```bash
python classifyImage.py <model.h5> <image.jpg>
```

**Example output:**
```
Ac   2.31
As   1.07
Cb   0.84
Cu  91.45
...
Winner: Cu with 91.45
```

---

## Requirements

```bash
pip install tensorflow numpy matplotlib requests beautifulsoup4
```

---

## License

This project is licensed under the [MIT License](LICENSE).