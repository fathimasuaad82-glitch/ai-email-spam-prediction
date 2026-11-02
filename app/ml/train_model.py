
import pandas as pd
import joblib

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

# Project main folder location
BASE_DIR = Path(__file__).resolve().parents[2]

# Load dataset
data = pd.read_csv(BASE_DIR / "spam.csv", encoding="latin-1")

# Support common Kaggle CSV column names
if "v1" in data.columns and "v2" in data.columns:
    data = data.rename(columns={"v1": "label", "v2": "message"})

# Select required columns
data = data[["label", "message"]].dropna()

# Prepare data
X = data["message"].astype(str)
y = data["label"].astype(str).str.lower().str.strip()

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Create AI model
model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("classifier", MultinomialNB())
])

# Train model
model.fit(X_train, y_train)

# Test model
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

# Save trained model
joblib.dump(model, BASE_DIR / "spam_model.pkl")

print("AI Model Training Completed!")
print("Model Accuracy:", round(accuracy * 100, 2), "%")
print("Model saved successfully!")
