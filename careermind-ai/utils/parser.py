"""
CareerMind AI - Resume Parser Module
=====================================
Extracts structured information from PDF resumes including:
- Personal info (name, email, phone, LinkedIn, GitHub)
- Skills (matched against comprehensive vocabulary)
- Education institutions
- Years of experience (estimated from date ranges)
"""

import re
from pathlib import Path
from datetime import datetime
from typing import Optional
import PyPDF2
import spacy

# Load spaCy model for NER (Named Entity Recognition)
# This model recognizes persons, organizations, dates, etc.
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # If model not found, download it
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")


# ============================================================================
# COMPREHENSIVE SKILLS VOCABULARY
# ============================================================================
# Organized by category for easier maintenance and extension

SKILLS_VOCABULARY = {
    # Programming Languages
    "programming": [
        "python", "java", "javascript", "typescript", "c++", "c#", "c",
        "go", "golang", "rust", "r", "scala", "kotlin", "swift", "ruby",
        "php", "perl", "matlab", "julia", "haskell", "erlang", "elixir",
        "objective-c", "assembly", "fortran", "cobol", "lua", "dart",
        "groovy", "shell", "bash", "powershell", "vba", "sql", "nosql"
    ],

    # Machine Learning & AI
    "ml_ai": [
        "tensorflow", "pytorch", "scikit-learn", "sklearn", "keras",
        "huggingface", "transformers", "bert", "gpt", "llm", "nlp",
        "computer vision", "deep learning", "machine learning",
        "neural networks", "reinforcement learning", "mlflow",
        "weights & biases", "wandb", "mlops", "automl", "xgboost",
        "lightgbm", "catboost", "random forest", "svm", "clustering",
        "classification", "regression", "time series", "forecasting",
        "recommendation systems", "feature engineering", "model deployment",
        "onnx", "tensorrt", "opencv", "yolo", "segmentation", "cnn", "rnn",
        "lstm", "transformer", "attention", "fine-tuning", "rag",
        "langchain", "llama", "mistral", "stable diffusion", "generative ai",
        "prompt engineering", "embeddings", "vector database", "faiss",
        "pinecone", "chroma", "weaviate"
    ],

    # Data Science & Analytics
    "data": [
        "pandas", "numpy", "matplotlib", "seaborn", "plotly", "bokeh",
        "scipy", "statsmodels", "statistics", "hypothesis testing",
        "a/b testing", "experimentation", "sql", "mysql", "postgresql",
        "postgres", "mongodb", "cassandra", "redis", "elasticsearch",
        "spark", "pyspark", "hadoop", "hive", "presto", "airflow",
        "dbt", "etl", "elt", "data pipeline", "data warehouse",
        "snowflake", "databricks", "bigquery", "redshift", "tableau",
        "power bi", "looker", "metabase", "superset", "excel",
        "google sheets", "google analytics", "mixpanel", "amplitude",
        "data visualization", "business intelligence", "bi", "reporting",
        "dashboards", "kpis", "metrics", "jupyter", "notebook", "colab"
    ],

    # Web Development
    "web": [
        "react", "reactjs", "nextjs", "next.js", "vue", "vuejs", "angular",
        "svelte", "html", "html5", "css", "css3", "sass", "scss", "less",
        "tailwind", "tailwindcss", "bootstrap", "material ui", "chakra ui",
        "django", "fastapi", "flask", "express", "expressjs", "nodejs",
        "node.js", "deno", "bun", "rest api", "restful", "graphql",
        "websocket", "ajax", "json", "xml", "webpack", "vite", "rollup",
        "parcel", "babel", "eslint", "prettier", "npm", "yarn", "pnpm"
    ],

    # DevOps & Cloud
    "devops_cloud": [
        "docker", "kubernetes", "k8s", "aws", "amazon web services",
        "azure", "microsoft azure", "gcp", "google cloud", "terraform",
        "pulumi", "cloudformation", "ansible", "puppet", "chef",
        "ci/cd", "cicd", "jenkins", "github actions", "gitlab ci",
        "circleci", "travis ci", "argocd", "spinnaker", "linux", "unix",
        "ubuntu", "centos", "debian", "rhel", "bash", "shell scripting",
        "git", "github", "gitlab", "bitbucket", "svn", "nginx", "apache",
        "load balancer", "cdn", "cloudflare", "prometheus", "grafana",
        "datadog", "new relic", "splunk", "elk", "logstash", "kibana",
        "helm", "istio", "service mesh", "microservices", "serverless",
        "lambda", "cloud functions", "fargate", "ecs", "eks", "gke", "aks"
    ],

    # Mobile Development
    "mobile": [
        "ios", "android", "react native", "flutter", "swift", "swiftui",
        "kotlin", "java android", "objective-c", "xamarin", "ionic",
        "cordova", "mobile ui", "app store", "google play", "firebase",
        "push notifications", "mobile analytics", "responsive design"
    ],

    # Databases
    "databases": [
        "sql", "mysql", "postgresql", "postgres", "sqlite", "oracle",
        "sql server", "mssql", "mariadb", "mongodb", "dynamodb",
        "cassandra", "redis", "memcached", "neo4j", "graph database",
        "couchdb", "firebase", "firestore", "supabase", "planetscale",
        "cockroachdb", "timescaledb", "influxdb", "clickhouse"
    ],

    # Tools & Practices
    "tools": [
        "git", "github", "gitlab", "bitbucket", "jira", "confluence",
        "notion", "trello", "asana", "slack", "teams", "agile", "scrum",
        "kanban", "waterfall", "devops", "devsecops", "testing",
        "unit testing", "integration testing", "e2e testing", "tdd", "bdd",
        "pytest", "jest", "mocha", "cypress", "selenium", "playwright",
        "postman", "swagger", "openapi", "api design", "documentation",
        "vscode", "visual studio", "intellij", "pycharm", "vim", "emacs",
        "debugging", "profiling", "code review", "pair programming",
        "technical writing", "system design", "architecture"
    ],

    # Security
    "security": [
        "security", "cybersecurity", "penetration testing", "pen testing",
        "vulnerability assessment", "owasp", "encryption", "cryptography",
        "ssl", "tls", "https", "oauth", "jwt", "authentication",
        "authorization", "identity management", "sso", "mfa", "2fa",
        "compliance", "gdpr", "hipaa", "soc2", "pci", "iso 27001",
        "incident response", "threat modeling", "siem", "firewall", "vpn"
    ],

    # Soft Skills & Management
    "soft_skills": [
        "leadership", "communication", "teamwork", "collaboration",
        "problem solving", "critical thinking", "project management",
        "time management", "mentoring", "coaching", "presentation",
        "stakeholder management", "cross-functional", "remote work"
    ]
}

# Flatten all skills into a single set for matching
ALL_SKILLS = set()
for category_skills in SKILLS_VOCABULARY.values():
    ALL_SKILLS.update(skill.lower() for skill in category_skills)


# ============================================================================
# REGEX PATTERNS
# ============================================================================

# Email pattern: matches common email formats
EMAIL_PATTERN = re.compile(
    r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
)

# Phone pattern: matches various phone formats (US, international)
PHONE_PATTERN = re.compile(
    r'(?:\+?1[-.\s]?)?'  # Optional US country code
    r'(?:\(?\d{3}\)?[-.\s]?)?'  # Area code
    r'\d{3}[-.\s]?\d{4}'  # Main number
    r'(?:\s*(?:ext|x|extension)\.?\s*\d+)?',  # Optional extension
    re.IGNORECASE
)

# LinkedIn URL pattern
LINKEDIN_PATTERN = re.compile(
    r'(?:https?://)?(?:www\.)?linkedin\.com/in/[\w-]+/?',
    re.IGNORECASE
)

# GitHub URL pattern
GITHUB_PATTERN = re.compile(
    r'(?:https?://)?(?:www\.)?github\.com/[\w-]+/?',
    re.IGNORECASE
)

# Date range pattern for experience calculation
# Matches: "Jan 2020 - Mar 2023", "2019 - 2021", "January 2018 to Present"
DATE_RANGE_PATTERN = re.compile(
    r'(?:(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|'
    r'Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)'
    r'[\s,]*)?'
    r'(\d{4})'
    r'\s*[-–—to]+\s*'
    r'(?:(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|'
    r'Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)'
    r'[\s,]*)?'
    r'(\d{4}|[Pp]resent|[Cc]urrent|[Nn]ow)',
    re.IGNORECASE
)


# ============================================================================
# MAIN PARSING FUNCTIONS
# ============================================================================

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract raw text content from a PDF file.

    Args:
        file_path: Path to the PDF file

    Returns:
        Extracted text as a single string

    Raises:
        FileNotFoundError: If the PDF file doesn't exist
        PyPDF2.errors.PdfReadError: If the PDF is corrupted or encrypted
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    text_content = []

    # Open PDF and extract text from each page
    with open(path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Iterate through all pages
        for page_num, page in enumerate(pdf_reader.pages):
            try:
                page_text = page.extract_text()
                if page_text:
                    text_content.append(page_text)
            except Exception as e:
                # Log error but continue with other pages
                print(f"Warning: Could not extract text from page {page_num + 1}: {e}")

    # Join all pages with newlines
    return '\n'.join(text_content)


def extract_name(text: str, doc: spacy.tokens.Doc) -> Optional[str]:
    """
    Extract the candidate's name from resume text.
    Uses spaCy NER to find PERSON entities, prioritizing those at the start.

    Args:
        text: Raw resume text
        doc: spaCy Doc object (already processed)

    Returns:
        Best guess at the candidate's name, or None if not found
    """
    # Get all PERSON entities from spaCy
    person_entities = [ent.text.strip() for ent in doc.ents if ent.label_ == "PERSON"]

    if not person_entities:
        return None

    # The first PERSON entity is usually the candidate's name
    # (resumes typically start with the name)
    candidate_name = person_entities[0]

    # Clean up: remove extra whitespace and newlines
    candidate_name = ' '.join(candidate_name.split())

    # Validate: name should be 2-5 words, each starting with uppercase
    name_parts = candidate_name.split()
    if 1 <= len(name_parts) <= 5:
        # Check if at least first word starts with uppercase
        if name_parts[0][0].isupper():
            return candidate_name

    return person_entities[0] if person_entities else None


def extract_email(text: str) -> Optional[str]:
    """
    Extract email address from resume text.

    Args:
        text: Raw resume text

    Returns:
        First email found, or None if not found
    """
    matches = EMAIL_PATTERN.findall(text)
    return matches[0] if matches else None


def extract_phone(text: str) -> Optional[str]:
    """
    Extract phone number from resume text.

    Args:
        text: Raw resume text

    Returns:
        First phone number found (cleaned), or None if not found
    """
    matches = PHONE_PATTERN.findall(text)
    if matches:
        # Clean up the phone number
        phone = matches[0]
        # Remove extra whitespace
        phone = ' '.join(phone.split())
        return phone
    return None


def extract_linkedin(text: str) -> Optional[str]:
    """
    Extract LinkedIn profile URL from resume text.

    Args:
        text: Raw resume text

    Returns:
        LinkedIn URL, or None if not found
    """
    matches = LINKEDIN_PATTERN.findall(text)
    if matches:
        url = matches[0]
        # Ensure URL has https://
        if not url.startswith('http'):
            url = 'https://' + url
        return url
    return None


def extract_github(text: str) -> Optional[str]:
    """
    Extract GitHub profile URL from resume text.

    Args:
        text: Raw resume text

    Returns:
        GitHub URL, or None if not found
    """
    matches = GITHUB_PATTERN.findall(text)
    if matches:
        url = matches[0]
        # Ensure URL has https://
        if not url.startswith('http'):
            url = 'https://' + url
        return url
    return None


def extract_education(doc: spacy.tokens.Doc) -> list[str]:
    """
    Extract educational institutions from resume.
    Uses spaCy to find ORG entities that look like educational institutions.

    Args:
        doc: spaCy Doc object

    Returns:
        List of institution names
    """
    # Keywords that indicate educational institutions
    edu_keywords = [
        'university', 'college', 'institute', 'school', 'academy',
        'polytechnic', 'iit', 'mit', 'stanford', 'harvard', 'berkeley',
        'oxford', 'cambridge', 'ucla', 'nyu', 'cmu', 'caltech'
    ]

    institutions = []

    # Get all ORG entities
    for ent in doc.ents:
        if ent.label_ == "ORG":
            org_text = ent.text.strip().lower()
            # Check if it contains educational keywords
            if any(keyword in org_text for keyword in edu_keywords):
                # Add the original (non-lowercased) text
                clean_name = ' '.join(ent.text.split())
                if clean_name not in institutions:
                    institutions.append(clean_name)

    return institutions


def extract_skills(text: str) -> list[str]:
    """
    Extract skills from resume text by matching against vocabulary.
    Uses word boundary matching to avoid false positives.

    Args:
        text: Raw resume text

    Returns:
        Deduplicated list of matched skills (lowercase)
    """
    # Normalize text for matching
    text_lower = text.lower()

    found_skills = set()

    # Check each skill in our vocabulary
    for skill in ALL_SKILLS:
        # Create word boundary pattern for the skill
        # This prevents matching "r" inside "programming"
        pattern = r'\b' + re.escape(skill) + r'\b'

        if re.search(pattern, text_lower):
            found_skills.add(skill)

    # Handle some special cases and aliases
    skill_aliases = {
        'sklearn': 'scikit-learn',
        'postgres': 'postgresql',
        'k8s': 'kubernetes',
        'reactjs': 'react',
        'vuejs': 'vue',
        'nodejs': 'node.js',
        'expressjs': 'express',
        'golang': 'go',
    }

    # Add canonical names for aliases
    for alias, canonical in skill_aliases.items():
        if alias in found_skills:
            found_skills.add(canonical)

    # Sort alphabetically for consistent output
    return sorted(list(found_skills))


def estimate_experience(text: str) -> float:
    """
    Estimate total years of professional experience from date ranges in resume.
    Parses patterns like "Jan 2020 - Mar 2023" and accumulates non-overlapping years.

    Args:
        text: Raw resume text

    Returns:
        Estimated years of experience as float (e.g., 4.5)
    """
    current_year = datetime.now().year

    # Find all date range matches
    matches = DATE_RANGE_PATTERN.findall(text)

    if not matches:
        return 0.0

    total_years = 0.0

    for start_year_str, end_year_str in matches:
        try:
            start_year = int(start_year_str)

            # Handle "Present", "Current", "Now"
            if end_year_str.lower() in ['present', 'current', 'now']:
                end_year = current_year
            else:
                end_year = int(end_year_str)

            # Validate years are reasonable (1970 - current + 5)
            if 1970 <= start_year <= current_year + 5 and start_year <= end_year:
                years = end_year - start_year
                # Cap individual entries at 20 years (sanity check)
                years = min(years, 20)
                total_years += years

        except (ValueError, TypeError):
            continue

    # Cap total at 40 years (reasonable maximum for a career)
    total_years = min(total_years, 40.0)

    return round(total_years, 1)


def parse_resume(file_path: str) -> dict:
    """
    Main function to parse a resume PDF and extract all structured information.

    Args:
        file_path: Path to the resume PDF file

    Returns:
        Dictionary containing:
        - name: str | None
        - email: str | None
        - phone: str | None
        - linkedin: str | None
        - github: str | None
        - skills: list[str]
        - education: list[str]
        - experience_years: float
        - raw_text: str
        - parse_success: bool
        - error: str | None
    """
    result = {
        'name': None,
        'email': None,
        'phone': None,
        'linkedin': None,
        'github': None,
        'skills': [],
        'education': [],
        'experience_years': 0.0,
        'raw_text': '',
        'parse_success': False,
        'error': None
    }

    try:
        # Step 1: Extract raw text from PDF
        raw_text = extract_text_from_pdf(file_path)
        result['raw_text'] = raw_text

        if not raw_text.strip():
            result['error'] = "Could not extract text from PDF. The file may be scanned or image-based."
            return result

        # Step 2: Process text with spaCy for NER
        doc = nlp(raw_text[:100000])  # Limit to 100k chars for performance

        # Step 3: Extract each field
        result['name'] = extract_name(raw_text, doc)
        result['email'] = extract_email(raw_text)
        result['phone'] = extract_phone(raw_text)
        result['linkedin'] = extract_linkedin(raw_text)
        result['github'] = extract_github(raw_text)
        result['skills'] = extract_skills(raw_text)
        result['education'] = extract_education(doc)
        result['experience_years'] = estimate_experience(raw_text)

        result['parse_success'] = True

    except FileNotFoundError as e:
        result['error'] = str(e)
    except Exception as e:
        result['error'] = f"Error parsing resume: {str(e)}"

    return result


def format_resume_summary(resume_data: dict) -> str:
    """
    Format parsed resume data into a human-readable summary.
    Useful for display in the UI and as context for the AI.

    Args:
        resume_data: Dictionary from parse_resume()

    Returns:
        Formatted markdown string
    """
    if not resume_data.get('parse_success'):
        return f"**Error:** {resume_data.get('error', 'Unknown error')}"

    lines = ["## Resume Summary\n"]

    # Personal Info
    if resume_data.get('name'):
        lines.append(f"**Name:** {resume_data['name']}")
    if resume_data.get('email'):
        lines.append(f"**Email:** {resume_data['email']}")
    if resume_data.get('phone'):
        lines.append(f"**Phone:** {resume_data['phone']}")
    if resume_data.get('linkedin'):
        lines.append(f"**LinkedIn:** {resume_data['linkedin']}")
    if resume_data.get('github'):
        lines.append(f"**GitHub:** {resume_data['github']}")

    lines.append("")  # Blank line

    # Experience
    exp = resume_data.get('experience_years', 0)
    if exp > 0:
        lines.append(f"**Experience:** ~{exp} years")
    else:
        lines.append("**Experience:** Not detected")

    # Education
    education = resume_data.get('education', [])
    if education:
        lines.append(f"**Education:** {', '.join(education)}")

    lines.append("")  # Blank line

    # Skills
    skills = resume_data.get('skills', [])
    if skills:
        lines.append(f"**Skills ({len(skills)}):**")
        # Group into rows of 5 for readability
        for i in range(0, len(skills), 5):
            skill_row = skills[i:i+5]
            lines.append("  " + ", ".join(skill_row))
    else:
        lines.append("**Skills:** No skills detected")

    return '\n'.join(lines)


# ============================================================================
# TEST / DEBUG
# ============================================================================

if __name__ == "__main__":
    # Quick test with a sample PDF
    import sys

    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]
        print(f"Parsing: {pdf_path}\n")

        result = parse_resume(pdf_path)

        if result['parse_success']:
            print(format_resume_summary(result))
            print(f"\n[Raw text length: {len(result['raw_text'])} chars]")
        else:
            print(f"Error: {result['error']}")
    else:
        print("Usage: python parser.py <path_to_resume.pdf>")
        print("\nSkills vocabulary loaded with", len(ALL_SKILLS), "skills")
