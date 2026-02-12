import os
import json
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

VERSION = "v1"
MODEL_DIR = os.path.join("app", "models", VERSION)
os.makedirs(MODEL_DIR, exist_ok=True)

# Small demo training data (replace with real dataset later)
texts = [
    "Apple releases new AI chip for iPhone",
    "Stock markets rally after inflation report",
    "Team wins the championship in final match",
    "Government announces new policy for taxes",
    "New Python library improves machine learning training",
    "Company earnings beat analyst expectations",
    "Cricket match delayed due to rain",
    "Parliament debate on budget continues",
]
labels = [
    "tech",
    "business",
    "sports",
    "politics",
    "tech",
    "business",
    "sports",
    "politics",
]

vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
X = vectorizer.fit_transform(texts)

model = LogisticRegression(max_iter=200)
model.fit(X, labels)

joblib.dump(model, os.path.join(MODEL_DIR, "classifier.joblib"))
joblib.dump(vectorizer, os.path.join(MODEL_DIR, "vectorizer.joblib"))

meta_path = os.path.join("app", "models", "metadata.json")
with open(meta_path, "w", encoding="utf-8") as f:
    json.dump({"current_version": VERSION}, f, indent=2)

print(f"Saved model artifacts to {MODEL_DIR}")
