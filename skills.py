# Curated technical-skill ontology for the prototype.
SKILLS = {
    "python","java","c","c++","javascript","typescript","sql","mysql","postgresql",
    "mongodb","html","css","react","angular","node.js","express","flask","django",
    "fastapi","streamlit","git","github","docker","kubernetes","aws","azure","gcp",
    "linux","machine learning","deep learning","nlp","natural language processing",
    "computer vision","tensorflow","pytorch","scikit-learn","pandas","numpy",
    "matplotlib","power bi","tableau","excel","data analysis","data science",
    "rest api","graphql","microservices","spring boot","figma","cybersecurity",
    "networking","data structures","algorithms","oop","object oriented programming",
    "statistics","generative ai","llm","langchain","transformers"
}

ALIASES = {
    "natural language processing": "nlp",
    "object oriented programming": "oop",
    "machine-learning": "machine learning",
    "deep-learning": "deep learning",
    "scikit learn": "scikit-learn",
    "nodejs": "node.js",
    "powerbi": "power bi",
}

def normalize(text: str) -> str:
    t = text.lower()
    for alias, canonical in ALIASES.items():
        t = t.replace(alias, canonical)
    return t

def extract_skills(text: str):
    t = normalize(text)
    found = set()
    for skill in SKILLS:
        if skill in t:
            found.add(skill)
    return sorted(found)
