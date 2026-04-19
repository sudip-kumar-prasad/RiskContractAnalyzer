   

                                                                             
              
                                                                             
APP_TITLE = "Legal Contract Risk Analyzer"
APP_SUBTITLE = "AI-powered clause-level risk detection for legal documents"
APP_VERSION = "1.0.0"

TEAM_NAME = "MindMatrix"
TEAM_MEMBERS = [
    {"name": "Sudip Kumar Prasad", "urn": "2024-B-01112005A"},
    {"name": "Harshit Singh", "urn": "2024-B-21082007"},
    {"name": "Garv Gogna", "urn": "2024-B-15062006A"},
    {"name": "Yash Shriram Lahase", "urn": "2024-B-17112006C"}
]

                                                                             
                                                         
                                                                             
RISK_KEYWORDS = [
                           
    "indemnify", "indemnification", "indemnified", "hold harmless",
    "liability", "unlimited liability", "gross negligence",
                             
    "terminate", "termination", "penalty", "penalties", "liquidated damages",
    "forfeiture", "default",
                        
    "arbitration", "arbitral", "waive", "waiver", "waived",
    "jurisdiction", "governing law",
                           
    "irrevocable", "perpetual", "royalty-free", "sublicense",
    "assign", "assignment", "transfer of rights",
                     
    "non-disclosure", "proprietary", "trade secret", "confidential information",
                    
    "interest rate", "compound interest", "late payment", "surcharge",
    "deduct", "withhold", "escrow",
                              
    "non-compete", "non-solicitation", "garden leave", "restraint of trade",
]

                                                                             
                 
                                                                             
                                                               
RISK_KEYWORD_THRESHOLD = 1

                                                      
BASE_RISKY_CONFIDENCE = 0.85                                     
SAFE_CONFIDENCE = 0.92                                   

                                                                             
                                                              
                                                                             
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

                                                                             
                 
                                                                             
SIDEBAR_HOW_TO = """
**How to use:**
1. Upload a PDF or TXT contract file
2. The app will split it into clauses
3. Each clause is scanned for risk indicators
4. [!] Risky clauses are highlighted in red
5. [OK] Safe clauses appear in green

**Supported formats:** .pdf, .txt
"""

SIDEBAR_DISCLAIMER = """
> **Disclaimer:** This tool is for demonstration purposes only and does not constitute legal advice.
> Always consult a qualified lawyer before signing any contract.
"""
