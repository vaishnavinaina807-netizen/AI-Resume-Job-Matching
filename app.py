import streamlit as st
from pathlib import Path
from src.parser import extract_resume_text
from src.matcher import ResumeMatcher
from src.recommender import recommend_roles
from src.ui_helpers import render_metric_card

st.set_page_config(page_title="AI Resume & Job Matching", page_icon="🤖", layout="wide")

st.markdown("""
<style>
.main-title{font-size:42px;font-weight:800;margin-bottom:0}
.sub{color:#7f8c8d;font-size:17px}
.card{padding:18px;border:1px solid #ddd;border-radius:14px;margin:8px 0}
.skill{display:inline-block;padding:6px 10px;margin:4px;border-radius:18px;background:#eef2ff}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🤖 AI Resume & Job Matching</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Semantic resume intelligence • ATS analysis • skill-gap detection • role recommendations</div>', unsafe_allow_html=True)

@st.cache_resource
def get_matcher():
    return ResumeMatcher()

matcher = get_matcher()

left, right = st.columns(2)
with left:
    resume_file = st.file_uploader("📄 Upload Resume", type=["pdf", "docx", "txt"])
with right:
    job_text = st.text_area("💼 Paste Job Description", height=250,
        placeholder="Paste the complete job description here...")

if resume_file and job_text.strip():
    with st.spinner("Analyzing resume with NLP + semantic matching..."):
        resume_text = extract_resume_text(resume_file)
        result = matcher.analyze(resume_text, job_text)

    st.divider()
    st.subheader("📊 Match Intelligence")

    c1, c2, c3, c4 = st.columns(4)
    render_metric_card(c1, "Overall Match", f"{result['overall_score']}%")
    render_metric_card(c2, "Semantic Similarity", f"{result['semantic_score']}%")
    render_metric_card(c3, "Skill Match", f"{result['skill_score']}%")
    render_metric_card(c4, "ATS Score", f"{result['ats_score']}%")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["🎯 Skill Analysis", "🔍 ATS Insights", "💡 Recommendations", "🧠 Explainability"]
    )

    with tab1:
        st.write("### Matched Skills")
        matched = result["matched_skills"]
        st.markdown(" ".join(f'<span class="skill">✓ {s}</span>' for s in matched),
                    unsafe_allow_html=True)
        st.write("### Missing Skills")
        missing = result["missing_skills"]
        if missing:
            st.markdown(" ".join(f'<span class="skill">＋ {s}</span>' for s in missing),
                        unsafe_allow_html=True)
        else:
            st.success("No major skill gaps detected from the current skill dictionary.")

    with tab2:
        st.write("### ATS Keyword Coverage")
        st.progress(result["keyword_coverage"] / 100)
        st.write(f"Keyword coverage: **{result['keyword_coverage']}%**")
        for item in result["ats_feedback"]:
            st.write("•", item)

    with tab3:
        st.write("### Recommended Improvements")
        for item in result["recommendations"]:
            st.write("•", item)

        st.write("### Suggested Career Roles")
        for role, score in recommend_roles(resume_text):
            st.write(f"**{role}** — {score}% profile similarity")

    with tab4:
        st.write("### Why this score?")
        st.write(
            f"The system combines semantic similarity ({result['semantic_score']}%), "
            f"required-skill coverage ({result['skill_score']}%), and ATS keyword coverage "
            f"({result['keyword_coverage']}%) into an overall score."
        )
        st.write("### Detected Resume Signals")
        st.json({
            "skills_detected": result["resume_skills"],
            "job_skills_detected": result["job_skills"],
            "matched": result["matched_skills"],
            "missing": result["missing_skills"],
        })
else:
    st.info("Upload a resume and paste a job description to start the analysis.")
    st.markdown("""
### 🚀 Pro Features
- PDF/DOCX/TXT resume parsing
- NLP skill extraction
- Semantic similarity using transformer embeddings
- ATS keyword analysis
- Skill-gap detection
- Explainable scoring
- Career-role recommendations
- Clean Streamlit dashboard
""")
