# Teacher1 Development Container

This directory contains the VS Code Dev Container configuration for the Teacher1 project, providing a reproducible development environment with all necessary dependencies.

## What's Included

### System Dependencies
- **Python 3.10**: Compatible with rasa>=3.6.0 and all project requirements
- **PortAudio**: Required for `pyaudio` and speech recognition functionality
- **Tkinter**: GUI framework support (python3-tk)
- **Audio Tools**: ALSA utilities and PulseAudio for audio processing
- **Build Tools**: Essential development tools and compilers

### Python Dependencies
- All packages from `requirements.txt` are automatically installed
- Includes Rasa chatbot framework with compatible TensorFlow and spaCy versions
- WebSocket communication libraries
- Web interface dependencies (Flask)

### VS Code Extensions
- Python language support with IntelliSense
- Code formatting (Black, isort)
- Linting (Pylint)
- Jupyter notebook support

## Quick Start

1. **Open in VS Code**: Open this repository in VS Code
2. **Reopen in Container**: When prompted, click "Reopen in Container" or use Command Palette > "Dev Containers: Reopen in Container"
3. **Wait for Setup**: The container will build and install all dependencies automatically
4. **Start Developing**: All tools and dependencies are ready to use

## Port Forwarding

The container automatically forwards these ports:
- `8765`: Fractal AI WebSocket server
- `8766`: Rasa chatbot WebSocket server  
- `5000`: Flask web interface

## Audio Support

The container is configured with audio support for speech recognition and text-to-speech features:
- PortAudio libraries for microphone input
- PulseAudio for audio processing
- Proper user permissions for audio device access

## Manual Setup Alternative

If you prefer not to use Dev Containers, you can manually install dependencies:

```bash
# Install system dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y portaudio19-dev python3-tk alsa-utils

# Install Python dependencies
pip install -r requirements.txt

# Test the personalized chatbot
python personalized_chatbot.py
```

## Troubleshooting

### Container Build Issues
- Ensure Docker is running and VS Code has the Dev Container extension installed
- Try rebuilding the container: Command Palette > "Dev Containers: Rebuild Container"

### Audio Issues in Container
- Audio functionality may be limited in containerized environments
- For full audio testing, consider running components directly on the host system

### Permission Issues
- The container runs as the `vscode` user with appropriate permissions
- If you encounter permission issues, try rebuilding the container