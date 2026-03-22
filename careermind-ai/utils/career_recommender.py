"""
CareerMind AI - Career Recommendation Engine
=============================================
Recommends career paths based on current skills and experience.
Generates structured roadmaps for career progression.
"""

import json
from pathlib import Path
from typing import Optional

from .skill_gap import (
    load_job_skills_map,
    get_best_matching_roles,
    analyze_skill_gap,
    generate_learning_path,
    calculate_total_learning_time
)


# ============================================================================
# CAREER TRANSITION MATRIX
# ============================================================================
# Defines common career transitions and their difficulty

CAREER_TRANSITIONS = {
    # From Data Analyst
    "Data Analyst": {
        "Data Scientist": {"difficulty": "moderate", "typical_months": 6},
        "Data Engineer": {"difficulty": "moderate", "typical_months": 8},
        "Machine Learning Engineer": {"difficulty": "challenging", "typical_months": 12},
        "Product Manager": {"difficulty": "lateral", "typical_months": 4},
        "Business Intelligence": {"difficulty": "easy", "typical_months": 3},
    },

    # From Data Scientist
    "Data Scientist": {
        "Machine Learning Engineer": {"difficulty": "moderate", "typical_months": 6},
        "AI Research Engineer": {"difficulty": "challenging", "typical_months": 12},
        "Data Engineer": {"difficulty": "moderate", "typical_months": 6},
        "NLP Engineer": {"difficulty": "moderate", "typical_months": 6},
    },

    # From Software Engineer
    "Software Engineer": {
        "Backend Developer": {"difficulty": "easy", "typical_months": 2},
        "Full Stack Developer": {"difficulty": "moderate", "typical_months": 4},
        "DevOps Engineer": {"difficulty": "moderate", "typical_months": 6},
        "Machine Learning Engineer": {"difficulty": "challenging", "typical_months": 12},
        "Solutions Architect": {"difficulty": "moderate", "typical_months": 8},
    },

    # From Backend Developer
    "Backend Developer": {
        "Full Stack Developer": {"difficulty": "moderate", "typical_months": 4},
        "DevOps Engineer": {"difficulty": "moderate", "typical_months": 6},
        "Solutions Architect": {"difficulty": "moderate", "typical_months": 8},
        "Data Engineer": {"difficulty": "moderate", "typical_months": 6},
    },

    # From Frontend Developer
    "Frontend Developer": {
        "Full Stack Developer": {"difficulty": "moderate", "typical_months": 6},
        "Mobile Developer": {"difficulty": "moderate", "typical_months": 4},
        "Software Engineer": {"difficulty": "moderate", "typical_months": 4},
    },

    # From DevOps Engineer
    "DevOps Engineer": {
        "Cloud Engineer": {"difficulty": "easy", "typical_months": 3},
        "Solutions Architect": {"difficulty": "moderate", "typical_months": 6},
        "Security Engineer": {"difficulty": "moderate", "typical_months": 8},
        "Site Reliability Engineer": {"difficulty": "easy", "typical_months": 3},
    },
}


# ============================================================================
# ROLE EXPERIENCE FIT
# ============================================================================
# Which roles are better suited for different experience levels

ROLE_EXPERIENCE_FIT = {
    # Entry-level friendly roles
    "Data Analyst": {"ideal_years": (0, 5), "entry_friendly": True},
    "QA Engineer": {"ideal_years": (0, 6), "entry_friendly": True},
    "Frontend Developer": {"ideal_years": (0, 8), "entry_friendly": True},
    "Backend Developer": {"ideal_years": (0, 10), "entry_friendly": True},

    # Mid-level roles
    "Data Scientist": {"ideal_years": (1, 8), "entry_friendly": False},
    "Full Stack Developer": {"ideal_years": (2, 10), "entry_friendly": False},
    "Software Engineer": {"ideal_years": (0, 15), "entry_friendly": True},
    "DevOps Engineer": {"ideal_years": (2, 12), "entry_friendly": False},
    "Data Engineer": {"ideal_years": (2, 12), "entry_friendly": False},

    # Senior/Specialized roles
    "Machine Learning Engineer": {"ideal_years": (2, 15), "entry_friendly": False},
    "NLP Engineer": {"ideal_years": (2, 15), "entry_friendly": False},
    "Cloud Engineer": {"ideal_years": (3, 12), "entry_friendly": False},
    "Security Engineer": {"ideal_years": (3, 15), "entry_friendly": False},
    "Mobile Developer": {"ideal_years": (1, 12), "entry_friendly": True},
    "Computer Vision Engineer": {"ideal_years": (2, 15), "entry_friendly": False},

    # Leadership/Senior roles
    "Solutions Architect": {"ideal_years": (5, 20), "entry_friendly": False},
    "AI Research Engineer": {"ideal_years": (3, 20), "entry_friendly": False},
    "Product Manager": {"ideal_years": (3, 15), "entry_friendly": False},
}


# ============================================================================
# CAREER RECOMMENDATION FUNCTIONS
# ============================================================================

def recommend_careers(
    skills: list[str],
    experience_years: float,
    top_n: int = 3
) -> list[dict]:
    """
    Recommend career paths based on current skills and experience.

    Args:
        skills: List of user's skills
        experience_years: Years of professional experience
        top_n: Number of recommendations to return

    Returns:
        List of recommended roles with match scores and reasoning:
        [
            {
                "role": str,
                "match_score": float,
                "experience_fit": str,  # "ideal", "stretching", "overqualified"
                "reason": str,
                "next_steps": list[str],
                "avg_salary": int
            }
        ]
    """
    # Get base matches from skill analysis
    skill_matches = get_best_matching_roles(skills, top_n=10)

    if not skill_matches:
        return []

    recommendations = []

    for match in skill_matches:
        role = match["role"]

        # Analyze experience fit
        exp_fit_data = ROLE_EXPERIENCE_FIT.get(role, {
            "ideal_years": (0, 15),
            "entry_friendly": True
        })

        ideal_min, ideal_max = exp_fit_data["ideal_years"]

        if ideal_min <= experience_years <= ideal_max:
            experience_fit = "ideal"
            exp_score_modifier = 1.0
        elif experience_years < ideal_min:
            if exp_fit_data["entry_friendly"]:
                experience_fit = "approachable"
                exp_score_modifier = 0.9
            else:
                experience_fit = "stretching"
                exp_score_modifier = 0.75
        else:
            experience_fit = "overqualified"
            exp_score_modifier = 0.85

        # Adjust score based on experience fit
        adjusted_score = match["match_score"] * exp_score_modifier

        # Generate reasoning
        reason = _generate_recommendation_reason(
            role=role,
            match_score=match["match_score"],
            matched_count=match["matched_count"],
            total_required=match["total_required"],
            experience_years=experience_years,
            experience_fit=experience_fit
        )

        # Generate next steps
        next_steps = _generate_next_steps(
            role=role,
            skills=skills,
            experience_years=experience_years,
            experience_fit=experience_fit
        )

        recommendations.append({
            "role": role,
            "match_score": round(adjusted_score, 2),
            "skill_match_score": match["match_score"],
            "experience_fit": experience_fit,
            "reason": reason,
            "next_steps": next_steps,
            "avg_salary": match.get("avg_salary", 0),
            "description": match.get("description", "")
        })

    # Sort by adjusted score
    recommendations.sort(key=lambda x: x["match_score"], reverse=True)

    return recommendations[:top_n]


def _generate_recommendation_reason(
    role: str,
    match_score: float,
    matched_count: int,
    total_required: int,
    experience_years: float,
    experience_fit: str
) -> str:
    """Generate personalized reasoning for a role recommendation."""

    match_pct = int(match_score * 100)

    if match_pct >= 80:
        skill_assessment = f"You already have {matched_count}/{total_required} core skills"
    elif match_pct >= 60:
        skill_assessment = f"You have a solid foundation with {matched_count}/{total_required} skills"
    else:
        skill_assessment = f"Your {matched_count} matching skills provide a starting point"

    if experience_fit == "ideal":
        exp_assessment = f"Your {experience_years:.0f} years of experience is ideal for this role"
    elif experience_fit == "approachable":
        exp_assessment = "This role is accessible at your experience level"
    elif experience_fit == "stretching":
        exp_assessment = "This role typically requires more experience, but skills can bridge the gap"
    else:
        exp_assessment = "You may be overqualified; consider senior or lead positions"

    return f"{skill_assessment}. {exp_assessment}."


def _generate_next_steps(
    role: str,
    skills: list[str],
    experience_years: float,
    experience_fit: str
) -> list[str]:
    """Generate actionable next steps for pursuing a role."""

    steps = []

    # Get skill gap for specific recommendations
    gap = analyze_skill_gap(skills, role)

    if gap.get("error"):
        return ["Research the role requirements", "Build relevant projects", "Apply to positions"]

    missing_required = gap.get("missing_required", [])[:3]
    match_score = gap.get("match_score", 0)

    # Skill-based steps
    if missing_required:
        steps.append(f"Learn key missing skills: {', '.join(missing_required)}")
    elif match_score < 0.9 and gap.get("missing_nice_to_have"):
        nice_skills = gap["missing_nice_to_have"][:2]
        steps.append(f"Add differentiating skills: {', '.join(nice_skills)}")

    # Project-based steps
    project_suggestions = {
        "Data Scientist": "Complete a data analysis project with real-world data on Kaggle",
        "Machine Learning Engineer": "Deploy an ML model with MLOps pipeline (MLflow/Docker)",
        "Data Engineer": "Build an end-to-end ETL pipeline with Airflow",
        "Backend Developer": "Create a REST API with authentication and deploy it",
        "Frontend Developer": "Build a responsive React app with modern state management",
        "DevOps Engineer": "Set up a CI/CD pipeline with Docker and Kubernetes",
        "NLP Engineer": "Fine-tune a transformer model for a specific NLP task",
        "Cloud Engineer": "Get an AWS/Azure/GCP certification",
    }

    if role in project_suggestions:
        steps.append(project_suggestions[role])

    # Experience-based steps
    if experience_fit == "stretching":
        steps.append("Seek internships or junior positions to gain domain experience")
    elif experience_fit == "overqualified":
        steps.append("Target senior or lead positions that leverage your experience")

    # Interview prep
    if match_score >= 0.7:
        steps.append("Start applying and prepare for technical interviews")
    else:
        steps.append("Build portfolio projects demonstrating relevant skills")

    return steps[:4]  # Max 4 steps


# ============================================================================
# CAREER ROADMAP GENERATION
# ============================================================================

def generate_career_roadmap(
    current_role_guess: str,
    target_role: str,
    skills: list[str],
    experience_years: float = 0
) -> dict:
    """
    Generate a structured roadmap from current position to target role.

    Args:
        current_role_guess: Best guess at user's current role
        target_role: Desired role
        skills: Current skills list
        experience_years: Years of experience

    Returns:
        Dictionary containing:
        - current_level: str
        - target_role: str
        - estimated_months: int
        - feasibility: str ("straightforward", "achievable", "challenging")
        - phases: list of phase dictionaries
    """
    job_map = load_job_skills_map()

    # Validate target role
    if target_role not in job_map:
        return {
            "error": f"Unknown target role: {target_role}",
            "available_roles": list(job_map.keys())
        }

    # Analyze skill gap for target
    gap = analyze_skill_gap(skills, target_role)

    if gap.get("error"):
        return gap

    missing_required = gap.get("missing_required", [])
    missing_nice = gap.get("missing_nice_to_have", [])
    match_score = gap.get("match_score", 0)
    readiness = gap.get("readiness_level", "Beginner")

    # Determine current level
    if experience_years < 2:
        current_level = "Junior/Entry"
    elif experience_years < 5:
        current_level = "Mid-Level"
    elif experience_years < 10:
        current_level = "Senior"
    else:
        current_level = "Staff/Principal"

    # Estimate total months
    if match_score >= 0.85:
        estimated_months = 1
        feasibility = "minimal gap"
    elif match_score >= 0.7:
        estimated_months = 3
        feasibility = "straightforward"
    elif match_score >= 0.5:
        estimated_months = 6
        feasibility = "achievable"
    elif match_score >= 0.3:
        estimated_months = 9
        feasibility = "challenging"
    else:
        estimated_months = 12
        feasibility = "significant effort required"

    # Check transition difficulty from known paths
    if current_role_guess in CAREER_TRANSITIONS:
        transitions = CAREER_TRANSITIONS[current_role_guess]
        if target_role in transitions:
            trans_data = transitions[target_role]
            estimated_months = trans_data["typical_months"]
            feasibility = trans_data["difficulty"]

    # Generate learning path
    all_missing = missing_required + missing_nice[:3]  # Prioritize required
    learning_path = generate_learning_path(all_missing)

    # Divide into phases
    phases = _create_roadmap_phases(
        missing_required=missing_required,
        missing_nice=missing_nice,
        learning_path=learning_path,
        total_months=estimated_months,
        target_role=target_role
    )

    # Calculate total learning hours
    time_estimate = calculate_total_learning_time(learning_path)

    return {
        "current_level": current_level,
        "current_role_guess": current_role_guess,
        "target_role": target_role,
        "current_match_score": round(match_score, 2),
        "readiness_level": readiness,
        "estimated_months": estimated_months,
        "feasibility": feasibility,
        "total_learning_hours": time_estimate["total_hours"],
        "phases": phases,
        "final_advice": _generate_final_advice(match_score, target_role, current_role_guess)
    }


def _create_roadmap_phases(
    missing_required: list[str],
    missing_nice: list[str],
    learning_path: list[dict],
    total_months: int,
    target_role: str
) -> list[dict]:
    """Create structured phases for the roadmap."""

    phases = []

    if not missing_required and not missing_nice:
        # Already ready
        phases.append({
            "phase": 1,
            "title": "Job Application & Interview Prep",
            "duration_weeks": 4,
            "skills_to_learn": [],
            "activities": [
                "Update resume and LinkedIn for target role",
                "Practice technical interview questions",
                "Apply to positions and network"
            ]
        })
        return phases

    # Create learning path lookup
    skill_resources = {item["skill"].lower(): item for item in learning_path}

    # Phase 1: Foundations (high priority required skills)
    phase1_skills = missing_required[:4] if missing_required else []
    if phase1_skills:
        phase1_items = []
        for skill in phase1_skills:
            if skill.lower() in skill_resources:
                res = skill_resources[skill.lower()]
                phase1_items.append({
                    "skill": skill,
                    "resource": res["resource"],
                    "hours": res["estimated_hours"]
                })
            else:
                phase1_items.append({
                    "skill": skill,
                    "resource": f"Online course for {skill}",
                    "hours": 20
                })

        phases.append({
            "phase": 1,
            "title": "Core Skills Foundation",
            "duration_weeks": max(4, min(total_months * 2, 8)),
            "skills_to_learn": phase1_items,
            "activities": [
                "Complete structured courses for each skill",
                "Build small projects to practice",
                "Join relevant communities and forums"
            ]
        })

    # Phase 2: Advanced/Remaining required skills
    phase2_skills = missing_required[4:] if len(missing_required) > 4 else []
    if phase2_skills:
        phase2_items = []
        for skill in phase2_skills:
            if skill.lower() in skill_resources:
                res = skill_resources[skill.lower()]
                phase2_items.append({
                    "skill": skill,
                    "resource": res["resource"],
                    "hours": res["estimated_hours"]
                })
            else:
                phase2_items.append({
                    "skill": skill,
                    "resource": f"Online course for {skill}",
                    "hours": 20
                })

        phases.append({
            "phase": 2,
            "title": "Advanced Required Skills",
            "duration_weeks": max(4, total_months * 2 - 8),
            "skills_to_learn": phase2_items,
            "activities": [
                "Deepen understanding with intermediate/advanced materials",
                "Contribute to open source projects",
                "Start building portfolio project"
            ]
        })

    # Phase 3: Nice-to-have skills and differentiation
    if missing_nice:
        phase3_skills = missing_nice[:3]
        phase3_items = []
        for skill in phase3_skills:
            if skill.lower() in skill_resources:
                res = skill_resources[skill.lower()]
                phase3_items.append({
                    "skill": skill,
                    "resource": res["resource"],
                    "hours": res["estimated_hours"]
                })
            else:
                phase3_items.append({
                    "skill": skill,
                    "resource": f"Online course for {skill}",
                    "hours": 20
                })

        phases.append({
            "phase": len(phases) + 1,
            "title": "Competitive Edge Skills",
            "duration_weeks": 4,
            "skills_to_learn": phase3_items,
            "activities": [
                "Learn skills that differentiate you from other candidates",
                "Complete portfolio project showcasing all skills",
                "Write blog posts or create content about your learning"
            ]
        })

    # Final Phase: Application and Interview
    phases.append({
        "phase": len(phases) + 1,
        "title": "Job Search & Interviews",
        "duration_weeks": 4,
        "skills_to_learn": [],
        "activities": [
            f"Tailor resume for {target_role} positions",
            "Practice behavioral and technical interviews",
            "Apply to positions (aim for 5-10 per week)",
            "Follow up on applications and network"
        ]
    })

    return phases


def _generate_final_advice(
    match_score: float,
    target_role: str,
    current_role: str
) -> str:
    """Generate personalized final advice."""

    if match_score >= 0.85:
        return (
            f"You're nearly ready for {target_role} roles! Focus on interview "
            f"prep and building confidence. Your existing skills are a strong foundation."
        )
    elif match_score >= 0.6:
        return (
            f"The path from {current_role} to {target_role} is achievable with "
            f"consistent effort. Focus on the required skills first, and don't "
            f"wait until you're 'perfect' to start applying."
        )
    else:
        return (
            f"This transition requires significant learning, but is absolutely "
            f"possible. Consider intermediate roles if available, and focus on "
            f"building real projects. Many successful {target_role}s started "
            f"from different backgrounds."
        )


def guess_current_role(skills: list[str]) -> str:
    """
    Guess the user's current role based on their skills.

    Args:
        skills: List of user's skills

    Returns:
        Best matching role name
    """
    matches = get_best_matching_roles(skills, top_n=1)
    if matches:
        return matches[0]["role"]
    return "Software Engineer"  # Default fallback


# ============================================================================
# TEST / DEBUG
# ============================================================================

if __name__ == "__main__":
    # Test career recommendations
    test_skills = [
        "python", "pandas", "sql", "git", "jupyter",
        "matplotlib", "statistics", "excel"
    ]

    print("Testing career recommendations")
    print(f"Skills: {test_skills}")
    print(f"Experience: 2 years")
    print()

    # Get recommendations
    recommendations = recommend_careers(test_skills, experience_years=2)

    print("Top 3 Recommended Roles:")
    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec['role']} ({rec['match_score']*100:.0f}% match)")
        print(f"   Experience fit: {rec['experience_fit']}")
        print(f"   {rec['reason']}")
        print(f"   Next steps:")
        for step in rec['next_steps']:
            print(f"     - {step}")

    # Test roadmap
    print("\n" + "="*60)
    print("Testing career roadmap")
    print()

    current = guess_current_role(test_skills)
    target = "Machine Learning Engineer"

    print(f"Current role guess: {current}")
    print(f"Target role: {target}")
    print()

    roadmap = generate_career_roadmap(current, target, test_skills, experience_years=2)

    print(f"Feasibility: {roadmap['feasibility']}")
    print(f"Estimated time: {roadmap['estimated_months']} months")
    print(f"Total learning hours: {roadmap['total_learning_hours']}")
    print()

    for phase in roadmap['phases']:
        print(f"Phase {phase['phase']}: {phase['title']} ({phase['duration_weeks']} weeks)")
        if phase['skills_to_learn']:
            for skill_item in phase['skills_to_learn']:
                print(f"  - {skill_item['skill']}: {skill_item['resource']}")
        for activity in phase['activities'][:2]:
            print(f"  * {activity}")
        print()

    print(f"Final advice: {roadmap['final_advice']}")
