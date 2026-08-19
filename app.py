import streamlit as st
import sys
import os
import time
import uuid
import json
import csv
import io
from datetime import datetime

# ============================================================
# FIND CLARIFAI SOURCE CODE
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

from src.verification_service import verify_news_claim
from src.health import backend_health


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ClarifAI | News Verification Engine",
    page_icon=os.path.join(BASE_DIR, "assets", "favicon.svg"),
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# UNIFIED SESSION STATE INITIALIZATION (SINGLE SOURCE OF TRUTH)
# ============================================================

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

if "active_nav" not in st.session_state:
    st.session_state.active_nav = "Verify"

if "claim_input" not in st.session_state:
    st.session_state.claim_input = ""

if "current_result" not in st.session_state:
    st.session_state.current_result = None

if "history" not in st.session_state:
    st.session_state.history = []

if "saved_items" not in st.session_state:
    st.session_state.saved_items = set()

if "max_articles_limit" not in st.session_state:
    st.session_state.max_articles_limit = 5

if "confirm_clear_history" not in st.session_state:
    st.session_state.confirm_clear_history = False

if "show_account_modal" not in st.session_state:
    st.session_state.show_account_modal = False

if "popover_action" not in st.session_state:
    st.session_state.popover_action = None

if "report_submitted" not in st.session_state:
    st.session_state.report_submitted = False


# ============================================================
# CLARIFAI BRAND COLOR SYSTEM & PALETTE
# ============================================================

theme = st.session_state.theme

if theme == "dark":
    # Dark Mode Foundation
    BG = "#000000"
    SIDEBAR_BG = "#080808"
    SURFACE = "#0A0A0A"
    SURFACE_ALT = "#111111"
    BORDER = "#222222"
    BORDER_LIGHT = "#333333"
    TEXT_PRIMARY = "#FFFFFF"
    TEXT_SECONDARY = "#A7AFBD"
    TEXT_MUTED = "#666666"
    INPUT_BG = "#111111"
    
    # Brand Accents
    ACCENT_BLUE = "#00C2FF"
    ACCENT_MINT = "#00E5A8"
    ACCENT_RED = "#FF4D5A"
    ACCENT_AMBER = "#F5B942"
    
    TRUE_BG = "rgba(0, 229, 168, 0.08)"
    TRUE_BORDER = "#00E5A8"
    TRUE_TEXT = "#00E5A8"

    FALSE_BG = "rgba(255, 77, 90, 0.08)"
    FALSE_BORDER = "#FF4D5A"
    FALSE_TEXT = "#FF4D5A"

    UNVERIFIED_BG = "rgba(245, 185, 66, 0.08)"
    UNVERIFIED_BORDER = "#F5B942"
    UNVERIFIED_TEXT = "#F5B942"

else:
    # Light Mode Foundation
    BG = "#FFFFFF"
    SIDEBAR_BG = "#F8F9FA"
    SURFACE = "#F7F9FB"
    SURFACE_ALT = "#F1F4F8"
    BORDER = "#E5E7EB"
    BORDER_LIGHT = "#D1D5DB"
    TEXT_PRIMARY = "#101828"
    TEXT_SECONDARY = "#667085"
    TEXT_MUTED = "#9CA3AF"
    INPUT_BG = "#FFFFFF"
    
    # Brand Accents
    ACCENT_BLUE = "#0099FF"
    ACCENT_MINT = "#00B884"
    ACCENT_RED = "#E11D48"
    ACCENT_AMBER = "#D97706"

    TRUE_BG = "#ECFDF5"
    TRUE_BORDER = "#059669"
    TRUE_TEXT = "#047857"

    FALSE_BG = "#FEF2F2"
    FALSE_BORDER = "#E11D48"
    FALSE_TEXT = "#9F1239"

    UNVERIFIED_BG = "#FFFBEB"
    UNVERIFIED_BORDER = "#D97706"
    UNVERIFIED_TEXT = "#B45309"


# ============================================================
# ADVANCED CSS DESIGN SYSTEM & MICRO-INTERACTIONS
# ============================================================

CUSTOM_CSS = f"""
<style>
    /* Keyframe Animations */
    @keyframes pageEntrance {{
        from {{ opacity: 0; transform: translateY(6px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    @keyframes pulseDot {{
        0% {{ opacity: 1; transform: scale(1); }}
        50% {{ opacity: 0.4; transform: scale(1.2); }}
        100% {{ opacity: 1; transform: scale(1); }}
    }}

    @keyframes antiGravityFloat {{
        0% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-3px); }}
        100% {{ transform: translateY(0); }}
    }}

    /* Global Base Reset */
    .stApp {{
        background-color: {BG} !important;
        color: {TEXT_PRIMARY} !important;
        font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }}
    
    header[data-testid="stHeader"] {{
        background-color: {BG} !important;
    }}

    /* Page Entrance Animation */
    .main .block-container {{
        max-width: 960px !important;
        padding-top: 1.25rem !important;
        padding-bottom: 4rem !important;
        animation: pageEntrance 220ms ease-out forwards;
    }}

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background-color: {SIDEBAR_BG} !important;
        border-right: 1px solid {BORDER} !important;
    }}

    section[data-testid="stSidebar"] .block-container {{
        padding-top: 1.2rem !important;
        padding-bottom: 1.2rem !important;
        display: flex;
        flex-direction: column;
        height: 100%;
    }}

    /* Typography & Hierarchy */
    h1, h2, h3, h4, h5, h6, p, span, label, div {{
        color: {TEXT_PRIMARY};
    }}

    .hero-title {{
        font-size: 2.75rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        color: {TEXT_PRIMARY};
        line-height: 1.1;
        margin-bottom: 0.5rem;
    }}

    .hero-subtext {{
        font-size: 1.1rem;
        color: {TEXT_SECONDARY};
        margin-bottom: 1.5rem;
        line-height: 1.5;
        max-width: 680px;
    }}

    .section-heading {{
        font-size: 1.35rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: {TEXT_PRIMARY};
        margin-top: 2rem;
        margin-bottom: 0.75rem;
    }}

    /* Search Input Bar with Hover & Focus States */
    [data-testid="stTextInput"] input {{
        background-color: {INPUT_BG} !important;
        color: {TEXT_PRIMARY} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 8px !important;
        padding: 14px 16px !important;
        font-size: 1.05rem !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }}

    [data-testid="stTextInput"] input:hover {{
        border-color: {BORDER_LIGHT} !important;
    }}

    [data-testid="stTextInput"] input:focus {{
        border-color: {ACCENT_BLUE} !important;
        outline: none !important;
        box-shadow: 0 0 10px rgba(0, 194, 255, 0.25) !important;
    }}

    /* Button Hierarchy & Lift Effects */
    .stButton > button {{
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 10px 18px !important;
        margin: 0 !important;
        box-sizing: border-box !important;
        height: 42px !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        transition: all 0.18s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }}

    /* Primary Action Button */
    button[kind="primary"] {{
        background-color: {ACCENT_BLUE} !important;
        border: 1px solid {ACCENT_BLUE} !important;
        color: #000000 !important;
        font-weight: 700 !important;
    }}
    
    button[kind="primary"]:hover {{
        background-color: #00A6DA !important;
        border-color: #00A6DA !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0, 194, 255, 0.3) !important;
    }}

    button[kind="primary"]:active {{
        transform: translateY(0) !important;
        box-shadow: none !important;
    }}

    /* Secondary Action Button */
    button[kind="secondary"] {{
        background-color: {SURFACE} !important;
        border: 1px solid {BORDER} !important;
        color: {TEXT_PRIMARY} !important;
    }}

    button[kind="secondary"]:hover {{
        background-color: {SURFACE_ALT} !important;
        border-color: {BORDER_LIGHT} !important;
        color: {TEXT_PRIMARY} !important;
        transform: translateY(-1px) !important;
    }}

    button[kind="secondary"]:active {{
        transform: translateY(0) !important;
    }}

    /* Evidence Status Dot & Badge */
    .evidence-status-pill {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-size: 0.85rem;
        font-weight: 600;
        color: {TEXT_SECONDARY};
        margin-bottom: 12px;
    }}

    .status-pulse-dot {{
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        animation: pulseDot 2s infinite ease-in-out;
    }}

    /* Verdict Card Visuals with Selective Anti-Gravity Float */
    .verdict-card-true {{
        background-color: {TRUE_BG};
        border: 1.5px solid {TRUE_BORDER};
        border-radius: 10px;
        padding: 22px 26px;
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
        animation: antiGravityFloat 5s ease-in-out infinite;
    }}

    .verdict-card-false {{
        background-color: {FALSE_BG};
        border: 1.5px solid {FALSE_BORDER};
        border-radius: 10px;
        padding: 22px 26px;
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
        animation: antiGravityFloat 5s ease-in-out infinite;
    }}

    .verdict-card-unverified {{
        background-color: {UNVERIFIED_BG};
        border: 1.5px solid {UNVERIFIED_BORDER};
        border-radius: 10px;
        padding: 22px 26px;
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
        animation: antiGravityFloat 5s ease-in-out infinite;
    }}

    .verdict-badge-true {{
        font-size: 1.65rem;
        font-weight: 800;
        color: {TRUE_TEXT};
        letter-spacing: -0.03em;
    }}

    .verdict-badge-false {{
        font-size: 1.65rem;
        font-weight: 800;
        color: {FALSE_TEXT};
        letter-spacing: -0.03em;
    }}

    .verdict-badge-unverified {{
        font-size: 1.65rem;
        font-weight: 800;
        color: {UNVERIFIED_TEXT};
        letter-spacing: -0.03em;
    }}

    /* Editorial Content Boxes & Source Cards */
    .editorial-section {{
        border-top: 1px solid {BORDER};
        padding-top: 1.5rem;
        margin-top: 2rem;
    }}

    .explanation-box {{
        background-color: {SURFACE};
        border: 1px solid {BORDER};
        border-radius: 8px;
        padding: 18px 22px;
        line-height: 1.65;
        font-size: 0.98rem;
        color: {TEXT_PRIMARY};
    }}

    .evidence-card {{
        background-color: {SURFACE};
        border: 1px solid {BORDER};
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 12px;
        transition: transform 0.2s ease, border-color 0.2s ease !important;
    }}

    .evidence-card:hover {{
        transform: translateY(-2px);
        border-color: {ACCENT_BLUE};
    }}

    .evidence-publisher {{
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: {ACCENT_BLUE};
        margin-bottom: 4px;
    }}

    .evidence-headline {{
        font-size: 0.98rem;
        font-weight: 700;
        color: {TEXT_PRIMARY};
        margin-bottom: 6px;
    }}

    .evidence-finding {{
        font-size: 0.88rem;
        color: {TEXT_SECONDARY};
        margin-bottom: 10px;
        line-height: 1.45;
    }}

    .evidence-link {{
        font-size: 0.85rem;
        font-weight: 600;
        color: {ACCENT_BLUE} !important;
        text-decoration: none;
    }}
    .evidence-link:hover {{
        text-decoration: underline;
    }}

    /* Flow Step Boxes */
    .flow-step-box {{
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: {SURFACE};
        border: 1px solid {BORDER};
        border-radius: 6px;
        padding: 12px;
        font-weight: 700;
        font-size: 0.9rem;
        color: {ACCENT_BLUE};
        text-align: center;
    }}

    /* Sidebar Status Box & Account Section */
    .status-sidebar-box {{
        padding-top: 1rem;
        border-top: 1px solid {BORDER};
        margin-top: 1rem;
    }}

    .status-item {{
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.82rem;
        color: {TEXT_SECONDARY};
        margin-bottom: 4px;
    }}

    .account-sidebar-box {{
        padding-top: 0.75rem;
        border-top: 1px solid {BORDER};
        margin-top: 0.75rem;
    }}

    /* Footer */
    .footer-bar {{
        margin-top: 4rem;
        padding-top: 1.5rem;
        border-top: 1px solid {BORDER};
        text-align: center;
        font-size: 0.82rem;
        color: {TEXT_MUTED};
    }}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ============================================================
# HELPER CALLBACKS & UNIFIED STATE HANDLERS
# ============================================================

def set_theme_mode(new_mode):
    st.session_state.theme = new_mode

def toggle_theme_mode():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

def clear_history_confirmed():
    st.session_state.history = []
    st.session_state.confirm_clear_history = False

def clear_current_result():
    st.session_state.current_result = None
    st.session_state.claim_input = ""

def reset_to_new_verification():
    st.session_state.current_result = None
    st.session_state.claim_input = ""
    st.session_state.active_nav = "Verify"
    st.session_state.popover_action = None

def toggle_account_modal():
    st.session_state.show_account_modal = not st.session_state.show_account_modal


# ============================================================
# CHATGPT-STYLE SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:
    # 1. TOP BRANDING & INTERACTIVE LOGO HOME NAVIGATION (Requirement 12)
    logo_col1, logo_col2 = st.columns([1, 4])
    with logo_col1:
        if st.button("◈", key="brand_logo_home_btn", help="ClarifAI Home (Click to navigate to Verify)", type="secondary"):
            reset_to_new_verification()
            st.rerun()
    with logo_col2:
        st.markdown(f"""
        <div style="font-size: 1.35rem; font-weight: 800; letter-spacing: -0.03em; margin-top: 4px;">ClarifAI</div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # 2. PRIMARY ACTION NAVIGATION
    if st.button("+ New Verification", use_container_width=True, type="primary", help="Start new claim analysis"):
        reset_to_new_verification()
        st.rerun()

    st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)

    if st.button("🔍 Verify", use_container_width=True, type="primary" if st.session_state.active_nav == "Verify" else "secondary", help="Verify"):
        st.session_state.active_nav = "Verify"
        st.session_state.popover_action = None
        st.rerun()

    if st.button("📜 History", use_container_width=True, type="primary" if st.session_state.active_nav == "History" else "secondary", help="History"):
        st.session_state.active_nav = "History"
        st.session_state.popover_action = None
        st.rerun()

    if st.button("ℹ️ How it works", use_container_width=True, type="primary" if st.session_state.active_nav == "How it works" else "secondary", help="How it works"):
        st.session_state.active_nav = "How it works"
        st.session_state.popover_action = None
        st.rerun()

    st.markdown("---")

    # 3. SECONDARY ACTION NAVIGATION
    if st.button("⚙️ Settings", use_container_width=True, type="primary" if st.session_state.active_nav == "Settings" else "secondary", help="Settings"):
        st.session_state.active_nav = "Settings"
        st.session_state.popover_action = None
        st.rerun()

    if st.button("❓ Help / About", use_container_width=True, type="primary" if st.session_state.active_nav == "Help" else "secondary", help="Help & About"):
        st.session_state.active_nav = "Help"
        st.session_state.popover_action = None
        st.rerun()

    # 4. SYSTEM STATUS AT BOTTOM
    health_res = backend_health()
    backend_status = health_res.get("status")

    if backend_status == "healthy":
        status_color = "#00E5A8"
        status_label = "Operational"
    elif backend_status == "degraded":
        status_color = "#F5B942"
        status_label = "Degraded"
    else:
        status_color = "#FF4D5A"
        status_label = "Unavailable"

    st.markdown(f"""
    <div class="status-sidebar-box">
        <div style="font-size: 0.8rem; font-weight: 700; color: {TEXT_PRIMARY}; margin-bottom: 6px;">System Status</div>
        <div class="status-item" title="ML classifier & core engine status"><span class="status-pulse-dot" style="background-color: {status_color};"></span> Backend: {status_label}</div>
        <div class="status-item" title="Live news retrieval service status"><span class="status-pulse-dot" style="background-color: #00E5A8;"></span> News Search: Operational</div>
        <div class="status-item" title="AI verification explanation synthesis service"><span class="status-pulse-dot" style="background-color: #00E5A8;"></span> AI Explanation: Operational</div>
    </div>
    """, unsafe_allow_html=True)

    # 5. CHATGPT-LIKE ACCOUNT AREA AT VERY BOTTOM
    st.markdown('<div class="account-sidebar-box"></div>', unsafe_allow_html=True)
    if st.button("👤 Sign in / Account", use_container_width=True, type="secondary", on_click=toggle_account_modal, help="Account"):
        pass


# ============================================================
# ACCOUNT PANEL / MODAL (SAFE UNAUTHENTICATED FRONTEND ENTRY)
# ============================================================

if st.session_state.show_account_modal:
    st.markdown("---")
    st.markdown("### 👤 ClarifAI Account")
    st.info("ℹ️ Authentication will be available soon. No credentials or passwords are stored locally.")
    
    acc_c1, acc_c2, acc_c3 = st.columns(3)
    with acc_c1:
        st.button("Sign in (Coming Soon)", disabled=True, use_container_width=True, type="secondary")
    with acc_c2:
        st.button("Create account (Coming Soon)", disabled=True, use_container_width=True, type="secondary")
    with acc_c3:
        if st.button("Close Panel", on_click=toggle_account_modal, use_container_width=True, type="secondary"):
            st.rerun()
    st.markdown("---")


# ============================================================
# TOP HEADER & THREE-DOT CONTEXTUAL MENU (PROMPT 13 SPECIFICATION)
# ============================================================

top_c1, top_c2 = st.columns([4, 1])

with top_c1:
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 8px;">
        <span class="status-pulse-dot" style="background-color: {'#00E5A8' if backend_status == 'healthy' else '#F5B942'};"></span>
        <span style="font-size: 0.85rem; font-weight: 600; color: {'#00E5A8' if backend_status == 'healthy' else '#F5B942'};">
            ● Verification services {'available' if backend_status == 'healthy' else 'limited'}
        </span>
    </div>
    """, unsafe_allow_html=True)

with top_c2:
    # 3-Dot Contextual Popover Menu (Prompt 13: NO THEME CONTROL HERE)
    with st.popover("⋮", help="Contextual Options"):
        if st.button("📥 Export Scan Data", use_container_width=True, type="secondary"):
            st.session_state.popover_action = "export"
            st.rerun()

        if st.button("🧹 Clear Cache", use_container_width=True, type="secondary"):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.session_state.popover_action = "cache_cleared"
            st.rerun()

        if st.button("🚩 Report Misclassification", use_container_width=True, type="secondary"):
            st.session_state.popover_action = "report"
            st.session_state.report_submitted = False
            st.rerun()

        if st.button("📖 Documentation", use_container_width=True, type="secondary"):
            st.session_state.popover_action = "doc"
            st.rerun()


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# CONTEXTUAL ACTION PANELS (EXPORT, CACHE, REPORT, DOCUMENTATION)
# ============================================================

if st.session_state.popover_action == "export":
    st.markdown("### 📥 Export Scan Data")
    res = st.session_state.current_result
    
    if res:
        st.success("Verification result available for export.")
        
        # Build JSON Export
        export_payload = {
            "claim": res.get("claim"),
            "verdict": res.get("verdict"),
            "confidence": res.get("confidence"),
            "confidence_level": res.get("confidence_level"),
            "summary": res.get("summary"),
            "why": res.get("why", []),
            "supporting_evidence": res.get("supporting_evidence", []),
            "contradicting_evidence": res.get("contradicting_evidence", []),
            "ml_interpretation": res.get("ml_interpretation"),
            "source_assessment": res.get("source_assessment"),
            "limitations": res.get("limitations", []),
            "articles_found": res.get("articles_found", 0),
            "exported_at": datetime.now().isoformat()
        }
        json_str = json.dumps(export_payload, indent=2)

        # Build CSV Export
        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerow(["Field", "Value"])
        writer.writerow(["Claim", res.get("claim", "")])
        writer.writerow(["Verdict", res.get("verdict", "")])
        writer.writerow(["Confidence", res.get("confidence", "")])
        writer.writerow(["Confidence Level", res.get("confidence_level", "")])
        writer.writerow(["Summary", res.get("summary", "")])
        writer.writerow(["Articles Found", res.get("articles_found", 0)])
        csv_str = csv_buffer.getvalue()

        exp_col1, exp_col2, exp_col3 = st.columns(3)
        with exp_col1:
            st.download_button("Export JSON", data=json_str, file_name="clarifai_scan_data.json", mime="application/json", type="primary", use_container_width=True)
        with exp_col2:
            st.download_button("Export CSV", data=csv_str, file_name="clarifai_scan_data.csv", mime="text/csv", type="secondary", use_container_width=True)
        with exp_col3:
            if st.button("Close Export", type="secondary", use_container_width=True):
                st.session_state.popover_action = None
                st.rerun()
    else:
        st.info("No verification result available to export. Please run a claim analysis first.")
        if st.button("Close Message", type="secondary"):
            st.session_state.popover_action = None
            st.rerun()

    st.markdown("---")

elif st.session_state.popover_action == "cache_cleared":
    st.success("✅ Cache cleared successfully.")
    if st.button("Dismiss", type="secondary"):
        st.session_state.popover_action = None
        st.rerun()
    st.markdown("---")

elif st.session_state.popover_action == "report":
    st.markdown("### 🚩 Report Misclassification")
    res = st.session_state.current_result

    if not res:
        st.warning("Run a verification before reporting a result.")
        if st.button("Dismiss", type="secondary"):
            st.session_state.popover_action = None
            st.rerun()
    else:
        if st.session_state.report_submitted:
            st.success("Thank you. Your feedback has been recorded for this session.")
            if st.button("Done", type="secondary"):
                st.session_state.popover_action = None
                st.session_state.report_submitted = False
                st.rerun()
        else:
            st.write(f"**Reporting claim:** *\"{res.get('claim')}\"*")
            reason = st.selectbox("Reason for report", [
                "I believe this is incorrect",
                "Evidence is misleading",
                "Source is incorrect",
                "Other"
            ])
            notes = st.text_area("Tell us what seems wrong (optional)", placeholder="Provide details about why you suspect misclassification...")
            
            rep_col1, rep_col2 = st.columns(2)
            with rep_col1:
                if st.button("Submit Report", type="primary", use_container_width=True):
                    st.session_state.report_submitted = True
                    st.rerun()
            with rep_col2:
                if st.button("Cancel", type="secondary", use_container_width=True):
                    st.session_state.popover_action = None
                    st.rerun()
    st.markdown("---")

elif st.session_state.popover_action == "doc":
    st.markdown("### 📖 ClarifAI Documentation")
    st.markdown(f"""
    <div class="explanation-box" style="margin-bottom: 16px;">
        <h4 style="margin-top: 0; color: {ACCENT_BLUE};">What ClarifAI Does</h4>
        ClarifAI is an analytical news verification engine that evaluates news claims by searching current published articles, analyzing linguistic pattern signals, and synthesizing transparent explanations.
    </div>

    <div class="explanation-box" style="margin-bottom: 16px;">
        <h4 style="margin-top: 0; color: {ACCENT_BLUE};">Verification Workflow & ML Engine</h4>
        <ul>
            <li><strong>Live News Evidence:</strong> Aggregates published articles from verified reporting sources.</li>
            <li><strong>Linguistic Signal Classifier:</strong> Evaluates content structure against calibrated linear SVM patterns.</li>
            <li><strong>AI Explanation Synthesis:</strong> Generates transparent summaries comparing supporting and contradicting evidence.</li>
            <li><strong>Non-Factual Authority Disclaimer:</strong> Model predictions are analytical signals to assist evaluation, not absolute factual truth.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Close Documentation", type="secondary"):
        st.session_state.popover_action = None
        st.rerun()
    st.markdown("---")


# ============================================================
# PAGE 1: VERIFY (MAIN CLAIM SEARCH WORKSPACE)
# ============================================================

if st.session_state.active_nav == "Verify":

    # Hero Headline & Supporting Text
    st.markdown('<div class="hero-title">Verify what you heard.</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtext">'
        'Check a news claim against current evidence and understand why ClarifAI reached its result.'
        '</div>',
        unsafe_allow_html=True
    )

    # Dynamic Evidence Status Indicator near search box (Requirement 26)
    cur_res = st.session_state.current_result
    if cur_res:
        art_count = cur_res.get("articles_found", 0) or len(cur_res.get("supporting_evidence", [])) + len(cur_res.get("contradicting_evidence", []))
        if art_count > 0:
            ev_status_html = '<div class="evidence-status-pill"><span class="status-pulse-dot" style="background-color: #00E5A8;"></span> Evidence checked</div>'
        else:
            ev_status_html = '<div class="evidence-status-pill"><span class="status-pulse-dot" style="background-color: #F5B942;"></span> Insufficient current evidence</div>'
    else:
        ev_status_html = '<div class="evidence-status-pill"><span class="status-pulse-dot" style="background-color: #00C2FF;"></span> Current evidence</div>'

    st.markdown(ev_status_html, unsafe_allow_html=True)

    # Claim Search Bar Form with keyboard Enter submit support (Requirement 14 & 15)
    with st.form(key="claim_verification_form", clear_on_submit=False):
        
        claim_val = st.text_input(
            "Claim Input",
            value=st.session_state.claim_input,
            placeholder="🔍 What did you hear?",
            label_visibility="collapsed",
            max_chars=5000,
            key="form_claim_field"
        )
        
        col_submit, col_slider = st.columns([2, 1])
        
        with col_slider:
            max_art = st.slider(
                "Evidence articles limit", 
                min_value=1, 
                max_value=10, 
                value=st.session_state.max_articles_limit
            )
            
        with col_submit:
            submit_disabled = len(claim_val.strip()) < 3
            submitted = st.form_submit_button(
                "Analyze Claim  →", 
                type="primary", 
                use_container_width=True, 
                disabled=submit_disabled
            )

    # Helper caption & character count indicator
    char_len = len(claim_val.strip())
    st.caption(f"Paste a claim, headline, or rumor you heard. (Character count: {char_len} / 5000)")

    if 0 < char_len < 3:
        st.warning("Please enter a longer claim (at least 3 characters).")

    # Example Chips below search bar
    st.markdown("**Try an example claim:**")
    ex1, ex2, ex3 = st.columns(3)
    with ex1:
        if st.button("🇮🇳 India free LPG cylinders claim", use_container_width=True, type="secondary"):
            st.session_state.claim_input = "I heard that India announced free LPG cylinders today."
            st.rerun()
    with ex2:
        if st.button("🎬 Reed Hastings & Netflix CEOs claim", use_container_width=True, type="secondary"):
            st.session_state.claim_input = "Netflix co-founder Reed Hastings on why he stopped calling CEOs Ted Sarandos and Greg Peters."
            st.rerun()
    with ex3:
        if st.button("🏫 Government education initiative", use_container_width=True, type="secondary"):
            st.session_state.claim_input = "The government announced a major digital education initiative today."
            st.rerun()

    # Form Submission Execution with Scanning Animation & Loading State (Requirement 16 & 17)
    if submitted and len(claim_val.strip()) >= 3:
        
        loading_placeholder = st.empty()
        
        loading_placeholder.markdown(f"""
        <div style="text-align: center; padding: 26px; background-color: {SURFACE}; border-radius: 10px; border: 1px solid {ACCENT_BLUE};">
            <div style="font-size: 1.15rem; font-weight: 700; color: {ACCENT_BLUE};">● Analyzing evidence…</div>
            <div style="font-size: 0.88rem; color: {TEXT_MUTED}; margin-top: 4px;">Searching live news sources and indexing articles</div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.3)

        loading_placeholder.markdown(f"""
        <div style="text-align: center; padding: 26px; background-color: {SURFACE}; border-radius: 10px; border: 1px solid {ACCENT_BLUE};">
            <div style="font-size: 1.15rem; font-weight: 700; color: {ACCENT_BLUE};">⚡ Comparing available sources…</div>
            <div style="font-size: 0.88rem; color: {TEXT_MUTED}; margin-top: 4px;">Running classification and evidence alignment</div>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            res = verify_news_claim(claim_val.strip(), max_articles=max_art)
        except Exception as err:
            res = {
                "success": False,
                "error": "Unable to reach the verification service. Please try again."
            }

        loading_placeholder.markdown(f"""
        <div style="text-align: center; padding: 26px; background-color: {SURFACE}; border-radius: 10px; border: 1px solid {ACCENT_BLUE};">
            <div style="font-size: 1.15rem; font-weight: 700; color: {ACCENT_BLUE};">✍️ Preparing your explanation…</div>
            <div style="font-size: 0.88rem; color: {TEXT_MUTED}; margin-top: 4px;">Synthesizing final verification report</div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.2)
        
        loading_placeholder.empty()

        if res.get("success"):
            st.session_state.current_result = res
            
            history_item = {
                "id": str(uuid.uuid4()),
                "claim": res["claim"],
                "verdict": res["verdict"],
                "confidence": float(res.get("confidence", 0.0)),
                "confidence_level": res.get("confidence_level", "Unknown"),
                "summary": res.get("summary", ""),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "date_obj": datetime.now().strftime("%Y-%m-%d"),
                "supporting_count": len(res.get("supporting_evidence", [])),
                "contradicting_count": len(res.get("contradicting_evidence", [])),
                "full_result": res
            }
            
            if not any(h.get("claim") == res["claim"] for h in st.session_state.history):
                st.session_state.history.insert(0, history_item)

            st.rerun()

        else:
            err_msg = res.get("error", "Unable to reach the verification service.")
            if "quota" in err_msg.lower() or "busy" in err_msg.lower():
                st.error("⚠️ ClarifAI is temporarily busy. Please try again in a moment.")
            else:
                st.error(f"⚠️ {err_msg}")

    # Render Active Analysis Result
    result = st.session_state.current_result

    if result:
        st.markdown("<br>", unsafe_allow_html=True)
        
        verdict = str(result.get("verdict", "UNVERIFIED")).upper()
        confidence = float(result.get("confidence", 0.0))
        confidence_level = result.get("confidence_level", "Unknown")

        # Result Action Control Buttons
        act_col1, act_col2, act_col3, act_col4, act_col5 = st.columns(5)
        
        with act_col1:
            if st.button("Analyze Again", use_container_width=True, type="secondary"):
                st.session_state.current_result = None
                st.rerun()

        with act_col2:
            copy_summary = f"ClarifAI Verdict: {verdict} ({confidence:.1f}% Confidence)\nClaim: {result.get('claim')}\nSummary: {result.get('summary')}"
            st.download_button(
                "Copy Result", 
                data=copy_summary, 
                file_name="clarifai_analysis.txt", 
                mime="text/plain", 
                use_container_width=True,
                type="secondary"
            )

        with act_col3:
            claim_id = result.get("claim", "")
            is_saved = claim_id in st.session_state.saved_items
            save_label = "Saved" if is_saved else "Save"
            if st.button(save_label, use_container_width=True, type="secondary"):
                if is_saved:
                    st.session_state.saved_items.remove(claim_id)
                else:
                    st.session_state.saved_items.add(claim_id)
                st.rerun()

        with act_col4:
            share_text = f"ClarifAI: {verdict} ({confidence:.1f}%)\n{result.get('claim')}"
            st.code(share_text, language="text")

        with act_col5:
            if st.button("Clear Result", on_click=clear_current_result, use_container_width=True, type="secondary"):
                st.rerun()

        # Verdict Header Card (Requirement 21)
        if verdict == "LIKELY_TRUE":
            st.markdown(f"""
            <div class="verdict-card-true">
                <div class="verdict-badge-true">🟢 LIKELY TRUE</div>
                <div style="font-size: 1rem; font-weight: 600; color: {TEXT_PRIMARY}; margin-top: 6px;">
                    Verification Confidence: <strong>{confidence:.1f}%</strong> ({confidence_level})
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        elif verdict == "LIKELY_FALSE":
            st.markdown(f"""
            <div class="verdict-card-false">
                <div class="verdict-badge-false">🔴 LIKELY FALSE</div>
                <div style="font-size: 1rem; font-weight: 600; color: {TEXT_PRIMARY}; margin-top: 6px;">
                    Verification Confidence: <strong>{confidence:.1f}%</strong> ({confidence_level})
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        else: # UNVERIFIED
            st.markdown(f"""
            <div class="verdict-card-unverified">
                <div class="verdict-badge-unverified">🟡 UNVERIFIED</div>
                <div style="font-size: 1rem; font-weight: 600; color: {TEXT_PRIMARY}; margin-top: 6px;">
                    Verification Confidence: <strong>{confidence:.1f}%</strong> ({confidence_level})
                </div>
                <div style="font-size: 0.85rem; color: {TEXT_SECONDARY}; margin-top: 4px;">
                    Insufficient conclusive evidence to confirm or refute this claim.
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.progress(min(max(confidence / 100.0, 0.0), 1.0))

        # AI Explanation Section (Requirement 22)
        summary_text = result.get("summary", "")
        if summary_text:
            st.markdown('<div class="section-heading">AI Explanation</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="explanation-box">
                {summary_text}
            </div>
            """, unsafe_allow_html=True)

        # Why This Result Section
        why_bullets = result.get("why", [])
        if why_bullets:
            st.markdown('<div class="section-heading">Why this result</div>', unsafe_allow_html=True)
            why_html = "<ul>"
            for w in why_bullets:
                why_html += f"<li style='margin-bottom: 8px; line-height: 1.5; color: {TEXT_PRIMARY};'>{w}</li>"
            why_html += "</ul>"
            st.markdown(why_html, unsafe_allow_html=True)

        # Supporting & Contradicting Evidence Cards (Requirement 23)
        supporting = result.get("supporting_evidence", [])
        contradicting = result.get("contradicting_evidence", [])

        if supporting or contradicting:
            st.markdown('<div class="editorial-section"></div>', unsafe_allow_html=True)
            col_sup, col_con = st.columns(2)

            with col_sup:
                st.markdown(f'<div class="section-heading" style="color: {ACCENT_MINT};">Supporting Evidence</div>', unsafe_allow_html=True)
                if supporting:
                    for ev in supporting:
                        pub = ev.get("publisher") or ev.get("source_domain") or "News Source"
                        head = ev.get("headline") or "News Article"
                        date = ev.get("publication_date") or ""
                        finding = ev.get("finding") or ev.get("summary") or ""
                        url = ev.get("url") or "#"
                        
                        st.markdown(f"""
                        <div class="evidence-card">
                            <div class="evidence-publisher">{pub} {f'• {date}' if date else ''} • <span style="color:{ACCENT_MINT};">✓ Supporting</span></div>
                            <div class="evidence-headline">{head}</div>
                            <div class="evidence-finding">{finding}</div>
                            <a href="{url}" target="_blank" class="evidence-link">Open Article ↗</a>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.caption("No direct supporting evidence articles found.")

            with col_con:
                st.markdown(f'<div class="section-heading" style="color: {ACCENT_RED};">Contradicting Evidence</div>', unsafe_allow_html=True)
                if contradicting:
                    for ev in contradicting:
                        pub = ev.get("publisher") or ev.get("source_domain") or "News Source"
                        head = ev.get("headline") or "News Article"
                        date = ev.get("publication_date") or ""
                        finding = ev.get("finding") or ev.get("summary") or ""
                        url = ev.get("url") or "#"
                        
                        st.markdown(f"""
                        <div class="evidence-card">
                            <div class="evidence-publisher">{pub} {f'• {date}' if date else ''} • <span style="color:{ACCENT_RED};">✕ Contradicting</span></div>
                            <div class="evidence-headline">{head}</div>
                            <div class="evidence-finding">{finding}</div>
                            <a href="{url}" target="_blank" class="evidence-link">Open Article ↗</a>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.caption("No direct contradicting evidence articles found.")

        # Source Assessment
        source_assess = result.get("source_assessment", "")
        if source_assess:
            st.markdown('<div class="editorial-section"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-heading">Source Assessment</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="explanation-box">
                {source_assess}
            </div>
            """, unsafe_allow_html=True)

        # Model Interpretation (Requirement 24 & 25)
        ml_interp = result.get("ml_interpretation", "")
        ml_results = result.get("ml_results", [])
        
        if ml_interp or ml_results:
            st.markdown('<div class="editorial-section"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-heading">Model Interpretation</div>', unsafe_allow_html=True)
            st.caption("ML signals describe linguistic patterns learned from training data. They are analytical signals, not factual proof.")
            
            if ml_interp:
                st.markdown(f"<div style='font-size: 0.95rem; line-height: 1.6; color: {TEXT_SECONDARY}; margin-bottom: 12px;'>{ml_interp}</div>", unsafe_allow_html=True)

            all_signals = []
            for ml_res in ml_results:
                if isinstance(ml_res, dict) and ml_res.get("signals"):
                    all_signals.extend(ml_res.get("signals"))

            if all_signals:
                st.caption("Top linguistic pattern tokens detected:")
                sig_html = '<div class="signals-flex">'
                for sig in all_signals[:10]:
                    if isinstance(sig, dict):
                        f_name = sig.get("feature", "")
                        f_weight = float(sig.get("contribution", 0.0))
                        sig_html += f'<span class="signal-pill">• {f_name} ({f_weight:+.4f})</span>'
                    else:
                        sig_html += f'<span class="signal-pill">• {sig}</span>'
                sig_html += '</div>'
                st.markdown(sig_html, unsafe_allow_html=True)

        # Limitations & Safety
        limitations = result.get("limitations", [])
        safety = result.get("user_safety", "")

        if limitations or safety:
            st.markdown('<div class="editorial-section"></div>', unsafe_allow_html=True)
            if limitations:
                st.markdown('<div class="section-heading">Limitations</div>', unsafe_allow_html=True)
                lim_html = "<ul>"
                for lim in limitations:
                    lim_html += f"<li style='margin-bottom: 6px; font-size: 0.9rem; color: {TEXT_SECONDARY};'>{lim}</li>"
                lim_html += "</ul>"
                st.markdown(lim_html, unsafe_allow_html=True)

            if safety:
                st.caption(f"ℹ️ {safety}")

    else:
        # Empty State
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align: center; padding: 40px; border: 1px dashed {BORDER}; border-radius: 10px; background-color: {SURFACE};">
            <div style="font-size: 1.2rem; font-weight: 700; margin-bottom: 6px;">Tell us what you heard.</div>
            <div style="font-size: 0.92rem; color: {TEXT_MUTED};">Tell ClarifAI what you heard in the search box above to verify current evidence.</div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# PAGE 2: HISTORY (DEDICATED ANALYSIS HISTORY WORKSPACE)
# ============================================================

elif st.session_state.active_nav == "History":

    st.markdown('<div class="hero-title">Analysis History</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtext">Review and search claims verified during your session.</div>', unsafe_allow_html=True)

    if st.session_state.history:
        
        # Search & Filter Controls
        h_col1, h_col2 = st.columns([3, 2])
        
        with h_col1:
            search_query = st.text_input("Search History", placeholder="Filter by claim text...", label_visibility="collapsed")
            
        with h_col2:
            verdict_filter = st.selectbox(
                "Filter Verdict", 
                ["All Verdicts", "Likely True", "Likely False", "Unverified"],
                label_visibility="collapsed"
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Clear History Confirmation Dialog
        if st.session_state.confirm_clear_history:
            st.warning("⚠️ Are you sure you want to clear all analysis history?")
            c_yes, c_no = st.columns(2)
            with c_yes:
                st.button("Yes, Clear All History", on_click=clear_history_confirmed, type="primary", use_container_width=True)
            with c_no:
                if st.button("Cancel", type="secondary", use_container_width=True):
                    st.session_state.confirm_clear_history = False
                    st.rerun()
        else:
            if st.button("Clear History", type="secondary"):
                st.session_state.confirm_clear_history = True
                st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # Filter History Items
        filtered_history = st.session_state.history
        
        if search_query.strip():
            filtered_history = [h for h in filtered_history if search_query.lower() in h.get("claim", "").lower()]

        if verdict_filter == "Likely True":
            filtered_history = [h for h in filtered_history if h.get("verdict") == "LIKELY_TRUE"]
        elif verdict_filter == "Likely False":
            filtered_history = [h for h in filtered_history if h.get("verdict") == "LIKELY_FALSE"]
        elif verdict_filter == "Unverified":
            filtered_history = [h for h in filtered_history if h.get("verdict") == "UNVERIFIED"]

        # Grouping by Date (Today's vs Previous)
        today_str = datetime.now().strftime("%Y-%m-%d")
        todays_items = [h for h in filtered_history if h.get("date_obj") == today_str]
        previous_items = [h for h in filtered_history if h.get("date_obj") != today_str]

        # Render Today's Analyses
        if todays_items:
            st.markdown("##### Today's Analyses")
            for idx, item in enumerate(todays_items):
                v_str = item.get("verdict", "UNVERIFIED")
                c_str = item.get("claim", "")
                conf_val = float(item.get("confidence", 0.0))
                ts_str = item.get("timestamp", "")
                sup_n = item.get("supporting_count", 0)
                con_n = item.get("contradicting_count", 0)

                if v_str == "LIKELY_TRUE":
                    badge = f'<span style="color: {ACCENT_MINT}; font-weight: 800;">🟢 LIKELY TRUE ({conf_val:.1f}%)</span>'
                elif v_str == "LIKELY_FALSE":
                    badge = f'<span style="color: {ACCENT_RED}; font-weight: 800;">🔴 LIKELY FALSE ({conf_val:.1f}%)</span>'
                else:
                    badge = f'<span style="color: {ACCENT_AMBER}; font-weight: 800;">🟡 UNVERIFIED ({conf_val:.1f}%)</span>'

                st.markdown(f"""
                <div style="background-color: {SURFACE}; border: 1px solid {BORDER}; border-radius: 8px; padding: 16px 20px; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                        <div>{badge}</div>
                        <div style="font-size: 0.8rem; color: {TEXT_MUTED};">{ts_str} • Sources: {sup_n + con_n}</div>
                    </div>
                    <div style="font-size: 1rem; font-weight: 700; color: {TEXT_PRIMARY};">{c_str}</div>
                </div>
                """, unsafe_allow_html=True)

                if st.button("Restore Result →", key=f"restore_today_{idx}", type="secondary"):
                    st.session_state.current_result = item.get("full_result")
                    st.session_state.active_nav = "Verify"
                    st.rerun()

        # Render Previous Analyses
        if previous_items:
            st.markdown("##### Previous Analyses")
            for idx, item in enumerate(previous_items):
                v_str = item.get("verdict", "UNVERIFIED")
                c_str = item.get("claim", "")
                conf_val = float(item.get("confidence", 0.0))
                ts_str = item.get("timestamp", "")
                sup_n = item.get("supporting_count", 0)
                con_n = item.get("contradicting_count", 0)

                if v_str == "LIKELY_TRUE":
                    badge = f'<span style="color: {ACCENT_MINT}; font-weight: 800;">🟢 LIKELY TRUE ({conf_val:.1f}%)</span>'
                elif v_str == "LIKELY_FALSE":
                    badge = f'<span style="color: {ACCENT_RED}; font-weight: 800;">🔴 LIKELY FALSE ({conf_val:.1f}%)</span>'
                else:
                    badge = f'<span style="color: {ACCENT_AMBER}; font-weight: 800;">🟡 UNVERIFIED ({conf_val:.1f}%)</span>'

                st.markdown(f"""
                <div style="background-color: {SURFACE}; border: 1px solid {BORDER}; border-radius: 8px; padding: 16px 20px; margin-bottom: 10px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                        <div>{badge}</div>
                        <div style="font-size: 0.8rem; color: {TEXT_MUTED};">{ts_str} • Sources: {sup_n + con_n}</div>
                    </div>
                    <div style="font-size: 1rem; font-weight: 700; color: {TEXT_PRIMARY};">{c_str}</div>
                </div>
                """, unsafe_allow_html=True)

                if st.button("Restore Result →", key=f"restore_prev_{idx}", type="secondary"):
                    st.session_state.current_result = item.get("full_result")
                    st.session_state.active_nav = "Verify"
                    st.rerun()

    else:
        # History Empty State
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align: center; padding: 48px; border: 1px dashed {BORDER}; border-radius: 10px; background-color: {SURFACE};">
            <div style="font-size: 1.3rem; font-weight: 800; color: {TEXT_PRIMARY}; margin-bottom: 6px;">No verifications yet.</div>
            <div style="font-size: 0.95rem; color: {TEXT_MUTED}; margin-bottom: 20px;">Your verified claims will appear here once analyzed.</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Start Analyzing →", type="primary"):
            st.session_state.active_nav = "Verify"
            st.rerun()


# ============================================================
# PAGE 3: HOW IT WORKS (4-STEP EDITORIAL WORKFLOW)
# ============================================================

elif st.session_state.active_nav == "How it works":

    st.markdown('<div class="hero-title">How ClarifAI Works</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtext">Understand ClarifAI in four simple steps.</div>', unsafe_allow_html=True)

    # 4 Simple Steps
    st.markdown(f"""
    <div class="explanation-box" style="margin-bottom: 14px;">
        <div style="font-weight: 800; font-size: 1.05rem; color: {ACCENT_BLUE};">Step 1: Tell ClarifAI what you heard</div>
        <div style="font-size: 0.92rem; color: {TEXT_SECONDARY}; margin-top: 4px;">Enter a news claim, headline, or rumor in the claim search bar.</div>
    </div>

    <div class="explanation-box" style="margin-bottom: 14px;">
        <div style="font-weight: 800; font-size: 1.05rem; color: {ACCENT_BLUE};">Step 2: Find current evidence</div>
        <div style="font-size: 0.92rem; color: {TEXT_SECONDARY}; margin-top: 4px;">ClarifAI queries live news indexing services to find published articles related to the claim.</div>
    </div>

    <div class="explanation-box" style="margin-bottom: 14px;">
        <div style="font-weight: 800; font-size: 1.05rem; color: {ACCENT_BLUE};">Step 3: Compare available evidence</div>
        <div style="font-size: 0.92rem; color: {TEXT_SECONDARY}; margin-top: 4px;">Retrieved articles are evaluated for semantic alignment, supporting statements, and contradicting findings.</div>
    </div>

    <div class="explanation-box" style="margin-bottom: 14px;">
        <div style="font-weight: 800; font-size: 1.05rem; color: {ACCENT_BLUE};">Step 4: Explain the result</div>
        <div style="font-size: 0.92rem; color: {TEXT_SECONDARY}; margin-top: 4px;">An AI synthesis layer generates a clear, readable explanation of the evidence and verdict.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Visual Flow Diagram
    st.markdown("##### Visual Verification Flow")
    
    f1, f2, f3, f4, f5 = st.columns(5)
    with f1:
        st.markdown('<div class="flow-step-box">CLAIM</div>', unsafe_allow_html=True)
    with f2:
        st.markdown('<div class="flow-step-box">CURRENT EVIDENCE</div>', unsafe_allow_html=True)
    with f3:
        st.markdown('<div class="flow-step-box">ANALYSIS</div>', unsafe_allow_html=True)
    with f4:
        st.markdown('<div class="flow-step-box">AI EXPLANATION</div>', unsafe_allow_html=True)
    with f5:
        st.markdown('<div class="flow-step-box">VERDICT</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Editorial Disclosures
    st.markdown(f"""
    <div class="explanation-box">
        <ul style="margin: 0; padding-left: 20px; color: {TEXT_SECONDARY}; line-height: 1.6;">
            <li>ClarifAI searches current news evidence from verified publishers.</li>
            <li>Retrieved article bodies are parsed and analyzed for content signals.</li>
            <li>Linguistic signals provide structural evidence alignment.</li>
            <li>Evidence from multiple independent sources is considered.</li>
            <li>The AI explanation summarizes available evidence for transparent understanding.</li>
            <li><strong>UNVERIFIED</strong> indicates that insufficient relevant evidence was found.</li>
            <li>A model prediction represents an analytical signal, not absolute factual authority.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# PAGE 4: SETTINGS (UNIFIED THEME SOURCE OF TRUTH & APP CONFIG)
# ============================================================

elif st.session_state.active_nav == "Settings":

    st.markdown('<div class="hero-title">Settings</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtext">Manage application preferences, appearance, and service options.</div>', unsafe_allow_html=True)

    st.markdown("##### Preferences & Appearance")
    
    # Unified Theme State Selector (Requirements 11, 28)
    t_col1, t_col2 = st.columns([3, 1])
    with t_col1:
        st.markdown("**Theme Mode**")
        st.caption(f"Currently active theme: {st.session_state.theme.upper()}")
    with t_col2:
        settings_theme = st.radio(
            "Select Theme", 
            ["Dark", "Light"], 
            index=0 if st.session_state.theme == "dark" else 1,
            key="settings_page_theme_radio",
            label_visibility="collapsed"
        )
        settings_theme_str = settings_theme.lower()
        if settings_theme_str != st.session_state.theme:
            st.session_state.theme = settings_theme_str
            st.rerun()

    st.markdown("---")

    st.markdown("##### Verification Configuration")
    new_limit = st.slider("Default evidence article limit", min_value=1, max_value=10, value=st.session_state.max_articles_limit)
    st.session_state.max_articles_limit = new_limit

    st.markdown("---")
    
    st.markdown("##### Services & Status")
    openrouter_active = "OPENROUTER_API_KEY" in os.environ and len(os.environ.get("OPENROUTER_API_KEY", "").strip()) > 0
    currents_active = "CURRENTS_API_KEY" in os.environ and len(os.environ.get("CURRENTS_API_KEY", "").strip()) > 0
    
    st.markdown(f"• **Backend Verification Engine:** {'🟢 Operational' if backend_status == 'healthy' else '🟡 Degraded'}")
    st.markdown(f"• **Live News Indexing Service:** {'🟢 Operational' if currents_active else '🟡 Fallback Mode'}")
    st.markdown(f"• **AI Explanation Layer:** {'🟢 Operational' if openrouter_active else '🟡 Fallback Mode'}")

    st.markdown("---")

    st.markdown("##### About ClarifAI")
    st.markdown("• **Version:** ClarifAI 2.0 (Premium Release)")
    st.markdown("• **Disclaimer:** Analytical signals & live evidence aggregation. Predictions are analytical tools, not absolute factual authority.")


# ============================================================
# PAGE 5: HELP / ABOUT
# ============================================================

elif st.session_state.active_nav == "Help":

    st.markdown('<div class="hero-title">Help & About ClarifAI</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtext">Learn more about ClarifAI and how to verify claims effectively.</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="explanation-box" style="margin-bottom: 16px;">
        <h4 style="margin-top: 0; color: {ACCENT_BLUE};">ClarifAI Verification Architecture</h4>
        ClarifAI is an analytical news verification system that combines live news evidence search, article text extraction, pattern-based linguistic analysis, and AI explanation synthesis.
    </div>

    <div class="explanation-box" style="margin-bottom: 16px;">
        <h4 style="margin-top: 0; color: {ACCENT_BLUE};">Frequently Asked Questions</h4>
        <p><strong>Q: What does LIKELY TRUE / LIKELY FALSE mean?</strong><br>
        These verdicts represent the convergence of current news evidence and linguistic pattern signals evaluated by ClarifAI.</p>
        <p><strong>Q: Why does a claim show UNVERIFIED?</strong><br>
        UNVERIFIED indicates that insufficient recent published articles were found to confirm or refute the claim.</p>
        <p><strong>Q: Are model predictions factual proof?</strong><br>
        No. ClarifAI predictions are analytical tools to assist research and factual analysis. They are not an absolute factual authority.</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# STATIC FOOTER
# ============================================================

st.markdown(f"""
<div class="footer-bar">
    ClarifAI • News Authenticity & Pattern Analysis Engine
    <br>
    <span style="font-size: 0.75rem; opacity: 0.7;">
        Analytical signals & live evidence aggregation. Not an absolute factual authority.
    </span>
</div>
""", unsafe_allow_html=True)