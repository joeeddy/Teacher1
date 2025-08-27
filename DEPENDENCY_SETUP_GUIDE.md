# Teacher1 Dependency Setup Guide

## 🔍 Dependency Status Summary

This guide provides a comprehensive overview of the Teacher1 project dependencies and setup instructions.

### Current Status (as of dependency check)

**Environment:**
- Python Version: 3.12.3
- Platform: Ubuntu/Linux environment
- Package Manager: pip

**Critical Issues Identified:**
1. **Python Version Compatibility**: Rasa requires Python <3.11, but Python 3.12.3 is installed
2. **Missing System Packages**: tkinter not available (should be built-in)
3. **No Dependencies Installed**: All packages from requirements.txt are missing
4. **Project Module Import Failures**: All project modules fail due to missing dependencies

### Dependency Categories

#### ✅ Available
- `speech_recognition` (local project file - not the package)

#### ❌ Critical Missing
- numpy
- matplotlib  
- websockets
- flask
- flask-cors
- tensorflow
- spacy
- rasa (incompatible with Python 3.12)
- rasa-sdk (incompatible with Python 3.12)

#### ⚠️ Optional Missing
- pyaudio (audio input/output)
- pyttsx3 (text-to-speech)
- tkinter (GUI - should be built-in)

## 🚀 Setup Instructions

### Option 1: Python 3.12 Setup (No Rasa)

If you want to use Python 3.12 and don't need Rasa functionality:

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install python3-tk portaudio19-dev libasound2-dev

# Install Python packages
pip install -r requirements-python312.txt
```

**Note**: This setup excludes Rasa due to Python version incompatibility.

### Option 2: Python 3.10 Setup (Full Compatibility)

For full Rasa support, use Python 3.10:

```bash
# Install Python 3.10 using pyenv (recommended)
curl https://pyenv.run | bash
pyenv install 3.10.12
pyenv virtualenv 3.10.12 teacher1
pyenv activate teacher1

# Install system dependencies
sudo apt-get update
sudo apt-get install python3-tk portaudio19-dev libasound2-dev

# Install Python packages
pip install -r requirements-python310.txt

# Train Rasa model
cd rasa_bot
rasa train
```

### Option 3: Docker/Container Setup

Use the provided dev container configuration:

```bash
# Open in VS Code with Dev Containers extension
# Or build manually:
cd .devcontainer
docker build -t teacher1-dev .
docker run -it teacher1-dev
```

## 🧪 Testing Dependencies

Use the provided dependency checker tools:

```bash
# Comprehensive dependency check
python dependency_checker.py

# Detailed import analysis
python missing_deps_analysis.py

# Original test scripts
python .devcontainer/test_setup.py
python setup.py  # This will also attempt installation
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. "No module named 'tkinter'"

**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# CentOS/RHEL/Fedora
sudo yum install tkinter
# or
sudo dnf install python3-tkinter
```

#### 2. "No module named 'pyaudio'"

**Solution:**
```bash
# Install system dependencies first
# Ubuntu/Debian
sudo apt-get install portaudio19-dev

# macOS
brew install portaudio

# Then install Python package
pip install pyaudio
```

#### 3. Rasa Installation Fails (Python 3.12)

**Solution:** Use Python 3.10 or alternative chatbot framework.

#### 4. Import Errors in Project Modules

**Root Cause:** Missing dependencies (numpy, websockets, pyttsx3, etc.)

**Solution:** Install all required packages first, then test project modules.

### Project Module Dependencies

| Module | Requires | Status |
|--------|----------|--------|
| `big_text_gui.py` | tkinter | ❌ Missing |
| `fractal_modules.py` | numpy | ❌ Missing |
| `text_to_speech.py` | pyttsx3 | ❌ Missing |
| `websocket_communication.py` | websockets | ❌ Missing |
| `speech_recognition.py` | SpeechRecognition | ⚠️ Local file exists |

## 📋 Verification Checklist

After installation, verify setup:

- [ ] Python version compatible with requirements
- [ ] All packages from requirements.txt installed
- [ ] System packages (tkinter, audio libraries) available
- [ ] Project modules import successfully
- [ ] Rasa model trains successfully (if using Python 3.10)
- [ ] Web interface starts without errors
- [ ] WebSocket communication works
- [ ] Audio features functional (if needed)

## 🔧 Development Recommendations

1. **Use Python 3.10** for full compatibility with all features
2. **Use virtual environments** to avoid conflicts
3. **Install system dependencies** before Python packages
4. **Test incrementally** after each installation step
5. **Use the dependency checker** to verify setup

## 📞 Getting Help

If you encounter issues:

1. Run `python dependency_checker.py` for detailed analysis
2. Check the specific error messages for missing system packages
3. Ensure you're using a compatible Python version
4. Consider using the provided Docker/dev container setup

## 🔄 Alternative Solutions

If full setup is problematic:

1. **Web-only mode**: Install only flask, flask-cors for web interface
2. **Core features**: Install only numpy, matplotlib for basic functionality  
3. **No audio**: Skip pyaudio, pyttsx3 for headless operation
4. **Alternative AI**: Use different chatbot framework instead of Rasa