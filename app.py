import os
import streamlit as st

# Mandatory: set_page_config must be the first Streamlit command
st.set_page_config(
    page_title="Legal Risk Analyzer",
    page_icon="[Risk]",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Move model check AFTER page config
if not os.path.exists("models/best_model.joblib"):
    st.warning("Warning: ML model not found. Using rule-based detection.")

import time
import json

from app_config import (
    APP_TITLE,
    APP_SUBTITLE,
    COLOUR,
    SIDEBAR_HOW_TO,
    SIDEBAR_DISCLAIMER,
    TEAM_NAME,
    TEAM_MEMBERS,
)
from utils.file_handler import extract_text_from_upload, get_file_metadata
from utils.clause_segmenter import segment_document
from utils.risk_predictor import analyze_clauses, compute_summary_stats
from utils.export_handler import generate_pdf_report
from components.result_display import (
    inject_card_styles,
    render_summary_metrics,
    render_clause_list,
)

from src.agents.legal_agent import LegalAgent, AgentState

if "agent_report" not in st.session_state:
    st.session_state.agent_report = None
if "last_analyzed_file" not in st.session_state:
    st.session_state.last_analyzed_file = None

def _inject_global_styles() -> None:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
        }}

        .stApp {{
            background: linear-gradient(135deg, #0E1117 0%, #141824 100%);
        }}

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
            color: #FFFFFF;
            text-shadow: 0px 4px 15px rgba(124,106,247,0.4);
            margin: 0 0 8px 0;
            line-height: 1.15;
        }}
        .hero-subtitle {{
            color: {COLOUR['text_secondary']};
            font-size: 1.05rem;
            font-weight: 400;
            margin: 0;
        }}

        [data-testid="stMetric"] {{
            background-color: {COLOUR['bg_card']};
            border-radius: 10px;
            padding: 15px;
            border: 1px solid rgba(255,255,255,0.05);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def main():
    _inject_global_styles()
    inject_card_styles()

    with st.sidebar:
        st.markdown(
            f"""
            <div style="text-align:center; padding: 16px 0 24px;">
                <div style="font-size:2.8rem;">[Risk]</div>
                <div style="font-weight:800;font-size:1.1rem;color:{COLOUR['text_primary']};">
                    Contract Analyzer
                </div>
                <div style="font-size:11px;color:{COLOUR['text_secondary']};margin-top:4px;">
                    Powered by Trained ML & Agentic AI
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.markdown(SIDEBAR_HOW_TO)
        
        st.markdown("---")
        st.markdown("### Display Options")
        show_safe = st.checkbox("Show safe clauses", value=True)
        
        st.markdown("---")
        st.markdown("### Risk Legend")
        st.markdown(
            f"""
            <div style="display:flex;flex-direction:column;gap:8px;font-size:13px;">
                <div>
                    <span style="color:{COLOUR['border_risky']};font-weight:700;">[!] RISKY</span>
                    &nbsp;— Flagged by ML Model
                </div>
                <div>
                    <span style="color:{COLOUR['border_safe']};font-weight:700;">[OK] SAFE</span>
                    &nbsp;— High confidence safe
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        st.markdown("---")
        st.markdown(f"### Proposed by: {TEAM_NAME}")
        for member in TEAM_MEMBERS:
            st.markdown(f"**{member['name']}**  \n<small>{member['urn']}</small>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(SIDEBAR_DISCLAIMER)

    st.markdown(
        f"""
        <div class="hero-banner">
            <h1 class="hero-title">{APP_TITLE}</h1>
            <p class="hero-subtitle">{APP_SUBTITLE}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Upload Contract Document (PDF, TXT)",
        type=["pdf", "txt"],
        help="Drag and drop your contract here. Limit 200MB.",
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        if st.session_state.get("last_analyzed_file") != uploaded_file.name:
            st.session_state.agent_report = None
            st.session_state.last_analyzed_file = uploaded_file.name

        with st.status("Analyzing document...", expanded=False) as status:
            st.write("Extracting text...")
            raw_text = extract_text_from_upload(uploaded_file)
            
            st.write("Segmenting clauses...")
            clauses = segment_document(raw_text)
            
            st.write("Running risk classification...")
            analyzed_clauses = analyze_clauses(clauses)
            
            stats = compute_summary_stats(analyzed_clauses)
            file_meta = get_file_metadata(uploaded_file)
            
            status.update(label="Risk Identification Complete", state="complete", expanded=False)

        _render_results(analyzed_clauses, stats, file_meta, raw_text, show_safe)
    else:
        st.info("Please upload a contract document to begin the analysis.")

def _render_results(analyzed_clauses, stats, meta, text, show_safe):
    st.markdown("### Analysis Dashboard")
    render_summary_metrics(stats)

    tab_audit, tab_ai = st.tabs(["Clause-Level Audit", "AI Deep Analysis"])

    with tab_audit:
        pdf_bytes = generate_pdf_report(analyzed_clauses, stats, meta)
        st.download_button(
            label="Download Full Assessment (PDF)",
            data=pdf_bytes,
            file_name=f"Risk_Report_{meta['name'].split('.')[0]}.pdf",
            mime="application/pdf",
        )
        render_clause_list(analyzed_clauses, show_safe)

    with tab_ai:
        st.markdown("### AI Deep Analysis")
        st.markdown(
            "This section uses an autonomous **Legal Agent** to perform semantic reasoning "
            "on flagged risky clauses and provide mitigation strategies."
        )

        risky_clauses = [c for c in analyzed_clauses if c["label"] == "Risky"]
        
        if not risky_clauses:
            st.success("No risky clauses identified for deep analysis.")
        else:
            if st.button("Run AI Deep Analysis", type="primary", use_container_width=True):
                agent = LegalAgent()
                if not agent.llm.is_available:
                    st.error("Groq API key not configured. Please add it to secrets.")
                else:
                    status_container = st.empty()
                    def update_status(state: AgentState):
                        status_container.info(f"⏳ **Agent Status**: {state.value}...")
                    
                    agent.state_callback = update_status
                    
                    with st.spinner("AI Agent is reasoning..."):
                        report = agent.generate_final_report(risky_clauses)
                        if report is None or not report.get("clause_assessments"):
                            st.error(f"Analysis failed. Error: {agent.last_error}")
                            st.session_state.agent_report = None
                        else:
                            st.session_state.agent_report = report
                    
                    status_container.empty()

            if st.session_state.agent_report:
                report = st.session_state.agent_report
                st.markdown("---")
                
                sum_col, disc_col = st.columns([2, 1])
                with sum_col:
                    st.info(report.get("contract_summary", "No summary available."))
                with disc_col:
                    st.warning(report.get("legal_disclaimer", "No disclaimer available."))

                st.markdown("#### Detailed Clause Assessments")
                for assessment in report.get("clause_assessments", []):
                    with st.expander(f"Assessment: {assessment.get('topic', 'Clause')}", expanded=True):
                        col_risk, col_mit = st.columns([1, 2])
                        with col_risk:
                            sev = assessment.get('risk_severity', 'Low')
                            st.markdown(f"**Severity**: {sev}")
                            st.write(assessment.get('explanation', ""))
                        with col_mit:
                            st.markdown("**Mitigation Strategy**")
                            st.write(assessment.get('mitigation', ""))

    # Footer
    st.markdown(
        f"""
        <div style="text-align:center;padding:40px 0 20px;color:{COLOUR['text_secondary']};font-size:12px;">
            Legal Contract Risk Analyzer |
            Milestone 2 Agentic Edition |
            Not legal advice
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    main()
