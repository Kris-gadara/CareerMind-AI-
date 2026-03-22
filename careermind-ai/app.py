"""
CareerMind AI - Main Application
=================================
A comprehensive offline career intelligence system built with Gradio.
Uses HuggingFace Phi-3 for analysis and Ollama for interactive chat.

Run with: python app.py
Then visit: http://127.0.0.1:7860
"""

import os
import gradio as gr
import pandas as pd
from pathlib import Path
from threading import Thread

# Import our utility modules
from utils.parser import parse_resume, format_resume_summary
from utils.skill_gap import (
    get_available_roles,
    analyze_skill_gap,
    get_best_matching_roles,
    generate_learning_path,
    calculate_total_learning_time
)
from utils.salary_predictor import get_predictor, LOCATION_MULTIPLIERS
from utils.career_recommender import (
    recommend_careers,
    generate_career_roadmap,
    guess_current_role
)
from utils.phi_analyzer import get_analyzer
from utils.chatbot import get_chatbot


# ============================================================================
# CUSTOM CSS
# ============================================================================

CUSTOM_CSS = """
/* Dark Professional Theme */
:root {
    --bg-primary: #0f0f14;
    --bg-secondary: #1a1a24;
    --bg-tertiary: #252532;
    --accent: #6c63ff;
    --accent-hover: #5a52e0;
    --text-primary: #e8e8f0;
    --text-secondary: #a0a0b0;
    --success: #4ade80;
    --warning: #fbbf24;
    --error: #f87171;
    --border: #3a3a4a;
}

/* Main container */
.gradio-container {
    background: var(--bg-primary) !important;
    max-width: 1400px !important;
}

/* Headers */
h1, h2, h3, h4 {
    color: var(--text-primary) !important;
}

.main-header {
    text-align: center;
    padding: 20px;
    background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
    border-radius: 12px;
    margin-bottom: 20px;
    border: 1px solid var(--border);
}

.main-header h1 {
    font-size: 2.5em;
    margin-bottom: 10px;
    background: linear-gradient(135deg, var(--accent), #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Tabs */
.tab-nav {
    background: var(--bg-secondary) !important;
    border-radius: 8px !important;
    padding: 8px !important;
}

.tab-nav button {
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
}

.tab-nav button.selected {
    background: var(--accent) !important;
    color: white !important;
}

/* Cards/Panels */
.info-panel {
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px;
    margin: 10px 0;
}

/* Skill badges */
.skill-badge {
    display: inline-block;
    background: var(--accent);
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    margin: 4px;
    font-size: 0.9em;
}

.skill-badge.missing {
    background: var(--error);
}

.skill-badge.nice {
    background: var(--warning);
    color: #1a1a24;
}

/* Progress bars */
.match-score {
    font-size: 2em;
    font-weight: bold;
    color: var(--accent);
}

/* Chat interface */
.chatbot {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}

/* Buttons */
.primary-btn {
    background: var(--accent) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
}

.primary-btn:hover {
    background: var(--accent-hover) !important;
}

/* Status indicators */
.status-ready {
    color: var(--success);
}

.status-loading {
    color: var(--warning);
}

.status-error {
    color: var(--error);
}

/* Tables */
table {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--border) !important;
}

th {
    background: var(--bg-tertiary) !important;
    color: var(--text-primary) !important;
}

td {
    color: var(--text-secondary) !important;
}

/* Markdown rendering */
.markdown-text {
    color: var(--text-secondary) !important;
}

.markdown-text h2 {
    color: var(--accent) !important;
    border-bottom: 1px solid var(--border);
    padding-bottom: 8px;
}

/* Footer */
.footer {
    text-align: center;
    padding: 20px;
    color: var(--text-secondary);
    font-size: 0.9em;
}
"""


# ============================================================================
# GLOBAL STATE
# ============================================================================

# Initialize components
phi_analyzer = get_analyzer()
salary_predictor = get_predictor()
chatbot = None  # Initialized after Phi analyzer loads


def initialize_ai_models(progress=gr.Progress()):
    """Initialize AI models in background."""
    global chatbot

    progress(0, desc="Starting CareerMind AI...")

    # Load Phi analyzer
    def phi_progress(msg):
        print(f"[Phi] {msg}")

    progress(0.2, desc="Loading AI model (this may take a few minutes)...")
    phi_analyzer.load_model(progress_callback=phi_progress)

    progress(0.8, desc="Initializing chatbot...")
    chatbot = get_chatbot(fallback_analyzer=phi_analyzer)

    progress(1.0, desc="Ready!")

    model_info = phi_analyzer.get_model_info()
    chat_status = chatbot.get_status()

    return f"AI Model: {model_info.get('model', 'Not loaded')} | Chatbot: {chat_status}"


# ============================================================================
# TAB 1: RESUME ANALYSIS
# ============================================================================

def process_resume(file, progress=gr.Progress()):
    """
    Process uploaded resume and generate analysis.

    Returns multiple outputs for the UI components.
    """
    if file is None:
        return (
            "Please upload a PDF resume.",  # status
            "",  # name
            "",  # skills
            "",  # experience
            "",  # education
            "",  # ai_analysis
            None  # state
        )

    progress(0.2, desc="Parsing resume...")

    # Parse the resume
    resume_data = parse_resume(file.name)

    if not resume_data.get("parse_success"):
        return (
            f"Error: {resume_data.get('error', 'Unknown error')}",
            "", "", "", "", "", None
        )

    progress(0.5, desc="Extracting information...")

    # Format extracted info
    name = resume_data.get("name", "Not detected")
    skills = resume_data.get("skills", [])
    skills_str = ", ".join(skills) if skills else "No skills detected"
    experience = f"{resume_data.get('experience_years', 0)} years"
    education = ", ".join(resume_data.get("education", [])) or "Not detected"

    progress(0.7, desc="Generating AI analysis...")

    # Generate AI analysis
    if phi_analyzer.is_loaded():
        ai_analysis = phi_analyzer.analyze_resume(resume_data)
    else:
        ai_analysis = format_resume_summary(resume_data)

    progress(1.0, desc="Complete!")

    # Set chatbot context
    if chatbot:
        chatbot.set_resume_context(resume_data)

    status = f"Successfully parsed resume with {len(skills)} skills detected."

    return (
        status,
        name,
        skills_str,
        experience,
        education,
        ai_analysis,
        resume_data  # State for other tabs
    )


# ============================================================================
# TAB 2: SKILL GAP ANALYSIS
# ============================================================================

def run_skill_gap_analysis(target_role, resume_state):
    """
    Analyze skill gap for a target role.

    Returns formatted results for UI components.
    """
    if not resume_state:
        return (
            "Please upload and analyze a resume first.",
            0,
            "No resume data",
            "",
            "",
            "",
            pd.DataFrame()
        )

    user_skills = resume_state.get("skills", [])

    if not user_skills:
        return (
            "No skills found in resume.",
            0,
            "No skills detected",
            "",
            "",
            "",
            pd.DataFrame()
        )

    # Run analysis
    gap = analyze_skill_gap(user_skills, target_role)

    if gap.get("error"):
        return (
            f"Error: {gap['error']}",
            0,
            "Error",
            "",
            "",
            "",
            pd.DataFrame()
        )

    # Format results
    match_score = gap["match_score"]
    match_pct = int(match_score * 100)

    # Matched skills HTML
    matched = gap.get("matched_skills", [])
    matched_html = " ".join([
        f'<span class="skill-badge">{s}</span>' for s in matched
    ]) if matched else "None"

    # Missing required HTML
    missing_req = gap.get("missing_required", [])
    missing_html = " ".join([
        f'<span class="skill-badge missing">{s}</span>' for s in missing_req
    ]) if missing_req else "All required skills covered!"

    # Nice to have HTML
    missing_nice = gap.get("missing_nice_to_have", [])
    nice_html = " ".join([
        f'<span class="skill-badge nice">{s}</span>' for s in missing_nice
    ]) if missing_nice else "None"

    readiness = gap.get("readiness_level", "Unknown")
    recommendation = gap.get("recommendation", "")

    # Generate learning path
    learning_path = generate_learning_path(missing_req[:5])
    time_est = calculate_total_learning_time(learning_path)

    # Create DataFrame for learning path table
    if learning_path:
        df = pd.DataFrame([
            {
                "Skill": item["skill"],
                "Resource": item["resource"],
                "Hours": item["estimated_hours"],
                "Priority": item["priority"].capitalize()
            }
            for item in learning_path
        ])
    else:
        df = pd.DataFrame(columns=["Skill", "Resource", "Hours", "Priority"])

    status = f"Analysis complete! Readiness: {readiness} ({match_pct}% match)"

    return (
        status,
        match_pct,
        f"**{readiness}** - {recommendation}",
        matched_html,
        missing_html,
        nice_html,
        df
    )


# ============================================================================
# TAB 3: SALARY PREDICTION
# ============================================================================

def predict_salary_handler(role, experience_str, location, resume_state):
    """
    Predict salary based on inputs.
    """
    # Parse experience
    try:
        experience = float(experience_str.split()[0]) if experience_str else 0
    except (ValueError, IndexError):
        experience = 0

    # Get skills from state or use empty list
    skills = resume_state.get("skills", []) if resume_state else []

    # Run prediction
    result = salary_predictor.predict(role, experience, skills, location)

    # Format output
    pred = result["predicted_salary"]
    range_min = result["salary_range"]["min"]
    range_max = result["salary_range"]["max"]

    salary_text = f"""
## Salary Estimate

### Predicted Salary: ${pred:,.0f}

**Range:** ${range_min:,.0f} - ${range_max:,.0f} USD

**Confidence:** {result['confidence'].capitalize()}
**Source:** {result['source'].replace('_', ' ').title()}

---

### Breakdown
"""

    breakdown = result.get("breakdown", {})
    if breakdown:
        salary_text += f"""
- **Base Salary:** ${breakdown.get('base_salary', 0):,.0f}
- **Experience Level:** {breakdown.get('experience_level', 'N/A')} ({breakdown.get('experience_multiplier', 1):.2f}x)
- **Location Multiplier:** {breakdown.get('location_multiplier', 1):.2f}x
- **Skill Premium:** ${breakdown.get('skill_premium', 0):,.0f}
"""
        premium_skills = breakdown.get("premium_skills", [])
        if premium_skills:
            salary_text += f"- **High-Value Skills:** {', '.join(premium_skills)}\n"

    # Add tip
    tip = result.get("tip", "")
    if tip:
        salary_text += f"\n---\n\n**Tip:** {tip}"

    # Market comparison
    comparison = salary_predictor.get_market_comparison(pred, role, location)
    if comparison.get("available"):
        salary_text += f"""

---

### Market Comparison

- **Market Median ({location}):** ${comparison['market_median']:,.0f}
- **Your Position:** {comparison['assessment'].title()} ({comparison['percentile']})
"""

    return salary_text


# ============================================================================
# TAB 4: CAREER CHATBOT
# ============================================================================

def chat_response(message, history, resume_state):
    """
    Handle chat messages with robust input handling.
    Accepts any input format - plain text, special characters, emojis, etc.
    Uses Gradio 6.x message format with role/content dictionaries.
    """
    global chatbot

    if chatbot is None:
        chatbot = get_chatbot(fallback_analyzer=phi_analyzer)

    # Sanitize and normalize input - accept any format
    if message is None:
        message = ""

    # Convert to string if not already
    if not isinstance(message, str):
        message = str(message)

    # Strip whitespace but preserve content
    message = message.strip()

    # Initialize history if needed - MUST be a list
    if history is None or not isinstance(history, list):
        history = []

    # Handle empty messages
    if not message:
        return history, ""

    # Ensure resume context is set
    if resume_state:
        chatbot.set_resume_context(resume_state)

    try:
        # Get response - the chatbot handles all text formats
        response = chatbot.chat(message)
    except Exception as e:
        response = f"I encountered an issue. Please try rephrasing: {str(e)[:50]}"

    # Add messages in Gradio 6.x message format
    # IMPORTANT: Each message MUST be a dict with 'role' and 'content'
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": response})

    return history, ""


def clear_chat():
    """Clear chat history and return empty list."""
    global chatbot
    if chatbot:
        chatbot.reset_conversation()
    # Return empty list for history and empty string for input
    return [], ""


# ============================================================================
# TAB 5: CAREER ROADMAP
# ============================================================================

def generate_roadmap_handler(target_role, resume_state):
    """
    Generate career roadmap.
    """
    if not resume_state:
        return "Please upload and analyze a resume first."

    skills = resume_state.get("skills", [])
    experience = resume_state.get("experience_years", 0)

    # Guess current role
    current_role = guess_current_role(skills)

    # Generate roadmap
    roadmap = generate_career_roadmap(
        current_role_guess=current_role,
        target_role=target_role,
        skills=skills,
        experience_years=experience
    )

    if roadmap.get("error"):
        return f"Error: {roadmap['error']}"

    # Format output
    output = f"""
## Career Roadmap: {current_role} to {target_role}

### Overview

- **Current Match Score:** {roadmap['current_match_score']*100:.0f}%
- **Current Readiness:** {roadmap['readiness_level']}
- **Estimated Time:** {roadmap['estimated_months']} months
- **Total Learning Hours:** {roadmap['total_learning_hours']} hours
- **Feasibility:** {roadmap['feasibility'].capitalize()}

---

"""

    # Add phases
    for phase in roadmap.get("phases", []):
        output += f"""
### Phase {phase['phase']}: {phase['title']}
**Duration:** {phase['duration_weeks']} weeks

"""
        # Skills to learn
        skills_to_learn = phase.get("skills_to_learn", [])
        if skills_to_learn:
            output += "**Skills to Learn:**\n"
            for skill_item in skills_to_learn:
                output += f"- **{skill_item['skill']}** (~{skill_item['hours']}h): {skill_item['resource']}\n"
            output += "\n"

        # Activities
        activities = phase.get("activities", [])
        if activities:
            output += "**Activities:**\n"
            for activity in activities:
                output += f"- {activity}\n"
            output += "\n"

    # Final advice
    output += f"""
---

### Final Advice

{roadmap.get('final_advice', '')}
"""

    return output


def get_career_recommendations(resume_state):
    """
    Get top career recommendations.
    """
    if not resume_state:
        return "Please upload and analyze a resume first."

    skills = resume_state.get("skills", [])
    experience = resume_state.get("experience_years", 0)

    recommendations = recommend_careers(skills, experience, top_n=3)

    if not recommendations:
        return "Could not generate recommendations. Please ensure your resume has skills extracted."

    output = "## Top Career Recommendations\n\n"

    for i, rec in enumerate(recommendations, 1):
        output += f"""
### {i}. {rec['role']}

**Match Score:** {rec['match_score']*100:.0f}% | **Experience Fit:** {rec['experience_fit'].capitalize()}
{f"**Average Salary:** ${rec['avg_salary']:,}" if rec.get('avg_salary') else ""}

{rec['reason']}

**Next Steps:**
"""
        for step in rec.get("next_steps", []):
            output += f"- {step}\n"

        output += "\n---\n"

    return output


# ============================================================================
# BUILD THE GRADIO UI
# ============================================================================

def build_app():
    """Construct the complete Gradio application."""

    # Create theme
    theme = gr.themes.Base(
        primary_hue="indigo",
        neutral_hue="slate",
    )

    with gr.Blocks(title="CareerMind AI") as app:

        # Header
        gr.HTML("""
        <div class="main-header">
            <h1>CareerMind AI</h1>
            <p style="color: #a0a0b0;">Your Intelligent Offline Career Advisor</p>
        </div>
        """)

        # Global state
        resume_state = gr.State(None)

        # Status bar
        with gr.Row():
            status_text = gr.Textbox(
                label="System Status",
                value="Initializing...",
                interactive=False,
                scale=4
            )
            init_btn = gr.Button("Initialize AI", variant="primary", scale=1)

        # Main tabs
        with gr.Tabs() as tabs:

            # ================================================================
            # TAB 1: Resume Analysis
            # ================================================================
            with gr.TabItem("Resume Analysis", id=1):
                gr.Markdown("### Upload your resume for AI-powered analysis")

                with gr.Row():
                    # Left column: Upload
                    with gr.Column(scale=1):
                        file_input = gr.File(
                            label="Upload Resume (PDF)",
                            file_types=[".pdf"],
                            type="filepath"
                        )
                        analyze_btn = gr.Button(
                            "Analyze Resume",
                            variant="primary"
                        )
                        parse_status = gr.Textbox(
                            label="Status",
                            interactive=False
                        )

                    # Right column: Extracted info
                    with gr.Column(scale=1):
                        name_output = gr.Textbox(label="Name", interactive=False)
                        exp_output = gr.Textbox(label="Experience", interactive=False)
                        edu_output = gr.Textbox(label="Education", interactive=False)
                        skills_output = gr.Textbox(
                            label="Skills",
                            interactive=False,
                            lines=3
                        )

                # AI Analysis
                gr.Markdown("### AI Analysis")
                ai_analysis_output = gr.Markdown(
                    value="*Upload a resume to see AI analysis*"
                )

                # Wire up analysis button
                analyze_btn.click(
                    fn=process_resume,
                    inputs=[file_input],
                    outputs=[
                        parse_status,
                        name_output,
                        skills_output,
                        exp_output,
                        edu_output,
                        ai_analysis_output,
                        resume_state
                    ]
                )

            # ================================================================
            # TAB 2: Skill Gap Analysis
            # ================================================================
            with gr.TabItem("Skill Gap", id=2):
                gr.Markdown("### Analyze your skill gap for target roles")

                with gr.Row():
                    role_dropdown = gr.Dropdown(
                        label="Select Target Role",
                        choices=get_available_roles(),
                        value="Machine Learning Engineer"
                    )
                    gap_btn = gr.Button("Analyze Gap", variant="primary")

                gap_status = gr.Textbox(label="Status", interactive=False)

                with gr.Row():
                    match_score_slider = gr.Slider(
                        label="Match Score",
                        minimum=0,
                        maximum=100,
                        value=0,
                        interactive=False
                    )

                readiness_output = gr.Markdown()

                with gr.Row():
                    with gr.Column():
                        gr.Markdown("#### You Have")
                        matched_skills_html = gr.HTML()

                    with gr.Column():
                        gr.Markdown("#### Missing Required")
                        missing_skills_html = gr.HTML()

                    with gr.Column():
                        gr.Markdown("#### Nice to Have")
                        nice_skills_html = gr.HTML()

                gr.Markdown("### Learning Path")
                learning_table = gr.DataFrame(
                    headers=["Skill", "Resource", "Hours", "Priority"],
                    interactive=False
                )

                gap_btn.click(
                    fn=run_skill_gap_analysis,
                    inputs=[role_dropdown, resume_state],
                    outputs=[
                        gap_status,
                        match_score_slider,
                        readiness_output,
                        matched_skills_html,
                        missing_skills_html,
                        nice_skills_html,
                        learning_table
                    ]
                )

            # ================================================================
            # TAB 3: Salary Prediction
            # ================================================================
            with gr.TabItem("Salary", id=3):
                gr.Markdown("### Estimate your market salary")

                with gr.Row():
                    salary_role = gr.Dropdown(
                        label="Role",
                        choices=get_available_roles(),
                        value="Software Engineer"
                    )
                    salary_exp = gr.Textbox(
                        label="Years of Experience",
                        value="3 years",
                        placeholder="e.g., 5 years"
                    )
                    salary_location = gr.Dropdown(
                        label="Location",
                        choices=list(LOCATION_MULTIPLIERS.keys()),
                        value="US - Other Major City"
                    )

                salary_btn = gr.Button("Predict Salary", variant="primary")

                salary_output = gr.Markdown(
                    value="*Fill in the fields above and click Predict Salary*"
                )

                salary_btn.click(
                    fn=predict_salary_handler,
                    inputs=[salary_role, salary_exp, salary_location, resume_state],
                    outputs=[salary_output]
                )

            # ================================================================
            # TAB 4: Career Chat
            # ================================================================
            with gr.TabItem("Career Chat", id=4):
                gr.Markdown("### Chat with your AI career counselor")

                chat_history = gr.Chatbot(
                    label="Conversation",
                    height=400,
                    value=[]  # Initialize with empty list
                )

                with gr.Row():
                    chat_input = gr.Textbox(
                        label="Your message",
                        placeholder="Ask me anything about your career...",
                        scale=4
                    )
                    send_btn = gr.Button("Send", variant="primary", scale=1)

                clear_btn = gr.Button("Clear Conversation")

                # Wire up chat
                send_btn.click(
                    fn=chat_response,
                    inputs=[chat_input, chat_history, resume_state],
                    outputs=[chat_history, chat_input]
                )

                chat_input.submit(
                    fn=chat_response,
                    inputs=[chat_input, chat_history, resume_state],
                    outputs=[chat_history, chat_input]
                )

                clear_btn.click(
                    fn=clear_chat,
                    outputs=[chat_history, chat_input]
                )

            # ================================================================
            # TAB 5: Career Roadmap
            # ================================================================
            with gr.TabItem("Roadmap", id=5):
                gr.Markdown("### Plan your career transition")

                with gr.Row():
                    with gr.Column():
                        rec_btn = gr.Button(
                            "Get Career Recommendations",
                            variant="secondary"
                        )
                        recommendations_output = gr.Markdown(
                            value="*Click to see recommended roles based on your resume*"
                        )

                gr.Markdown("---")

                with gr.Row():
                    roadmap_role = gr.Dropdown(
                        label="Target Role",
                        choices=get_available_roles(),
                        value="Machine Learning Engineer"
                    )
                    roadmap_btn = gr.Button("Generate Roadmap", variant="primary")

                roadmap_output = gr.Markdown(
                    value="*Select a target role and click Generate Roadmap*"
                )

                rec_btn.click(
                    fn=get_career_recommendations,
                    inputs=[resume_state],
                    outputs=[recommendations_output]
                )

                roadmap_btn.click(
                    fn=generate_roadmap_handler,
                    inputs=[roadmap_role, resume_state],
                    outputs=[roadmap_output]
                )

        # Footer
        gr.HTML("""
        <div class="footer">
            <p>CareerMind AI - Offline Career Intelligence System</p>
            <p>Powered by HuggingFace Transformers & Ollama</p>
        </div>
        """)

        # Initialize button handler
        init_btn.click(
            fn=initialize_ai_models,
            outputs=[status_text]
        )

    return app


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    print("""
    ===========================================================
    |                                                         |
    |              CareerMind AI                              |
    |        Offline Career Intelligence System               |
    |                                                         |
    ===========================================================
    |                                                         |
    |  Starting server...                                     |
    |  Open http://127.0.0.1:7860 in your browser             |
    |                                                         |
    |  Click "Initialize AI" to load the AI models            |
    |                                                         |
    ===========================================================
    """)

    # Build and launch the app
    app = build_app()

    app.launch(
        server_name=os.environ.get("GRADIO_SERVER_NAME", "127.0.0.1"),
        server_port=int(os.environ.get("GRADIO_SERVER_PORT", 7860)),
        share=False,
        show_error=True,
        quiet=False
    )
