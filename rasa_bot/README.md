# Teacher1 BlenderBot Chatbot

This directory contains the BlenderBot chatbot integration for the Teacher1 educational project.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r ../requirements.txt
```

### 2. Test the Chatbot
```bash
# Interactive chat with text-to-speech
python chatbot_integration.py

# Text-only mode
python chatbot_integration.py --no-tts

# With speech recognition (requires microphone)
python chatbot_integration.py --speech
```

### 3. Enable WebSocket Communication
```bash
# Connect to Fractal AI system
python chatbot_integration.py --websocket
```

## File Structure

- `chatbot_integration.py` - Main integration script with Teacher1 components
- `README.md` - This documentation file

## Features

The chatbot is designed for early learners and includes:

### AI-Powered Conversation
- **BlenderBot Model**: Uses facebook/blenderbot-400M-distill from HuggingFace
- **Child-Friendly Filtering**: Automatically filters inappropriate content
- **Educational Focus**: Responses tailored for learning and encouragement
- **Fallback Responses**: Educational templates when model is unavailable

### Educational Content
- **Math**: Simple addition, subtraction, counting discussions
- **Reading**: Letter sounds, word recognition, story discussions
- **Spelling**: Basic word spelling encouragement
- **Numbers**: Counting, number recognition, comparison help
- **General Learning**: Encouraging responses that promote curiosity

### Integration Features
- **Text-to-Speech**: Responses can be spoken aloud using the existing `text_to_speech.py`
- **Speech Recognition**: Input can be received via voice (using existing `speech_recognition.py`)
- **WebSocket Communication**: Bidirectional communication with Fractal AI system
- **GUI Integration**: Can be integrated with the existing `big_text_gui.py`

## Model Configuration

### BlenderBot Model
- **Default Model**: `facebook/blenderbot-400M-distill`
- **Custom Model**: Use `--model-name` parameter to specify different models
- **Automatic Download**: Model downloads automatically on first use
- **Fallback Mode**: Uses educational templates if model unavailable

### Child-Friendly Features
- **Content Filtering**: Removes inappropriate words and themes
- **Educational Enhancement**: Adds encouraging endings to responses
- **Topic Detection**: Recognizes educational topics (math, reading, etc.)
- **Positive Language**: Converts negative language to learning opportunities

## Customization

### Adding New Educational Responses
Edit the `educational_responses` dictionary in `chatbot_integration.py`:

```python
self.educational_responses = {
    'your_topic': [
        "Response option 1",
        "Response option 2",
        "Response option 3"
    ]
}
```

### Modifying Content Filters
Update the `inappropriate_words` set to adjust content filtering:

```python
self.inappropriate_words = {
    'word1', 'word2', 'word3'  # Add words to filter
}
```

## Advanced Usage

### WebSocket Integration with Fractal AI
The chatbot automatically integrates with the Fractal AI system:

```bash
# Enable WebSocket communication
python chatbot_integration.py --websocket

# Custom ports
python chatbot_integration.py --websocket --websocket-port 8766 --target-port 8765
```

### Custom Model Loading
Use different BlenderBot variants:

```bash
# Use a different model
python chatbot_integration.py --model-name facebook/blenderbot-1B-distill

# Smaller model for lower memory usage
python chatbot_integration.py --model-name facebook/blenderbot-90M
```

## Troubleshooting

### Model Loading Issues
- **Network Issues**: Model downloads from HuggingFace require internet connection
- **Memory Issues**: Use smaller models like `facebook/blenderbot-90M` for limited memory
- **Fallback Mode**: System automatically uses educational templates if model fails

### Speech Recognition Issues
- Ensure microphone permissions are granted
- Test the standalone speech recognition: `python ../speech_recognition.py`

### Text-to-Speech Issues
- Install pyttsx3 if not already installed: `pip install pyttsx3`
- Test standalone TTS: `python ../text_to_speech.py`

### WebSocket Communication Issues
- Ensure Fractal AI system is running on target port
- Check firewall settings for local network communication
- Use `--websocket-port` and `--target-port` to configure ports

## Development

### Testing Changes
Use the interactive mode to test responses:
```bash
python chatbot_integration.py
```

### Debugging
Enable verbose output and check logs for detailed information:
```bash
python chatbot_integration.py --websocket  # Shows WebSocket communication logs
```

### Performance Optimization
- Use CPU-only mode by default (automatically configured)
- GPU support available if CUDA is installed
- Model caching reduces subsequent startup times