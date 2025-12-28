import json
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# Path handling (PRODUCTION-SAFE)
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

RAW_PATH = DATA_DIR / "raw" / "Electronics_5.json"
OUT_PATH = DATA_DIR / "processed" / "interactions.csv"

OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

if not RAW_PATH.exists():
    raise FileNotFoundError(f"Raw dataset not found at {RAW_PATH}")

# --------------------------------------------------
# Preprocessing logic
# --------------------------------------------------
records = []

with open(RAW_PATH, "r", encoding="utf-8") as f:
    for line in f:
        review = json.loads(line)

        if review.get("overall", 0) >= 4:
            records.append({
                "user_id": review["reviewerID"],
                "item_id": review["asin"],
                "timestamp": review["unixReviewTime"],
                "label": 1
            })

df = pd.DataFrame(records)

# Temporal ordering (important for recommenders)
df = df.sort_values("timestamp")

# Remove sparse users/items
df = df.groupby("user_id").filter(lambda x: len(x) >= 5)
df = df.groupby("item_id").filter(lambda x: len(x) >= 5)

df.to_csv(OUT_PATH, index=False)

print(f"Saved {len(df)} interactions to {OUT_PATH}")
print(df.head())
