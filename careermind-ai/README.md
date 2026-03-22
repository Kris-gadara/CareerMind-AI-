# 🧠 CareerMind AI - Complete Career Intelligence System

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Gradio](https://img.shields.io/badge/Gradio-6.9-orange.svg)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Production-green.svg)

> **Your Intelligent Offline Career Advisor - 100% Local, No Data Leaves Your Machine**

CareerMind AI is a comprehensive, production-ready career intelligence system that runs completely locally using free HuggingFace models (Phi-3) and Ollama. Get AI-powered career guidance, resume analysis, salary predictions, and personalized roadmaps without sending your data to external servers.

---

## 📸 Screenshots

```
┌─────────────────────────────────────────────────────────┐
│  CareerMind AI - Your Offline Career Intelligence       │
│                                                          │
│  Tab 1: Resume Analysis    Tab 2: Skill Gap             │
│  Tab 3: Salary Prediction  Tab 4: Career Chat           │
│  Tab 5: Career Roadmap                                  │
└─────────────────────────────────────────────────────────┘
```

---

## ✨ Features

### 🎯 Core Capabilities

| Feature | Description |
|---------|-------------|
| **Resume Analysis** | Upload PDF resumes and get AI-powered insights with skill extraction |
| **Skill Gap Analysis** | Compare your skills against 18+ tech roles with match scores |
| **Salary Prediction** | Get market salary estimates for 35+ locations worldwide |
| **Career Recommendations** | Discover roles that match your skillset with AI scoring |
| **Career Roadmap** | Generate structured learning paths to reach your target role |
| **AI Chatbot** | Interactive career counseling with Ollama/Phi-3 fallback |

### 🚀 What Makes It Special

- **100% Offline** - No data sent to external APIs
- **Free Models** - Uses Microsoft Phi-3 (HuggingFace) and Ollama
- **Smart Fallbacks** - Works even without AI models loaded
- **18 Tech Roles** - Comprehensive job market coverage
- **374 Skills** - Extensive skill vocabulary database
- **35 Locations** - Global salary data with regional multipliers
- **Curated Learning Paths** - Links to Coursera, Udemy, official docs

---

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
- [Configuration](#configuration)
- [Architecture](#architecture)
- [Advanced Features](#advanced-features)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Contributing](#contributing)
- [License](#license)

---

## 🔧 Prerequisites

### Required

- **Python 3.10+** (Python 3.11 recommended)
- **4GB+ RAM** (8GB recommended for AI models)
- **5GB+ disk space** (for model downloads on first run)
- **Internet connection** (only for initial model download)

### Optional but Recommended

- **Ollama** - For enhanced chatbot experience
  - Download: https://ollama.ai/download
  - Recommended models: `mistral`, `llama2:7b`, `phi3`
- **NVIDIA GPU** - For 5-10x faster AI inference (CUDA support)
- **SSD Storage** - Faster model loading and better performance

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | Dual-core 2.0 GHz | Quad-core 3.0+ GHz |
| RAM | 4 GB | 8+ GB |
| Storage | 5 GB free | 10+ GB SSD |
| GPU | - | NVIDIA GPU with 4GB+ VRAM |
| OS | Windows 10, macOS 11, Ubuntu 20.04+ | Latest versions |

---

## 📥 Installation

### Step 1: Clone the Repository

```bash
# Clone this repository
git clone https://github.com/yourusername/careermind-ai.git
cd careermind-ai
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# This installs:
# - Gradio 6.9+ (Web UI)
# - Transformers 4.44 (AI models)
# - spaCy 3.7+ (NLP)
# - PyPDF2 (PDF parsing)
# - And more...
```

### Step 4: Download spaCy Model

```bash
# Download English language model for spaCy
python -m spacy download en_core_web_sm
```

### Step 5: Install Ollama (Optional, for Enhanced Chat)

#### Windows
1. Download from https://ollama.ai/download
2. Run the installer
3. Open terminal and run:
```bash
ollama serve
ollama pull mistral
```

#### macOS
```bash
brew install ollama
ollama serve
ollama pull mistral
```

#### Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve
ollama pull mistral
```

---

## 🚀 Quick Start

### Run the Application

```bash
# Navigate to project directory
cd careermind-ai

# Start the application
python app.py

# Open in browser
# http://127.0.0.1:7860
```

### First-Time Setup (In Browser)

1. **Click "Initialize AI"** button
   - This loads the Phi-3 model (2-5 minutes on first run)
   - Models are cached for future use
   - Progress shown in status bar

2. **Upload a Resume** (Tab 1: Resume Analysis)
   - Click "Upload Resume (PDF)"
   - Select your PDF resume
   - Click "Analyze Resume"
   - View extracted skills and AI analysis

3. **Explore Features**
   - **Skill Gap** - Select target role, see missing skills
   - **Salary** - Get personalized salary estimate
   - **Career Chat** - Ask career questions naturally
   - **Roadmap** - Generate transition plan to new role

---

## 📖 Usage Guide

### Tab 1: Resume Analysis

**Upload and analyze your resume with AI**

```
1. Upload PDF Resume
   ├─ Accepts standard PDF format
   ├─ Scanned PDFs may have limited extraction
   └─ Max recommended size: 5MB

2. Click "Analyze Resume"
   ├─ Extracts: Name, Email, Phone, LinkedIn, GitHub
   ├─ Detects: 374 technical skills
   ├─ Estimates: Years of experience from dates
   └─ AI analyzes strengths and areas to improve

3. Review Results
   ├─ Personal info verification
   ├─ Skill list (click to see all)
   ├─ Experience summary
   └─ AI-powered recommendations
```

**Sample Skills Detected:**
- Programming: Python, JavaScript, Java, C++, Go, Rust
- ML/AI: TensorFlow, PyTorch, Scikit-learn, Transformers
- Data: Pandas, NumPy, SQL, Spark, Tableau, Power BI
- Cloud: AWS, Azure, GCP, Docker, Kubernetes, Terraform

### Tab 2: Skill Gap Analysis

**Compare your skills against any tech role**

```
1. Select Target Role
   └─ Choose from 18 roles:
      ├─ Machine Learning Engineer
      ├─ Data Scientist
      ├─ Data Analyst
      ├─ Backend/Frontend Developer
      ├─ DevOps Engineer
      ├─ And 13 more...

2. View Match Analysis
   ├─ Match Score: 0-100%
   ├─ Readiness Level: Beginner → Ready
   ├─ Matched Skills: What you have ✅
   ├─ Missing Required: Critical gaps ❌
   └─ Nice-to-Have: Bonus skills ⚡

3. Get Learning Path
   ├─ Prioritized skill list
   ├─ Curated learning resources
   ├─ Estimated hours per skill
   └─ Total timeline estimate
```

**Example Output:**
```
Role: Machine Learning Engineer
Match Score: 73%
Readiness: Intermediate

You Have (8 skills):
✅ Python, SQL, Git, Pandas, NumPy, Matplotlib, Jupyter, Statistics

Missing Required (3 skills):
❌ PyTorch, Docker, MLflow

Learning Path:
1. PyTorch → Fast.ai Course (50h)
2. Docker → Official Tutorial (20h)
3. MLflow → Documentation (15h)

Total: 85 hours (~2 months at 10h/week)
```

### Tab 3: Salary Prediction

**Get realistic salary estimates**

```
1. Input Parameters
   ├─ Role: Auto-filled from analysis
   ├─ Experience: Your years of experience
   └─ Location: Choose from 35 locations

2. View Prediction
   ├─ Predicted Salary: $X - $Y USD
   ├─ Market Median: Benchmark
   ├─ Percentile: Where you stand
   └─ Breakdown: How calculated

3. Salary Factors
   ├─ Base Role Salary
   ├─ Experience Multiplier (0.75x - 1.6x)
   ├─ Location Adjustment (0.18x - 1.35x)
   ├─ Premium Skills Bonus ($2-5k each)
   └─ Extra Skills Bonus ($1.5k each)
```

**Location Examples:**
- US - San Francisco: 1.35x multiplier
- US - New York: 1.25x
- US - Remote: 0.95x
- UK - London: 0.85x
- India - Bangalore: 0.25x

### Tab 4: Career Chat

**Ask anything about your career**

**Features:**
- Natural language input - type normally!
- Accepts any format (questions, statements, keywords)
- Handles typos and informal language
- Remembers context from your resume
- Smart fallbacks when AI unavailable

**Example Questions:**
```
"How do I prepare for a data science interview?"
"What skills should I learn to become a senior engineer?"
"How can I transition from analyst to ML engineer?"
"What's the average salary for DevOps in Seattle?"
"Review my resume" (after uploading)
"help me with salary negotiation"
"what are the best courses for learning react?"
```

**Chat Capabilities:**
- Resume tips and optimization
- Salary negotiation strategies
- Interview preparation
- Skill development advice
- Career transition planning
- Job search tactics
- Portfolio building

### Tab 5: Career Roadmap

**Plan your career transition**

```
1. Get Recommendations
   └─ Click "Get Career Recommendations"
      ├─ Top 3 matching roles based on your skills
      ├─ Match scores and reasoning
      ├─ Next steps for each role
      └─ Salary potential

2. Select Target Role
   └─ Choose from dropdown

3. Generate Roadmap
   ├─ Current vs Target comparison
   ├─ Estimated timeline (months)
   ├─ Phase-by-phase plan
   ├─ Skills to learn per phase
   ├─ Activities and milestones
   └─ Final success advice

4. Follow the Plan
   ├─ Phase 1: Core fundamentals (4-8 weeks)
   ├─ Phase 2: Advanced required skills
   ├─ Phase 3: Nice-to-have skills
   └─ Phase 4: Job application prep
```

**Sample Roadmap:**
```
Current: Data Analyst
Target: Machine Learning Engineer
Timeline: 6 months
Total Learning: 200 hours

Phase 1: Core ML Skills (8 weeks)
  - Learn: PyTorch, Neural Networks, Statistics
  - Resources: Fast.ai, Coursera ML Specialization
  - Project: Build image classifier

Phase 2: Engineering Skills (8 weeks)
  - Learn: Docker, MLflow, APIs
  - Resources: Official docs, tutorials
  - Project: Deploy model with FastAPI

Phase 3: Competitive Edge (4 weeks)
  - Learn: Transformers, LangChain,Kubernetes
  - Project: Full ML pipeline

Phase 4: Job Search (4 weeks)
  - Update resume/portfolio
  - Practice LeetCode (ML problems)
  - Apply to positions (5-10/week)
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env
```

Edit `.env` with your settings:

```bash
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral

# Force CPU-only mode (useful for limited GPU memory)
FORCE_CPU=false

# HuggingFace cache directory (optional)
# HF_HOME=/path/to/cache

# Gradio Server
GRADIO_SERVER_NAME=127.0.0.1
GRADIO_SERVER_PORT=7860

# Debug Mode
DEBUG=false
```

### Using Custom Salary Model

**You can plug in your own trained ML model:**

```python
# 1. Train your model (scikit-learn example)
from sklearn.ensemble import RandomForestRegressor
import pickle

model = RandomForestRegressor()
model.fit(X_train, y_train)

# 2. Save to models/ directory
with open('models/salary_model.pkl', 'wb') as f:
    pickle.dump(model, f)

# 3. Optionally save label encoders
with open('models/label_encoders.pkl', 'wb') as f:
    pickle.dump(encoders, f)

# 4. Restart CareerMind AI
# Your model will be automatically loaded!
```

### Customizing Job Roles

Edit `data/job_skills_map.json`:

```json
{
  "Your Custom Role": {
    "required_skills": ["skill1", "skill2", "skill3"],
    "nice_to_have": ["skill4", "skill5"],
    "avg_salary_usd": 120000,
    "description": "Your role description",
    "experience_levels": {
      "junior": {"years": [0, 2], "salary_mult": 0.75},
      "mid": {"years": [2, 5], "salary_mult": 1.0},
      "senior": {"years": [5, 10], "salary_mult": 1.3}
    }
  }
}
```

---

## 🏗️ Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      Gradio Web UI (Port 7860)              │
│  ┌──────────┬──────────┬────────┬──────────┬──────────┐    │
│  │  Resume  │   Skill  │ Salary │  Career  │ Roadmap  │    │
│  │ Analysis │   Gap    │        │   Chat   │          │    │
│  └────┬─────┴────┬─────┴───┬────┴────┬─────┴────┬─────┘    │
└───────┼──────────┼─────────┼─────────┼──────────┼──────────┘
        │          │         │         │          │
        ▼          ▼         ▼         ▼          ▼
┌───────────────────────────────────────────────────────────┐
│                     Utils Package                          │
│  ┌─────────┐ ┌───────────┐ ┌────────┐ ┌────────────────┐  │
│  │ Parser  │ │ Skill Gap │ │ Salary │ │ Career Recomm. │  │
│  │ (21 KB) │ │  (23 KB)  │ │(17 KB) │ │    (23 KB)     │  │
│  └─────────┘ └───────────┘ └────────┘ └────────────────┘  │
│  ┌───────────────────┐  ┌─────────────────────────────┐   │
│  │  Phi-3 Analyzer   │  │     Ollama Chatbot          │   │
│  │  (HuggingFace)    │  │     (Local LLM)             │   │
│  │     (20 KB)       │  │       (18 KB)               │   │
│  └───────────────────┘  └─────────────────────────────┘   │
└───────────────────────────────────────────────────────────┘
        │                           │
        ▼                           ▼
┌───────────────────┐     ┌─────────────────────┐
│  HuggingFace      │     │      Ollama         │
│  Phi-3-mini       │     │   mistral/llama2    │
│  (Downloaded)     │     │   (Local Server)    │
│  ~2-4GB           │     │   Port 11434        │
└───────────────────┘     └─────────────────────┘
```

### File Structure

```
careermind-ai/
├── app.py                      (600 lines) - Main Gradio application
├── requirements.txt            - Python dependencies
├── README.md                   - This file
├── .env.example                - Environment template
├── setup.sh                    - Automated setup script
├── test_modules.py             - Unit tests for all modules
│
├── models/                     - ML models (optional)
│   ├── salary_model.pkl        - Your trained model (optional)
│   └── label_encoders.pkl      - Feature encoders (optional)
│
├── data/                       - Static data files
│   └── job_skills_map.json     - 18 tech roles, 374 skills
│
├── utils/                      - Core business logic
│   ├── __init__.py             - Package exports
│   ├── parser.py               - PDF parsing + skill extraction
│   ├── skill_gap.py            - Gap analysis + learning paths
│   ├── salary_predictor.py     - Salary estimation engine
│   ├── career_recommender.py   - Career suggestions + roadmaps
│   ├── phi_analyzer.py         - HuggingFace Phi-3 integration
│   └── chatbot.py              - Ollama chat interface
│
└── assets/                     - UI assets
    └── custom.css              - Dark theme styles
```

### Data Flow

```
1. Resume Upload
   PDF → PyPDF2 → Raw Text → spaCy NER → Structured Data
   ↓
   Skills Extraction (374 vocab) → Resume State

2. Skill Gap
   Resume State + Target Role → job_skills_map.json
   ↓
   Match Scoring → Learning Path → Curated Resources

3. Salary Prediction
   Role + Experience + Location + Skills
   ↓
   ML Model (if available) OR Rule-based Algorithm
   ↓
   Salary Range + Market Comparison

4. Career Chat
   User Input → Ollama API (if running)
   ↓ (fallback)
   Phi-3 Analyzer (if loaded)
   ↓ (fallback)
   Rule-based Responses

5. Roadmap
   Current Skills + Target Role → Gap Analysis
   ↓
   Phase Generation → Learning Timeline → Final Advice
```

---

## 🎓 Advanced Features

### Running Tests

```bash
# Run all module tests
python test_modules.py

# Expected output:
# [PASS] Parser (6/6)
# [PASS] Skill Gap (6/6)
# [PASS] Salary Predictor (6/6)
# [PASS] Career Recommender (6/6)
# [PASS] Phi Analyzer (6/6)
# [PASS] Chatbot (6/6)
```

### Using Different AI Models

**Change Ollama Model:**
```bash
# Install a different model
ollama pull llama2:13b

# Set in environment
export OLLAMA_MODEL=llama2:13b

# Restart app
python app.py
```

**Change Phi Model:**

Edit `utils/phi_analyzer.py`:
```python
MODEL_OPTIONS = [
    "microsoft/Phi-3-mini-4k-instruct",  # Default
    "microsoft/Phi-3-medium-4k-instruct",  # Larger model
    "microsoft/phi-2",  # Smaller, faster
]
```

### Sharing the App

**Local Network Access:**
```python
# In app.py, change:
app.launch(
    server_name="0.0.0.0",  # Listen on all IPs
    server_port=7860,
    share=False
)
```

**Gradio Share (Temporary Public URL):**
```python
app.launch(share=True)
# Generates: https://xxxxx.gradio.live
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. "CUDA out of memory"

**Solution:**
```bash
# Force CPU mode
export FORCE_CPU=true
python app.py
```

#### 2. "Module not found: spacy model"

**Solution:**
```bash
python -m spacy download en_core_web_sm
```

#### 3. "Connection refused: Ollama"

**Solution:**
```bash
# Start Ollama server
ollama serve

# In another terminal:
ollama pull mistral
```

#### 4. "Resume parsing returns empty"

**Causes & Solutions:**
- **Scanned PDF (image-based):** Use OCR to convert to text PDF first
- **Encrypted PDF:** Remove encryption
- **Corrupted PDF:** Try re-saving from source

#### 5. "Port 7860 already in use"

**Solution:**
```bash
# Use different port
export GRADIO_SERVER_PORT=7861
python app.py
```

#### 6. "Model download is slow/fails"

**Solutions:**
```bash
# Use HuggingFace mirror (if in China)
export HF_ENDPOINT=https://hf-mirror.com

# Or download manually:
# Visit: https://huggingface.co/microsoft/Phi-3-mini-4k-instruct
# Download files to: ~/.cache/huggingface/
```

#### 7. "Gradio version compatibility error"

**Solution:**
```bash
# Upgrade to latest
pip install --upgrade gradio gradio-client

# Or use specific version
pip install gradio==6.9.0
```

### Performance Optimization

**Speed up model loading:**
```bash
# Use SSD for cache
export HF_HOME=/path/to/ssd/cache

# Use quantized models
# Already implemented in phi_analyzer.py
```

**Reduce memory usage:**
```python
# In phi_analyzer.py, use smaller model:
MODEL_OPTIONS = [
    "TinyLlama/TinyLlama-1.1B-Chat-v1.0",  # Only 1.1B params
]
```

---

## ❓ FAQ

**Q: Do I need an internet connection?**
A: Only for initial model download (~2-4GB). After that, 100% offline.

**Q: What if I don't have Ollama?**
A: The chat will automatically fall back to Phi-3 or rule-based responses.

**Q: Can I use this commercially?**
A: Check model licenses (Phi-3: MIT, Mistral: Apache 2.0). Code: MIT license.

**Q: How accurate are the salary predictions?**
A: Uses US-based 2024-2025 market data. Your location/company may vary ±20%.

**Q: Can it parse non-English resumes?**
A: Currently optimized for English. Spanish/French may work partially.

**Q: How do I add my company's custom roles?**
A: Edit `data/job_skills_map.json` with your roles and required skills.

**Q: Will this send my resume to OpenAI/Anthropic?**
A: No. Everything runs locally. Zero external API calls.

**Q: What's the difference between rule-based and ML salary prediction?**
A: Rule-based uses formula with industry averages. ML model learns from training data.

**Q: Can I export my career roadmap?**
A: Yes, use browser print/save or copy the markdown output.

---

## 🤝 Contributing

Contributions welcome! Here's how:

```bash
# 1. Fork the repository
# 2. Create feature branch
git checkout -b feature/amazing-feature

# 3. Make changes and test
python test_modules.py

# 4. Commit with clear message
git commit -m "Add amazing feature: description"

# 5. Push and create PR
git push origin feature/amazing-feature
```

**Contribution Ideas:**
- Add more job roles to `job_skills_map.json`
- Expand skill vocabulary in `parser.py`
- Add new learning resources in `skill_gap.py`
- Improve AI prompts in `phi_analyzer.py`
- Create new UI themes
- Write integration tests
- Add multilingual support

---

## 📜 License

MIT License - See [LICENSE](LICENSE) file for details.

This means you can:
- ✅ Use commercially
- ✅ Modify and distribute
- ✅ Use privately
- ✅ Use for patent purposes

**Model Licenses:**
- Microsoft Phi-3: MIT License
- Mistral: Apache 2.0 License

---

## 🙏 Acknowledgments

This project uses:
- [Microsoft Phi-3](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct) - AI analysis
- [Ollama](https://ollama.ai/) - Local LLM serving
- [Gradio](https://gradio.app/) - Web UI framework
- [HuggingFace Transformers](https://huggingface.co/) - Model loading
- [spaCy](https://spacy.io/) - NLP and entity extraction
- [PyPDF2](https://pypdf2.readthedocs.io/) - PDF text extraction

Special thanks to:
- All open-source contributors
- Career counselors who inspired this project
- Early testers and feedback providers

---

## 📞 Support & Contact

- **Issues:** [GitHub Issues](https://github.com/yourusername/careermind-ai/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/careermind-ai/discussions)
- **Email:** your.email@example.com

---

## 🗺️ Roadmap

**Current Version: 1.0.0**

### Planned Features (v1.1)
- [ ] Multi-language resume support (Spanish, French, German)
- [ ] Cover letter generator
- [ ] LinkedIn profile analyzer
- [ ] Job posting keyword matcher
- [ ] Interview question generator

### Future (v2.0)
- [ ] Voice chat interface
- [ ] Mobile app (React Native)
- [ ] Company culture fit analyzer
- [ ] Network/connection analyzer
- [ ] Automated job application tracker

---

## 📊 Project Stats

- **Total Lines of Code:** ~3,500
- **Modules:** 7 core utilities
- **Supported Roles:** 18 tech positions
- **Skills Database:** 374 technical skills
- **Locations:** 35 global markets
- **Learning Resources:** 50+ curated links
- **Test Coverage:** 6/6 modules passing

---

## 🌟 Star History

If you find this project useful, please consider giving it a star ⭐

---

**Built with AI, for your career. 🚀**

*Made with ❤️ by the CareerMind AI team*

---

## Quick Links

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Contributing](#contributing)

---

**Last Updated:** March 2026
**Version:** 1.0.0
**Status:** ✅ Production Ready
