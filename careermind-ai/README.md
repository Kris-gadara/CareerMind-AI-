# CareerMind AI

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Gradio](https://img.shields.io/badge/Gradio-4.44-orange.svg)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

> **Your Intelligent Offline Career Advisor**

CareerMind AI is a comprehensive, production-ready career intelligence system that runs **100% locally**. It uses free HuggingFace models (Phi-3) and Ollama for AI-powered career guidance without sending your data to external servers.

---

## Features

- **Resume Analysis** - Upload PDF resumes and get AI-powered insights
- **Skill Gap Analysis** - Compare your skills against 18+ tech roles
- **Salary Prediction** - Get market salary estimates based on role, experience, and location
- **Career Recommendations** - Discover roles that match your skillset
- **Career Roadmap** - Get a structured learning path to reach your target role
- **AI Chatbot** - Interactive career counseling with Ollama/Phi-3

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Gradio Web UI                          │
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
│  └─────────┘ └───────────┘ └────────┘ └────────────────┘  │
│  ┌───────────────────┐  ┌─────────────────────────────┐   │
│  │  Phi-3 Analyzer   │  │     Ollama Chatbot          │   │
│  │  (HuggingFace)    │  │     (Local LLM)             │   │
│  └───────────────────┘  └─────────────────────────────┘   │
└───────────────────────────────────────────────────────────┘
        │                           │
        ▼                           ▼
┌───────────────────┐     ┌─────────────────────┐
│  HuggingFace      │     │      Ollama         │
│  Phi-3-mini       │     │   mistral/llama2    │
│  (Downloaded)     │     │   (Local Server)    │
└───────────────────┘     └─────────────────────┘
```

---

## Prerequisites

### Required

- **Python 3.10+**
- **4GB+ RAM** (8GB recommended for AI models)
- **5GB+ disk space** for model downloads

### Optional but Recommended

- **Ollama** - For the interactive chatbot
- **NVIDIA GPU** - For faster AI inference (CUDA)

---

## Installation

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/careermind-ai.git
cd careermind-ai

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Install spaCy Model

```bash
python -m spacy download en_core_web_sm
```

### 3. Install Ollama (Optional, for Chatbot)

#### Windows

Download from: https://ollama.ai/download

#### macOS

```bash
brew install ollama
```

#### Linux

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

After installation, start Ollama and pull a model:

```bash
ollama serve  # Start the server (run in separate terminal)
ollama pull mistral  # Download the mistral model
```

---

## Quick Start

```bash
# Navigate to the project directory
cd careermind-ai

# Run the application
python app.py

# Open in browser
# http://127.0.0.1:7860
```

### First-Time Setup

1. Click **"Initialize AI"** to load the Phi-3 model (takes 2-5 minutes on first run)
2. Upload a PDF resume in the **Resume Analysis** tab
3. Explore the other tabs to analyze skills, predict salary, and more!

---

## Usage Guide

### Tab 1: Resume Analysis

1. Click "Upload Resume (PDF)" and select your resume
2. Click "Analyze Resume"
3. View extracted information and AI-generated analysis

### Tab 2: Skill Gap

1. Select a target role from the dropdown
2. Click "Analyze Gap"
3. See matched skills, missing skills, and a learning path

### Tab 3: Salary

1. Select role, enter experience, and choose location
2. Click "Predict Salary"
3. View salary range and market comparison

### Tab 4: Career Chat

1. Type questions about your career
2. Get personalized advice based on your resume
3. Example questions:
   - "How can I transition to machine learning?"
   - "What skills should I learn next?"
   - "How do I prepare for technical interviews?"

### Tab 5: Roadmap

1. Click "Get Career Recommendations" to see suggested roles
2. Select a target role and click "Generate Roadmap"
3. Follow the phase-by-phase learning plan

---

## Using Your Own Salary Model

CareerMind AI includes a rule-based salary predictor, but you can plug in your own trained ML model:

1. Train a scikit-learn model that predicts salary
2. Save it as `models/salary_model.pkl`:
   ```python
   import pickle
   with open('models/salary_model.pkl', 'wb') as f:
       pickle.dump(your_model, f)
   ```
3. If using label encoders, save them as `models/label_encoders.pkl`
4. Restart the application

---

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and customize:

```bash
# Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral

# Force CPU-only mode
FORCE_CPU=false

# Gradio server
GRADIO_SERVER_NAME=127.0.0.1
GRADIO_SERVER_PORT=7860
```

---

## FAQ

### Q: What if Ollama isn't running?

**A:** The chatbot will automatically fall back to the Phi-3 model for responses. If neither is available, it uses rule-based responses.

### Q: The model download is taking forever

**A:** First-time model downloads can be 2-4GB. Ensure stable internet. After download, models are cached locally.

### Q: Can I use a different LLM for the chatbot?

**A:** Yes! Install any Ollama-compatible model:

```bash
ollama pull llama2:7b  # or any other model
```

Then set `OLLAMA_MODEL=llama2:7b` in your environment.

### Q: My GPU isn't being used

**A:** Ensure CUDA is properly installed for PyTorch:

```bash
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

### Q: Resume parsing missed my skills

**A:** The skill extraction uses keyword matching. Ensure your resume has skills clearly listed. You can extend the vocabulary in `utils/parser.py`.

---

## Project Structure

```
careermind-ai/
├── app.py                    # Main Gradio application
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── .env.example              # Environment template
├── setup.sh                  # Setup script
├── models/
│   ├── salary_model.pkl      # Optional: your ML model
│   └── label_encoders.pkl    # Optional: label encoders
├── data/
│   └── job_skills_map.json   # Role-skills mapping
├── utils/
│   ├── __init__.py
│   ├── parser.py             # Resume PDF parser
│   ├── skill_gap.py          # Skill gap analysis
│   ├── salary_predictor.py   # Salary estimation
│   ├── career_recommender.py # Career recommendations
│   ├── chatbot.py            # Ollama chatbot
│   └── phi_analyzer.py       # HuggingFace Phi-3
└── assets/
    └── custom.css            # UI styling
```

---

## Technical Details

### Models Used

- **Phi-3-mini-4k-instruct** (primary) - Microsoft's compact but powerful LLM
- **phi-2** (fallback) - Smaller Microsoft model
- **TinyLlama** (ultra-light fallback) - For low-resource environments
- **mistral** (Ollama) - For interactive chat

### Key Libraries

- **Gradio 4.44** - Web UI framework
- **Transformers 4.44** - HuggingFace model loading
- **spaCy 3.7** - NLP for entity extraction
- **PyPDF2** - PDF text extraction
- **scikit-learn** - ML utilities

---

## Performance Tips

1. **First run is slow** - Models need to download (2-4GB)
2. **Use GPU if available** - 5-10x faster inference
3. **Close other apps** - Models require significant RAM
4. **SSD recommended** - Faster model loading

---

## Troubleshooting

### "CUDA out of memory"

Add to your environment:

```bash
FORCE_CPU=true
```

### "Module not found: spacy model"

```bash
python -m spacy download en_core_web_sm
```

### "Connection refused: Ollama"

Start the Ollama server:

```bash
ollama serve
```

### Resume parsing returns empty

- Ensure the PDF contains selectable text (not scanned image)
- Try re-saving the PDF from a text editor

---

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

## License

MIT License - See LICENSE file for details.

---

## Acknowledgments

- [Microsoft Phi-3](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct)
- [Ollama](https://ollama.ai/)
- [Gradio](https://gradio.app/)
- [HuggingFace](https://huggingface.co/)
- [spaCy](https://spacy.io/)

---

**Built with AI, for your career.**
