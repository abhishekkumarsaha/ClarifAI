"""
ClarifAI Evidence Analyzer

Aggregates article/source information and ML results.
It does NOT make the final factual verdict.
"""

from urllib.parse import urlparse


def _get_domain(item):
    """
    Extract a normalized publisher domain from an evidence item.
    """

    # Prefer the final publisher URL.
    url = (
        item.get("final_url")
        or item.get("url")
        or item.get("source_url")
        or ""
    )

    if url:

        try:

            parsed = urlparse(url)

            domain = (
                parsed.netloc
                .lower()
                .strip()
                .replace("www.", "")
            )

            if domain:
                return domain

        except Exception:
            pass

    # Fallback to source/provider fields.
    source = (
        item.get("source")
        or item.get("publisher")
        or item.get("domain")
        or ""
    )

    if source:

        source = (
            str(source)
            .lower()
            .strip()
            .replace("www.", "")
        )

        # Handle things such as:
        # "semafor.com"
        # "Semafor"
        if "." in source:
            return source

        return source

    return ""


def analyze_evidence(evidence):
    """
    Aggregate evidence statistics.

    This function does not decide whether a claim is true or false.
    """

    if not evidence:

        return {
            "articles_found": 0,
            "articles_extracted": 0,
            "independent_domains": 0,
            "domains": [],
            "source_details": [],
            "ml_real_count": 0,
            "ml_fake_count": 0,
            "ml_neutral_count": 0,
            "average_ml_confidence": 0.0,
            "evidence_articles": [],
        }

    successful = [
        item
        for item in evidence
        if item.get(
            "extraction_success",
            False,
        )
    ]

    # --------------------------------------------------------
    # SOURCE / DOMAIN ANALYSIS
    # --------------------------------------------------------

    domains = set()

    source_details = []

    for item in successful:

        domain = _get_domain(item)

        if domain:
            domains.add(domain)

        source_details.append(
            {
                "source": (
                    item.get("source")
                    or item.get("publisher")
                    or domain
                    or "Unknown source"
                ),
                "domain": domain,
                "title": (
                    item.get("article_title")
                    or item.get("title")
                    or ""
                ),
                "url": (
                    item.get("final_url")
                    or item.get("url")
                    or ""
                ),
                "published_at": item.get(
                    "published_at"
                ),
            }
        )

    # --------------------------------------------------------
    # ML ANALYSIS
    # --------------------------------------------------------

    real_count = 0
    fake_count = 0
    neutral_count = 0

    ml_confidences = []

    for item in successful:

        result = item.get(
            "ml_analysis"
        )

        if not result:
            continue

        if not isinstance(
            result,
            dict,
        ):
            continue

        prediction = str(
            result.get(
                "prediction",
                "",
            )
        ).upper()

        if prediction == "REAL":

            real_count += 1

        elif prediction == "FAKE":

            fake_count += 1

        else:

            neutral_count += 1

        confidence = result.get(
            "confidence"
        )

        if confidence is not None:

            try:

                ml_confidences.append(
                    float(confidence)
                )

            except (
                ValueError,
                TypeError,
            ):

                pass

    # --------------------------------------------------------
    # AVERAGE ML CONFIDENCE
    # --------------------------------------------------------

    average_confidence = (
        sum(ml_confidences)
        / len(ml_confidences)
        if ml_confidences
        else 0.0
    )

    # --------------------------------------------------------
    # RETURN
    # --------------------------------------------------------

    return {

        "articles_found": len(
            evidence
        ),

        "articles_extracted": len(
            successful
        ),

        "independent_domains": len(
            domains
        ),

        "domains": sorted(
            domains
        ),

        "source_details": source_details,

        "ml_real_count": real_count,

        "ml_fake_count": fake_count,

        "ml_neutral_count": neutral_count,

        "average_ml_confidence": round(
            average_confidence,
            2,
        ),

        "evidence_articles": successful,
    }