#!/bin/bash
# CareerMind AI - Setup Script
# Run this script to install all dependencies

echo "🧠 CareerMind AI Setup"
echo "======================"
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1,2)
required_version="3.10"

echo "📋 Checking Python version..."
if python3 -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)" 2>/dev/null; then
    echo "✅ Python $python_version detected (required: $required_version+)"
else
    echo "❌ Python 3.10+ is required. Please install it first."
    exit 1
fi

echo ""
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies. Check your pip configuration."
    exit 1
fi

echo ""
echo "🔤 Downloading spaCy English model..."
python -m spacy download en_core_web_sm

if [ $? -ne 0 ]; then
    echo "⚠️  spaCy model download failed. Trying alternative method..."
    pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl
fi

echo ""
echo "🔍 Checking Ollama installation..."
if command -v ollama &> /dev/null; then
    echo "✅ Ollama is installed"
    echo "   Checking for mistral model..."
    if ollama list | grep -q "mistral"; then
        echo "✅ mistral model is available"
    else
        echo "⚠️  mistral model not found. Install it with: ollama pull mistral"
    fi
else
    echo "⚠️  Ollama is not installed."
    echo "   The chatbot will use the Phi-3 fallback instead."
    echo "   To install Ollama: https://ollama.ai/download"
fi

echo ""
echo "============================================"
echo "✅ Setup complete!"
echo ""
echo "🚀 To start CareerMind AI, run:"
echo "   python app.py"
echo ""
echo "🌐 Then open: http://127.0.0.1:7860"
echo "============================================"
