#  Legal Contract Risk Analyzer

> AI-powered, clause-level risk detection for legal documents — built with Streamlit.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29%2B-red?logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Overview

The **Legal Contract Risk Analyzer** is a single-page Streamlit web application that allows users to upload PDF or TXT contract documents, automatically splits them into individual clauses, and predicts which clauses carry legal risk using a rule-based NLP pipeline.

### Key Features

| Feature | Description |
|---|---|
| 📄 **File Upload** | Supports `.pdf` and `.txt` files up to any size |
| ✂️ **Clause Segmentation** | Automatically splits contract text into logical clauses |
| 🔍 **Risk Detection** | Flags clauses containing risky legal keywords |
| 📊 **KPI Dashboard** | Summary tiles: total / risky / safe clause counts + risk % |
| 🎨 **Premium Dark UI** | Gradient header, styled cards, confidence bars, filter tabs |
| 🏷️ **Risk Categories** | Identifies category of risk (Liability, Termination, IP, etc.) |

---

## Project Architecture

```
RiskContractAnalyzer/
├── app.py                        # ← Main Streamlit entry point
├── app_config.py                 # UI constants, risk keywords, colour palette
├── requirements.txt
├── .streamlit/
│   └── config.toml               # Custom Streamlit theme
├── components/
│   └── result_display.py         # Styled clause cards & KPI tiles
├── utils/
│   ├── file_handler.py           # PDF/TXT text extraction (UploadedFile)
│   ├── clause_segmenter.py       # Clause segmentation wrapper
│   └── risk_predictor.py         # Keyword-based risk prediction engine
├── src/
│   ├── data_preprocessing/       # Core NLP modules (segmenter, loader)
│   └── model_training/           # ML training pipeline (LogReg, DT)
├── data/
│   └── sample_contract.txt       # Sample contract for quick testing
└── train_classifier.py           # Model training entry point
```

---

## ⚡ Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/sudip-kumar-prasad/RiskContractAnalyzer.git
cd RiskContractAnalyzer
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
# venv\Scripts\activate       # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

Then open **http://localhost:8501** in your browser.

---

## 🧪 Testing with Sample Data

A sample contract is provided in `data/sample_contract.txt`. Upload it directly in the app to see the analyzer in action.

---

## 🔬 How the Pipeline Works

```
┌─────────────┐    ┌──────────────┐    ┌─────────────────┐    ┌─────────────┐
│  File Upload │ →  │ Text Extract │ →  │ Clause Segment  │ →  │ Risk Predict│
│ (PDF / TXT) │    │ (PyPDF2/str) │    │ (regex heuristic│    │  (keyword   │
└─────────────┘    └──────────────┘    │    matching)    │    │  matching)  │
                                        └─────────────────┘    └─────────────┘
```

1. **Text Extraction** — `utils/file_handler.py` reads the uploaded file into a string, handling multiple encodings
2. **Clause Segmentation** — `utils/clause_segmenter.py` splits text by double newlines and legal numbering patterns
3. **Risk Prediction** — `utils/risk_predictor.py` scans each clause for 40+ curated risky legal keywords and categories

---

## Dependencies

| Package | Purpose |
|---|---|
| `streamlit` | Web app framework |
| `PyPDF2` | PDF text extraction |
| `scikit-learn` | ML model (future integration) |
| `pandas` | Data handling |
| `joblib` | Model serialization |
| `nltk` | Text preprocessing |
| `spacy` | NLP pipeline (future) |

---

## ⚠️ Disclaimer

This tool is for **demonstration purposes only** and does not constitute legal advice. Always consult a qualified lawyer before signing any contract.


