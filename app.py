"""
app.py
------
Legal Contract Risk Analyzer — Single-page Streamlit Application.

Pipeline:
    Upload (PDF/TXT) → Text Extraction → Clause Segmentation
    → Risk Prediction → Results Display

Usage:
    streamlit run app.py
"""

import time
import streamlit as st

from app_config import (
    APP_TITLE,
    APP_SUBTITLE,
    COLOUR,
    SIDEBAR_HOW_TO,
    SIDEBAR_DISCLAIMER,
)
from utils.file_handler import extract_text_from_upload, get_file_metadata
from utils.clause_segmenter import segment_document
from utils.risk_predictor import analyze_clauses, compute_summary_stats
from components.result_display import (
    inject_card_styles,
    render_summary_metrics,
    render_clause_list,
)

# ---------------------------------------------------------------------------
# Page config — must be first Streamlit call
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Legal Risk Analyzer",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------------
# Global CSS overrides
# ---------------------------------------------------------------------------
def _inject_global_styles() -> None:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
        }}

        /* Background */
        .stApp {{
            background: linear-gradient(135deg, #0E1117 0%, #141824 100%);
        }}

        /* Hero banner */
        .hero-banner {{
            background: linear-gradient(135deg, #1a1040 0%, #0f2040 50%, #0d1f3c 100%);
            border: 1px solid rgba(124,106,247,0.3);
            border-radius: 16px;
            padding: 38px 44px;
            margin-bottom: 32px;
            position: relative;
            overflow: hidden;
        }}
        .hero-banner::before {{
            content: '';
            position: absolute;
            top: -80px; right: -80px;
            width: 280px; height: 280px;
            background: radial-gradient(circle, rgba(124,106,247,0.18) 0%, transparent 70%);
            pointer-events: none;
        }}
        .hero-title {{
            font-size: 2.8rem;
            font-weight: 800;
            background: linear-gradient(90deg, #B8B0FF 0%, #7C6AF7 50%, #4FC3F7 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0 0 8px 0;
            line-height: 1.15;
        }}
        .hero-subtitle {{
            color: {COLOUR['text_secondary']};
            font-size: 1.05rem;
            font-weight: 400;
            margin: 0;
        }}

        /* Upload zone */
        [data-testid="stFileUploader"] {{
            background: {COLOUR['bg_card']};
            border: 2px dashed rgba(124,106,247,0.45);
            border-radius: 14px;
            padding: 12px;
            transition: border-color 0.3s ease;
        }}
        [data-testid="stFileUploader"]:hover {{
            border-color: {COLOUR['accent']};
        }}

        /* Section heading */
        .section-title {{
            font-size: 1.1rem;
            font-weight: 700;
            color: {COLOUR['text_primary']};
            border-bottom: 2px solid {COLOUR['accent']};
            padding-bottom: 8px;
            margin: 28px 0 20px 0;
            display: inline-block;
        }}

        /* File info chip */
        .file-chip {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: {COLOUR['bg_card']};
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 8px;
            padding: 8px 14px;
            font-size: 13px;
            color: {COLOUR['text_secondary']};
            margin-bottom: 20px;
        }}

        /* Sidebar */
        [data-testid="stSidebar"] {{
            background: {COLOUR['bg_card']};
            border-right: 1px solid rgba(255,255,255,0.06);
        }}

        /* Toggle label */
        .stCheckbox label {{
            color: {COLOUR['text_secondary']};
            font-size: 14px;
        }}

        /* Progress / spinner */
        .stProgress > div > div {{
            background: {COLOUR['accent']};
        }}

        /* Divider */
        hr {{
            border-color: rgba(255,255,255,0.06);
        }}

        /* Filter tab styling */
        .stTabs [data-baseweb="tab"] {{
            color: {COLOUR['text_secondary']};
            font-size: 14px;
            font-weight: 500;
        }}
        .stTabs [aria-selected="true"] {{
            color: {COLOUR['accent_light']} !important;
            border-bottom-color: {COLOUR['accent']} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
def _render_sidebar() -> bool:
    """Renders the sidebar and returns the show_safe_clauses toggle value."""
    with st.sidebar:
        st.markdown(
            f"""
            <div style="text-align:center; padding: 16px 0 24px;">
                <div style="font-size:2.8rem;">⚖️</div>
                <div style="font-weight:800;font-size:1.1rem;color:{COLOUR['text_primary']};">
                    Contract Analyzer
                </div>
                <div style="font-size:11px;color:{COLOUR['text_secondary']};margin-top:4px;">
                    Powered by Rule-Based NLP
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.markdown(SIDEBAR_HOW_TO)
        st.markdown("---")

        st.markdown("### ⚙️ Display Options")
        show_safe = st.checkbox("Show safe clauses", value=True)

        st.markdown("---")

        st.markdown("### 🔍 Risk Legend")
        st.markdown(
            f"""
            <div style="display:flex;flex-direction:column;gap:8px;font-size:13px;">
                <div>
                    <span style="color:{COLOUR['border_risky']};font-weight:700;">⚠ RISKY</span>
                    &nbsp;— Contains risk keywords
                </div>
                <div>
                    <span style="color:{COLOUR['border_safe']};font-weight:700;">✔ SAFE</span>
                    &nbsp;— No risk keywords found
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.markdown(SIDEBAR_DISCLAIMER)

    return show_safe


# ---------------------------------------------------------------------------
# Hero Header
# ---------------------------------------------------------------------------
def _render_hero() -> None:
    st.markdown(
        f"""
        <div class="hero-banner">
            <p class="hero-title">{APP_TITLE}</p>
            <p class="hero-subtitle">{APP_SUBTITLE}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# File upload section
# ---------------------------------------------------------------------------
def _render_upload_section():
    st.markdown('<div class="section-title">📄 Upload Contract Document</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        label="Drag & drop your contract here, or click to browse",
        type=["pdf", "txt"],
        help="Supported formats: PDF (.pdf) and plain text (.txt)",
        label_visibility="visible",
    )
    return uploaded_file


# ---------------------------------------------------------------------------
# Analysis pipeline
# ---------------------------------------------------------------------------
def _run_pipeline(uploaded_file):
    """
    Runs the full analysis pipeline with a progress bar.
    Returns (analyzed_clauses, stats, metadata) or (None, None, None) on error.
    """
    meta = get_file_metadata(uploaded_file)

    # Show file info
    st.markdown(
        f"""
        <div class="file-chip">
            <span>📎</span>
            <strong>{meta['name']}</strong>
            &nbsp;|&nbsp; {meta['file_type']} &nbsp;|&nbsp; {meta['size_kb']} KB
        </div>
        """,
        unsafe_allow_html=True,
    )

    progress_bar = st.progress(0, text="Starting analysis…")

    try:
        # Step 1: Extract text
        progress_bar.progress(20, text="📖 Extracting text from document…")
        time.sleep(0.3)
        text = extract_text_from_upload(uploaded_file)

        if not text or not text.strip():
            st.error("⚠️ Could not extract any text from the document. Please try a different file.")
            progress_bar.empty()
            return None, None, None

        # Step 2: Segment clauses
        progress_bar.progress(50, text="✂️ Segmenting document into clauses…")
        time.sleep(0.3)
        clauses = segment_document(text)

        if not clauses:
            st.warning("No clauses could be extracted from this document. Try a more structured contract.")
            progress_bar.empty()
            return None, None, None

        # Step 3: Predict risk
        progress_bar.progress(80, text="🔍 Running risk analysis on each clause…")
        time.sleep(0.3)
        analyzed = analyze_clauses(clauses)
        stats = compute_summary_stats(analyzed)

        progress_bar.progress(100, text="✅ Analysis complete!")
        time.sleep(0.4)
        progress_bar.empty()

        return analyzed, stats, meta

    except ValueError as e:
        st.error(f"❌ File Error: {e}")
        progress_bar.empty()
        return None, None, None
    except Exception as e:
        st.error(f"❌ Unexpected error during analysis: {e}")
        progress_bar.empty()
        return None, None, None


# ---------------------------------------------------------------------------
# Results section
# ---------------------------------------------------------------------------
def _render_results(analyzed_clauses, stats, show_safe: bool) -> None:
    st.markdown("---")

    # KPI summary tiles
    st.markdown('<div class="section-title">📊 Risk Summary</div>', unsafe_allow_html=True)
    render_summary_metrics(stats)

    st.markdown("<br>", unsafe_allow_html=True)

    # Risk gauge visual
    risk_pct = stats["risk_percentage"]
    gauge_color = (
        COLOUR["border_risky"] if risk_pct >= 50
        else "#F5A623" if risk_pct >= 25
        else COLOUR["border_safe"]
    )
    st.markdown(
        f"""
        <div style="background:{COLOUR['bg_card']};border-radius:12px;padding:18px 24px;
                    border:1px solid rgba(255,255,255,0.08);margin-bottom:28px;">
            <div style="display:flex;justify-content:space-between;margin-bottom:8px;">
                <span style="font-size:14px;color:{COLOUR['text_secondary']};font-weight:500;">
                    Overall Contract Risk
                </span>
                <span style="font-size:14px;color:{gauge_color};font-weight:700;">{risk_pct}%</span>
            </div>
            <div style="background:rgba(255,255,255,0.08);border-radius:6px;height:10px;">
                <div style="width:{risk_pct}%;background:linear-gradient(90deg,{gauge_color}88,{gauge_color});
                            height:10px;border-radius:6px;transition:width 0.6s ease;"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Clause list with filter tabs
    st.markdown('<div class="section-title">📋 Clause Analysis</div>', unsafe_allow_html=True)

    risky_count = stats["risky_count"]
    safe_count  = stats["safe_count"]

    tab_all, tab_risky, tab_safe = st.tabs([
        f"All ({stats['total']})",
        f"⚠️ Risky ({risky_count})",
        f"✅ Safe ({safe_count})",
    ])

    with tab_all:
        render_clause_list(analyzed_clauses, show_safe=show_safe)

    with tab_risky:
        risky_clauses = [c for c in analyzed_clauses if c["label"] == "Risky"]
        if risky_clauses:
            render_clause_list(risky_clauses, show_safe=False)
        else:
            st.success("🎉 No risky clauses were found in this document!")

    with tab_safe:
        safe_clauses = [c for c in analyzed_clauses if c["label"] == "Safe"]
        if safe_clauses:
            render_clause_list(safe_clauses, show_safe=True)
        else:
            st.warning("All clauses were flagged as risky.")


# ---------------------------------------------------------------------------
# Empty state
# ---------------------------------------------------------------------------
def _render_empty_state() -> None:
    st.markdown(
        f"""
        <div style="text-align:center;padding:60px 20px;color:{COLOUR['text_secondary']};">
            <div style="font-size:5rem;margin-bottom:16px;">📜</div>
            <div style="font-size:1.3rem;font-weight:600;color:{COLOUR['text_primary']};margin-bottom:8px;">
                No document uploaded yet
            </div>
            <div style="font-size:14px;max-width:420px;margin:0 auto;">
                Upload a PDF or TXT contract file using the uploader above
                to instantly analyze it for risky clauses.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------
def main() -> None:
    _inject_global_styles()
    inject_card_styles()

    show_safe = _render_sidebar()
    _render_hero()

    uploaded_file = _render_upload_section()

    if uploaded_file is not None:
        analyzed_clauses, stats, meta = _run_pipeline(uploaded_file)
        if analyzed_clauses is not None:
            _render_results(analyzed_clauses, stats, show_safe)
    else:
        _render_empty_state()

    # Footer
    st.markdown(
        f"""
        <div style="text-align:center;padding:40px 0 20px;color:{COLOUR['text_secondary']};font-size:12px;">
            ⚖️ Legal Contract Risk Analyzer &nbsp;|&nbsp;
            For demonstration only &nbsp;|&nbsp;
            Not legal advice
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
