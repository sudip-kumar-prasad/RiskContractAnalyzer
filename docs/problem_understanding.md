# Problem Understanding & Legal Use-Case Description

## 1. Background

Legal contracts form the backbone of every commercial transaction, employment relationship, and service engagement. Organizations routinely handle hundreds—sometimes thousands—of contracts per quarter, each containing dozens of clauses that define rights, obligations, penalties, and risks for every party involved.

Traditionally, reviewing these contracts is a **manual, time-intensive process** carried out by legal professionals who must read every clause, identify problematic language, and flag potential risks. This approach suffers from several fundamental limitations:

| Challenge | Impact |
|---|---|
| **Volume** | Legal teams cannot keep pace with the growing number of contracts in mid-to-large enterprises |
| **Fatigue & Oversight** | Human reviewers inevitably miss risky clauses in lengthy documents, especially under time pressure |
| **Inconsistency** | Different reviewers may apply differing standards to the same clause, leading to uneven risk assessment |
| **Cost** | Senior legal counsel is expensive; spending billable hours on first-pass screening is economically inefficient |
| **Turnaround Time** | Slow review cycles delay deal closures and business operations |

---

## 2. Why Automate Contract Risk Detection?

An **ML-based Contract Risk Classification** system addresses each of the above challenges by applying Natural Language Processing (NLP) and supervised machine-learning techniques to:

1. **Parse contract documents automatically** — extracting raw text from PDF and TXT uploads without manual transcription.
2. **Segment the document into individual clauses** — using rule-based heuristics and NLP segmentation to isolate each contractual obligation or provision.
3. **Classify every clause as *Risky* or *Safe*** — leveraging a trained classifier (Logistic Regression / Decision Tree) built on TF-IDF feature vectors derived from the clause text.
4. **Present actionable results** — providing a clear, colour-coded dashboard that highlights risky clauses, their risk categories (e.g., Liability, Termination, IP, Financial), and confidence scores.

### Key Value Propositions

- **Speed**: A contract that takes a human reviewer 30–60 minutes can be scanned in under 10 seconds.
- **Consistency**: Every clause is evaluated against the same trained model and keyword library, eliminating subjective variation.
- **Scalability**: The system handles one contract or one thousand with equal ease.
- **Cost Reduction**: First-pass risk screening is automated; human lawyers focus only on flagged clauses, reducing billable time by up to 70%.
- **Early Warning**: Business teams can upload draft contracts *before* legal review and receive an immediate risk snapshot.

---

## 3. Legal Use-Case Description

### 3.1 Target Users

| User Role | How They Benefit |
|---|---|
| **In-house Legal Counsel** | Rapid triage of incoming contracts; focus review time on high-risk clauses |
| **Contract Managers** | Track risk exposure across a portfolio of vendor/client agreements |
| **Procurement Teams** | Evaluate supplier contracts before signing, without waiting for legal queue |
| **Startup Founders / SMEs** | Affordable first-pass legal review when access to full-time counsel is limited |
| **Legal-tech Researchers** | Benchmark and improve NLP models for contract understanding |

### 3.2 Applicable Contract Types

The system is designed to work with general-purpose business contracts, including but not limited to:

- **Service-Level Agreements (SLAs)**
- **Non-Disclosure Agreements (NDAs)**
- **Employment Contracts**
- **Vendor / Supplier Agreements**
- **Software Licensing Agreements**
- **Lease Agreements**

### 3.3 Risk Categories Detected

The classifier is trained and configured to flag clauses across the following risk categories:

| Category | Example Triggers |
|---|---|
| **Indemnity** | "indemnify", "hold harmless" |
| **Liability** | "unlimited liability", "gross negligence" |
| **Termination** | "terminate without notice", "forfeiture" |
| **Penalties** | "liquidated damages", "penalty" |
| **Dispute Resolution** | "binding arbitration", "waiver" |
| **IP / Rights** | "irrevocable", "perpetual license", "transfer of rights" |
| **Confidentiality** | "trade secret", "non-disclosure" |
| **Financial** | "compound interest", "late payment surcharge" |
| **Non-Compete** | "non-solicitation", "restraint of trade" |

### 3.4 Workflow

```
Legal / Business User
        │
        ▼
  Upload Contract (PDF / TXT)
        │
        ▼
  System extracts and segments clauses
        │
        ▼
  ML model classifies each clause
        │
        ▼
  Dashboard displays Risky vs Safe clauses
        │
        ▼
  User reviews flagged clauses with legal counsel
```

---

## 4. Limitations & Disclaimer

- This system is a **decision-support tool**, not a replacement for qualified legal advice.
- The classifier's accuracy is bounded by the quality and diversity of training data.
- Contracts in languages other than English are not currently supported.
- Highly domain-specific contracts (e.g., maritime law, pharmaceutical IP) may require additional fine-tuning.

> **Disclaimer:** This tool is intended for educational and demonstration purposes as part of a university project. It does not constitute legal advice. Always consult a qualified legal professional before acting on any contract analysis.
