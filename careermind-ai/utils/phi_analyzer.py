"""
CareerMind AI - Phi-3 Resume Analyzer
======================================
Uses Microsoft's Phi-3-mini (or fallback models) for intelligent
resume analysis and career advice generation.

This module loads the model lazily to save memory and provides
fallback options if the primary model isn't available.
"""

import os
import torch
from typing import Optional, Callable
from threading import Lock


class PhiResumeAnalyzer:
    """
    Uses microsoft/Phi-3-mini-4k-instruct (free, runs on CPU/GPU)
    to generate intelligent resume analysis and career advice.

    Falls back to smaller models if Phi-3 is not available.
    Model is loaded lazily (only when first used) to save memory.
    """

    # Models to try, in order of preference
    MODEL_OPTIONS = [
        "microsoft/Phi-3-mini-4k-instruct",  # Primary: 3.8B params, best quality
        "microsoft/phi-2",                    # Fallback: 2.7B params
        "TinyLlama/TinyLlama-1.1B-Chat-v1.0", # Ultra-light: 1.1B params
    ]

    def __init__(self):
        """Initialize the analyzer (model loaded on first use)."""
        self.model = None
        self.tokenizer = None
        self.model_name = None
        self._loaded = False
        self._loading = False
        self._lock = Lock()
        self._device = None

        # Check environment for CPU-only mode
        self._force_cpu = os.environ.get("FORCE_CPU", "false").lower() == "true"

    def _get_device(self) -> str:
        """Determine the best available device."""
        if self._force_cpu:
            return "cpu"

        if torch.cuda.is_available():
            # Check CUDA memory
            try:
                gpu_mem = torch.cuda.get_device_properties(0).total_memory
                if gpu_mem >= 4 * 1024**3:  # At least 4GB
                    return "cuda"
            except Exception:
                pass

        # Check for Apple Silicon MPS
        if hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            return "mps"

        return "cpu"

    def load_model(self, progress_callback: Optional[Callable[[str], None]] = None) -> bool:
        """
        Load the AI model. Tries models in order until one succeeds.

        Args:
            progress_callback: Optional callback for progress updates.
                              Called with status messages.

        Returns:
            True if model loaded successfully, False otherwise.
        """
        # Thread-safe loading
        with self._lock:
            if self._loaded:
                return True

            if self._loading:
                return False

            self._loading = True

        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM

            self._device = self._get_device()

            if progress_callback:
                progress_callback(f"Detected device: {self._device}")

            # Try each model option
            for model_name in self.MODEL_OPTIONS:
                try:
                    if progress_callback:
                        progress_callback(f"Loading {model_name}...")

                    # Load tokenizer
                    self.tokenizer = AutoTokenizer.from_pretrained(
                        model_name,
                        trust_remote_code=True
                    )

                    # Configure model loading based on device and memory
                    load_kwargs = {
                        "trust_remote_code": True,
                        "low_cpu_mem_usage": True,
                    }

                    if self._device == "cuda":
                        # Try to use bitsandbytes for 4-bit quantization
                        try:
                            from transformers import BitsAndBytesConfig

                            quantization_config = BitsAndBytesConfig(
                                load_in_4bit=True,
                                bnb_4bit_compute_dtype=torch.float16
                            )
                            load_kwargs["quantization_config"] = quantization_config
                            load_kwargs["device_map"] = "auto"

                            if progress_callback:
                                progress_callback("Using 4-bit quantization for GPU")

                        except ImportError:
                            # bitsandbytes not available, load normally
                            load_kwargs["torch_dtype"] = torch.float16
                            load_kwargs["device_map"] = "auto"

                    elif self._device == "mps":
                        load_kwargs["torch_dtype"] = torch.float16

                    # Load model
                    self.model = AutoModelForCausalLM.from_pretrained(
                        model_name,
                        **load_kwargs
                    )

                    # Move to device if not using device_map
                    if "device_map" not in load_kwargs:
                        self.model = self.model.to(self._device)

                    self.model.eval()  # Set to evaluation mode
                    self.model_name = model_name
                    self._loaded = True

                    if progress_callback:
                        progress_callback(f"Successfully loaded {model_name}")

                    return True

                except Exception as e:
                    if progress_callback:
                        progress_callback(f"Failed to load {model_name}: {str(e)[:100]}")
                    continue

            # All models failed
            if progress_callback:
                progress_callback("Could not load any model. AI features will be limited.")

            return False

        except ImportError as e:
            if progress_callback:
                progress_callback(f"Missing dependency: {e}")
            return False

        finally:
            self._loading = False

    def is_loaded(self) -> bool:
        """Check if model is loaded and ready."""
        return self._loaded and self.model is not None

    def get_model_info(self) -> dict:
        """Get information about the loaded model."""
        if not self._loaded:
            return {"loaded": False, "model": None, "device": None}

        return {
            "loaded": True,
            "model": self.model_name,
            "device": self._device,
            "parameters": "~4B" if "Phi-3" in (self.model_name or "") else "~2B"
        }

    def _build_phi3_prompt(self, system: str, user: str) -> str:
        """
        Build a prompt using Phi-3 chat template format.

        Args:
            system: System message defining the AI's role
            user: User message/query

        Returns:
            Formatted prompt string
        """
        # Phi-3 chat format
        if "Phi-3" in (self.model_name or ""):
            return f"""<|system|>
{system}<|end|>
<|user|>
{user}<|end|>
<|assistant|>
"""
        elif "phi-2" in (self.model_name or "").lower():
            # Phi-2 is a base model, use simple instruction format
            return f"""Instruct: {system}

Input: {user}

Output:"""
        else:
            # TinyLlama chat format
            return f"""<|system|>
{system}</s>
<|user|>
{user}</s>
<|assistant|>
"""

    def _generate(self, prompt: str, max_new_tokens: int = 512) -> str:
        """
        Run inference and return the generated text.

        Args:
            prompt: The formatted prompt
            max_new_tokens: Maximum tokens to generate

        Returns:
            Generated text response
        """
        if not self._loaded:
            return "Model not loaded. Please load the model first."

        try:
            # Tokenize input
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=2048  # Leave room for generation
            )

            # Move inputs to device
            if self._device and "device_map" not in str(type(self.model)):
                inputs = {k: v.to(self._device) for k, v in inputs.items()}

            # Generate
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_new_tokens,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.9,
                    repetition_penalty=1.1,
                    pad_token_id=self.tokenizer.eos_token_id
                )

            # Decode output
            full_output = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Extract just the assistant's response
            # Remove the prompt from the output
            if prompt in full_output:
                response = full_output[len(prompt):].strip()
            else:
                # Try to find response after assistant marker
                markers = ["<|assistant|>", "Output:", "Assistant:"]
                response = full_output
                for marker in markers:
                    if marker in response:
                        response = response.split(marker)[-1].strip()
                        break

            return response

        except Exception as e:
            return f"Error during generation: {str(e)}"

    def analyze_resume(self, resume_data: dict) -> str:
        """
        Generate a structured resume analysis using AI.

        Args:
            resume_data: Dictionary from parser.parse_resume() containing:
                        skills, experience_years, education, name, etc.

        Returns:
            Markdown-formatted analysis with sections:
            - Strengths
            - Areas to Improve
            - Career Fit Assessment
            - Growth Potential
        """
        if not self._loaded:
            return self._fallback_analysis(resume_data)

        # Build context from resume data
        skills = resume_data.get("skills", [])
        experience = resume_data.get("experience_years", 0)
        education = resume_data.get("education", [])
        name = resume_data.get("name", "the candidate")

        skills_str = ", ".join(skills[:20]) if skills else "No skills detected"
        edu_str = ", ".join(education) if education else "Not specified"

        system_prompt = """You are an expert career advisor and resume analyst.
Analyze resumes objectively and provide actionable feedback.
Be encouraging but honest about gaps. Use markdown formatting.
Keep your response under 400 words."""

        user_prompt = f"""Analyze this resume profile and provide structured feedback:

**Name:** {name}
**Experience:** {experience} years
**Education:** {edu_str}
**Skills ({len(skills)}):** {skills_str}

Provide analysis in this exact format:

## Strengths
[List 2-3 specific strengths based on the skills and experience]

## Areas to Improve
[List 2-3 specific areas that could be strengthened]

## Career Fit Assessment
[Brief assessment of what roles this person is suited for]

## Growth Potential
[1-2 sentences about career growth trajectory and recommendations]"""

        prompt = self._build_phi3_prompt(system_prompt, user_prompt)
        response = self._generate(prompt, max_new_tokens=600)

        return response if response else self._fallback_analysis(resume_data)

    def _fallback_analysis(self, resume_data: dict) -> str:
        """
        Generate a basic analysis without AI when model is unavailable.

        Args:
            resume_data: Resume data dictionary

        Returns:
            Basic markdown analysis
        """
        skills = resume_data.get("skills", [])
        experience = resume_data.get("experience_years", 0)

        # Categorize skills
        programming = [s for s in skills if s in ["python", "java", "javascript", "typescript", "c++", "go", "rust"]]
        ml_skills = [s for s in skills if s in ["tensorflow", "pytorch", "scikit-learn", "deep learning", "machine learning"]]
        cloud_skills = [s for s in skills if s in ["aws", "azure", "gcp", "docker", "kubernetes"]]

        analysis = f"""## Resume Analysis

### Strengths
- **Technical breadth:** {len(skills)} skills identified across multiple domains
- **Programming:** {', '.join(programming) if programming else 'Consider highlighting programming languages'}
{"- **ML/AI expertise:** " + ', '.join(ml_skills) if ml_skills else ""}
{"- **Cloud/DevOps:** " + ', '.join(cloud_skills) if cloud_skills else ""}

### Areas to Improve
{"- Consider adding cloud certifications (AWS/GCP/Azure)" if not cloud_skills else ""}
{"- Deep learning frameworks would strengthen ML profile" if not ml_skills and programming else ""}
- Ensure your resume quantifies achievements with metrics
- Tailor skill keywords to target job descriptions

### Career Fit Assessment
Based on {experience} years of experience and your skill set, you appear well-suited for
{"senior technical roles" if experience >= 5 else "mid-level positions" if experience >= 2 else "entry-level or junior positions"}.

### Growth Potential
{"With your strong foundation, focus on specialization and leadership skills." if experience >= 5 else "Continue building depth in your core skills while exploring adjacent technologies."}

---
*Note: This is a basic analysis. Enable the AI model for deeper insights.*"""

        return analysis

    def generate_cover_letter_tips(self, resume_data: dict, target_role: str) -> str:
        """
        Generate specific cover letter tips for a target role.

        Args:
            resume_data: Resume data dictionary
            target_role: The role being applied for

        Returns:
            3 specific cover letter tips
        """
        if not self._loaded:
            return self._fallback_cover_letter_tips(target_role)

        skills = resume_data.get("skills", [])[:15]
        experience = resume_data.get("experience_years", 0)

        system_prompt = """You are an expert career coach specializing in tech cover letters.
Provide specific, actionable advice for cover letter writing.
Be concise and practical."""

        user_prompt = f"""A candidate with {experience} years of experience and skills in
{', '.join(skills)} is applying for a {target_role} position.

Provide exactly 3 specific tips for writing their cover letter.
Each tip should be 1-2 sentences. Number them 1, 2, 3.
Focus on how to highlight relevant skills and experience for this specific role."""

        prompt = self._build_phi3_prompt(system_prompt, user_prompt)
        response = self._generate(prompt, max_new_tokens=300)

        return response if response else self._fallback_cover_letter_tips(target_role)

    def _fallback_cover_letter_tips(self, target_role: str) -> str:
        """Fallback cover letter tips when AI is unavailable."""
        return f"""**Cover Letter Tips for {target_role}:**

1. **Lead with relevance:** Start by mentioning a specific skill or achievement directly related to {target_role}. Show you understand what the role requires.

2. **Quantify your impact:** Instead of listing responsibilities, highlight specific outcomes. Use numbers: "Improved pipeline efficiency by 40%" is stronger than "Worked on data pipelines."

3. **Show enthusiasm for the company:** Research the company and mention something specific that excites you about their work or mission. This shows genuine interest beyond just needing a job."""

    def answer_career_question(self, question: str, resume_context: dict) -> str:
        """
        Answer a specific career question with resume context.

        Args:
            question: The user's career question
            resume_context: Resume data for personalization

        Returns:
            AI-generated answer
        """
        if not self._loaded:
            return "I'd love to help with your career question, but the AI model isn't loaded yet. Please wait for model initialization or try again later."

        skills = resume_context.get("skills", [])[:15]
        experience = resume_context.get("experience_years", 0)

        system_prompt = """You are CareerMind AI, an expert career counselor for tech professionals.
Give practical, actionable advice based on the person's background.
Be concise (under 150 words) and encouraging."""

        context_str = f"(Background: {experience}yrs experience, skills: {', '.join(skills)})"

        user_prompt = f"""{context_str}

Question: {question}

Provide a helpful, personalized answer:"""

        prompt = self._build_phi3_prompt(system_prompt, user_prompt)
        return self._generate(prompt, max_new_tokens=250)

    def generate_interview_tips(self, target_role: str, skills: list[str]) -> str:
        """
        Generate interview preparation tips for a specific role.

        Args:
            target_role: Role being interviewed for
            skills: Candidate's skills

        Returns:
            Interview preparation advice
        """
        if not self._loaded:
            return f"""**Interview Tips for {target_role}:**

1. Review fundamentals of your top skills: {', '.join(skills[:5])}
2. Prepare STAR-format stories for behavioral questions
3. Practice system design or coding problems relevant to the role
4. Research the company's tech stack and recent projects
5. Prepare thoughtful questions about team culture and growth"""

        system_prompt = """You are a tech interview coach with experience at top companies.
Provide specific, actionable interview preparation tips.
Be encouraging and practical."""

        user_prompt = f"""A candidate skilled in {', '.join(skills[:10])} is preparing for
a {target_role} interview.

Provide 5 specific preparation tips. Be concrete and actionable.
Include both technical and behavioral preparation."""

        prompt = self._build_phi3_prompt(system_prompt, user_prompt)
        return self._generate(prompt, max_new_tokens=400)


# ============================================================================
# Singleton instance
# ============================================================================

_analyzer_instance = None
_analyzer_lock = Lock()


def get_analyzer() -> PhiResumeAnalyzer:
    """Get or create the singleton PhiResumeAnalyzer instance."""
    global _analyzer_instance
    with _analyzer_lock:
        if _analyzer_instance is None:
            _analyzer_instance = PhiResumeAnalyzer()
    return _analyzer_instance


# ============================================================================
# TEST / DEBUG
# ============================================================================

if __name__ == "__main__":
    print("PhiResumeAnalyzer Test")
    print("=" * 50)

    analyzer = PhiResumeAnalyzer()

    print("Loading model (this may take a few minutes)...")

    def progress(msg):
        print(f"  {msg}")

    success = analyzer.load_model(progress_callback=progress)

    if success:
        print(f"\nModel loaded: {analyzer.get_model_info()}")

        # Test with sample resume
        test_resume = {
            "name": "John Doe",
            "skills": ["python", "pytorch", "sql", "docker", "aws", "pandas", "git"],
            "experience_years": 3,
            "education": ["Stanford University"]
        }

        print("\n--- Resume Analysis ---")
        analysis = analyzer.analyze_resume(test_resume)
        print(analysis)

        print("\n--- Cover Letter Tips ---")
        tips = analyzer.generate_cover_letter_tips(test_resume, "Machine Learning Engineer")
        print(tips)

    else:
        print("\nModel loading failed. Testing fallback responses...")

        test_resume = {
            "skills": ["python", "pandas", "sql"],
            "experience_years": 2,
            "education": []
        }

        print("\n--- Fallback Analysis ---")
        print(analyzer._fallback_analysis(test_resume))
