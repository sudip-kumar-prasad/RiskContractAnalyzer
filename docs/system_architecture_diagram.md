# System Architecture Diagram — NLP Pipeline

This document provides a text-based representation of the system architecture that can be easily recreated in **Draw.io** (diagrams.net). The pipeline follows a linear flow from document upload to UI display.

---

## High-Level Pipeline Flow

```
┌─────────────────────┐
│                     │
│   Document Upload   │
│   (PDF / TXT)       │
│                     │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│                     │
│   Text Extraction   │
│   (PyPDF2 / Raw)    │
│                     │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│                     │
│  Clause Segmentation│
│  (Regex Heuristics) │
│                     │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│                     │
│  TF-IDF             │
│  Vectorization      │
│  (scikit-learn)     │
│                     │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│                     │
│  Classifier Model   │
│  (LogReg / DTree)   │
│                     │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│                     │
│   UI Display        │
│   (Streamlit)       │
│                     │
└─────────────────────┘
```

---

## Draw.io Recreation Guide

To recreate this diagram in Draw.io, follow these steps:

### Step 1 — Create Six Rounded Rectangle Shapes

Create the following boxes (use **Rounded Rectangle** shape), stacking them vertically with equal spacing:

| Box # | Label | Suggested Colour |
|-------|-------|-----------------|
| 1 | **Document Upload** (PDF / TXT) | Light Blue (`#DAE8FC`) |
| 2 | **Text Extraction** (PyPDF2 / Raw Read) | Light Green (`#D5E8D4`) |
| 3 | **Clause Segmentation** (Regex Heuristics) | Light Yellow (`#FFF2CC`) |
| 4 | **TF-IDF Vectorization** (scikit-learn) | Light Orange (`#FFE6CC`) |
| 5 | **Classifier Model** (Logistic Regression / Decision Tree) | Light Purple (`#E1D5E7`) |
| 6 | **UI Display** (Streamlit Dashboard) | Light Red (`#F8CECC`) |

### Step 2 — Connect With Arrows

Draw **downward arrows** between each consecutive box:

```
Box 1  ──▶  Box 2  ──▶  Box 3  ──▶  Box 4  ──▶  Box 5  ──▶  Box 6
```

Use solid arrows with the default style. Optionally, add labels on the arrows:

| Arrow | Label |
|-------|-------|
| 1 → 2 | `Raw file bytes` |
| 2 → 3 | `Plain text string` |
| 3 → 4 | `List of clause dicts` |
| 4 → 5 | `TF-IDF sparse matrix` |
| 5 → 6 | `Classified clauses + stats` |

### Step 3 — Add Annotations (Optional)

- **Left sidebar**: Add a text box listing the Python modules at each stage:
  - `utils/file_handler.py`
  - `utils/clause_segmenter.py`
  - `src/model_training/feature_extractor.py`
  - `src/model_training/trainer.py`
  - `app.py` + `components/result_display.py`

- **Title**: Add a title text at the top: *"ML-Based Contract Risk Classification — NLP Pipeline"*

---

## Detailed Component Breakdown

```
┌──────────────────────────────────────────────────────────────────────┐
│                        SYSTEM ARCHITECTURE                          │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ┌──────────────┐                                                   │
│   │  USER LAYER  │                                                   │
│   │              │                                                   │
│   │  Browser     │◄──── http://localhost:8501                        │
│   └──────┬───────┘                                                   │
│          │                                                           │
│          ▼                                                           │
│   ┌──────────────────────────────────────────────────┐               │
│   │              PRESENTATION LAYER                   │               │
│   │                                                   │               │
│   │  ┌──────────┐  ┌─────────────┐  ┌────────────┐  │               │
│   │  │ Hero     │  │ File Upload │  │ KPI Tiles  │  │               │
│   │  │ Header   │  │ Widget      │  │ Dashboard  │  │               │
│   │  └──────────┘  └──────┬──────┘  └────────────┘  │               │
│   │                       │          ┌────────────┐  │               │
│   │                       │          │ Clause     │  │               │
│   │                       │          │ Cards      │  │               │
│   │                       │          └────────────┘  │               │
│   │  Modules: app.py, components/result_display.py   │               │
│   └───────────────────────┬──────────────────────────┘               │
│                           │                                          │
│                           ▼                                          │
│   ┌──────────────────────────────────────────────────┐               │
│   │              PROCESSING LAYER                     │               │
│   │                                                   │               │
│   │  ┌────────────────┐    ┌──────────────────────┐  │               │
│   │  │ Text Extraction│───▶│ Clause Segmentation  │  │               │
│   │  │ file_handler.py│    │ clause_segmenter.py  │  │               │
│   │  └────────────────┘    └──────────┬───────────┘  │               │
│   │                                   │              │               │
│   │                                   ▼              │               │
│   │                        ┌──────────────────────┐  │               │
│   │                        │ Risk Prediction      │  │               │
│   │                        │ risk_predictor.py    │  │               │
│   │                        └──────────────────────┘  │               │
│   └──────────────────────────────────────────────────┘               │
│                                                                      │
│   ┌──────────────────────────────────────────────────┐               │
│   │              ML TRAINING LAYER                    │               │
│   │              (Offline / Batch)                    │               │
│   │                                                   │               │
│   │  ┌────────────┐  ┌──────────────┐  ┌──────────┐ │               │
│   │  │ Data       │─▶│ TF-IDF       │─▶│ Model    │ │               │
│   │  │ Loader     │  │ Vectorizer   │  │ Trainer  │ │               │
│   │  └────────────┘  └──────────────┘  └────┬─────┘ │               │
│   │                                         │       │               │
│   │                  ┌──────────────┐  ┌────▼─────┐ │               │
│   │                  │ Model Saver  │◄─│Evaluator │ │               │
│   │                  │ (.pkl files) │  │(F1, Acc) │ │               │
│   │                  └──────────────┘  └──────────┘ │               │
│   │                                                   │               │
│   │  Modules: src/model_training/*                    │               │
│   └──────────────────────────────────────────────────┘               │
│                                                                      │
│   ┌──────────────────────────────────────────────────┐               │
│   │              CONFIGURATION LAYER                  │               │
│   │                                                   │               │
│   │  ┌──────────────────┐  ┌───────────────────────┐ │               │
│   │  │ app_config.py    │  │ .streamlit/config.toml│ │               │
│   │  │ (keywords, theme │  │ (Streamlit theme)     │ │               │
│   │  │  thresholds, UI) │  │                       │ │               │
│   │  └──────────────────┘  └───────────────────────┘ │               │
│   └──────────────────────────────────────────────────┘               │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Technology Stack at Each Stage

| Pipeline Stage | Technology | Purpose |
|---|---|---|
| Document Upload | Streamlit `st.file_uploader` | Accept PDF/TXT files from the user |
| Text Extraction | PyPDF2, Python `open()` | Extract raw text from uploaded documents |
| Clause Segmentation | Python `re` (regex) | Split text into individual contractual clauses |
| TF-IDF Vectorization | scikit-learn `TfidfVectorizer` | Convert clause text into numerical feature vectors |
| Classifier Model | scikit-learn `LogisticRegression`, `DecisionTreeClassifier` | Classify each clause as Risky or Safe |
| Model Evaluation | scikit-learn `classification_report`, `f1_score` | Evaluate model performance and select the best model |
| UI Display | Streamlit, custom CSS | Render the interactive dashboard with risk analysis results |

---

## Data Flow Summary (for Draw.io Flowchart)

```
User uploads PDF/TXT
        │
        ▼
  ┌─────────────┐
  │ PyPDF2 /    │──── Extracts text from file
  │ Raw Read    │
  └──────┬──────┘
         │  plain text (str)
         ▼
  ┌─────────────┐
  │ Regex-based │──── Splits into clause dicts
  │ Segmenter   │     [{clause_id, text}, ...]
  └──────┬──────┘
         │  list[dict]
         ▼
  ┌─────────────┐
  │ TF-IDF      │──── Converts text to feature vectors
  │ Vectorizer  │     max_features=10000, ngrams=(1,2)
  └──────┬──────┘
         │  sparse matrix
         ▼
  ┌─────────────┐
  │ Classifier  │──── Predicts Risky (1) or Safe (0)
  │ (LR / DT)   │     + confidence scores
  └──────┬──────┘
         │  classified clauses
         ▼
  ┌─────────────┐
  │ Streamlit   │──── KPI tiles, clause cards,
  │ Dashboard   │     filter tabs, confidence bars
  └─────────────┘
```
