# Teacher1 - Educational Learning Platform

An interactive educational platform for early learners featuring AI-powered components, conversational chatbot, speech recognition, and text-to-speech capabilities.

## Features

### Core Components
- **Fractal AI System**: Advanced AI components for educational pattern recognition
- **Interactive GUI**: Large text interface designed for early learners
- **Speech Recognition**: Voice input capabilities for hands-free interaction
- **Text-to-Speech**: Audio output for enhanced accessibility
- **Rasa Chatbot**: Conversational AI for educational assistance
- **WebSocket Communication**: Real-time bidirectional communication between AI systems

### Educational Capabilities
- Math lessons (addition, subtraction, counting)
- Reading practice (phonics, word recognition)
- Spelling exercises
- Number recognition and comparison
- Interactive conversational learning
- AI-powered educational insights and adaptive responses

### Advanced Features
- **Bidirectional AI Communication**: Real-time interaction between Fractal AI and Rasa chatbot
- **Turn-taking Protocol**: Intelligent conversation management between AI systems
- **Educational Context Integration**: AI insights tailored for learning applications
- **Message Deduplication**: Prevention of communication loops and spam
- **Structured JSON Messaging**: Standardized communication format for reliability

## Quick Start

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/joeeddy/Teacher1.git
   cd Teacher1
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the Rasa chatbot**
   ```bash
   cd rasa_bot
   rasa train
   cd ..
   ```

### Running the Applications

#### GUI Application
```bash
python big_text_gui.py
```

#### Text-to-Speech Demo
```bash
python text_to_speech.py
```

#### Speech Recognition Demo
```bash
python speech_recognition.py
```

#### Fractal AI System
```bash
python fractal_emergent_ai_gen10.py
```

#### Rasa Chatbot
```bash
# Interactive chatbot with text-to-speech
python rasa_bot/chatbot_integration.py

# Text-only mode
python rasa_bot/chatbot_integration.py --no-tts

# With speech recognition
python rasa_bot/chatbot_integration.py --speech

# Alternative: Rasa shell
cd rasa_bot
rasa shell
```

#### WebSocket Communication System
```bash
# Test bidirectional communication between AI systems
python websocket_demo.py --test

# Run both Fractal AI and Rasa with WebSocket communication
python websocket_demo.py --both

# Run individual systems with WebSocket enabled
python fractal_emergent_ai_gen10.py --websocket --quick
python rasa_bot/chatbot_integration.py --websocket --no-tts
```

## Project Structure

```
Teacher1/
├── requirements.txt           # Project dependencies
├── README.md                 # This file
├── WEBSOCKET_COMMUNICATION.md # WebSocket system documentation  
├── big_text_gui.py          # GUI application for early learners
├── speech_recognition.py     # Speech input functionality
├── text_to_speech.py        # Audio output functionality
├── fractal_emergent_ai_gen10.py  # Advanced AI system
├── fractal_modules.py       # AI system modules
├── websocket_communication.py    # WebSocket communication core
├── websocket_demo.py        # WebSocket demonstration script
├── test_websocket_communication.py # WebSocket testing suite
└── rasa_bot/               # Chatbot directory
    ├── README.md           # Chatbot-specific documentation
    ├── config.yml          # Rasa configuration
    ├── domain.yml          # Bot domain definition
    ├── chatbot_integration.py  # Integration with Teacher1
    ├── data/               # Training data
    │   ├── nlu.yml        # Natural language understanding
    │   ├── stories.yml    # Conversation flows
    │   └── rules.yml      # Conversation rules
    └── models/            # Trained models (generated)
```

## Dependencies

### Core Dependencies
- `numpy` - Numerical computing for AI components
- `matplotlib` - Plotting and visualization
- `tkinter` - GUI framework (built-in with Python)

### Speech and Audio
- `speechrecognition` - Voice input processing
- `pyaudio` - Audio interface
- `pyttsx3` - Text-to-speech synthesis

### Rasa Chatbot
- `rasa` - Conversational AI framework
- `rasa-sdk` - SDK for custom actions
- `tensorflow` - Machine learning backend
- `spacy` - Natural language processing

### WebSocket Communication
- `websockets` - Bidirectional WebSocket communication between AI systems

## Usage Examples

### Basic Chatbot Interaction
```python
# Start the integrated chatbot
python rasa_bot/chatbot_integration.py

# Example conversation:
# You: Hello
# Bot: Hello! I'm your learning assistant. How can I help you learn today?
# You: I want to learn math
# Bot: Let's practice math! Can you tell me what 2 + 3 equals?
```

### AI-Enhanced Educational Interaction
```python
# Start both AI systems with WebSocket communication
python websocket_demo.py --both

# Example interaction flow:
# Student: "Why is math so hard?"
# Rasa: "Math can feel challenging, but your brain is amazing at finding patterns!"
# [Rasa asks Fractal AI for insights about learning patterns]
# Fractal AI: "Analysis shows optimal learning with visual-spatial patterns and positive feedback"
# Rasa: "Let's try some fun math games that help your brain see cool number patterns!"
```

### Combining Components
The platform is designed for integration. For example, you could:

1. Use the GUI to display large text
2. Use speech recognition for voice input
3. Process input through the Rasa chatbot
4. Use text-to-speech for audio responses
5. Apply the fractal AI for advanced pattern recognition
6. Enable WebSocket communication for real-time AI collaboration

### WebSocket Communication Examples
```python
# Test the bidirectional communication system
python websocket_demo.py --test

# Run Fractal AI with WebSocket insights
python fractal_emergent_ai_gen10.py --websocket --quick

# Run Rasa chatbot with AI integration  
python rasa_bot/chatbot_integration.py --websocket --no-tts

# See WEBSOCKET_COMMUNICATION.md for detailed documentation
```

## Development

### Adding New Educational Content

1. **Extend Rasa training data** in `rasa_bot/data/`
2. **Add new responses** in `rasa_bot/domain.yml`
3. **Create custom actions** for complex educational logic
4. **Integrate with existing components** for multimedia experiences

### Customizing the AI System

The fractal AI system in `fractal_emergent_ai_gen10.py` can be extended for:
- Pattern recognition in student responses
- Adaptive learning algorithms
- Educational content generation

### Training the Chatbot

After modifying training data:
```bash
cd rasa_bot
rasa train
```

## Troubleshooting

### Installation Issues
- Ensure Python 3.7+ is installed
- For audio issues, install platform-specific audio libraries
- On macOS: `brew install portaudio`
- On Ubuntu: `sudo apt-get install portaudio19-dev`

### Rasa Training Issues
- Verify YAML syntax in training files
- Ensure sufficient training examples for each intent
- Check TensorFlow compatibility

### Audio Issues
- Test microphone permissions
- Verify speaker/headphone connections
- Check system audio settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with appropriate tests
4. Submit a pull request

## License

This project is open source. Please check the repository for license details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the Rasa documentation: https://rasa.com/docs/
3. Open an issue on the GitHub repository