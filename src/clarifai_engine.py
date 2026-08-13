from predict import predict_news, clean_text
from explain import explain_prediction


def analyze_news(title, article):
    """
    Complete ClarifAI analysis.

    Returns:
        Prediction
        Confidence
        Confidence level
        Key model signals
    """

    # -----------------------------------------
    # Get prediction
    # -----------------------------------------

    result = predict_news(
        title,
        article
    )

    # -----------------------------------------
    # Stop if input is invalid
    # -----------------------------------------

    if not result["success"]:
        return result

    # -----------------------------------------
    # Prepare text for explanation
    # -----------------------------------------

    combined_text = f"{title} {article}"

    cleaned_text = clean_text(
        combined_text
    )

    # -----------------------------------------
    # Get model signals
    # -----------------------------------------

    signals = explain_prediction(
        cleaned_text,
        top_n=10
    )

    # -----------------------------------------
    # Add explanation
    # -----------------------------------------

    result["signals"] = signals

    return result