# Input-Output Specification

This document defines the formal input-output contract for the ML-Based Contract Risk Classification system. It specifies what the system accepts, what it produces, and the data formats at each stage of the pipeline.

---

## 1. System-Level Input

### 1.1 User Input

| Parameter | Specification |
|---|---|
| **Input Type** | File upload via Streamlit web UI |
| **Accepted Formats** | `.pdf`, `.txt` |
| **Encoding** | UTF-8 (with fallback to Latin-1 for `.txt` files) |
| **Max File Size** | No hard limit (bounded by server memory) |
| **Language** | English |
| **Content** | Legal contract documents (SLAs, NDAs, employment contracts, vendor agreements, etc.) |

### 1.2 Example Input

A plain-text contract file containing clauses such as:

```
1. TERMINATION
   Either party may terminate this Agreement upon 30 days written notice
   to the other party.

2. LIABILITY
   The Contractor shall indemnify and hold harmless the Client from any
   claims arising from gross negligence or wilful misconduct.

3. PAYMENT TERMS
   Payment is due within 30 days of invoice date. Late payments will
   incur a compound interest charge of 1.5% per month.
```

---

## 2. System-Level Output

### 2.1 Per-Clause Output

For each clause extracted from the uploaded document, the system returns:

| Field | Type | Description | Example |
|---|---|---|---|
| `clause_id` | `int` | Sequential identifier (1-indexed) | `2` |
| `text` | `str` | Full text content of the clause | `"The Contractor shall indemnify..."` |
| `label` | `str` | Risk classification result | `"Risky"` or `"Safe"` |
| `confidence` | `float` | Model confidence score (0.0 – 1.0) | `0.91` |
| `matched_keywords` | `list[str]` | Risk keywords found in clause | `["indemnify", "gross negligence"]` |
| `categories` | `list[str]` | Risk categories triggered | `["Indemnity", "Liability"]` |

### 2.2 Summary Statistics Output

The system also computes aggregate metrics displayed in a KPI dashboard:

| Field | Type | Description | Example |
|---|---|---|---|
| `total` | `int` | Total number of clauses extracted | `12` |
| `risky_count` | `int` | Number of clauses classified as Risky | `5` |
| `safe_count` | `int` | Number of clauses classified as Safe | `7` |
| `risk_percentage` | `float` | Percentage of risky clauses | `41.7` |

### 2.3 UI Display Output

The Streamlit dashboard renders the following visual components:

| Component | Description |
|---|---|
| **KPI Tiles** | Summary cards showing total, risky, safe counts, and risk percentage |
| **Clause Cards** | Colour-coded cards (red = Risky, green = Safe) with confidence bars |
| **Risk Category Badges** | Tags indicating the risk category (Liability, Termination, IP, etc.) |
| **Filter Tabs** | Tabs to view All / Risky Only / Safe Only clauses |

---

## 3. Internal Pipeline Data Flow

The following table documents the intermediate data structures passed between pipeline stages:

### Stage 1: Text Extraction

| | Specification |
|---|---|
| **Input** | `UploadedFile` object (Streamlit file uploader) |
| **Output** | `str` — raw text content of the document |
| **Module** | `utils/file_handler.py` |

### Stage 2: Clause Segmentation

| | Specification |
|---|---|
| **Input** | `str` — raw document text |
| **Output** | `list[dict]` — each dict contains `{"clause_id": int, "text": str}` |
| **Module** | `utils/clause_segmenter.py` |
| **Logic** | Splits on double newlines and legal numbering patterns (regex-based) |

### Stage 3: Feature Extraction (ML Pipeline)

| | Specification |
|---|---|
| **Input** | `list[str]` — clause text strings |
| **Output** | Sparse TF-IDF matrix (`scipy.sparse.csr_matrix`) |
| **Module** | `src/model_training/feature_extractor.py` |
| **Config** | `max_features=10,000`, `ngram_range=(1,2)`, `sublinear_tf=True` |

### Stage 4: Classification

| | Specification |
|---|---|
| **Input** | TF-IDF feature matrix |
| **Output** | Binary labels (`1` = Risky, `0` = Safe) with probability scores |
| **Module** | `src/model_training/trainer.py` |
| **Models** | Logistic Regression, Decision Tree (best model selected by F1-score) |

### Stage 5: Risk Prediction (Runtime)

| | Specification |
|---|---|
| **Input** | `list[dict]` — clause dicts from Stage 2 |
| **Output** | `list[dict]` — clause dicts augmented with `label`, `confidence`, `matched_keywords`, `categories` |
| **Module** | `utils/risk_predictor.py` |

### Stage 6: UI Rendering

| | Specification |
|---|---|
| **Input** | Analyzed clause list + summary statistics dict |
| **Output** | Rendered Streamlit dashboard (HTML/CSS via `st.markdown`) |
| **Module** | `components/result_display.py`, `app.py` |

---

## 4. Data Format Summary

```
Input:   .pdf / .txt file
           │
           ▼
Stage 1: str (raw text)
           │
           ▼
Stage 2: [ {"clause_id": 1, "text": "..."}, {"clause_id": 2, "text": "..."}, ... ]
           │
           ▼
Stage 3: scipy.sparse.csr_matrix (TF-IDF vectors)
           │
           ▼
Stage 4: [1, 0, 1, 0, ...] (binary labels) + [0.91, 0.88, ...] (probabilities)
           │
           ▼
Stage 5: [ {"clause_id": 1, "text": "...", "label": "Risky", "confidence": 0.91,
             "matched_keywords": [...], "categories": [...]}, ... ]
           │
           ▼
Stage 6: Streamlit Dashboard (KPI tiles, clause cards, filter tabs)
```

---

## 5. Error Handling

| Scenario | System Response |
|---|---|
| Unsupported file format | Error message displayed; upload rejected |
| Empty document | Warning: "No text could be extracted" |
| PDF with no extractable text (scanned image) | Warning: "No text found — file may be image-based" |
| Encoding error (`.txt`) | Automatic fallback from UTF-8 to Latin-1 |
| Zero clauses after segmentation | Warning: "No clauses could be identified" |
