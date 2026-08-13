import os
import re
import math
import joblib


# =========================================================
# PATH CONFIGURATION
# =========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "calibrated_svm_model.pkl"
)

VECTORIZER_PATH = os.path.join(
    BASE_DIR,
    "models",
    "final_tfidf_vectorizer.pkl"
)


# =========================================================
# LOAD MODEL
# =========================================================

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


# =========================================================
# TEXT CLEANING
# =========================================================

def clean_text(text):
    """
    Clean news text before sending it to the ML model.
    """

    text = str(text)

    # Convert to lowercase
    text = text.lower()

    # Remove URLs
    text = re.sub(
        r"http\S+|www\S+|https\S+",
        " ",
        text
    )

    # Remove HTML tags
    text = re.sub(
        r"<.*?>",
        " ",
        text
    )

    # Keep only letters and spaces
    text = re.sub(
        r"[^a-z\s]",
        " ",
        text
    )

    # Remove extra spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    return text


# =========================================================
# CONFIDENCE INTERPRETATION
# =========================================================

def get_confidence_level(confidence):
    """
    Convert numerical confidence into a human-readable level.
    """

    percentage = confidence * 100

    if percentage >= 95:
        return "Very High"

    elif percentage >= 80:
        return "High"

    elif percentage >= 60:
        return "Moderate"

    else:
        return "Low"


# =========================================================
# MAIN PREDICTION FUNCTION
# =========================================================

def predict_news(title, article):
    """
    Predict whether a news article is Fake or Real.

    Parameters:
        title   : News headline
        article : News article content

    Returns:
        Dictionary containing prediction,
        confidence and processed information.
    """

    # -----------------------------------------------------
    # Input validation
    # -----------------------------------------------------

    if not title or not article:
        return {
            "success": False,
            "error": "Please provide both a news title and article."
        }

    # -----------------------------------------------------
    # Combine title and article
    # -----------------------------------------------------

    combined_text = f"{title} {article}"

    # -----------------------------------------------------
    # Clean text
    # -----------------------------------------------------

    cleaned_text = clean_text(combined_text)

    # Check if anything remains after cleaning
    if not cleaned_text.strip():

        return {
            "success": False,
            "error": "The provided text does not contain usable content."
        }

    # -----------------------------------------------------
    # TF-IDF transformation
    # -----------------------------------------------------

    features = vectorizer.transform(
        [cleaned_text]
    )

    # -----------------------------------------------------
    # Prediction
    # -----------------------------------------------------

    prediction = model.predict(
        features
    )[0]

    # -----------------------------------------------------
    # Probability
    # -----------------------------------------------------

    probabilities = model.predict_proba(
        features
    )[0]

    confidence = max(probabilities)

    # -----------------------------------------------------
    # Label conversion
    # -----------------------------------------------------

    if prediction == 1:
        label = "REAL"
    else:
        label = "FAKE"

    # -----------------------------------------------------
    # Confidence level
    # -----------------------------------------------------

    confidence_level = get_confidence_level(
        confidence
    )

    # -----------------------------------------------------
    # Return result
    # -----------------------------------------------------

    return {
        "success": True,
        "prediction": label,
        "confidence": round(confidence * 100, 2),
        "confidence_level": confidence_level
    }