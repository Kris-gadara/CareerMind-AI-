# 🧠 CareerMind AI

> **Your Intelligent Offline Career Advisor - 100% Local, 100% Private**

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Gradio](https://img.shields.io/badge/Gradio-6.9-orange.svg)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen.svg)

CareerMind AI is a comprehensive, production-ready career intelligence system that runs **100% locally**. It uses free HuggingFace models (Microsoft Phi-3) and Ollama for AI-powered career guidance without sending your data to external servers or APIs.

---

## 🎯 Key Features

### 📄 Resume Analysis
- **PDF Upload & Parsing** - Extract text from any PDF resume
- **Skill Detection** - Automatically identify 370+ technical skills
- **Experience Estimation** - Calculate years of experience from job history
- **AI-Powered Insights** - Get detailed resume analysis from Phi-3 model

### 📊 Skill Gap Analysis
- **18+ Tech Roles** - Compare against Data Scientist, ML Engineer, DevOps, etc.
- **Match Scoring** - See your skill overlap percentage
- **Learning Paths** - Get curated courses and resources for missing skills
- **Time Estimates** - Know how long it takes to bridge the gap

### 💰 Salary Prediction
- **Market Rates** - Predict salary based on role, experience, and location
- **35+ Locations** - US cities, international markets, remote work
- **Skill Premiums** - See how high-value skills affect compensation
- **Salary Ranges** - Get min/max estimates with confidence levels

### 💬 Career Chat
- **AI Counselor** - Interactive chat with Ollama (mistral/llama2) or Phi-3
- **Natural Language** - Ask anything in plain English
- **Personalized Advice** - Context-aware based on your resume
- **Rule-Based Fallback** - Works even without AI models loaded

### 🗺️ Career Roadmap
- **Role Recommendations** - Discover careers that match your skills
- **Transition Plans** - Step-by-step roadmaps to target roles
- **Phase-Based Learning** - Organized into manageable time blocks
- **Actionable Steps** - Concrete activities for each phase

---

## 🚀 Quick Start

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/careermind-ai.git
cd careermind-ai

# 2. Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR: venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download spaCy model
python -m spacy download en_core_web_sm

# 5. Run the application
python app.py
```

**Open:** http://127.0.0.1:7860

---

## 📋 Prerequisites

### Required
- **Python 3.10+** (tested on 3.10, 3.11)
- **4GB+ RAM** (8GB recommended for AI models)
- **5GB+ disk space** (for model downloads on first run)
- **Windows, macOS, or Linux**

### Optional but Recommended
- **Ollama** - For interactive chatbot (faster, better responses)
- **NVIDIA GPU** - 5-10x faster AI inference
- **Internet** - Only for initial model downloads (then fully offline)

---

## 🎮 Usage Guide

### Tab 1: Resume Analysis

1. **Upload Resume**
   - Click "Upload Resume (PDF)"
   - Select your PDF file
   - Click "Analyze Resume"

2. **View Results**
   - **Left Panel**: Extracted info (name, skills, experience, education)
   - **Right Panel**: AI analysis with strengths, areas to improve, career fit

3. **What Gets Extracted**
   - Name, email, phone, LinkedIn, GitHub
   - 370+ skills (Python, AWS, Docker, React, etc.)
   - Years of experience (from date ranges)
   - Education institutions

### Tab 2: Skill Gap Analysis

1. **Select Target Role**
   - Choose from 18 tech roles (Data Scientist, ML Engineer, etc.)
   - Click "Analyze Gap"

2. **Understand Results**
   - **Match Score**: Your skill overlap percentage (0-100%)
   - **You Have**: Skills you already possess
   - **Missing Required**: Critical skills to learn
   - **Nice to Have**: Optional but valuable skills
   - **Learning Path**: Courses and resources with time estimates

3. **Readiness Levels**
   - **Ready** (90%+): Start applying!
   - **Intermediate** (70-89%): 2-4 months away
   - **Developing** (40-69%): 4-8 months of learning
   - **Beginner** (<40%): 6-12 months recommended

### Tab 3: Salary Prediction

1. **Enter Details**
   - **Role**: Select target job title
   - **Experience**: Enter years (e.g., "3 years")
   - **Location**: Choose from 35+ locations

2. **Get Estimate**
   - Click "Predict Salary"
   - View salary range, market median, breakdown
   - **Tip**: See how adding skills increases value

3. **Understanding Predictions**
   - **Source**: ML model (if loaded) or rule-based
   - **Confidence**: High/Medium/Low
   - **Breakdown**: Base salary + experience + location + skills

### Tab 4: Career Chat

1. **Ask Anything**
   - Type questions naturally: "How do I improve my resume?"
   - No special format needed - plain English works!

2. **Example Questions**
   - "What skills should I learn for data science?"
   - "How do I negotiate salary?"
   - "What are good interview preparation tips?"
   - "How can I transition from analyst to engineer?"

3. **Chat Features**
   - Remembers conversation context
   - Personalized based on your resume
   - Works with Ollama (preferred) or Phi-3 fallback
   - Clear button to start fresh

### Tab 5: Career Roadmap

1. **Get Recommendations**
   - Click "Get Career Recommendations"
   - See top 3 roles that match your skills

2. **Generate Roadmap**
   - Select target role from dropdown
   - Click "Generate Roadmap"

3. **Follow Your Plan**
   - **Phase-based**: Organized into learning phases
   - **Time estimates**: Weeks per phase, months total
   - **Resources**: Specific courses for each skill
   - **Activities**: Actionable steps (projects, networking, etc.)

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file (copy from `.env.example`):

```bash
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral

# Force CPU-only mode (if GPU issues)
FORCE_CPU=false

# Gradio Server
GRADIO_SERVER_NAME=127.0.0.1
GRADIO_SERVER_PORT=7860

# Debug Mode
DEBUG=false
```

### Installing Ollama (Optional)

Ollama provides the best chatbot experience. It's free and runs locally.

**Windows:**
```bash
# Download from: https://ollama.ai/download
# Then run:
ollama serve
ollama pull mistral
```

**macOS:**
```bash
brew install ollama
ollama serve
ollama pull mistral
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve
ollama pull mistral
```

**Alternative Models:**
```bash
ollama pull llama2        # Meta's Llama 2
ollama pull codellama     # Code-focused
ollama pull llama2:13b    # Larger, better quality
```

### Using Your Own Salary Model

CareerMind includes rule-based salary prediction, but you can plug in your own ML model:

```python
# 1. Train your model (scikit-learn)
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor()
model.fit(X_train, y_train)

# 2. Save it
import pickle
with open('careermind-ai/models/salary_model.pkl', 'wb') as f:
    pickle.dump(model, f)

# 3. Optionally save encoders
with open('careermind-ai/models/label_encoders.pkl', 'wb') as f:
    pickle.dump(encoders, f)

# 4. Restart CareerMind AI
```

The app will automatically detect and use your model!

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Gradio Web UI (Port 7860)                 │
│  ┌────────────┬────────────┬──────────┬──────────┬────────┐ │
│  │  Resume    │  Skill Gap │  Salary  │  Career  │ Road-  │ │
│  │  Analysis  │  Analysis  │  Predict │  Chat    │ map    │ │
│  └─────┬──────┴──────┬─────┴────┬─────┴────┬─────┴───┬────┘ │
└────────┼─────────────┼──────────┼──────────┼─────────┼──────┘
         │             │          │          │         │
         ▼             ▼          ▼          ▼         ▼
┌────────────────────────────────────────────────────────────┐
│                    Utils Package                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐ │
│  │ parser   │  │skill_gap │  │  salary  │  │   career   │ │
│  │  .py     │  │   .py    │  │   .py    │  │recommender │ │
│  └──────────┘  └──────────┘  └──────────┘  └────────────┘ │
│  ┌───────────────────────┐  ┌──────────────────────────┐  │
│  │   phi_analyzer.py     │  │      chatbot.py          │  │
│  │  (HuggingFace Phi-3)  │  │   (Ollama Interface)     │  │
│  └───────────────────────┘  └──────────────────────────┘  │
└──────────┬─────────────────────────────┬──────────────────┘
           │                             │
           ▼                             ▼
    ┌──────────────┐            ┌─────────────────┐
    │ HuggingFace  │            │     Ollama      │
    │  Phi-3-mini  │            │  mistral/llama2 │
    │ (Downloaded) │            │ (Local Server)  │
    └──────────────┘            └─────────────────┘
```

---

## 📁 Project Structure

```
careermind-ai/
├── app.py                      # Main Gradio application (600+ lines)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── test_modules.py             # Unit tests for all modules
├── .env.example                # Environment template
├── setup.sh                    # Automated setup script
│
├── models/                     # ML models (optional)
│   ├── salary_model.pkl        # Your custom salary model
│   └── label_encoders.pkl      # Associated encoders
│
├── data/                       # Data files
│   └── job_skills_map.json     # 18 roles with skill requirements
│
├── utils/                      # Core modules
│   ├── __init__.py             # Package exports
│   ├── parser.py               # PDF parsing & skill extraction
│   ├── skill_gap.py            # Skill gap analysis engine
│   ├── salary_predictor.py     # Salary estimation
│   ├── career_recommender.py   # Career path recommendations
│   ├── phi_analyzer.py         # Phi-3 AI integration
│   └── chatbot.py              # Ollama chatbot interface
│
└── assets/                     # UI assets
    └── custom.css              # Dark theme styling
```

---

## 🧪 Testing

Run the included test suite:

```bash
# Test all modules (no AI models required)
python test_modules.py

# Output:
# [PASS] Parser
# [PASS] Skill Gap
# [PASS] Salary Predictor
# [PASS] Career Recommender
# [PASS] Phi Analyzer
# [PASS] Chatbot
# Total: 6/6 tests passed
```

---

## 🐛 Troubleshooting

### "CUDA out of memory"
**Solution:** Force CPU mode
```bash
# In .env file:
FORCE_CPU=true

# Or before running:
export FORCE_CPU=true  # Linux/Mac
set FORCE_CPU=true     # Windows
python app.py
```

### "Module not found: spacy model"
**Solution:**
```bash
python -m spacy download en_core_web_sm
```

### "Connection refused: Ollama"
**Solutions:**
1. Start Ollama server: `ollama serve`
2. Or use without Ollama (Phi-3 fallback works)

### Chat gives "Data incompatible with messages format"
**Solution:** This is now fixed! Clear your browser cache and reload.

### Resume parsing returns empty
**Solutions:**
1. Ensure PDF has selectable text (not scanned image)
2. Try re-saving PDF from a text editor
3. Use OCR tool to convert scanned PDF

### Model download is very slow
**Solutions:**
1. First download is 2-4GB (one-time)
2. Models cache in `~/.cache/huggingface/`
3. Ensure stable internet connection
4. Subsequent runs use cached models

### Port 7860 already in use
**Solution:**
```bash
# Change port in .env:
GRADIO_SERVER_PORT=7861

# Or directly:
python app.py --server-port 7861
```

### GPU not being used
**Solution:**
```bash
# Install CUDA-enabled PyTorch:
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

---

## ⚡ Performance Tips

1. **First Run is Slow**
   - Models download (2-4GB)
   - Subsequent runs are fast (models cached)

2. **Use GPU if Available**
   - 5-10x faster inference
   - Install CUDA + PyTorch GPU version

3. **Close Other Applications**
   - AI models need RAM (4-8GB)
   - Close browser tabs, IDEs during first load

4. **SSD Recommended**
   - Faster model loading from disk

5. **Ollama for Best Chat**
   - Faster than Phi-3
   - Better conversation quality
   - Easy to install (see above)

---

## 🔒 Privacy & Security

### 100% Local
- ✅ No data sent to external APIs
- ✅ No telemetry or tracking
- ✅ Your resume never leaves your machine
- ✅ All processing happens offline

### What Gets Stored
- **Locally Only:**
  - Your resume data (in memory, cleared on reload)
  - Chat history (in memory, cleared on reload)
  - AI models (cached in `~/.cache/`)

### Safe to Use With
- ✅ Confidential resumes
- ✅ Sensitive career information
- ✅ Company networks (no external calls)

---

## 🎨 Customization

### Adding New Roles

Edit `data/job_skills_map.json`:

```json
{
  "Your New Role": {
    "required_skills": ["skill1", "skill2", "skill3"],
    "nice_to_have": ["skill4", "skill5"],
    "avg_salary_usd": 120000,
    "description": "What this role does",
    "experience_levels": {
      "junior": {"years": [0, 2], "salary_mult": 0.75},
      "mid": {"years": [2, 5], "salary_mult": 1.0},
      "senior": {"years": [5, 10], "salary_mult": 1.3}
    }
  }
}
```

### Adding New Skills

Edit `utils/parser.py` and add to `SKILLS_VOCABULARY`:

```python
SKILLS_VOCABULARY = {
    "programming": [
        "python", "java", "your_new_skill"
    ],
    # ... more categories
}
```

### Changing Theme Colors

Edit `assets/custom.css`:

```css
:root {
    --cm-accent: #6c63ff;        /* Change to your color */
    --cm-bg-primary: #0f0f14;    /* Background color */
}
```

---

## 🤝 Contributing

Contributions welcome! Here's how:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Test** your changes (`python test_modules.py`)
4. **Commit** (`git commit -m 'Add AmazingFeature'`)
5. **Push** (`git push origin feature/AmazingFeature`)
6. **Open** a Pull Request

### Ideas for Contributions
- Add more job roles to `job_skills_map.json`
- Improve skill extraction patterns
- Add support for Word documents (.docx)
- Create a Docker container
- Add more learning resources
- Improve UI/UX

---

## 📜 License

MIT License - See [LICENSE](LICENSE) file for details.

Free for personal and commercial use.

---

## 🙏 Acknowledgments

### Models & Libraries
- [Microsoft Phi-3](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct) - Compact yet powerful LLM
- [Ollama](https://ollama.ai/) - Easy local LLM deployment
- [Gradio](https://gradio.app/) - Beautiful web UI framework
- [HuggingFace Transformers](https://huggingface.co/transformers/) - Model loading and inference
- [spaCy](https://spacy.io/) - NLP and entity extraction
- [PyPDF2](https://pypdf2.readthedocs.io/) - PDF text extraction

### Inspiration
- Career counselors and coaches
- Open-source community
- Privacy-focused AI movement

---

## 📞 Support

### Getting Help
- **GitHub Issues**: [Report bugs or request features](https://github.com/yourusername/careermind-ai/issues)
- **Discussions**: Ask questions in GitHub Discussions
- **Documentation**: This README and inline code comments

### Frequently Asked Questions

**Q: Do I need internet after installation?**
A: No! After models are downloaded, everything runs offline.

**Q: Is this better than ChatGPT for career advice?**
A: Different use case! This is specialized for career intelligence with resume analysis, salary prediction, and skill gap analysis. ChatGPT is general-purpose.

**Q: Can I use this commercially?**
A: Yes! MIT License allows commercial use.

**Q: What's the difference between Ollama and Phi-3?**
A: Ollama (mistral/llama2) is faster and gives better chat responses. Phi-3 is a fallback that's built-in. Both run locally.

**Q: How accurate are salary predictions?**
A: Rule-based estimates use industry averages. For better accuracy, train and plug in your own ML model using real salary data.

**Q: Can I add my company's internal roles?**
A: Yes! Edit `job_skills_map.json` to add custom roles and skill requirements.

---

## 🗺️ Roadmap

### Planned Features
- [ ] Word document (.docx) support
- [ ] LinkedIn profile import
- [ ] Cover letter generator
- [ ] Interview question generator
- [ ] Job description analyzer
- [ ] Docker container for easy deployment
- [ ] Mobile-responsive UI
- [ ] Multi-language support
- [ ] Export reports as PDF
- [ ] Compare multiple resumes

### Version History
- **v1.0.0** (Current) - Initial release with 5 core features
  - Resume analysis
  - Skill gap analysis
  - Salary prediction
  - Career chat
  - Career roadmap

---

## 💡 Tips for Best Results

### Resume Tips
- Use text-based PDFs (not scanned images)
- List skills clearly in a "Skills" section
- Include date ranges for work experience
- Add education institutions' full names

### Chat Tips
- Ask specific questions: "How do I learn Docker?" vs "Help me"
- Provide context: "I'm a junior developer wanting to..."
- Try different phrasings if you don't get a good answer
- Use the Resume Analysis tab first for personalized advice

### Skill Gap Tips
- Update your resume first (so analysis is accurate)
- Check multiple target roles (you might be closer than you think!)
- Focus on "required" skills before "nice-to-have"
- Follow the learning path links provided

### Salary Tips
- Select your actual location (not where you wish to work)
- Be honest about experience years
- Check the breakdown to understand the components
- Use estimates as negotiation data points, not absolute truth

---

## 🌟 Star History

If you find CareerMind AI helpful, please ⭐ star the repo!

---

**Built with ❤️ for your career success.**

**100% Local. 100% Private. 100% Yours.**
