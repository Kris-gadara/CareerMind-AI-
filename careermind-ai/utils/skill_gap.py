"""
CareerMind AI - Skill Gap Analysis Module
==========================================
Analyzes the gap between user's current skills and target role requirements.
Provides match scores, readiness levels, and personalized learning paths.
"""

import json
from pathlib import Path
from typing import Optional


# ============================================================================
# DATA LOADING
# ============================================================================

def load_job_skills_map() -> dict:
    """
    Load the job skills mapping from JSON file.

    Returns:
        Dictionary mapping role names to their skill requirements

    Raises:
        FileNotFoundError: If job_skills_map.json doesn't exist
    """
    # Look for the JSON file relative to this module
    module_dir = Path(__file__).parent.parent
    json_path = module_dir / "data" / "job_skills_map.json"

    if not json_path.exists():
        raise FileNotFoundError(
            f"Job skills map not found at: {json_path}\n"
            "Please ensure data/job_skills_map.json exists."
        )

    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_available_roles() -> list[str]:
    """
    Get list of all available job roles.

    Returns:
        Sorted list of role names
    """
    job_map = load_job_skills_map()
    return sorted(job_map.keys())


# ============================================================================
# SKILL GAP ANALYSIS
# ============================================================================

def analyze_skill_gap(user_skills: list[str], target_role: str) -> dict:
    """
    Analyze the skill gap between user's skills and a target role.

    Args:
        user_skills: List of user's skills (lowercase)
        target_role: Name of the target job role

    Returns:
        Dictionary containing:
        - target_role: str
        - matched_skills: list - skills the user has that are required
        - missing_required: list - required skills the user lacks
        - missing_nice_to_have: list - optional skills the user could learn
        - extra_skills: list - user skills not in role requirements
        - match_score: float - 0.0 to 1.0 match percentage
        - readiness_level: str - "Beginner", "Intermediate", "Ready", "Overqualified"
        - recommendation: str - personalized advice
    """
    job_map = load_job_skills_map()

    # Validate target role exists
    if target_role not in job_map:
        return {
            "target_role": target_role,
            "error": f"Unknown role: {target_role}",
            "available_roles": list(job_map.keys())
        }

    role_data = job_map[target_role]
    required_skills = set(s.lower() for s in role_data.get("required_skills", []))
    nice_to_have = set(s.lower() for s in role_data.get("nice_to_have", []))
    user_skills_set = set(s.lower() for s in user_skills)

    # Calculate matches and gaps
    matched_required = user_skills_set.intersection(required_skills)
    missing_required = required_skills - user_skills_set
    matched_nice = user_skills_set.intersection(nice_to_have)
    missing_nice = nice_to_have - user_skills_set
    extra_skills = user_skills_set - required_skills - nice_to_have

    # Calculate match score (weighted: required skills count more)
    if len(required_skills) == 0:
        required_score = 1.0
    else:
        required_score = len(matched_required) / len(required_skills)

    if len(nice_to_have) == 0:
        nice_score = 0.5
    else:
        nice_score = len(matched_nice) / len(nice_to_have)

    # Weighted average: 80% required, 20% nice-to-have
    match_score = (required_score * 0.8) + (nice_score * 0.2)

    # Determine readiness level
    if match_score >= 0.9:
        readiness_level = "Ready"
    elif match_score >= 0.7:
        readiness_level = "Intermediate"
    elif match_score >= 0.4:
        readiness_level = "Developing"
    else:
        readiness_level = "Beginner"

    # Check for overqualification (has many extra relevant skills)
    if match_score >= 0.85 and len(extra_skills) > 5:
        readiness_level = "Overqualified"

    # Generate personalized recommendation
    recommendation = _generate_recommendation(
        target_role=target_role,
        matched_count=len(matched_required),
        required_count=len(required_skills),
        missing_required=list(missing_required),
        readiness_level=readiness_level
    )

    return {
        "target_role": target_role,
        "role_description": role_data.get("description", ""),
        "matched_skills": sorted(list(matched_required)),
        "matched_nice_to_have": sorted(list(matched_nice)),
        "missing_required": sorted(list(missing_required)),
        "missing_nice_to_have": sorted(list(missing_nice)),
        "extra_skills": sorted(list(extra_skills)),
        "match_score": round(match_score, 2),
        "readiness_level": readiness_level,
        "recommendation": recommendation
    }


def _generate_recommendation(
    target_role: str,
    matched_count: int,
    required_count: int,
    missing_required: list[str],
    readiness_level: str
) -> str:
    """
    Generate a personalized recommendation based on skill gap analysis.

    Args:
        target_role: Target job role
        matched_count: Number of required skills matched
        required_count: Total required skills for role
        missing_required: List of missing required skills
        readiness_level: Current readiness level

    Returns:
        Personalized recommendation string
    """
    if readiness_level == "Ready":
        return (
            f"Excellent! You have the core skills for {target_role}. "
            "Focus on real-world projects and interview preparation. "
            "Consider learning the 'nice-to-have' skills to stand out."
        )

    elif readiness_level == "Overqualified":
        return (
            f"You exceed the typical requirements for {target_role}. "
            "You might consider more senior positions or specialized roles "
            "that leverage your broader skill set."
        )

    elif readiness_level == "Intermediate":
        # Suggest 2-3 priority skills
        priority_skills = missing_required[:3]
        skills_str = ", ".join(priority_skills)
        return (
            f"You're on track for {target_role}! "
            f"Priority skills to learn: {skills_str}. "
            f"With {required_count - matched_count} skills to go, "
            "you could be ready in 2-4 months with focused learning."
        )

    elif readiness_level == "Developing":
        priority_skills = missing_required[:4]
        skills_str = ", ".join(priority_skills)
        return (
            f"Good foundation! To become a {target_role}, focus on: {skills_str}. "
            "Consider taking structured courses and building portfolio projects. "
            "Estimated timeline: 4-8 months with consistent effort."
        )

    else:  # Beginner
        priority_skills = missing_required[:3]
        skills_str = ", ".join(priority_skills)
        return (
            f"Starting your journey to {target_role}! "
            f"Begin with foundational skills: {skills_str}. "
            "Look for beginner-friendly courses and start with small projects. "
            "This path typically takes 6-12 months of dedicated learning."
        )


# ============================================================================
# BEST MATCHING ROLES
# ============================================================================

def get_best_matching_roles(user_skills: list[str], top_n: int = 3) -> list[dict]:
    """
    Find roles that best match the user's current skill set.

    Args:
        user_skills: List of user's skills
        top_n: Number of top roles to return

    Returns:
        List of dictionaries, each containing:
        - role: str - role name
        - match_score: float - 0.0 to 1.0
        - matched_count: int - number of required skills matched
        - missing_count: int - number of required skills missing
        - description: str - role description
    """
    job_map = load_job_skills_map()
    user_skills_set = set(s.lower() for s in user_skills)

    role_scores = []

    for role_name, role_data in job_map.items():
        required_skills = set(s.lower() for s in role_data.get("required_skills", []))
        nice_to_have = set(s.lower() for s in role_data.get("nice_to_have", []))

        # Calculate match
        matched_required = user_skills_set.intersection(required_skills)
        matched_nice = user_skills_set.intersection(nice_to_have)

        if len(required_skills) == 0:
            required_score = 0.5
        else:
            required_score = len(matched_required) / len(required_skills)

        if len(nice_to_have) == 0:
            nice_score = 0.5
        else:
            nice_score = len(matched_nice) / len(nice_to_have)

        # Weighted score
        match_score = (required_score * 0.8) + (nice_score * 0.2)

        role_scores.append({
            "role": role_name,
            "match_score": round(match_score, 2),
            "matched_count": len(matched_required),
            "total_required": len(required_skills),
            "missing_count": len(required_skills) - len(matched_required),
            "description": role_data.get("description", ""),
            "avg_salary": role_data.get("avg_salary_usd", 0)
        })

    # Sort by match score descending
    role_scores.sort(key=lambda x: x["match_score"], reverse=True)

    return role_scores[:top_n]


# ============================================================================
# LEARNING PATH GENERATION
# ============================================================================

# Curated learning resources for common skills
LEARNING_RESOURCES = {
    # Programming Languages
    "python": {
        "resource": "Python for Everybody (Coursera) or Automate the Boring Stuff",
        "url": "https://www.coursera.org/specializations/python",
        "estimated_hours": 40,
        "priority": "high"
    },
    "javascript": {
        "resource": "The Odin Project - JavaScript Path",
        "url": "https://www.theodinproject.com/paths/full-stack-javascript",
        "estimated_hours": 60,
        "priority": "high"
    },
    "typescript": {
        "resource": "TypeScript Handbook (Official Docs)",
        "url": "https://www.typescriptlang.org/docs/handbook/",
        "estimated_hours": 20,
        "priority": "medium"
    },
    "sql": {
        "resource": "SQLBolt Interactive Tutorial",
        "url": "https://sqlbolt.com/",
        "estimated_hours": 15,
        "priority": "high"
    },
    "java": {
        "resource": "Java Programming Masterclass (Udemy)",
        "url": "https://www.udemy.com/course/java-the-complete-java-developer-course/",
        "estimated_hours": 80,
        "priority": "high"
    },
    "go": {
        "resource": "A Tour of Go (Official)",
        "url": "https://tour.golang.org/",
        "estimated_hours": 25,
        "priority": "medium"
    },
    "rust": {
        "resource": "The Rust Programming Language Book",
        "url": "https://doc.rust-lang.org/book/",
        "estimated_hours": 50,
        "priority": "medium"
    },

    # ML/AI
    "tensorflow": {
        "resource": "TensorFlow Developer Certificate Course (Coursera)",
        "url": "https://www.coursera.org/professional-certificates/tensorflow-in-practice",
        "estimated_hours": 60,
        "priority": "high"
    },
    "pytorch": {
        "resource": "PyTorch Tutorials (Official) + Fast.ai",
        "url": "https://pytorch.org/tutorials/",
        "estimated_hours": 50,
        "priority": "high"
    },
    "scikit-learn": {
        "resource": "Scikit-learn User Guide + Kaggle Learn",
        "url": "https://scikit-learn.org/stable/user_guide.html",
        "estimated_hours": 30,
        "priority": "high"
    },
    "deep learning": {
        "resource": "Deep Learning Specialization (Coursera - Andrew Ng)",
        "url": "https://www.coursera.org/specializations/deep-learning",
        "estimated_hours": 100,
        "priority": "high"
    },
    "machine learning": {
        "resource": "Machine Learning by Stanford (Coursera - Andrew Ng)",
        "url": "https://www.coursera.org/learn/machine-learning",
        "estimated_hours": 60,
        "priority": "high"
    },
    "nlp": {
        "resource": "Natural Language Processing Specialization (Coursera)",
        "url": "https://www.coursera.org/specializations/natural-language-processing",
        "estimated_hours": 80,
        "priority": "high"
    },
    "transformers": {
        "resource": "HuggingFace Course (Free)",
        "url": "https://huggingface.co/course",
        "estimated_hours": 40,
        "priority": "high"
    },
    "huggingface": {
        "resource": "HuggingFace Course (Free)",
        "url": "https://huggingface.co/course",
        "estimated_hours": 40,
        "priority": "high"
    },
    "mlflow": {
        "resource": "MLflow Official Documentation + Tutorials",
        "url": "https://mlflow.org/docs/latest/tutorials-and-examples/index.html",
        "estimated_hours": 15,
        "priority": "medium"
    },
    "langchain": {
        "resource": "LangChain Documentation + YouTube Tutorials",
        "url": "https://python.langchain.com/docs/get_started/introduction",
        "estimated_hours": 25,
        "priority": "medium"
    },

    # Data
    "pandas": {
        "resource": "Pandas Documentation + Kaggle Learn",
        "url": "https://pandas.pydata.org/docs/getting_started/index.html",
        "estimated_hours": 20,
        "priority": "high"
    },
    "numpy": {
        "resource": "NumPy Quickstart Tutorial",
        "url": "https://numpy.org/doc/stable/user/quickstart.html",
        "estimated_hours": 10,
        "priority": "high"
    },
    "spark": {
        "resource": "Apache Spark with Python (Udemy/Coursera)",
        "url": "https://spark.apache.org/docs/latest/quick-start.html",
        "estimated_hours": 40,
        "priority": "medium"
    },
    "airflow": {
        "resource": "Apache Airflow Documentation + Astronomer Guides",
        "url": "https://airflow.apache.org/docs/apache-airflow/stable/tutorial/index.html",
        "estimated_hours": 25,
        "priority": "medium"
    },
    "tableau": {
        "resource": "Tableau Free Training Videos",
        "url": "https://www.tableau.com/learn/training",
        "estimated_hours": 30,
        "priority": "medium"
    },
    "power bi": {
        "resource": "Microsoft Power BI Learning Path",
        "url": "https://learn.microsoft.com/en-us/training/powerplatform/power-bi",
        "estimated_hours": 30,
        "priority": "medium"
    },
    "statistics": {
        "resource": "Statistics with Python Specialization (Coursera)",
        "url": "https://www.coursera.org/specializations/statistics-with-python",
        "estimated_hours": 50,
        "priority": "high"
    },

    # Web
    "react": {
        "resource": "React Official Tutorial + Beta Docs",
        "url": "https://react.dev/learn",
        "estimated_hours": 40,
        "priority": "high"
    },
    "nextjs": {
        "resource": "Next.js Learn (Official)",
        "url": "https://nextjs.org/learn",
        "estimated_hours": 25,
        "priority": "medium"
    },
    "django": {
        "resource": "Django Official Tutorial + Django for Beginners Book",
        "url": "https://docs.djangoproject.com/en/stable/intro/tutorial01/",
        "estimated_hours": 40,
        "priority": "high"
    },
    "fastapi": {
        "resource": "FastAPI Official Tutorial",
        "url": "https://fastapi.tiangolo.com/tutorial/",
        "estimated_hours": 20,
        "priority": "high"
    },
    "rest api": {
        "resource": "RESTful API Design Best Practices",
        "url": "https://restfulapi.net/",
        "estimated_hours": 10,
        "priority": "high"
    },
    "graphql": {
        "resource": "How to GraphQL (Free Tutorial)",
        "url": "https://www.howtographql.com/",
        "estimated_hours": 15,
        "priority": "medium"
    },
    "html": {
        "resource": "MDN HTML Learning Path",
        "url": "https://developer.mozilla.org/en-US/docs/Learn/HTML",
        "estimated_hours": 15,
        "priority": "high"
    },
    "css": {
        "resource": "MDN CSS Learning Path",
        "url": "https://developer.mozilla.org/en-US/docs/Learn/CSS",
        "estimated_hours": 25,
        "priority": "high"
    },

    # DevOps/Cloud
    "docker": {
        "resource": "Docker Getting Started Guide + Play with Docker",
        "url": "https://docs.docker.com/get-started/",
        "estimated_hours": 20,
        "priority": "high"
    },
    "kubernetes": {
        "resource": "Kubernetes Official Tutorials + Killer.sh",
        "url": "https://kubernetes.io/docs/tutorials/",
        "estimated_hours": 50,
        "priority": "high"
    },
    "aws": {
        "resource": "AWS Cloud Practitioner Training (Free)",
        "url": "https://aws.amazon.com/training/digital/aws-cloud-practitioner-essentials/",
        "estimated_hours": 60,
        "priority": "high"
    },
    "azure": {
        "resource": "Microsoft Azure Fundamentals Learning Path",
        "url": "https://learn.microsoft.com/en-us/training/paths/azure-fundamentals/",
        "estimated_hours": 50,
        "priority": "high"
    },
    "gcp": {
        "resource": "Google Cloud Skills Boost",
        "url": "https://www.cloudskillsboost.google/",
        "estimated_hours": 50,
        "priority": "high"
    },
    "terraform": {
        "resource": "HashiCorp Terraform Tutorials",
        "url": "https://developer.hashicorp.com/terraform/tutorials",
        "estimated_hours": 30,
        "priority": "medium"
    },
    "ci/cd": {
        "resource": "GitHub Actions Documentation",
        "url": "https://docs.github.com/en/actions/learn-github-actions",
        "estimated_hours": 20,
        "priority": "high"
    },
    "linux": {
        "resource": "Linux Journey (Free Interactive)",
        "url": "https://linuxjourney.com/",
        "estimated_hours": 30,
        "priority": "high"
    },
    "git": {
        "resource": "Pro Git Book (Free) + Learn Git Branching",
        "url": "https://learngitbranching.js.org/",
        "estimated_hours": 15,
        "priority": "high"
    },
    "bash": {
        "resource": "Bash Scripting Tutorial",
        "url": "https://www.gnu.org/software/bash/manual/bash.html",
        "estimated_hours": 20,
        "priority": "medium"
    },

    # Testing
    "testing": {
        "resource": "Testing Python Applications with pytest",
        "url": "https://docs.pytest.org/en/stable/getting-started.html",
        "estimated_hours": 15,
        "priority": "medium"
    },
    "selenium": {
        "resource": "Selenium Documentation",
        "url": "https://www.selenium.dev/documentation/",
        "estimated_hours": 20,
        "priority": "medium"
    }
}


def generate_learning_path(missing_skills: list[str]) -> list[dict]:
    """
    Generate a learning path for missing skills with curated resources.

    Args:
        missing_skills: List of skills to learn

    Returns:
        List of dictionaries, each containing:
        - skill: str
        - resource: str
        - url: str
        - estimated_hours: int
        - priority: str ("high", "medium", "low")
    """
    learning_path = []

    for skill in missing_skills:
        skill_lower = skill.lower()

        if skill_lower in LEARNING_RESOURCES:
            resource_data = LEARNING_RESOURCES[skill_lower]
            learning_path.append({
                "skill": skill,
                "resource": resource_data["resource"],
                "url": resource_data.get("url", ""),
                "estimated_hours": resource_data["estimated_hours"],
                "priority": resource_data["priority"]
            })
        else:
            # Generate generic resource recommendation
            learning_path.append({
                "skill": skill,
                "resource": f"Search '{skill} tutorial' on YouTube/Udemy/Coursera",
                "url": f"https://www.google.com/search?q={skill.replace(' ', '+')}+tutorial",
                "estimated_hours": 20,
                "priority": "medium"
            })

    # Sort by priority (high first) then by estimated hours (shorter first)
    priority_order = {"high": 0, "medium": 1, "low": 2}
    learning_path.sort(key=lambda x: (priority_order.get(x["priority"], 1), x["estimated_hours"]))

    return learning_path


def calculate_total_learning_time(learning_path: list[dict]) -> dict:
    """
    Calculate total estimated learning time for a path.

    Args:
        learning_path: List from generate_learning_path()

    Returns:
        Dictionary with total hours, weeks (at 10hr/week), and months
    """
    total_hours = sum(item["estimated_hours"] for item in learning_path)

    return {
        "total_hours": total_hours,
        "weeks_at_10h_per_week": round(total_hours / 10, 1),
        "months_at_10h_per_week": round(total_hours / 40, 1)
    }


# ============================================================================
# TEST / DEBUG
# ============================================================================

if __name__ == "__main__":
    # Test the skill gap analysis
    print("Available roles:", get_available_roles())
    print()

    # Test with sample skills
    test_skills = ["python", "pandas", "sql", "git", "jupyter", "matplotlib"]

    print(f"Testing with skills: {test_skills}\n")

    # Get best matching roles
    print("Best matching roles:")
    matches = get_best_matching_roles(test_skills)
    for match in matches:
        print(f"  {match['role']}: {match['match_score']*100:.0f}% match")
    print()

    # Analyze gap for top role
    gap = analyze_skill_gap(test_skills, matches[0]["role"])
    print(f"Gap analysis for {gap['target_role']}:")
    print(f"  Match score: {gap['match_score']*100:.0f}%")
    print(f"  Readiness: {gap['readiness_level']}")
    print(f"  Missing required: {gap['missing_required']}")
    print(f"  Recommendation: {gap['recommendation']}")
    print()

    # Generate learning path
    if gap['missing_required']:
        print("Learning path:")
        path = generate_learning_path(gap['missing_required'][:5])
        for item in path:
            print(f"  - {item['skill']}: {item['resource']} (~{item['estimated_hours']}h)")

        time_estimate = calculate_total_learning_time(path)
        print(f"\nTotal time: {time_estimate['total_hours']}h "
              f"(~{time_estimate['months_at_10h_per_week']} months at 10h/week)")
