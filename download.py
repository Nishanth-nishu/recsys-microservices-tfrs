from pathlib import Path
import kagglehub
import shutil

# --------------------------------------------------
# Path handling (PRODUCTION-SAFE)
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# Download dataset via KaggleHub (cache already in /scratch)
# --------------------------------------------------
dataset_path = Path(
    kagglehub.dataset_download("shivamparab/amazon-electronics-reviews")
)

print("Dataset downloaded to:", dataset_path)

SOURCE_FILE = dataset_path / "Electronics_5.json"

if not SOURCE_FILE.exists():
    raise FileNotFoundError(f"Expected file not found: {SOURCE_FILE}")

TARGET_FILE = RAW_DIR / "Electronics_5.json"

# Copy once (idempotent)
if not TARGET_FILE.exists():
    shutil.copy2(SOURCE_FILE, TARGET_FILE)
    print(f"Copied dataset to {TARGET_FILE}")
else:
    print(f"Dataset already exists at {TARGET_FILE}")
