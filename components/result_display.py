"""
components/result_display.py
-----------------------------
Streamlit rendering functions for displaying clause analysis results.
Provides styled cards for risky/safe clauses and summary KPI tiles.
"""

import streamlit as st
from typing import Dict, List
from app_config import COLOUR


# ---------------------------------------------------------------------------
# CSS helper
# ---------------------------------------------------------------------------

def inject_card_styles() -> None:
    """Inject custom CSS for clause cards, badges, and KPI tiles."""
    st.markdown(
        f"""
        <style>
        /* ---- Risky clause card ---- */
        .risky-card {{
            background: {COLOUR['bg_risky']};
            border: 1.5px solid {COLOUR['border_risky']};
            border-left: 5px solid {COLOUR['border_risky']};
            border-radius: 10px;
            padding: 16px 20px;
            margin-bottom: 14px;
            box-shadow: 0 2px 12px rgba(255, 75, 75, 0.15);
        }}

        /* ---- Safe clause card ---- */
        .safe-card {{
            background: {COLOUR['bg_safe']};
            border: 1.5px solid {COLOUR['border_safe']};
            border-left: 5px solid {COLOUR['border_safe']};
            border-radius: 10px;
            padding: 16px 20px;
            margin-bottom: 14px;
        }}

        /* ---- Clause header row ---- */
        .clause-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
        }}

        /* ---- Label badge ---- */
        .badge-risky {{
            background: {COLOUR['badge_risky']};
            color: white;
            font-size: 11px;
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 20px;
            letter-spacing: 0.5px;
        }}
        .badge-safe {{
            background: {COLOUR['badge_safe']};
            color: #0E1117;
            font-size: 11px;
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 20px;
            letter-spacing: 0.5px;
        }}

        /* ---- Clause text ---- */
        .clause-text {{
            color: {COLOUR['text_primary']};
            font-size: 14px;
            line-height: 1.7;
            margin: 0;
        }}

        /* ---- Keyword tags ---- */
        .keyword-tag {{
            display: inline-block;
            background: rgba(255,75,75,0.15);
            color: {COLOUR['border_risky']};
            border: 1px solid {COLOUR['border_risky']};
            font-size: 11px;
            padding: 2px 8px;
            border-radius: 12px;
            margin: 3px 3px 0 0;
        }}

        /* ---- Category chip ---- */
        .cat-chip {{
            display: inline-block;
            background: rgba(124,106,247,0.18);
            color: {COLOUR['accent_light']};
            border: 1px solid {COLOUR['accent']};
            font-size: 10px;
            padding: 2px 7px;
            border-radius: 10px;
            margin: 3px 3px 0 0;
        }}

        /* ---- KPI tile ---- */
        .kpi-tile {{
            background: {COLOUR['bg_card']};
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.08);
        }}
        .kpi-value {{
            font-size: 2.4rem;
            font-weight: 800;
            line-height: 1.1;
        }}
        .kpi-label {{
            font-size: 13px;
            color: {COLOUR['text_secondary']};
            margin-top: 4px;
        }}

        /* ---- Confidence bar ---- */
        .conf-bar-wrap {{
            margin-top: 10px;
            background: rgba(255,255,255,0.08);
            border-radius: 4px;
            height: 4px;
        }}
        .conf-bar-fill {{
            height: 4px;
            border-radius: 4px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# KPI Summary tiles
# ---------------------------------------------------------------------------

def render_summary_metrics(stats: Dict) -> None:
    """
    Renders four KPI tiles: Total, Risky, Safe, Risk%.

    Args:
        stats: dict from risk_predictor.compute_summary_stats()
    """
    col1, col2, col3, col4 = st.columns(4)

    cols_data = [
        (col1, str(stats["total"]),                "Total Clauses",   COLOUR["accent_light"]),
        (col2, str(stats["risky_count"]),           "⚠️ Risky Clauses", COLOUR["border_risky"]),
        (col3, str(stats["safe_count"]),            "✅ Safe Clauses",  COLOUR["border_safe"]),
        (col4, f"{stats['risk_percentage']}%",      "Risk Level",       "#F5A623"),
    ]

    for col, value, label, colour in cols_data:
        with col:
            st.markdown(
                f"""
                <div class="kpi-tile">
                    <div class="kpi-value" style="color:{colour};">{value}</div>
                    <div class="kpi-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ---------------------------------------------------------------------------
# Individual clause renderers
# ---------------------------------------------------------------------------

def render_risky_clause(clause: Dict) -> None:
    """
    Renders a single risky clause as a styled red card.

    Args:
        clause: An analyzed clause dict from risk_predictor.analyze_clauses()
    """
    conf_pct = int(clause["confidence"] * 100)
    keywords_html = "".join(
        f'<span class="keyword-tag">🔑 {kw}</span>'
        for kw in clause["matched_keywords"]
    )
    categories_html = "".join(
        f'<span class="cat-chip">{cat}</span>'
        for cat in clause["categories"]
    )

    st.markdown(
        f"""
        <div class="risky-card">
            <div class="clause-header">
                <span style="color:{COLOUR['text_secondary']};font-size:12px;font-weight:600;">
                    CLAUSE #{clause['id']}
                </span>
                <span class="badge-risky">⚠ RISKY</span>
                <span style="font-size:12px;color:{COLOUR['text_secondary']};margin-left:auto;">
                    {conf_pct}% confidence
                </span>
            </div>
            <p class="clause-text">{clause['text']}</p>
            <div style="margin-top:12px;">
                {keywords_html}
            </div>
            <div style="margin-top:6px;">
                {categories_html}
            </div>
            <div class="conf-bar-wrap">
                <div class="conf-bar-fill" style="width:{conf_pct}%; background:{COLOUR['border_risky']};"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_safe_clause(clause: Dict) -> None:
    """
    Renders a single safe clause as a subtle green card.

    Args:
        clause: An analyzed clause dict from risk_predictor.analyze_clauses()
    """
    conf_pct = int(clause["confidence"] * 100)

    st.markdown(
        f"""
        <div class="safe-card">
            <div class="clause-header">
                <span style="color:{COLOUR['text_secondary']};font-size:12px;font-weight:600;">
                    CLAUSE #{clause['id']}
                </span>
                <span class="badge-safe">✔ SAFE</span>
                <span style="font-size:12px;color:{COLOUR['text_secondary']};margin-left:auto;">
                    {conf_pct}% confidence
                </span>
            </div>
            <p class="clause-text">{clause['text']}</p>
            <div class="conf-bar-wrap">
                <div class="conf-bar-fill" style="width:{conf_pct}%; background:{COLOUR['border_safe']};"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_clause_list(analyzed_clauses: List[Dict], show_safe: bool = True) -> None:
    """
    Renders all clauses in order, using the appropriate card for each.

    Args:
        analyzed_clauses: Full list from risk_predictor.analyze_clauses()
        show_safe: Whether to render safe clauses (default True)
    """
    for clause in analyzed_clauses:
        if clause["label"] == "Risky":
            render_risky_clause(clause)
        elif show_safe:
            render_safe_clause(clause)
