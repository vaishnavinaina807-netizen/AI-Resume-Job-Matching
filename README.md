# 🤖 AI Resume & Job Matching

An AI-powered resume intelligence platform that compares a candidate's resume with a target job description using NLP, semantic similarity, skill extraction, ATS-style keyword analysis, skill-gap detection and career-role recommendations.

## Core capabilities

- PDF, DOCX and TXT resume parsing
- Curated technical skill ontology
- Transformer-based semantic similarity (`all-MiniLM-L6-v2`)
- ATS keyword coverage analysis
- Matched and missing skill detection
- Explainable composite scoring
- Career-role recommendations
- Streamlit dashboard

## Scoring design

**Overall Match = 50% semantic similarity + 35% skill coverage + 15% keyword coverage**

**ATS Score = 60% skill coverage + 40% keyword coverage**

These are project-defined indicators, not hiring decisions.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

Open the local Streamlit URL shown in the terminal.

## Project structure

```text
AI-Resume-Job-Matching/
├── app.py
├── requirements.txt
├── README.md
├── src/
│   ├── matcher.py
│   ├── parser.py
│   ├── recommender.py
│   ├── skills.py
│   └── ui_helpers.py
└── tests/
```

## Important

The semantic model is downloaded by `sentence-transformers` on first use. If it is unavailable, the application uses a lightweight token-similarity fallback.

For real-world recruitment, scoring should be validated on representative data and should not be used as the sole basis for employment decisions.
