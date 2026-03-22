"""
CareerMind AI - Module Test Script
===================================
Tests each utility module independently without requiring AI models.
Run this to verify all components are working correctly.

Usage:
    python test_modules.py
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def test_parser():
    """Test the parser module (skill extraction, not PDF parsing)."""
    print("\n" + "="*60)
    print("Testing: utils/parser.py")
    print("="*60)

    from utils.parser import extract_skills, estimate_experience, ALL_SKILLS

    # Test skill vocabulary
    print(f"\n[OK] Skills vocabulary loaded: {len(ALL_SKILLS)} skills")

    # Test skill extraction
    sample_text = """
    I am a software engineer with expertise in Python, TensorFlow, and AWS.
    I have worked with Docker, Kubernetes, and implemented machine learning models.
    Proficient in SQL, Pandas, and data visualization with Matplotlib.
    """

    skills = extract_skills(sample_text)
    print(f"[OK] Extracted skills: {skills}")
    assert len(skills) > 5, "Should extract multiple skills"
    assert "python" in skills, "Should find Python"
    assert "tensorflow" in skills, "Should find TensorFlow"
    print(f"[OK] Skill extraction passed ({len(skills)} skills found)")

    # Test experience estimation
    exp_text = """
    Work Experience:
    Senior Engineer at Company A (Jan 2020 - Present)
    Junior Developer at Company B (Jun 2017 - Dec 2019)
    """

    years = estimate_experience(exp_text)
    print(f"[OK] Estimated experience: {years} years")
    assert years > 0, "Should estimate positive experience"

    print("\n[PASS] parser.py - All tests passed!")
    return True


def test_skill_gap():
    """Test the skill gap analysis module."""
    print("\n" + "="*60)
    print("Testing: utils/skill_gap.py")
    print("="*60)

    from utils.skill_gap import (
        load_job_skills_map,
        get_available_roles,
        analyze_skill_gap,
        get_best_matching_roles,
        generate_learning_path
    )

    # Test job map loading
    job_map = load_job_skills_map()
    print(f"[OK] Loaded job skills map: {len(job_map)} roles")
    assert len(job_map) > 0, "Should have roles defined"

    # Test available roles
    roles = get_available_roles()
    print(f"[OK] Available roles: {roles[:5]}...")
    assert len(roles) > 0, "Should have roles available"

    # Test skill gap analysis
    test_skills = ["python", "pandas", "sql", "git", "jupyter"]
    gap = analyze_skill_gap(test_skills, "Data Scientist")

    print(f"[OK] Skill gap analysis:")
    print(f"     Match score: {gap['match_score']}")
    print(f"     Readiness: {gap['readiness_level']}")
    print(f"     Missing: {gap['missing_required'][:3]}...")

    assert "match_score" in gap, "Should include match score"
    assert "missing_required" in gap, "Should identify missing skills"

    # Test best matching roles
    matches = get_best_matching_roles(test_skills, top_n=3)
    print(f"[OK] Best matching roles:")
    for m in matches:
        print(f"     - {m['role']}: {m['match_score']*100:.0f}%")

    assert len(matches) == 3, "Should return top 3 matches"

    # Test learning path
    path = generate_learning_path(["docker", "kubernetes"])
    print(f"[OK] Learning path generated: {len(path)} items")
    assert len(path) > 0, "Should generate learning path"

    print("\n[PASS] skill_gap.py - All tests passed!")
    return True


def test_salary_predictor():
    """Test the salary predictor module."""
    print("\n" + "="*60)
    print("Testing: utils/salary_predictor.py")
    print("="*60)

    from utils.salary_predictor import SalaryPredictor, LOCATION_MULTIPLIERS

    # Test location multipliers
    print(f"[OK] Location multipliers loaded: {len(LOCATION_MULTIPLIERS)} locations")

    # Test predictor
    predictor = SalaryPredictor()
    print(f"[OK] SalaryPredictor initialized")
    print(f"     ML model available: {predictor.model_available}")

    # Test prediction
    result = predictor.predict(
        role="Machine Learning Engineer",
        experience_years=5,
        skills=["python", "pytorch", "aws", "docker"],
        location="US - San Francisco Bay Area"
    )

    print(f"[OK] Salary prediction:")
    print(f"     Predicted: ${result['predicted_salary']:,}")
    print(f"     Range: ${result['salary_range']['min']:,} - ${result['salary_range']['max']:,}")
    print(f"     Source: {result['source']}")

    assert result["predicted_salary"] > 0, "Should predict positive salary"
    assert result["source"] in ["ml_model", "rule_based"], "Should indicate source"

    # Test locations
    locations = predictor.get_available_locations()
    print(f"[OK] Available locations: {len(locations)}")

    print("\n[PASS] salary_predictor.py - All tests passed!")
    return True


def test_career_recommender():
    """Test the career recommender module."""
    print("\n" + "="*60)
    print("Testing: utils/career_recommender.py")
    print("="*60)

    from utils.career_recommender import (
        recommend_careers,
        generate_career_roadmap,
        guess_current_role
    )

    test_skills = ["python", "pandas", "sql", "statistics", "matplotlib", "jupyter"]

    # Test career recommendations
    recommendations = recommend_careers(test_skills, experience_years=2)
    print(f"[OK] Career recommendations:")
    for rec in recommendations:
        print(f"     - {rec['role']}: {rec['match_score']*100:.0f}%")

    assert len(recommendations) > 0, "Should return recommendations"

    # Test role guessing
    current = guess_current_role(test_skills)
    print(f"[OK] Guessed current role: {current}")
    assert current, "Should guess a role"

    # Test roadmap generation
    roadmap = generate_career_roadmap(
        current_role_guess=current,
        target_role="Machine Learning Engineer",
        skills=test_skills,
        experience_years=2
    )

    print(f"[OK] Career roadmap:")
    print(f"     Target: {roadmap['target_role']}")
    print(f"     Estimated months: {roadmap['estimated_months']}")
    print(f"     Phases: {len(roadmap['phases'])}")

    assert "phases" in roadmap, "Should include phases"
    assert roadmap["estimated_months"] > 0, "Should estimate time"

    print("\n[PASS] career_recommender.py - All tests passed!")
    return True


def test_phi_analyzer():
    """Test the Phi analyzer module (without loading model)."""
    print("\n" + "="*60)
    print("Testing: utils/phi_analyzer.py")
    print("="*60)

    from utils.phi_analyzer import PhiResumeAnalyzer

    analyzer = PhiResumeAnalyzer()
    print(f"[OK] PhiResumeAnalyzer initialized")
    print(f"     Model loaded: {analyzer.is_loaded()}")

    # Test fallback analysis (no model needed)
    test_resume = {
        "skills": ["python", "pandas", "sql"],
        "experience_years": 2,
        "education": ["Test University"]
    }

    fallback_result = analyzer._fallback_analysis(test_resume)
    print(f"[OK] Fallback analysis works:")
    print(f"     Length: {len(fallback_result)} chars")

    assert len(fallback_result) > 100, "Should generate substantial analysis"

    # Test cover letter fallback
    tips = analyzer._fallback_cover_letter_tips("Data Scientist")
    print(f"[OK] Cover letter tips fallback works")
    assert "Data Scientist" in tips, "Should mention target role"

    print("\n[PASS] phi_analyzer.py - All tests passed!")
    return True


def test_chatbot():
    """Test the chatbot module (without Ollama)."""
    print("\n" + "="*60)
    print("Testing: utils/chatbot.py")
    print("="*60)

    from utils.chatbot import CareerChatbot

    chatbot = CareerChatbot()
    print(f"[OK] CareerChatbot initialized")

    # Check Ollama (will likely fail in test environment)
    ollama_status = chatbot.is_ollama_running()
    print(f"[OK] Ollama status checked: {'Available' if ollama_status else 'Not available'}")

    # Test resume context
    chatbot.set_resume_context({
        "name": "Test User",
        "skills": ["python", "sql"],
        "experience_years": 3,
        "parse_success": True
    })
    print(f"[OK] Resume context set")

    # Test rule-based response
    response = chatbot._rule_based_response("How can I improve my resume?")
    print(f"[OK] Rule-based response:")
    print(f"     Length: {len(response)} chars")

    assert len(response) > 50, "Should generate response"
    assert "resume" in response.lower(), "Should be relevant to question"

    # Test conversation stats
    stats = chatbot.get_conversation_stats()
    print(f"[OK] Conversation stats: {stats}")

    print("\n[PASS] chatbot.py - All tests passed!")
    return True


def run_all_tests():
    """Run all module tests."""
    print("""
    ===========================================================
    |                                                         |
    |              CareerMind AI - Module Tests               |
    |                                                         |
    ===========================================================
    """)

    tests = [
        ("Parser", test_parser),
        ("Skill Gap", test_skill_gap),
        ("Salary Predictor", test_salary_predictor),
        ("Career Recommender", test_career_recommender),
        ("Phi Analyzer", test_phi_analyzer),
        ("Chatbot", test_chatbot),
    ]

    results = []

    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"\n[FAIL] {name}: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    passed = sum(1 for _, r in results if r)
    total = len(results)

    for name, success in results:
        status = "[PASS]" if success else "[FAIL]"
        print(f"  {status} {name}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n All tests passed! CareerMind AI is ready. ")
        return 0
    else:
        print("\n Some tests failed. Please check the errors above. ")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
