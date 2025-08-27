# Teacher1 Setup Instructions

This document provides comprehensive setup instructions for the Teacher1 educational platform, addressing Python version compatibility and Rasa requirements.

## Current Environment Status

✅ **Working Components** (Python 3.13.5):
- Core mathematical operations (numpy 2.3.1)
- Plotting and visualization (matplotlib 3.10.0) 
- WebSocket communication (websockets 15.0.1)
- Web interface framework (Flask 3.1.0)
- AI fractal modules
- GUI applications (tkinter)

⚠️ **Limited Components**:
- Rasa chatbot (requires Python 3.8-3.11)
- Speech recognition/TTS (network installation issues)

## Setup Options

### Option 1: Use Current Environment (Partial Functionality)

**Best for**: Testing core features, AI components, web interface development

```bash
# Use the conda python that's already set up
/usr/share/miniconda/bin/python setup.py

# Test core functionality  
/usr/share/miniconda/bin/python fractal_emergent_ai.py
/usr/share/miniconda/bin/python big_text_gui.py
/usr/share/miniconda/bin/python websocket_demo.py --test
```

**Available Features**:
- ✅ Fractal AI system
- ✅ WebSocket communication
- ✅ Web interface development
- ✅ Mathematical plotting
- ✅ GUI applications
- ❌ Rasa chatbot
- ❌ Speech features (temporarily)

### Option 2: Full Rasa-Compatible Environment (Recommended)

**Best for**: Complete Teacher1 functionality including Rasa chatbot

#### Quick Setup:
```bash
# Run the automated setup script
./setup_rasa_environment.sh
```

#### Manual Setup:
```bash
# Create Python 3.10 environment
conda create -n teacher1-rasa python=3.10 -y

# Activate environment
conda activate teacher1-rasa

# Install core dependencies
conda install numpy matplotlib flask -y
pip install websockets flask-cors

# Install speech dependencies
pip install SpeechRecognition pyttsx3

# Install Rasa and ML packages
pip install rasa>=3.6.0 rasa-sdk>=3.6.0 tensorflow>=2.12.0 spacy>=3.4.0

# Setup and test
python setup.py
```

#### Usage:
```bash
# Always activate the environment first
conda activate teacher1-rasa

# Run setup and train Rasa
python setup.py
cd rasa_bot && rasa train

# Run Teacher1 components
python big_text_gui.py
python rasa_bot/chatbot_integration.py
python websocket_demo.py --both
```

### Option 3: Docker/DevContainer (Alternative)

Use the provided `.devcontainer` setup which includes Python 3.10 and all dependencies:

```bash
# Open in VS Code with Dev Containers extension
# Or use Docker directly
docker build -f .devcontainer/Dockerfile .
```

## Troubleshooting

### Common Issues:

1. **"Rasa not found"**
   - Solution: Use Python 3.10 environment (Option 2)

2. **"PyAudio installation failed"**
   - Solution: Install system audio libraries first:
   ```bash
   sudo apt-get install portaudio19-dev python3-dev
   ```

3. **"Network timeout during pip install"**
   - Solution: Try again later or use conda alternatives:
   ```bash
   conda install -c conda-forge package_name
   ```

4. **"Permission denied" errors**
   - Solution: Use user installation or conda environment
   ```bash
   pip install --user package_name
   ```

### Testing Your Setup:

```bash
# Test basic functionality
python -c "
import numpy, matplotlib, websockets, flask
print('✅ Core dependencies working')
"

# Test Rasa (if installed)
python -c "
try:
    import rasa
    print(f'✅ Rasa {rasa.__version__} available')
except ImportError:
    print('⚠️ Rasa not available - use Python 3.10 environment')
"

# Test speech (if installed)
python -c "
try:
    import pyttsx3, speech_recognition
    print('✅ Speech components available')
except ImportError:
    print('⚠️ Speech components not installed')
"
```

## Development Workflow

### For Core Development (Current Environment):
```bash
# Use current conda python
/usr/share/miniconda/bin/python your_script.py
```

### For Full Featured Development:
```bash
# Switch to Rasa environment
conda activate teacher1-rasa
python your_script.py
```

### For Production Deployment:
- Use the devcontainer configuration
- Or create deployment with Python 3.10 base image
- Ensure all system dependencies are installed

## Next Steps

1. Choose your preferred setup option based on needs
2. Run the appropriate setup commands
3. Test functionality with provided examples
4. Begin development with your chosen environment

For questions or issues, refer to the main README.md or the DEPENDENCY_INSTALLATION_REPORT.md for detailed status information.