# 🛡️ FairGuard-Rank

**Smart Recruitment AI Platform**

FairGuard-Rank is an intelligent, fair, and secure recruitment platform built with Streamlit. It automates resume screening while actively mitigating AI bias, explaining its decisions, and defending against prompt injection attacks. 

## ✨ Features

- **📂 Upload & Ingest**
  - Batch upload resumes (PDF, DOCX, TXT).
  - Parse job descriptions and dynamically extract required skills.
  - Dashboard metrics tracking ingested candidates and security clearances.
  
- **🛡️ Security & Integrity Shield**
  - Detects and flags prompt injection and keyword stuffing attacks from adversarial resumes.
  - Generates sanitized text previews to ensure safe downstream processing.

- **📊 Rankings & Skill Gap Analysis**
  - Ranks candidates based on semantic match to the job description.
  - Identifies matched, missing, and additional skills.
  - **Explainable AI (XAI):** Uses SHAP visual attributions to explain *why* a candidate received their score (top positive drivers and missing skill penalties).

- **⚖️ Fairness & Compliance Center**
  - **Demographic Fairness Audit:** Measures Statistical Parity Difference (SPD) and Disparate Impact (DI).
  - **Debiasing:** Mitigates demographic disparity using reweighing algorithms to achieve fairness thresholds.
  - **AI Self-Preference Audit:** Detects if the system exhibits a bias toward LLM-generated resumes over human-written ones.

- **✅ Decision Console**
  - Human-in-the-loop compliance logging.
  - Track recruiter decisions (Approve, Reject, Flag for Interview) directly within the app.

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- [Streamlit](https://streamlit.io/)
- Pandas

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/FairGuard-Rank.git
   cd FairGuard-Rank
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(Ensure you have the required NLP, SHAP, and fairness packages installed as per your environment setup.)*

3. Run the application:
   ```bash
   streamlit run fairguard_rank/app.py
   ```

## 🏗️ Project Structure
- `app.py`: Main Streamlit application entry point.
- `style.css`: Custom premium CSS styling.
- `modules/`:
  - `defense_scanner.py`: Sanitizes text and detects injections.
  - `extractor.py`: Extracts skills and entities.
  - `matcher.py`: Computes similarity and ranks candidates.
  - `xai_engine.py`: SHAP explanation and skill gap analysis.
  - `fairness.py`: Fairness assessment and bias mitigation (reweighing, AI self-preference).
  - `ingestion.py`: Document parsing (PDF, DOCX, TXT).

## 📄 License
This project is licensed under the MIT License.
