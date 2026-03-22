"""
CareerMind AI - Salary Prediction Module
=========================================
Predicts salary ranges based on role, experience, skills, and location.
Uses ML model if available, otherwise falls back to rule-based estimation.
"""

import pickle
import json
from pathlib import Path
from typing import Optional
import numpy as np


# ============================================================================
# LOCATION MULTIPLIERS
# ============================================================================
# These adjust the base US salary based on location/market

LOCATION_MULTIPLIERS = {
    # United States - Major Tech Hubs
    "US - San Francisco Bay Area": 1.35,
    "US - New York City": 1.25,
    "US - Seattle": 1.20,
    "US - Los Angeles": 1.15,
    "US - Austin": 1.10,
    "US - Boston": 1.15,
    "US - Denver": 1.05,
    "US - Other Major City": 1.00,
    "US - Remote": 0.95,

    # International - High Cost
    "UK - London": 0.85,
    "Switzerland - Zurich": 1.20,
    "Germany - Munich/Berlin": 0.75,
    "Netherlands - Amsterdam": 0.80,
    "Canada - Toronto": 0.75,
    "Canada - Vancouver": 0.75,
    "Australia - Sydney": 0.80,
    "Singapore": 0.85,

    # International - Medium Cost
    "Ireland - Dublin": 0.70,
    "France - Paris": 0.65,
    "Spain - Madrid/Barcelona": 0.55,
    "Italy - Milan": 0.55,
    "Japan - Tokyo": 0.65,
    "South Korea - Seoul": 0.55,
    "UAE - Dubai": 0.70,

    # International - Lower Cost (but growing tech scenes)
    "India - Bangalore": 0.25,
    "India - Mumbai/Delhi": 0.22,
    "India - Other": 0.18,
    "Poland - Warsaw": 0.40,
    "Portugal - Lisbon": 0.45,
    "Brazil - Sao Paulo": 0.30,
    "Mexico - Mexico City": 0.35,
    "Philippines - Manila": 0.20,
    "Vietnam - Ho Chi Minh": 0.20,

    # Remote - International
    "Remote - US Company": 0.85,
    "Remote - International": 0.60,
}

# Skill premium: extra value for in-demand skills (added per matching skill)
SKILL_PREMIUMS = {
    # Hot ML/AI skills
    "llm": 5000,
    "langchain": 4000,
    "transformers": 4000,
    "pytorch": 3500,
    "tensorflow": 3000,
    "gpt": 3500,
    "rag": 4000,
    "fine-tuning": 3500,

    # Cloud certifications/expertise
    "kubernetes": 3500,
    "aws": 3000,
    "terraform": 3000,
    "docker": 2000,

    # Backend/Systems
    "rust": 4000,
    "go": 3000,
    "system design": 3500,

    # Data Engineering
    "spark": 3000,
    "airflow": 2500,
    "dbt": 2500,
    "snowflake": 2500,

    # Security
    "security": 3000,
    "penetration testing": 3500,
}


# ============================================================================
# SALARY PREDICTOR CLASS
# ============================================================================

class SalaryPredictor:
    """
    Wrapper around the user's pre-trained salary model.pkl.
    Falls back to rule-based estimation if model file not found.

    The rule-based approach uses:
    1. Base salary from job_skills_map.json
    2. Experience multipliers (Junior 0.75x, Mid 1.0x, Senior 1.3x, Staff 1.6x)
    3. Location multipliers
    4. Skill premiums for in-demand skills
    """

    def __init__(self, model_path: str = "models/salary_model.pkl"):
        """
        Initialize the salary predictor.

        Args:
            model_path: Path to the trained sklearn model pickle file
        """
        self.model = None
        self.encoders = None
        self.model_available = False
        self.job_skills_map = None

        # Load the job skills map for base salaries
        self._load_job_skills_map()

        # Try to load the ML model
        self._load_model(model_path)

    def _load_job_skills_map(self):
        """Load the job skills mapping for base salary data."""
        try:
            module_dir = Path(__file__).parent.parent
            json_path = module_dir / "data" / "job_skills_map.json"

            with open(json_path, 'r', encoding='utf-8') as f:
                self.job_skills_map = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load job_skills_map.json: {e}")
            self.job_skills_map = {}

    def _load_model(self, path: str):
        """
        Attempt to load the ML model and encoders.

        Args:
            path: Path to the model pickle file
        """
        try:
            module_dir = Path(__file__).parent.parent
            model_path = module_dir / path

            if model_path.exists():
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)

                # Try to load label encoders
                encoders_path = model_path.parent / "label_encoders.pkl"
                if encoders_path.exists():
                    with open(encoders_path, 'rb') as f:
                        self.encoders = pickle.load(f)

                self.model_available = True
                print(f"Loaded salary prediction model from {model_path}")
            else:
                print(f"No ML model found at {model_path}. Using rule-based estimation.")

        except Exception as e:
            print(f"Could not load ML model: {e}. Using rule-based estimation.")
            self.model_available = False

    def predict(
        self,
        role: str,
        experience_years: float,
        skills: list[str],
        location: str = "US - Other Major City"
    ) -> dict:
        """
        Predict salary for given parameters.

        Args:
            role: Job role/title
            experience_years: Years of experience
            skills: List of skills
            location: Location key from LOCATION_MULTIPLIERS

        Returns:
            Dictionary containing:
            - predicted_salary: float - point estimate
            - salary_range: dict - {"min": float, "max": float}
            - currency: str - "USD"
            - confidence: str - "high", "medium", "low"
            - source: str - "ml_model" or "rule_based"
            - breakdown: dict - factors contributing to prediction
        """
        if self.model_available:
            return self._ml_predict(role, experience_years, skills, location)
        else:
            return self._rule_based_estimate(role, experience_years, skills, location)

    def _ml_predict(
        self,
        role: str,
        experience_years: float,
        skills: list[str],
        location: str
    ) -> dict:
        """
        Use the ML model to predict salary.

        This method assumes the model was trained with specific features.
        Adjust as needed based on your actual model's interface.
        """
        try:
            # This is a placeholder implementation
            # Actual implementation depends on your model's expected input format

            # Example: Create feature vector
            features = [
                experience_years,
                len(skills),
                LOCATION_MULTIPLIERS.get(location, 1.0),
            ]

            # If you have encoders for categorical features
            if self.encoders and 'role_encoder' in self.encoders:
                try:
                    role_encoded = self.encoders['role_encoder'].transform([role])[0]
                    features.insert(0, role_encoded)
                except ValueError:
                    # Role not in training data, fall back to rule-based
                    return self._rule_based_estimate(role, experience_years, skills, location)

            # Predict
            prediction = self.model.predict([features])[0]

            # Estimate confidence based on how well the features match training data
            confidence = "medium"

            return {
                "predicted_salary": round(prediction, -2),  # Round to nearest 100
                "salary_range": {
                    "min": round(prediction * 0.9, -2),
                    "max": round(prediction * 1.1, -2)
                },
                "currency": "USD",
                "confidence": confidence,
                "source": "ml_model",
                "breakdown": {
                    "note": "Prediction from trained ML model"
                }
            }

        except Exception as e:
            print(f"ML prediction failed: {e}. Falling back to rule-based.")
            return self._rule_based_estimate(role, experience_years, skills, location)

    def _rule_based_estimate(
        self,
        role: str,
        experience_years: float,
        skills: list[str],
        location: str
    ) -> dict:
        """
        Fallback rule-based salary estimation.

        Algorithm:
        1. Get base salary from job_skills_map (or use default)
        2. Apply experience multiplier
        3. Apply location multiplier
        4. Add skill premiums for in-demand skills
        5. Add bonus for skills beyond required set
        """
        breakdown = {}

        # Step 1: Get base salary
        if role in self.job_skills_map:
            base_salary = self.job_skills_map[role].get("avg_salary_usd", 100000)
            required_skills = set(s.lower() for s in
                                  self.job_skills_map[role].get("required_skills", []))
            confidence = "medium"
        else:
            # Unknown role - use average tech salary
            base_salary = 100000
            required_skills = set()
            confidence = "low"

        breakdown["base_salary"] = base_salary

        # Step 2: Apply experience multiplier
        if experience_years < 2:
            exp_multiplier = 0.75
            exp_level = "Junior"
        elif experience_years < 5:
            exp_multiplier = 1.0
            exp_level = "Mid-Level"
        elif experience_years < 10:
            exp_multiplier = 1.3
            exp_level = "Senior"
        else:
            exp_multiplier = 1.6
            exp_level = "Staff/Principal"

        breakdown["experience_level"] = exp_level
        breakdown["experience_multiplier"] = exp_multiplier

        # Step 3: Apply location multiplier
        loc_multiplier = LOCATION_MULTIPLIERS.get(location, 1.0)
        breakdown["location"] = location
        breakdown["location_multiplier"] = loc_multiplier

        # Step 4: Calculate skill premium
        user_skills_lower = set(s.lower() for s in skills)
        skill_premium = 0

        premium_skills_matched = []
        for skill, premium in SKILL_PREMIUMS.items():
            if skill.lower() in user_skills_lower:
                skill_premium += premium
                premium_skills_matched.append(skill)

        breakdown["skill_premium"] = skill_premium
        breakdown["premium_skills"] = premium_skills_matched

        # Step 5: Bonus for extra skills beyond required
        if required_skills:
            extra_skills_count = len(user_skills_lower - required_skills)
            extra_skills_bonus = extra_skills_count * 1500  # $1500 per extra skill
            breakdown["extra_skills_bonus"] = extra_skills_bonus
        else:
            extra_skills_bonus = 0
            breakdown["extra_skills_bonus"] = 0

        # Calculate final salary
        base_adjusted = base_salary * exp_multiplier * loc_multiplier
        total_salary = base_adjusted + skill_premium + extra_skills_bonus

        # Round to nearest $1000
        predicted_salary = round(total_salary, -3)

        # Calculate range (±15%)
        salary_min = round(predicted_salary * 0.85, -3)
        salary_max = round(predicted_salary * 1.15, -3)

        # Generate tip
        tip = self._generate_salary_tip(skills, role)

        return {
            "predicted_salary": predicted_salary,
            "salary_range": {
                "min": salary_min,
                "max": salary_max
            },
            "currency": "USD",
            "confidence": confidence,
            "source": "rule_based",
            "breakdown": breakdown,
            "tip": tip
        }

    def _generate_salary_tip(self, current_skills: list[str], role: str) -> str:
        """
        Generate a tip for increasing salary potential.

        Args:
            current_skills: User's current skills
            role: Target role

        Returns:
            Actionable tip string
        """
        user_skills_lower = set(s.lower() for s in current_skills)

        # Find high-value skills the user doesn't have
        missing_premium_skills = []
        for skill, premium in sorted(SKILL_PREMIUMS.items(), key=lambda x: -x[1]):
            if skill.lower() not in user_skills_lower:
                missing_premium_skills.append((skill, premium))

        if missing_premium_skills:
            top_skill, top_premium = missing_premium_skills[0]
            return (
                f"Adding {top_skill} to your skillset could increase "
                f"your market value by ~${top_premium:,}/year."
            )

        return "Your skills are well-optimized for market value. Focus on deepening expertise."

    def get_available_locations(self) -> list[str]:
        """Return list of available location options."""
        return sorted(LOCATION_MULTIPLIERS.keys())

    def get_market_comparison(
        self,
        predicted_salary: float,
        role: str,
        location: str = "US - Other Major City"
    ) -> dict:
        """
        Compare predicted salary against market data.

        Args:
            predicted_salary: The predicted salary
            role: Job role
            location: Location

        Returns:
            Dictionary with market comparison data
        """
        if role not in self.job_skills_map:
            return {"available": False}

        base_salary = self.job_skills_map[role].get("avg_salary_usd", 100000)
        loc_multiplier = LOCATION_MULTIPLIERS.get(location, 1.0)

        # Adjusted market median for location
        market_median = base_salary * loc_multiplier

        # Calculate percentile (rough estimate)
        diff_pct = (predicted_salary - market_median) / market_median

        if diff_pct > 0.2:
            percentile = "top 20%"
            assessment = "above market"
        elif diff_pct > 0.05:
            percentile = "top 40%"
            assessment = "competitive"
        elif diff_pct > -0.05:
            percentile = "around median"
            assessment = "at market rate"
        elif diff_pct > -0.2:
            percentile = "bottom 40%"
            assessment = "below market"
        else:
            percentile = "bottom 20%"
            assessment = "significantly below market"

        return {
            "available": True,
            "market_median": round(market_median, -2),
            "predicted_salary": predicted_salary,
            "difference": round(predicted_salary - market_median, -2),
            "percentile": percentile,
            "assessment": assessment
        }


# ============================================================================
# Singleton instance for easy import
# ============================================================================

_predictor_instance = None


def get_predictor() -> SalaryPredictor:
    """Get or create the singleton SalaryPredictor instance."""
    global _predictor_instance
    if _predictor_instance is None:
        _predictor_instance = SalaryPredictor()
    return _predictor_instance


# ============================================================================
# TEST / DEBUG
# ============================================================================

if __name__ == "__main__":
    # Test the salary predictor
    predictor = SalaryPredictor()

    print("Available locations:")
    for loc in predictor.get_available_locations()[:10]:
        print(f"  - {loc}")
    print("  ... and more\n")

    # Test prediction
    test_skills = ["python", "pytorch", "docker", "aws", "kubernetes", "transformers"]
    test_role = "Machine Learning Engineer"
    test_experience = 4.0
    test_location = "US - San Francisco Bay Area"

    print(f"Test prediction:")
    print(f"  Role: {test_role}")
    print(f"  Experience: {test_experience} years")
    print(f"  Location: {test_location}")
    print(f"  Skills: {', '.join(test_skills)}")
    print()

    result = predictor.predict(test_role, test_experience, test_skills, test_location)

    print(f"Results:")
    print(f"  Predicted Salary: ${result['predicted_salary']:,}")
    print(f"  Range: ${result['salary_range']['min']:,} - ${result['salary_range']['max']:,}")
    print(f"  Confidence: {result['confidence']}")
    print(f"  Source: {result['source']}")
    print()

    if 'breakdown' in result:
        print("Breakdown:")
        for key, value in result['breakdown'].items():
            print(f"  {key}: {value}")
    print()

    if 'tip' in result:
        print(f"Tip: {result['tip']}")

    # Market comparison
    comparison = predictor.get_market_comparison(
        result['predicted_salary'], test_role, test_location
    )
    if comparison.get('available'):
        print(f"\nMarket Comparison:")
        print(f"  Market Median: ${comparison['market_median']:,}")
        print(f"  Your Position: {comparison['assessment']} ({comparison['percentile']})")
