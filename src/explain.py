import os
import joblib


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

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


model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


def explain_prediction(text, top_n=10):
    """
    Identify important TF-IDF features associated
    with the model's prediction.
    """

    features = vectorizer.transform([text])

    feature_names = vectorizer.get_feature_names_out()

    # Calibrated SVM contains the underlying SVM
    svm = model.calibrated_classifiers_[0].estimator

    coefficients = svm.coef_[0]

    feature_values = features.toarray()[0]

    contributions = feature_values * coefficients

    prediction = model.predict(features)[0]

    if prediction == 0:
        # Features pushing toward FAKE
        important_indices = contributions.argsort()[:top_n]
    else:
        # Features pushing toward REAL
        important_indices = contributions.argsort()[-top_n:][::-1]

    important_features = []

    for index in important_indices:

        if feature_values[index] > 0:

            important_features.append({
                "feature": feature_names[index],
                "contribution": round(
                    float(contributions[index]),
                    4
                )
            })

    return important_features