from .skills import extract_skills

ROLE_SKILLS = {
    "AI/ML Engineer": {"python","machine learning","deep learning","numpy","pandas","scikit-learn","pytorch","tensorflow"},
    "Data Scientist": {"python","sql","statistics","pandas","numpy","machine learning","data analysis"},
    "Data Analyst": {"sql","excel","power bi","tableau","python","data analysis"},
    "Backend Developer": {"python","java","node.js","sql","rest api","docker","git"},
    "Frontend Developer": {"html","css","javascript","react","typescript","git"},
    "Full Stack Developer": {"html","css","javascript","react","node.js","sql","rest api","git"},
    "Cloud/DevOps Engineer": {"linux","docker","kubernetes","aws","azure","gcp","git"},
    "NLP Engineer": {"python","nlp","natural language processing","transformers","machine learning","pytorch"},
}

def recommend_roles(text, limit=5):
    skills = set(extract_skills(text))
    scores = []
    for role, required in ROLE_SKILLS.items():
        score = round(100 * len(skills & required) / max(1, len(required)), 2)
        scores.append((role, score))
    return sorted(scores, key=lambda x: x[1], reverse=True)[:limit]
