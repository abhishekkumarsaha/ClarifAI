import streamlit as st
import sys
import os

# ============================================================
# FIND CLARIFAI SOURCE CODE
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")

if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

from unified_processor import extract_url_content, run_unified_analysis


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ClarifAI | News Authenticity Analysis",
    page_icon=os.path.join(BASE_DIR, "assets", "favicon.svg"),
    layout="centered",
    initial_sidebar_state="collapsed"
)


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

if "news_title" not in st.session_state:
    st.session_state.news_title = ""

if "news_article" not in st.session_state:
    st.session_state.news_article = ""

if "url_input" not in st.session_state:
    st.session_state.url_input = ""

if "url_extracted_title" not in st.session_state:
    st.session_state.url_extracted_title = ""

if "url_extracted_article" not in st.session_state:
    st.session_state.url_extracted_article = ""

if "url_source_domain" not in st.session_state:
    st.session_state.url_source_domain = None

if "history" not in st.session_state:
    st.session_state.history = []

if "current_analysis" not in st.session_state:
    st.session_state.current_analysis = None


# ============================================================
# PRESET HELPER CALLBACKS
# ============================================================

def load_real_preset():
    st.session_state.news_title = "WASHINGTON (Reuters) - U.S. officials announce national infrastructure initiative"
    st.session_state.news_article = "WASHINGTON (Reuters) - The United States government today announced a comprehensive program to upgrade high-speed internet and digital learning facilities across nationwide schools and universities. Federal leaders welcomed the bipartisan initiative."

def load_fake_preset():
    st.session_state.news_title = "Secret alien technology discovered beneath Antarctic ice shelf, whistleblowers claim"
    st.session_state.news_article = "BREAKING: Anonymous sources inside secret military research facilities report the excavation of an ancient extraterrestrial vessel deep under Antarctica. Government officials have reportedly suppressed the miracle energy generator found on board."

def clear_all():
    st.session_state.news_title = ""
    st.session_state.news_article = ""
    st.session_state.url_input = ""
    st.session_state.url_extracted_title = ""
    st.session_state.url_extracted_article = ""
    st.session_state.url_source_domain = None
    st.session_state.current_analysis = None

def toggle_theme():
    if st.session_state.theme == "dark":
        st.session_state.theme = "light"
    else:
        st.session_state.theme = "dark"


# ============================================================
# DUAL THEME CSS SYSTEM
# ============================================================

current_theme = st.session_state.theme

if current_theme == "dark":
    bg_main = "#000000"
    bg_surface = "#111111"
    bg_input = "#181818"
    border_color = "#222222"
    border_focus = "#3B82F6"
    text_primary = "#F5F5F5"
    text_secondary = "#AAAAAA"
    text_muted = "#777777"
    accent_blue = "#3B82F6"
    
    toggle_bg = "#FFFFFF"
    toggle_fg = "#000000"
    toggle_label = "🌙 Dark Mode"
    
    real_bg = "#052E16"
    real_border = "#22C55E"
    real_text = "#4ADE80"
    
    fake_bg = "#450A0A"
    fake_border = "#EF4444"
    fake_text = "#FCA5A5"

else:
    bg_main = "#FFFFFF"
    bg_surface = "#F8F9FA"
    bg_input = "#FFFFFF"
    border_color = "#E5E7EB"
    border_focus = "#3B82F6"
    text_primary = "#111827"
    text_secondary = "#4B5563"
    text_muted = "#6B7280"
    accent_blue = "#3B82F6"
    
    toggle_bg = "#000000"
    toggle_fg = "#FFFFFF"
    toggle_label = "☀️ Light Mode"
    
    real_bg = "#DCFCE7"
    real_border = "#16A34A"
    real_text = "#15803D"
    
    fake_bg = "#FEE2E2"
    fake_border = "#DC2626"
    fake_text = "#B91C1C"


THEME_CSS = f"""
<style>
    /* Global Reset */
    .stApp {{
        background-color: {bg_main} !important;
        color: {text_primary} !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }}
    
    header[data-testid="stHeader"] {{
        background-color: {bg_main} !important;
    }}
    
    section[data-testid="stSidebar"] {{
        display: none !important;
    }}
    button[data-testid="baseButton-headerNoPadding"] {{
        display: none !important;
    }}

    .main .block-container {{
        max-width: 860px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 5rem !important;
    }}
    
    .brand-title-wrap {{
        display: flex;
        align-items: center;
        gap: 12px;
    }}

    .brand-title-text {{
        font-size: 1.75rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        color: {text_primary};
        margin: 0;
        line-height: 1.1;
    }}
    
    .brand-subtext {{
        font-size: 0.85rem;
        color: {text_secondary};
        margin-top: 2px;
    }}
    
    .star-mark {{
        color: #EF4444;
        font-weight: bold;
        margin-left: 2px;
    }}

    .theme-toggle-btn button {{
        background-color: {toggle_bg} !important;
        color: {toggle_fg} !important;
        border: 1px solid {border_color} !important;
        border-radius: 20px !important;
        padding: 6px 14px !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
    }}

    .stTextInput > label, .stTextArea > label {{
        color: {text_primary} !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        margin-bottom: 6px !important;
    }}

    .stTextInput input, .stTextArea textarea {{
        background-color: {bg_input} !important;
        color: {text_primary} !important;
        border: 1px solid {border_color} !important;
        border-radius: 6px !important;
        font-size: 0.95rem !important;
        padding: 10px 12px !important;
    }}

    .stTextInput input:focus, .stTextArea textarea:focus {{
        border-color: {border_focus} !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
    }}

    .stButton > button {{
        border-radius: 6px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: all 0.15s ease !important;
    }}
    
    button[kind="primary"] {{
        background-color: {accent_blue} !important;
        border: 1px solid {accent_blue} !important;
        color: #FFFFFF !important;
    }}
    button[kind="primary"]:hover {{
        background-color: #2563EB !important;
        border-color: #2563EB !important;
    }}

    button[kind="secondary"] {{
        background-color: {bg_surface} !important;
        border: 1px solid {border_color} !important;
        color: {text_primary} !important;
    }}
    button[kind="secondary"]:hover {{
        border-color: {text_secondary} !important;
    }}
    
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        border-bottom: 1px solid {border_color};
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: transparent !important;
        color: {text_secondary} !important;
        border-radius: 6px 6px 0 0 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 8px 16px !important;
    }}
    
    .stTabs [aria-selected="true"] {{
        color: {text_primary} !important;
        border-bottom: 2px solid {accent_blue} !important;
    }}

    .verdict-card-real {{
        background-color: {real_bg};
        border: 1px solid {real_border};
        border-radius: 8px;
        padding: 18px 22px;
        margin-top: 1.5rem;
        margin-bottom: 1.25rem;
    }}
    
    .verdict-card-fake {{
        background-color: {fake_bg};
        border: 1px solid {fake_border};
        border-radius: 8px;
        padding: 18px 22px;
        margin-top: 1.5rem;
        margin-bottom: 1.25rem;
    }}

    .verdict-title-real {{
        font-size: 1.5rem;
        font-weight: 700;
        color: {real_text};
        margin: 0 0 4px 0;
        letter-spacing: -0.02em;
    }}
    
    .verdict-title-fake {{
        font-size: 1.5rem;
        font-weight: 700;
        color: {fake_text};
        margin: 0 0 4px 0;
        letter-spacing: -0.02em;
    }}

    .metrics-row {{
        display: grid;
        grid-template-columns: 1fr 1fr 1fr 1fr;
        gap: 10px;
        margin-top: 1rem;
        margin-bottom: 1.25rem;
    }}
    
    .metric-card {{
        background-color: {bg_surface};
        border: 1px solid {border_color};
        border-radius: 6px;
        padding: 12px 14px;
    }}

    .metric-card-label {{
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: {text_secondary};
        margin-bottom: 4px;
    }}

    .metric-card-val {{
        font-size: 1.25rem;
        font-weight: 700;
        color: {text_primary};
    }}

    .signal-grid-container {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 10px;
        margin-top: 12px;
        margin-bottom: 16px;
    }}
    
    .signal-card {{
        background-color: {bg_surface};
        border: 1px solid {border_color};
        border-radius: 6px;
        padding: 10px 14px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        font-size: 0.88rem;
        font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
    }}
    
    .signal-feature {{
        color: {accent_blue};
        font-weight: 600;
    }}

    .signal-weight-pos {{
        color: #22C55E;
        font-size: 0.8rem;
        font-weight: 600;
    }}
    
    .signal-weight-neg {{
        color: #EF4444;
        font-size: 0.8rem;
        font-weight: 600;
    }}

    .info-disclaimer-box {{
        background-color: {bg_surface};
        border: 1px solid {border_color};
        border-left: 3px solid {accent_blue};
        border-radius: 6px;
        padding: 12px 16px;
        font-size: 0.85rem;
        color: {text_secondary};
        line-height: 1.5;
        margin-top: 1.5rem;
    }}
    
    .static-footer {{
        position: relative;
        bottom: 0;
        left: 0;
        width: 100%;
        margin-top: 4rem;
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
        border-top: 1px solid {border_color};
        text-align: center;
        font-size: 0.82rem;
        color: {text_muted};
        background-color: {bg_main};
    }}
</style>
"""

st.markdown(THEME_CSS, unsafe_allow_html=True)


# ============================================================
# HEADER WITH SVG LOGO & MOON/SUN THEME SWITCH BUTTON
# ============================================================

col_head, col_theme = st.columns([4, 1.2])

with col_head:
    st.markdown(f"""
    <div class="brand-title-wrap">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40" width="36" height="36" fill="none">
            <path d="M 28 11.5 A 13 13 0 1 0 28 28.5" stroke="{text_primary}" stroke-width="3.8" stroke-linecap="round" />
            <path d="M 16 20.5 L 20 24.5 L 28 15" stroke="{accent_blue}" stroke-width="3.8" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
        <div>
            <h1 class="brand-title-text">ClarifAI</h1>
            <div class="brand-subtext">News Authenticity & Pattern Analysis System</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_theme:
    st.markdown('<div class="theme-toggle-btn">', unsafe_allow_html=True)
    st.button(toggle_label, on_click=toggle_theme, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# RECENT ANALYSES (SESSION HISTORY COMPONENT)
# ============================================================

if st.session_state.history:
    with st.expander("📜 Recent Analyses", expanded=True):
        st.caption("Click any past analysis to view full evaluation details:")
        for idx, item in enumerate(reversed(st.session_state.history)):
            badge = "🟢 Likely Real" if item["prediction"] == "REAL" else "🔴 Likely Fake"
            conf = f"{item['confidence']:.1f}%"
            snip = item["title"][:50] + "..." if len(item["title"]) > 50 else item["title"]
            btn_label = f"{badge} ({conf}) • {snip}"
            
            if st.button(btn_label, key=f"hist_btn_{idx}_{item['title'][:10]}", use_container_width=True, type="secondary"):
                st.session_state.current_analysis = item


# ============================================================
# SUBMISSION WORKSPACE (DUAL TABS: PASTE vs URL)
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

tab_paste, tab_url = st.tabs(["📝 Paste Article", "🔗 Analyze Article URL"])

active_input_method = "manual"
active_source_url = None
active_source_domain = None

# ------------------------------------------------------------
# TAB 1: PASTE ARTICLE
# ------------------------------------------------------------

with tab_paste:
    st.caption("Enter or paste news text manually for pattern evaluation.")
    
    p_col1, p_col2, p_col3 = st.columns([1, 1, 2])
    with p_col1:
        st.button("Load Real Sample", on_click=load_real_preset, use_container_width=True, type="secondary")
    with p_col2:
        st.button("Load Fake Sample", on_click=load_fake_preset, use_container_width=True, type="secondary")

    st.markdown('##### News Headline <span class="star-mark">*</span>', unsafe_allow_html=True)
    st.text_input(
        "News Headline",
        key="news_title",
        placeholder="Enter the news headline...",
        label_visibility="collapsed"
    )

    st.markdown('##### News Article Body <span class="star-mark">*</span>', unsafe_allow_html=True)
    st.text_area(
        "News Article Body",
        key="news_article",
        placeholder="Paste the full body text of the article here...",
        height=220,
        label_visibility="collapsed"
    )

    p_article = st.session_state.get("news_article", "")
    words_pasted = len(p_article.split()) if p_article.strip() else 0
    chars_pasted = len(p_article) if p_article.strip() else 0
    
    if words_pasted > 0:
        st.caption(f"📊 Article stats: **{words_pasted}** words | **{chars_pasted}** characters | ~**{max(1, round(words_pasted/200))}** min read")


# ------------------------------------------------------------
# TAB 2: ANALYZE ARTICLE URL
# ------------------------------------------------------------

with tab_url:
    st.caption("Provide a direct web link to automatically extract content for analysis.")

    st.markdown('##### Article Web URL <span class="star-mark">*</span>', unsafe_allow_html=True)
    url_input_val = st.text_input(
        "Article Web URL",
        key="url_input",
        placeholder="https://example-news.com/article-path",
        label_visibility="collapsed"
    )

    fetch_btn = st.button("Fetch Article Content", type="secondary")

    if fetch_btn:
        if not url_input_val.strip():
            st.warning("⚠️ Please enter a news article URL first.")
        else:
            with st.spinner("Fetching article content from webpage using trafilatura..."):
                ext_res = extract_url_content(url_input_val.strip())
                if ext_res["success"]:
                    st.session_state.url_extracted_title = ext_res["title"]
                    st.session_state.url_extracted_article = ext_res["article_text"]
                    st.session_state.url_source_domain = ext_res["source_domain"]
                    st.success(f"✓ Successfully extracted article from {ext_res['source_domain']}!")
                else:
                    st.error(f"❌ {ext_res['error']}")

    if st.session_state.url_extracted_article:
        st.markdown(f"**Extracted Headline:** {st.session_state.url_extracted_title}")
        st.text_area(
            "Extracted Content Preview (Review before analysis)",
            value=st.session_state.url_extracted_article,
            height=180,
            disabled=False
        )


# Active Input Resolution
p_title = st.session_state.get("news_title", "")
p_body = st.session_state.get("news_article", "")
u_title = st.session_state.get("url_extracted_title", "")
u_body = st.session_state.get("url_extracted_article", "")

if p_title.strip() and p_body.strip():
    target_title = p_title
    target_article = p_body
    active_input_method = "manual"
    active_source_url = None
    active_source_domain = "Pasted Input"
elif u_title.strip() and u_body.strip():
    target_title = u_title
    target_article = u_body
    active_input_method = "url"
    active_source_url = st.session_state.get("url_input", "")
    active_source_domain = st.session_state.get("url_source_domain", "Web Article")
else:
    target_title = p_title or u_title
    target_article = p_body or u_body
    active_input_method = "url" if u_body else "manual"


# ============================================================
# MAIN ACTION TOOLBAR (ANALYZE & RESET)
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

act_col1, act_col2 = st.columns([3, 1])

with act_col1:
    analyze_clicked = st.button("🔍 Analyze Article", type="primary", use_container_width=True)

with act_col2:
    st.button("Clear / Reset", on_click=clear_all, use_container_width=True, type="secondary")


# ============================================================
# UNIFIED ANALYSIS WORKFLOW EXECUTION
# ============================================================

if analyze_clicked:
    if not target_title.strip() or not target_article.strip():
        st.warning("⚠️ Please provide both a headline and article text before analyzing.")
    else:
        with st.spinner("Executing unified ClarifAI pattern analysis..."):
            res = run_unified_analysis(
                title=target_title,
                article_text=target_article,
                input_method=active_input_method,
                source_url=active_source_url,
                source_domain=active_source_domain
            )

        if res["success"]:
            analysis_data = res["analysis"]
            st.session_state.current_analysis = analysis_data
            
            # Append to session history (keep up to 10 recent analyses)
            st.session_state.history.append(analysis_data)
            if len(st.session_state.history) > 10:
                st.session_state.history.pop(0)

        else:
            st.error(f"❌ {res['error']}")


# ============================================================
# DISPLAY STANDARDIZED ANALYSIS OBJECT RESULT
# ============================================================

analysis = st.session_state.current_analysis

if analysis:
    st.markdown("---")
    st.markdown("### Analysis Verdict")

    pred = analysis["prediction"]
    conf = analysis["confidence"]
    conf_level = analysis["confidence_level"]
    signals = analysis.get("signals", [])
    domain = analysis.get("source_domain") or "Pasted Input"
    method = "URL Extraction" if analysis["input_method"] == "url" else "Manual Input"

    # Verdict Header Card
    if pred == "REAL":
        st.markdown(f"""
        <div class="verdict-card-real">
            <div class="verdict-title-real">LIKELY REAL</div>
            <div style="font-size: 0.9rem; color: {text_secondary};">
                Linguistic patterns and feature representation align with standard news reporting.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="verdict-card-fake">
            <div class="verdict-title-fake">LIKELY FAKE</div>
            <div style="font-size: 0.9rem; color: {text_secondary};">
                Linguistic patterns and feature representation align with unverified or sensationalized reporting.
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Standardized Metrics Grid
    words_cnt = analysis["word_count"]
    read_time = max(1, round(words_cnt / 200))
    
    st.markdown(f"""
    <div class="metrics-row">
        <div class="metric-card">
            <div class="metric-card-label">Model Confidence</div>
            <div class="metric-card-val">{conf:.1f}%</div>
        </div>
        <div class="metric-card">
            <div class="metric-card-label">Confidence Level</div>
            <div class="metric-card-val">{conf_level}</div>
        </div>
        <div class="metric-card">
            <div class="metric-card-label">Source / Domain</div>
            <div class="metric-card-val" style="font-size: 1.05rem;">{domain}</div>
        </div>
        <div class="metric-card">
            <div class="metric-card-label">Article Length</div>
            <div class="metric-card-val" style="font-size: 1.05rem;">{words_cnt} w (~{read_time}m)</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Progress Bar
    st.progress(min(max(conf / 100.0, 0.0), 1.0))

    # Side-by-Side Key Model Signals
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("##### Key Model Signals")
    st.caption("These are patterns that influenced the model's classification. They are not factual evidence.")

    if signals:
        grid_html = '<div class="signal-grid-container">'
        for sig in signals:
            feat = sig.get("feature", "")
            contrib = sig.get("contribution", 0.0)
            weight_cls = "signal-weight-pos" if contrib >= 0 else "signal-weight-neg"
            grid_html += f'<div class="signal-card"><span class="signal-feature">• {feat}</span><span class="{weight_cls}">{contrib:+.4f}</span></div>'
        grid_html += '</div>'
        st.markdown(grid_html, unsafe_allow_html=True)
    else:
        st.info("No significant model feature signals detected for this specific input text.")

    # Disclaimer Box & Timestamp Metadata
    st.markdown(f"""
    <div class="info-disclaimer-box">
        <strong>ℹ️ Research & Fact-Analysis Disclaimer:</strong><br>
        ClarifAI provides statistical machine-learning predictions based on linguistic patterns learned from training data. 
        It evaluates text structure and feature representation; it does not perform live fact-verification against external databases or guarantee absolute factual truth.<br><br>
        <span style="font-size: 0.78rem; color: {text_muted};">Analyzed at: {analysis['analyzed_at']} | Method: {method}</span>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# COMPACT COLLAPSIBLE METHODOLOGY & STATIC BOTTOM FOOTER
# ============================================================

st.markdown("<br><br>", unsafe_allow_html=True)

with st.expander("ℹ️ System Methodology & Technology Stack Overview"):
    st.markdown("""
    **ClarifAI Technical Architecture:**
    - **Classification Model:** Calibrated Linear Support Vector Machine (`CalibratedClassifierCV` wrapping `LinearSVC`).
    - **Calibration Method:** Platt Scaling via Sigmoid cross-validation for calibrated probability outputs.
    - **Feature Engineering:** TF-IDF (Term Frequency-Inverse Document Frequency) N-gram Vectorization.
    - **Interpretability Layer:** Direct linear decision-boundary weight projection (`feature_values × coefficients`).
    - **Dataset & Pipeline:** Pre-trained on news corpora for news authenticity classification.
    """)

st.markdown(f"""
<div class="static-footer">
    ClarifAI • News Authenticity & Pattern Analysis Engine
</div>
""", unsafe_allow_html=True)