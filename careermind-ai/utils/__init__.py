"""
CareerMind AI - Utilities Package
==================================
This package contains all the core modules for the CareerMind AI system.

Modules:
- parser: Resume PDF parsing and skill extraction
- skill_gap: Skill gap analysis and learning paths
- salary_predictor: Salary estimation based on role/skills
- career_recommender: Career recommendations and roadmaps
- phi_analyzer: HuggingFace Phi-3 based resume analysis
- chatbot: Ollama-powered interactive chatbot
"""

from .parser import (
    parse_resume,
    extract_skills,
    estimate_experience,
    format_resume_summary,
    ALL_SKILLS
)

from .skill_gap import (
    load_job_skills_map,
    get_available_roles,
    analyze_skill_gap,
    get_best_matching_roles,
    generate_learning_path,
    calculate_total_learning_time
)

from .salary_predictor import (
    SalaryPredictor,
    get_predictor,
    LOCATION_MULTIPLIERS
)

from .career_recommender import (
    recommend_careers,
    generate_career_roadmap,
    guess_current_role
)

from .phi_analyzer import (
    PhiResumeAnalyzer,
    get_analyzer
)

from .chatbot import (
    CareerChatbot,
    get_chatbot
)

__all__ = [
    # Parser
    "parse_resume",
    "extract_skills",
    "estimate_experience",
    "format_resume_summary",
    "ALL_SKILLS",

    # Skill Gap
    "load_job_skills_map",
    "get_available_roles",
    "analyze_skill_gap",
    "get_best_matching_roles",
    "generate_learning_path",
    "calculate_total_learning_time",

    # Salary
    "SalaryPredictor",
    "get_predictor",
    "LOCATION_MULTIPLIERS",

    # Career
    "recommend_careers",
    "generate_career_roadmap",
    "guess_current_role",

    # AI
    "PhiResumeAnalyzer",
    "get_analyzer",
    "CareerChatbot",
    "get_chatbot",
]

__version__ = "1.0.0"
