"""
app_config.py
-------------
Central configuration for the Legal Contract Risk Analyzer Streamlit app.
Contains UI constants, risk keyword lists, and colour palette definitions.
"""

# ---------------------------------------------------------------------------
# App metadata
# ---------------------------------------------------------------------------
APP_TITLE = "⚖️ Legal Contract Risk Analyzer"
APP_SUBTITLE = "AI-powered clause-level risk detection for legal documents"
APP_VERSION = "1.0.0"

# ---------------------------------------------------------------------------
# Risk keyword library (used by the dummy risk predictor)
# ---------------------------------------------------------------------------
RISK_KEYWORDS = [
    # Liability & indemnity
    "indemnify", "indemnification", "indemnified", "hold harmless",
    "liability", "unlimited liability", "gross negligence",
    # Termination & penalties
    "terminate", "termination", "penalty", "penalties", "liquidated damages",
    "forfeiture", "default",
    # Dispute resolution
    "arbitration", "arbitral", "waive", "waiver", "waived",
    "jurisdiction", "governing law",
    # Intellectual property
    "irrevocable", "perpetual", "royalty-free", "sublicense",
    "assign", "assignment", "transfer of rights",
    # Confidentiality
    "non-disclosure", "proprietary", "trade secret", "confidential information",
    # Financial risk
    "interest rate", "compound interest", "late payment", "surcharge",
    "deduct", "withhold", "escrow",
    # Employment / non-compete
    "non-compete", "non-solicitation", "garden leave", "restraint of trade",
]

# ---------------------------------------------------------------------------
# Risk thresholds
# ---------------------------------------------------------------------------
# A clause is marked Risky if it contains >= this many keywords
RISK_KEYWORD_THRESHOLD = 1

# Confidence score modelling (used in dummy predictor)
BASE_RISKY_CONFIDENCE = 0.85     # base score when keywords found
SAFE_CONFIDENCE = 0.92           # score for safe clauses

# ---------------------------------------------------------------------------
# UI colour palette (hex strings injected via st.markdown CSS)
# ---------------------------------------------------------------------------
COLOUR = {
    "bg_dark":       "#0E1117",
    "bg_card":       "#1A1D27",
    "bg_risky":      "#2D1B1B",
    "bg_safe":       "#1B2D1F",
    "border_risky":  "#FF4B4B",
    "border_safe":   "#21D07A",
    "accent":        "#7C6AF7",
    "accent_light":  "#B8B0FF",
    "text_primary":  "#FFFFFF",
    "text_secondary":"#9DA3B4",
    "badge_risky":   "#FF4B4B",
    "badge_safe":    "#21D07A",
}

# ---------------------------------------------------------------------------
# Sidebar content
# ---------------------------------------------------------------------------
SIDEBAR_HOW_TO = """
**How to use:**
1. Upload a PDF or TXT contract file
2. The app will split it into clauses
3. Each clause is scanned for risk indicators
4. ⚠️ Risky clauses are highlighted in red
5. ✅ Safe clauses appear in green

**Supported formats:** `.pdf`, `.txt`
"""

SIDEBAR_DISCLAIMER = """
> **Disclaimer:** This tool is for demonstration purposes only and does not constitute legal advice.
> Always consult a qualified lawyer before signing any contract.
"""
