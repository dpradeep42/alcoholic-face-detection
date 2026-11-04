# alcoholic-face-detection

Two small experiments from the same project:

* **Face attributes.** `drunk.csv` and `normal.csv` are rows of facial attributes (smile, emotion scores, eye occlusion, and so on). `train.ipynb` fits a small Keras network and an XGBoost classifier that label a row as intoxicated (`1`) or not (`0`). `demo.ipynb` trains the same style of network and plots loss and accuracy. `FaceAnalysis.ipynb` is empty.
* **License plates.** `VehicleDetection/NumberDetection.ipynb` reads a still photo, finds a plate-shaped region with OpenCV, reads the text with Tesseract, and can append the plate and a timestamp to a Google Sheet named `DriverInfo`. `VehicleDetection/detect_plate.py` runs only the OpenCV crop, which does not need a camera or a Google account.

## Setup

Python 3.12.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Plate OCR also needs the Tesseract binary. The architecture diagram in `demo.ipynb` needs Graphviz:

```bash
sudo apt install tesseract-ocr graphviz
```

Open the notebooks from the repo root (face notebooks) or from `VehicleDetection/` (the plate notebook). Jupyter is not pinned in `requirements.txt`; install `notebook` if you want the `.ipynb` files.

## Credentials

Plate detection and the face notebooks do not need Google credentials. Only the last cells of `NumberDetection.ipynb`, which call `gspread`, do.

Do not commit a service-account JSON file. `VehicleDetection/DriverInfo-aa8a84cd0cc5.json` is no longer tracked. A real private key is still in git history (see below), so revoke that key in Google Cloud. This repo does not rewrite history.

To log rows to the sheet:

1. Create a Google Cloud service account, download its JSON key, and share the `DriverInfo` spreadsheet with that account's email.
2. Point the process at the key in either of these ways:
   * `export GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/key.json`
   * or copy the key to `VehicleDetection/credentials.json`

`VehicleDetection/credentials.py` checks the environment variable first, then the gitignored file. Both `VehicleDetection/*.json` and `.env` are ignored.

### Key that was committed earlier

History was left as-is. These commits touched `VehicleDetection/DriverInfo-aa8a84cd0cc5.json`:

| Commit | `private_key_id` | What is in the file |
| --- | --- | --- |
| `57669bd31d8d8f6b7b46555ff1a1b1c4c552d4bd` | `aa8a84cd0cc5e2543ce408dfda9ef00b9c20c137` | Valid 2048-bit RSA private key |
| `ee2c78aa1e60756dd8e749ef5940d8edd5f3d8f0` | `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` | Same key material, with the leading portion overwritten by `x` so the PEM no longer parses |
| `98b6cb7b2c6f48c642dc0a1c551b49ece163f010` | `xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` | Short placeholder, not a real key |

Delete or rotate the key for `private_key_id` `aa8a84cd0cc5e2543ce408dfda9ef00b9c20c137` in Google Cloud. The full key is still reachable from the first commit.

## Usage

Crop a plate from the sample photo (no Tesseract, no Google account):

```bash
python VehicleDetection/detect_plate.py VehicleDetection/data/images/car_3.jpg --output /tmp/plate.png
```

Other samples live in `VehicleDetection/data/images/`. With no arguments the script uses `car_3.jpg` and only prints the crop size.

In `VehicleDetection/NumberDetection.ipynb`, run the cells in order. The sheet cells call `load_gspread_client()` and then append `[plate text, timestamp]` to `DriverInfo` sheet 1. They raise `FileNotFoundError` until a key is configured.

Train the face classifier from the repo root by running `train.ipynb`. It reads `drunk.csv` and `normal.csv`, trains for 25 epochs, and saves `model.h5` (gitignored). `demo.ipynb` expects those same CSVs in the working directory.

## License

MIT. Copyright 2026 Pradeep Kumar Dasari. See [LICENSE](LICENSE).
