#!/bin/bash
# Teacher1 Rasa-Compatible Environment Setup Script
# This script sets up Python 3.10 environment with full Rasa support

echo "🎓 Teacher1 Rasa-Compatible Setup"
echo "=================================="

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "❌ Conda is required but not installed"
    echo "Please install Anaconda or Miniconda first"
    exit 1
fi

echo "📋 Setting up Python 3.10 environment for Rasa compatibility..."

# Create new conda environment with Python 3.10
echo "Creating conda environment 'teacher1-rasa' with Python 3.10..."
conda create -n teacher1-rasa python=3.10 -y

# Activate the environment
echo "Activating environment..."
conda activate teacher1-rasa

# Install core dependencies
echo "Installing core dependencies..."
conda install -n teacher1-rasa numpy matplotlib flask -y

# Install additional packages via pip in the new environment
echo "Installing additional dependencies via pip..."
conda run -n teacher1-rasa pip install websockets flask-cors

# Install speech dependencies
echo "Installing speech dependencies..."
conda run -n teacher1-rasa pip install SpeechRecognition pyttsx3

# Install Rasa with Rasa-compatible Python
echo "Installing Rasa and related ML packages..."
conda run -n teacher1-rasa pip install rasa>=3.6.0 rasa-sdk>=3.6.0 tensorflow>=2.12.0 spacy>=3.4.0

echo ""
echo "✅ Setup completed!"
echo ""
echo "To use Teacher1 with full Rasa support:"
echo "  conda activate teacher1-rasa"
echo "  python setup.py"
echo ""
echo "To train Rasa model:"
echo "  conda activate teacher1-rasa"
echo "  cd rasa_bot"
echo "  rasa train"
echo ""
echo "To run Teacher1 components:"
echo "  conda activate teacher1-rasa" 
echo "  python rasa_bot/chatbot_integration.py"