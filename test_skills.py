from src.skills import extract_skills

def test_skill_extraction():
    skills = extract_skills("Python, SQL and Machine Learning")
    assert "python" in skills
    assert "sql" in skills
    assert "machine learning" in skills
