import re
from .skills import extract_skills

class ResumeMatcher:
    def __init__(self):
        self._model = None
        try:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception:
            self._model = None

    def semantic_similarity(self, a, b):
        if self._model is not None:
            from sentence_transformers.util import cos_sim
            va = self._model.encode(a, convert_to_tensor=True)
            vb = self._model.encode(b, convert_to_tensor=True)
            score = float(cos_sim(va, vb).item())
            return max(0, min(100, round((score + 1) * 50, 2)))

        # Dependency-light fallback: token Jaccard similarity.
        wa = set(re.findall(r"[a-zA-Z][a-zA-Z0-9+#.-]{2,}", a.lower()))
        wb = set(re.findall(r"[a-zA-Z][a-zA-Z0-9+#.-]{2,}", b.lower()))
        if not wa or not wb:
            return 0.0
        return round(100 * len(wa & wb) / len(wa | wb), 2)

    def analyze(self, resume, job):
        resume_skills = extract_skills(resume)
        job_skills = extract_skills(job)
        rset, jset = set(resume_skills), set(job_skills)

        matched = sorted(rset & jset)
        missing = sorted(jset - rset)

        skill_score = round(100 * len(matched) / max(1, len(jset)), 2)
        semantic = self.semantic_similarity(resume, job)

        job_keywords = set(re.findall(r"\b[a-zA-Z][a-zA-Z0-9+#.-]{2,}\b", job.lower()))
        resume_words = set(re.findall(r"\b[a-zA-Z][a-zA-Z0-9+#.-]{2,}\b", resume.lower()))
        coverage = round(100 * len(job_keywords & resume_words) / max(1, len(job_keywords)), 2)

        ats = round(0.60 * skill_score + 0.40 * coverage, 2)
        overall = round(0.50 * semantic + 0.35 * skill_score + 0.15 * coverage, 2)

        feedback = []
        if coverage < 50:
            feedback.append("Low keyword coverage: mirror relevant job terminology naturally in the resume.")
        elif coverage < 75:
            feedback.append("Moderate keyword coverage: add missing job-relevant terminology where truthful.")
        else:
            feedback.append("Strong keyword coverage for the supplied job description.")

        if missing:
            feedback.append("Review the missing skills and add only skills you genuinely possess or can demonstrate.")
        else:
            feedback.append("The detected skill set covers all skills found in the current job-description ontology.")

        recommendations = []
        if missing:
            recommendations.append("Prioritize these skill gaps: " + ", ".join(missing[:8]))
        recommendations.append("Add measurable outcomes to experience/project bullets.")
        recommendations.append("Use clear section headings: Summary, Skills, Projects, Experience, Education.")
        recommendations.append("Keep terminology consistent with the target role without keyword stuffing.")

        return {
            "overall_score": overall,
            "semantic_score": semantic,
            "skill_score": skill_score,
            "ats_score": ats,
            "keyword_coverage": coverage,
            "resume_skills": resume_skills,
            "job_skills": job_skills,
            "matched_skills": matched,
            "missing_skills": missing,
            "ats_feedback": feedback,
            "recommendations": recommendations,
        }
