"""
utils/risk_predictor.py
------------------------
Dummy rule-based risk prediction engine.
Uses keyword matching against a curated list of risky legal terms.
In a production system, this would be replaced by a trained ML model.
"""

import re
from typing import Dict, List
from app_config import (
    RISK_KEYWORDS,
    RISK_KEYWORD_THRESHOLD,
    BASE_RISKY_CONFIDENCE,
    SAFE_CONFIDENCE,
)

# ---------------------------------------------------------------------------
# Risk category mapping for richer UI context
# ---------------------------------------------------------------------------
_CATEGORY_MAP: Dict[str, str] = {
    "indemnify":           "Indemnity",
    "indemnification":     "Indemnity",
    "indemnified":         "Indemnity",
    "hold harmless":       "Indemnity",
    "liability":           "Liability",
    "unlimited liability": "Liability",
    "gross negligence":    "Liability",
    "terminate":           "Termination",
    "termination":         "Termination",
    "penalty":             "Penalties",
    "penalties":           "Penalties",
    "liquidated damages":  "Penalties",
    "forfeiture":          "Penalties",
    "default":             "Default",
    "arbitration":         "Dispute Resolution",
    "arbitral":            "Dispute Resolution",
    "waive":               "Waiver",
    "waiver":              "Waiver",
    "waived":              "Waiver",
    "jurisdiction":        "Jurisdiction",
    "governing law":       "Jurisdiction",
    "irrevocable":         "IP / Rights",
    "perpetual":           "IP / Rights",
    "royalty-free":        "IP / Rights",
    "sublicense":          "IP / Rights",
    "assign":              "IP / Rights",
    "assignment":          "IP / Rights",
    "transfer of rights":  "IP / Rights",
    "non-disclosure":      "Confidentiality",
    "proprietary":         "Confidentiality",
    "trade secret":        "Confidentiality",
    "confidential information": "Confidentiality",
    "interest rate":       "Financial",
    "compound interest":   "Financial",
    "late payment":        "Financial",
    "surcharge":           "Financial",
    "deduct":              "Financial",
    "withhold":            "Financial",
    "escrow":              "Financial",
    "non-compete":         "Non-Compete",
    "non-solicitation":    "Non-Compete",
    "garden leave":        "Non-Compete",
    "restraint of trade":  "Non-Compete",
}


def predict_clause_risk(clause: Dict) -> Dict:
    """
    Predicts whether a single clause is Risky or Safe.

    Args:
        clause (Dict): A clause dict with at least a 'text' key.

    Returns:
        The input dict augmented with:
            - label           (str)  : "Risky" or "Safe"
            - confidence      (float): prediction confidence score 0–1
            - matched_keywords (list): keywords found in the clause
            - categories      (list): risk categories from matched keywords
    """
    text_lower = clause["text"].lower()
    matched = []

    for keyword in RISK_KEYWORDS:
        pattern = r"\b" + re.escape(keyword) + r"\b"
        if re.search(pattern, text_lower):
            matched.append(keyword)

    is_risky = len(matched) >= RISK_KEYWORD_THRESHOLD

    # Confidence scales up slightly with more keyword hits
    if is_risky:
        bonus = min(0.10, len(matched) * 0.02)
        confidence = round(BASE_RISKY_CONFIDENCE + bonus, 3)
        label = "Risky"
    else:
        confidence = SAFE_CONFIDENCE
        label = "Safe"

    categories = list(
        dict.fromkeys(
            _CATEGORY_MAP.get(kw, "General Risk") for kw in matched
        )
    )

    return {
        **clause,
        "label": label,
        "confidence": confidence,
        "matched_keywords": matched,
        "categories": categories,
    }


def analyze_clauses(clauses: List[Dict]) -> List[Dict]:
    """
    Runs risk prediction on a list of clause dicts.

    Args:
        clauses (List[Dict]): Output from clause_segmenter.segment_document()

    Returns:
        List of clause dicts with risk prediction fields added.
    """
    return [predict_clause_risk(c) for c in clauses]


def compute_summary_stats(analyzed_clauses: List[Dict]) -> Dict:
    """
    Computes summary statistics for display in KPI tiles.

    Returns:
        dict with total, risky_count, safe_count, risk_percentage
    """
    total = len(analyzed_clauses)
    risky = sum(1 for c in analyzed_clauses if c["label"] == "Risky")
    safe = total - risky
    risk_pct = round((risky / total * 100) if total > 0 else 0.0, 1)

    return {
        "total": total,
        "risky_count": risky,
        "safe_count": safe,
        "risk_percentage": risk_pct,
    }
