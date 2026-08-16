import streamlit as st
from datetime import datetime

from src.article_analyzer import (
    analyze_pasted_article,
    analyze_article_url,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ClarifAI",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# SESSION STATE
# ============================================================

if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "history" not in st.session_state:
    st.session_state.history = []

if "theme" not in st.session_state:
    st.session_state.theme = "dark"


# ============================================================
# THEME
# ============================================================

theme = st.session_state.theme

if theme == "dark":

    BG = "#000000"
    CARD = "#0A0A0A"
    BORDER = "#242424"
    TEXT = "#FFFFFF"
    MUTED = "#A0A0A0"
    INPUT = "#111111"

else:

    BG = "#FFFFFF"
    CARD = "#F7F7F7"
    BORDER = "#D9D9D9"
    TEXT = "#111111"
    MUTED = "#666666"
    INPUT = "#FFFFFF"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    f"""
    <style>

    /* =====================================================
       GLOBAL
       ===================================================== */

    html,
    body,
    [data-testid="stAppViewContainer"],
    [data-testid="stApp"] {{
        background: {BG} !important;
        color: {TEXT} !important;
    }}

    [data-testid="stHeader"] {{
        background: {BG} !important;
    }}

    [data-testid="stMain"] {{
        background: {BG} !important;
    }}

    .block-container {{
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }}


    /* =====================================================
       TEXT
       ===================================================== */

    h1, h2, h3, h4, h5, h6,
    p, label, span, div {{
        color: {TEXT};
    }}

    .stMarkdown,
    .stCaption {{
        color: {TEXT};
    }}


    /* =====================================================
       BRAND
       ===================================================== */

    .brand {{
        font-size: 34px;
        font-weight: 700;
        letter-spacing: -1px;
        color: {TEXT} !important;
    }}

    .tagline {{
        color: {MUTED} !important;
        font-size: 15px;
        margin-top: -8px;
    }}


    /* =====================================================
       CUSTOM CARDS
       ===================================================== */

    .card {{
        background: {CARD} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 14px;
        padding: 24px;
        margin-top: 18px;
        color: {TEXT} !important;
    }}

    .result-card {{
        background: {CARD} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 18px;
        padding: 30px;
        margin-top: 25px;
        color: {TEXT} !important;
    }}

    .explanation {{
        background: {INPUT} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 12px;
        padding: 18px;
        line-height: 1.65;
        color: {TEXT} !important;
    }}


    /* =====================================================
       INPUTS
       ===================================================== */

    [data-testid="stTextInput"] input,
    [data-testid="stTextArea"] textarea {{
        background-color: {INPUT} !important;
        color: {TEXT} !important;
        border: 1px solid {BORDER} !important;
    }}

    [data-testid="stTextInput"] input::placeholder,
    [data-testid="stTextArea"] textarea::placeholder {{
        color: {MUTED} !important;
        opacity: 1 !important;
    }}


    /* =====================================================
       SELECT / RADIO
       ===================================================== */

    [data-testid="stRadio"] label,
    [data-testid="stRadio"] div {{
        color: {TEXT} !important;
    }}


    /* =====================================================
       BUTTONS
       ===================================================== */

    [data-testid="stButton"] button,
    [data-testid="stDownloadButton"] button {{
        background: {CARD} !important;
        color: {TEXT} !important;
        border: 1px solid {BORDER} !important;
    }}

    [data-testid="stButton"] button:hover,
    [data-testid="stDownloadButton"] button:hover {{
        border-color: {TEXT} !important;
        color: {TEXT} !important;
    }}


    /* =====================================================
       METRICS
       ===================================================== */

    [data-testid="stMetric"] {{
        background: {CARD} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 12px;
        padding: 15px;
    }}

    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] {{
        color: {TEXT} !important;
    }}


    /* =====================================================
       SIGNAL TAGS
       ===================================================== */

    .signal {{
        display: inline-block;
        padding: 7px 11px;
        margin: 4px;
        border: 1px solid {BORDER};
        border-radius: 8px;
        background: {INPUT};
        color: {TEXT} !important;
        font-size: 13px;
    }}


    /* =====================================================
       PROGRESS BAR
       ===================================================== */

    [data-testid="stProgress"] {{
        background: {CARD} !important;
    }}


    /* =====================================================
       DIVIDERS
       ===================================================== */

    hr {{
        border-color: {BORDER} !important;
    }}


    /* =====================================================
       ALERTS
       ===================================================== */

    [data-testid="stAlert"] {{
        color: {TEXT} !important;
    }}


    /* =====================================================
       FOOTER
       ===================================================== */

    .footer {{
        text-align: center;
        color: {MUTED} !important;
        font-size: 12px;
        margin-top: 50px;
    }}

    .muted {{
        color: {MUTED} !important;
        font-size: 14px;
    }}

    .prediction {{
        font-size: 34px;
        font-weight: 750;
        letter-spacing: -1px;
        color: {TEXT} !important;
    }}

    .confidence {{
        font-size: 42px;
        font-weight: 750;
        margin-top: 5px;
        color: {TEXT} !important;
    }}

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

header_col1, header_col2 = st.columns([8, 1])

with header_col1:

    st.markdown(
        '<div class="brand">◈ ClarifAI</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="tagline">'
        'News authenticity & linguistic pattern analysis'
        '</div>',
        unsafe_allow_html=True,
    )


with header_col2:

    theme_icon = "☀" if theme == "dark" else "☾"

    if st.button(theme_icon, use_container_width=True):

        st.session_state.theme = (
            "light" if theme == "dark" else "dark"
        )

        st.rerun()


# ============================================================
# INPUT MODE
# ============================================================

st.markdown("### Analyze an article")

mode = st.radio(
    "Input method",
    ["Paste Article", "Article URL"],
    horizontal=True,
    label_visibility="collapsed",
)


# ============================================================
# PASTE ARTICLE
# ============================================================

if mode == "Paste Article":

    title = st.text_input(
        "Headline",
        placeholder="Enter the article headline...",
    )

    article_text = st.text_area(
        "Article",
        placeholder="Paste the complete article text here...",
        height=280,
    )

    analyze_button = st.button(
        "Analyze Article",
        type="primary",
        use_container_width=True,
    )

    if analyze_button:

        if not article_text.strip():

            st.error("Please enter the article text.")

        else:

            with st.spinner("Analyzing article..."):

                try:

                    result = analyze_pasted_article(
                        title,
                        article_text,
                    )

                    st.session_state.analysis = result

                    st.session_state.history.insert(
                        0,
                        result,
                    )

                except Exception as error:

                    st.error(str(error))


# ============================================================
# URL MODE
# ============================================================

else:

    url = st.text_input(
        "Article URL",
        placeholder="https://example.com/news/article",
    )

    analyze_button = st.button(
        "Fetch & Analyze Article",
        type="primary",
        use_container_width=True,
    )

    if analyze_button:

        if not url.strip():

            st.error("Please enter an article URL.")

        else:

            with st.spinner(
                "Fetching and analyzing article..."
            ):

                try:

                    result = analyze_article_url(url)

                    st.session_state.analysis = result

                    st.session_state.history.insert(
                        0,
                        result,
                    )

                except Exception as error:

                    st.error(str(error))


# ============================================================
# RESULTS
# ============================================================

analysis = st.session_state.analysis

if analysis:

    st.markdown("---")

    prediction = str(
        analysis.get("prediction", "UNKNOWN")
    ).upper()

    confidence = float(
        analysis.get("confidence", 0)
    )

    if confidence <= 1:
        confidence *= 100

    confidence_level = analysis.get(
        "confidence_level",
        "Unknown",
    )

    if prediction == "FAKE":

        prediction_text = "LIKELY FAKE"
        prediction_symbol = "●"

    else:

        prediction_text = "LIKELY REAL"
        prediction_symbol = "●"


    # --------------------------------------------------------
    # RESULT HEADER
    # --------------------------------------------------------

    st.markdown(
        '<div class="result-card">',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="prediction">'
        f'{prediction_symbol} {prediction_text}'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="muted">'
        f'Confidence level: {confidence_level}'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="confidence">'
        f'{confidence:.2f}%'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.progress(
        min(confidence / 100, 1.0)
    )

    st.markdown("</div>", unsafe_allow_html=True)


    # --------------------------------------------------------
    # ARTICLE INFORMATION
    # --------------------------------------------------------

    st.markdown("### Article Information")

    info1, info2, info3 = st.columns(3)

    with info1:

        st.metric(
            "Word Count",
            analysis.get("word_count", "—"),
        )

    with info2:

        st.metric(
            "Source",
            analysis.get(
                "source_domain",
                "Manual Input",
            ),
        )

    with info3:

        st.metric(
            "Input",
            analysis.get(
                "input_method",
                "—",
            ).title(),
        )


    # --------------------------------------------------------
    # HEADLINE
    # --------------------------------------------------------

    st.markdown("### Headline")

    st.markdown(
        f'<div class="card">'
        f'{analysis.get("title", "Untitled Article")}'
        f'</div>',
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # MODEL SIGNALS
    # --------------------------------------------------------

    st.markdown("### Key Model Signals")

    signals = analysis.get("signals", [])

    if signals:

        signal_html = ""

        for signal in signals:

            if isinstance(signal, dict):

                feature = signal.get(
                    "feature",
                    "",
                )

                contribution = float(
                    signal.get(
                        "contribution",
                        0,
                    )
                )

                signal_html += (
                    f'<span class="signal">'
                    f'{feature} '
                    f'({contribution:+.4f})'
                    f'</span>'
                )

            else:

                signal_html += (
                    f'<span class="signal">'
                    f'{signal}'
                    f'</span>'
                )

        st.markdown(
            signal_html,
            unsafe_allow_html=True,
        )

    else:

        st.caption(
            "No model signals available."
        )


    # --------------------------------------------------------
    # AI EXPLANATION
    # --------------------------------------------------------

    ai_explanation = analysis.get(
        "ai_explanation"
    )

    if ai_explanation:

        st.markdown("### AI Explanation")

        st.markdown(
            f'<div class="explanation">'
            f'{ai_explanation}'
            f'</div>',
            unsafe_allow_html=True,
        )

    else:

        st.info(
            "AI explanation is currently unavailable. "
            "The machine-learning prediction remains available."
        )


    # --------------------------------------------------------
    # SOURCE
    # --------------------------------------------------------

    source_url = analysis.get(
        "source_url"
    )

    if source_url:

        st.markdown("### Source")

        st.markdown(
            f"[Open original article]({source_url})"
        )


    # --------------------------------------------------------
    # DOWNLOAD REPORT
    # --------------------------------------------------------

    st.markdown("### Export")

    report = f"""
CLARIFAI
News Authenticity & Linguistic Pattern Analysis
================================================

Headline:
{analysis.get("title", "N/A")}

Prediction:
{prediction_text}

Confidence:
{confidence:.2f}%

Confidence Level:
{confidence_level}

Source:
{analysis.get("source_domain", "Manual Input")}

URL:
{analysis.get("source_url", "N/A")}

Input Method:
{analysis.get("input_method", "N/A")}

Word Count:
{analysis.get("word_count", "N/A")}

Key Model Signals:
"""

    for signal in signals:

        if isinstance(signal, dict):

            report += (
                f"\n- {signal.get('feature', '')}: "
                f"{float(signal.get('contribution', 0)):+.4f}"
            )

        else:

            report += f"\n- {signal}"

    report += f"""

AI Explanation:
{ai_explanation or "Not available."}


DISCLAIMER
----------
ClarifAI provides a machine-learning prediction
based on linguistic patterns learned from training
data.

This result does not constitute factual verification
and should not be treated as definitive proof that
an article is true or false.
"""

    st.download_button(
        "Download Analysis Report",
        report,
        file_name="ClarifAI_Analysis_Report.txt",
        mime="text/plain",
        use_container_width=True,
    )


    # --------------------------------------------------------
    # DISCLAIMER
    # --------------------------------------------------------

    st.caption(
        "ClarifAI is a pattern-based machine-learning "
        "classifier, not a live fact-checking system. "
        "Verify important claims using trusted sources."
    )


# ============================================================
# HISTORY
# ============================================================

if st.session_state.history:

    st.markdown("---")

    st.markdown("### Recent Analyses")

for index, item in enumerate(
    st.session_state.history[:5]
):

    item_prediction = str(
        item.get(
            "prediction",
            "UNKNOWN",
        )
    ).upper()

    item_confidence = float(
        item.get(
            "confidence",
            0,
        )
    )

    if item_confidence <= 1:
        item_confidence *= 100

    history_title = item.get(
        "title",
        "Untitled Article",
    )

    st.markdown(
        f"""
        <div class="card" style="
            margin-top: 10px;
            padding: 16px 20px;
        ">
            <strong>{item_prediction}</strong>
            &nbsp;—&nbsp;
            {item_confidence:.1f}%
            &nbsp;—&nbsp;
            {history_title[:100]}
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "Clear History",
        use_container_width=True,
    ):

        st.session_state.history = []

        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        ClarifAI · Machine Learning News Analysis
        <br>
        Predictions are analytical signals, not factual verification.
    </div>
    """,
    unsafe_allow_html=True,
)