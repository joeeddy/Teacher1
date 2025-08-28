# Teacher1 - Educational Learning Platform

An interactive educational platform for early learners featuring AI-powered components, conversational chatbot, speech recognition, and text-to-speech capabilities.

## Features

### Core Components
- **Fractal AI System**: Advanced AI components for educational pattern recognition
- **Interactive GUI**: Large text interface designed for early learners
- **Speech Recognition**: Voice input capabilities for hands-free interaction
- **Text-to-Speech**: Audio output for enhanced accessibility
- **WebSocket Communication**: Real-time bidirectional communication between AI systems
- **Web Interface**: Modern web-based chat interface with embedded content viewer

### Educational Capabilities
- Math lessons (addition, subtraction, counting)
- Reading practice (phonics, word recognition)
- Spelling exercises
- Number recognition and comparison
- Interactive conversational learning
- AI-powered educational insights and adaptive responses
- Embedded educational content from trusted websites

### Advanced Features
- **Bidirectional AI Communication**: Real-time interaction between AI systems
- **Turn-taking Protocol**: Intelligent conversation management between AI systems
- **Educational Context Integration**: AI insights tailored for learning applications
- **Message Deduplication**: Prevention of communication loops and spam
- **Structured JSON Messaging**: Standardized communication format for reliability
- **Embedded Webview Component**: Secure iframe integration for educational content
- **Responsive Design**: Touch-optimized interface for tablets and smartphones
- **Accessibility Features**: Screen reader support and keyboard navigation

## 🧠 Fractal Emergent AI (Compressed Version)

**teacher1** demonstrates a unique approach to AGI:  
It implements a **fractal, emergent AI architecture**—where intelligence arises from recursive, self-similar agent patterns and dynamic, multi-scale interactions.

> **Note:**  
> This repository presents a **compressed/minimal version** of my full fractal emergent AI system. The core principles and agentic behaviors are preserved, but some advanced features and large-scale dynamics have been simplified for clarity, portability, and community collaboration.

- Use as a template or seed for your own fractal, agentic projects—or to propose enhancements!

**Contributions and AGI research partnerships are welcome!**

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


### Quick Verification

**Test Core System:**
```bash
# Verify WebSocket communication (mock systems)
python websocket_demo.py --test
```
**Expected:** Should show successful bidirectional communication between mock AI systems.

**Test Real Integration:**
```bash
# Start integrated WebSocket communication  
python websocket_demo.py --both
```
**Expected:** AI systems should start, establish WebSocket connections, and begin exchanging educational insights.

**Verify Individual Components:**
```bash
# Test Fractal AI visualization
python fractal_emergent_ai.py --quick

# Test personalized chatbot
python personalized_chatbot.py
```

If any test fails, see the [Troubleshooting](#troubleshooting) section.

### Running the Applications

#### Web Interface (Recommended)
```bash
# Start the modern web interface with embedded content viewer
python web_interface/app.py
```
Then open your browser to: http://localhost:5000

Features:
- Interactive chat with embedded educational content
- **Dual Chatbot Support**: Switch between Personalized Education and HuggingFace Conversational AI
- Mobile and tablet optimized
- Secure iframe integration with trusted educational sites
- Accessibility support for all users

**API Endpoints:**
- `POST /start_session` - Start personalized educational session
- `POST /start_huggingface_session` - Start conversational AI session
- `POST /chat` - Send messages (supports `chatbot_type` parameter)
- `GET /health` - System status including chatbot availability

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
python fractal_emergent_ai.py
```

#### Personalized Chatbot
```bash
# Interactive chatbot with educational features
python personalized_chatbot.py
```

#### HuggingFace BlenderBot Chatbot
```bash
# Install HuggingFace dependencies (optional)
pip install transformers torch

# Test HuggingFace chatbot (runs in fallback mode without transformers)
python huggingface_chatbot.py

# Test HuggingFace WebSocket integration
python huggingface_websocket_chatbot.py --duration 30

# Test multi-chatbot communication (Fractal AI ↔ HuggingFace ↔ Personalized)
python test_multi_chatbot_communication.py
```

**Features:**
- State-of-the-art conversational AI using Facebook's BlenderBot model
- Graceful fallback to simple responses when transformers not installed
- WebSocket integration for real-time communication with other AI systems
- Educational content filtering and age-appropriate responses
- Compatible interface with existing Teacher1 chatbot system

**Requirements:**
- Optional: `transformers` and `torch` for full AI capabilities
- Fallback mode works without additional dependencies

#### WebSocket Communication System
```bash
# Test bidirectional communication between AI systems
python websocket_demo.py --test

# Run both Fractal AI and Chatbot with WebSocket communication
python websocket_demo.py --both

# Run individual systems with WebSocket enabled
python fractal_emergent_ai.py --websocket --quick
python personalized_chatbot.py
```

## Real-World WebSocket Integration

### 🚀 Quick Start for Production Use

**For immediate testing:**
```bash
# Test the system works (mock mode)
python websocket_demo.py --test

# Run real integrated system
python websocket_demo.py --both
```

**For production deployment:**
```bash
# Terminal 1: Start with student interaction interface
python personalized_chatbot.py

# Terminal 2: Start AI analysis
python fractal_emergent_ai.py --websocket
```

### Overview

The Teacher1 platform features **real bidirectional WebSocket communication** between AI systems. This enables dynamic, real-time AI collaboration for enhanced educational experiences where systems can initiate conversations, share insights, and provide coordinated responses to students.

### System Requirements

**Core Dependencies:**
```bash
# Required for all WebSocket functionality
pip install numpy>=1.21.0 matplotlib>=3.5.0 websockets>=12.0
```

**Port Configuration:**
- Fractal AI: Server on port 8765, connects to port 8766
- Chatbot: Server on port 8766, connects to port 8765
- Both ports must be available on localhost

### Step-by-Step Setup Guide

#### 1. Environment Preparation
```bash
# Clone and setup the repository
git clone https://github.com/joeeddy/Teacher1.git
cd Teacher1

# Install core dependencies
pip install -r requirements.txt
```

#### 2. System Verification
Test that both AI systems can run independently before enabling WebSocket communication:

```bash
# Test Fractal AI (should display visualization)
python fractal_emergent_ai.py --quick

# Test personalized chatbot (should start interactive session)
python personalized_chatbot.py
```

**Expected Output:** Both systems should start without errors. Exit with Ctrl+C.

#### 3. WebSocket Integration Testing

**A. Mock System Test (Development/Demo):**
```bash
python websocket_demo.py --test
```
**Expected Output:**
```
🎓 Teacher1 WebSocket Communication Demo
==================================================
🧪 Running test mode with mock systems...
🔗 Starting WebSocket servers...
🤖 Mock systems communicating...
📊 Communication Statistics:
   - Messages exchanged: 8-15
   - AI responses: 4-8  
   - Chatbot responses: 4-7
✅ Test completed successfully
```

**B. Real System Integration (Production):**
```bash
# Terminal 1: Start both systems with WebSocket communication
python websocket_demo.py --both
```

**Expected Output:**
```
🎓 Teacher1 WebSocket Communication Demo
==================================================
🚀 Starting both systems with WebSocket communication...

🧠 Starting Fractal AI with WebSocket communication...
   Server: localhost:8765
   Target: localhost:8766 (Chatbot)

🤖 Starting Chatbot with WebSocket communication...
   Server: localhost:8766  
   Target: localhost:8765 (Fractal AI)

🔗 WebSocket servers established
✅ Bidirectional connection confirmed
```

#### 4. Runtime Verification

**Verify Active Communication:**
Monitor the logs for bidirectional message exchange:

```
💬 Fractal AI → Chatbot: "High activation patterns detected in learning sequences..."
💬 Chatbot → Fractal AI: "How can we apply this to student engagement?"
💬 Fractal AI → Chatbot: "Pattern analysis suggests visual-spatial learning optimization..."
```

**Communication Statistics:**
```
📊 Fractal AI Communication Summary:
   Messages exchanged: 12
   Connected clients: 1
   Client connection: True
   Last insights: ["High variance patterns emerging - creative phase"]

📊 Chatbot Communication Summary:  
   Messages sent: 6
   Messages received: 6
   Active connections: 1
```

### Alternative Deployment Methods

#### Method 1: Individual System Deployment
```bash
# Terminal 1: Start Fractal AI with WebSocket
python fractal_emergent_ai.py --websocket --quick

# Terminal 2: Start Chatbot with WebSocket  
python personalized_chatbot.py --websocket --no-tts
```

#### Method 2: Production Integration with Student Interaction
```bash
# Start full system with student chat interface
python personalized_chatbot.py --websocket

# In another terminal, run AI analysis
python fractal_emergent_ai.py --websocket
```

**Student Interaction Example:**
```
Student: "Why is math so hard?"
Chatbot: "Math can feel challenging, but your brain is amazing at finding patterns!"

[Behind the scenes: Chatbot ↔ Fractal AI communication]
Chatbot → AI: "Student expressing math difficulty. Learning pattern insights?"
AI → Chatbot: "Analysis shows optimal learning with game-based pattern recognition"

Chatbot: "Let's try some fun math games that help your brain see cool number patterns!"
```

### Troubleshooting Guide

#### Common Issues and Solutions

**1. Port Already in Use**
```
Error: [Errno 98] Address already in use
```
**Solution:**
```bash
# Check what's using the ports
sudo netstat -tulpn | grep -E ":(8765|8766)"

# Kill processes if needed
sudo fuser -k 8765/tcp
sudo fuser -k 8766/tcp
```

**2. Module Import Errors**
```
ModuleNotFoundError: No module named 'websockets'
```
**Solution:**
```bash
# Install missing dependencies
pip install websockets numpy matplotlib
```

**3. Connection Timeouts**
```
WebSocket connection failed: ConnectionRefused
```
**Solution:**
```bash
# Ensure both systems start within 5 seconds of each other
# Check firewall settings for localhost ports 8765, 8766
# Verify no other applications are using these ports
```

**5. Silent Communication (No Message Exchange)**
```
Systems connected but no messages flowing
```
**Solution:**
```bash
# Check AI analysis threshold settings
# Ensure conversation_state is 'idle' 
# Verify message handlers are properly registered
# Check logs for deduplication issues
```

#### Debug Mode

Enable detailed logging for troubleshooting:
```bash
# Set debug environment
export PYTHONPATH="${PYTHONPATH}:."
export WEBSOCKET_DEBUG=1

# Run with verbose output
python websocket_demo.py --both --debug
```

#### Health Check Commands

```bash
# Verify WebSocket server status
curl -H "Connection: Upgrade" -H "Upgrade: websocket" http://localhost:8765
curl -H "Connection: Upgrade" -H "Upgrade: websocket" http://localhost:8766

# Test basic connectivity
python -c "
import asyncio
import websockets
async def test():
    try:
        async with websockets.connect('ws://localhost:8765') as ws:
            print('✅ Port 8765 accessible')
    except:
        print('❌ Port 8765 not accessible')
asyncio.run(test())
"
```

### Performance Monitoring

#### Message Flow Analysis
Monitor real-time communication patterns:
```bash
# View communication logs
tail -f websocket_communication.log

# Monitor message statistics  
python -c "
from websocket_communication import WebSocketCommunicator
# Statistics will be displayed in real-time
"
```

#### Expected Performance Metrics
- **Message Latency:** < 50ms between systems
- **Connection Stability:** 99%+ uptime during operation
- **Message Success Rate:** 100% delivery with acknowledgments
- **Memory Usage:** < 100MB per system with WebSocket enabled

### Integration Verification Checklist

- [ ] ✅ Both systems start without dependency errors
- [ ] ✅ WebSocket servers bind to ports 8765 and 8766 successfully  
- [ ] ✅ Cross-system client connections established
- [ ] ✅ Bidirectional message exchange confirmed
- [ ] ✅ Message deduplication working (no loops)
- [ ] ✅ Educational insights flowing between systems
- [ ] ✅ Student interactions trigger AI collaboration
- [ ] ✅ Communication logs show expected message patterns
- [ ] ✅ Error handling and reconnection working properly
- [ ] ✅ Performance metrics within expected ranges

## Project Structure

```
Teacher1/
├── requirements.txt           # Project dependencies
├── README.md                 # This file
├── WEBSOCKET_COMMUNICATION.md # WebSocket system documentation  
├── WEB_INTERFACE_DOCUMENTATION.md # Web interface documentation
├── big_text_gui.py          # GUI application for early learners
├── speech_recognition.py     # Speech input functionality
├── text_to_speech.py        # Audio output functionality
├── fractal_emergent_ai.py  # Advanced AI system
├── fractal_modules.py       # AI system modules
├── websocket_communication.py    # WebSocket communication core
├── websocket_demo.py        # WebSocket demonstration script
├── test_websocket_communication.py # WebSocket testing suite
├── test_web_interface.py    # Web interface testing suite
├── web_interface/           # Web-based chat interface
│   ├── app.py              # Flask web application
│   ├── config.py           # Security and configuration settings
│   ├── templates/
│   │   └── index.html      # Main chat interface template
│   └── static/
│       ├── css/
│       │   └── style.css   # Responsive styles and accessibility
│       └── js/
│           └── chat.js     # Chat interaction and iframe management
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

### WebSocket Communication
- `websockets` - Bidirectional WebSocket communication between AI systems

## Usage Examples

### Web Interface Chat (Recommended)
```bash
# Start the modern web interface
python web_interface/app.py
```
Then open: http://localhost:5000

**Example web chat with embedded content:**
```
You: Show me educational content about science
Bot: I'd love to help you learn about science! Let me show you some great educational resources.

[The bot opens an embedded Wikipedia page about science in the iframe]

You: Open math learning resources  
Bot: Here are some excellent math resources from Khan Academy!

[The bot opens Khan Academy math section in the iframe]
```

**Features:**
- Touch-optimized for tablets and smartphones
- Embedded educational content from trusted sites
- Accessible design with screen reader support
- Secure domain whitelisting and iframe sandboxing

### Basic Chatbot Interaction
```python
# Start the integrated chatbot
python personalized_chatbot.py

# Example conversation:
# You: Hello
# Bot: Hello! I'm your learning assistant. How can I help you learn today?
# You: I want to learn math
# Bot: Let's practice math! Can you tell me what 2 + 3 equals?
```

### AI-Enhanced Educational Interaction

**Real-World Example with Student:**
```bash
# Start full integrated system with student interface
python personalized_chatbot.py --websocket

# In another terminal, monitor AI insights
python fractal_emergent_ai.py --websocket
```

**Example interaction flow:**
```
Student: "Why is math so hard?"
Chatbot: "Math can feel challenging, but your brain is amazing at finding patterns!"

[Behind-the-scenes AI collaboration]
Chatbot → Fractal AI: "Student expressing math difficulty. What learning patterns show best engagement?"
Fractal AI → Chatbot: "Analysis shows optimal learning with game-based pattern recognition and immediate positive feedback loops."

Chatbot: "Let's try some fun math games that help your brain see the cool patterns in numbers! Would you like to start with addition patterns?"
```

**Advanced Integration Testing:**
```bash
# Monitor real-time bidirectional communication
python websocket_demo.py --both

# Expected AI insights being shared:
# "High activation patterns detected in learning sequences..."
# "Pattern analysis suggests visual-spatial learning optimization..."
# "Current neural pathway strength indicates optimal timing for concept introduction..."
```

### Combining Components
The platform is designed for integration. For example, you could:

1. Use the GUI to display large text
2. Use speech recognition for voice input
3. Process input through the chatbot
4. Use text-to-speech for audio responses
5. Apply the fractal AI for advanced pattern recognition
6. Enable WebSocket communication for real-time AI collaboration

### WebSocket Communication Examples

**Real System Integration (Production Use):**
```bash
# Full integrated system with bidirectional AI communication
python websocket_demo.py --both

# Individual system deployment
python fractal_emergent_ai.py --websocket --quick
python personalized_chatbot.py --websocket --no-tts
```

**Development and Testing:**
```bash  
# Test mode with mock systems (for development/demos)
python websocket_demo.py --test

# Individual component testing
python websocket_demo.py --ai-only
python websocket_demo.py --chatbot-only
```

See [Real-World WebSocket Integration](#real-world-websocket-integration) section for complete setup guide and [WEBSOCKET_COMMUNICATION.md](WEBSOCKET_COMMUNICATION.md) for technical documentation.

## Development

### Adding New Educational Content

1. **Extend chatbot capabilities** in `personalized_chatbot.py`
2. **Add new educational responses** to existing chatbot logic
3. **Create custom functions** for complex educational logic
4. **Integrate with existing components** for multimedia experiences

### Customizing the AI System

The fractal AI system in `fractal_emergent_ai.py` can be extended for:
- Pattern recognition in student responses
- Adaptive learning algorithms
- Educational content generation

### Training the Chatbot

After modifying training data:
```bash
```

## Troubleshooting

### Installation Issues
- Ensure Python 3.7+ is installed
- For audio issues, install platform-specific audio libraries
- On macOS: `brew install portaudio`
- On Ubuntu: `sudo apt-get install portaudio19-dev`

### WebSocket Integration Issues

**Dependency Installation Problems:**
```bash
# For pip timeout issues, try using system packages:
# Ubuntu/Debian:
sudo apt-get install python3-numpy python3-matplotlib python3-websockets

# Or install with longer timeout:
pip install --timeout 300 websockets numpy matplotlib
```

**Port Conflicts:**
```bash
# Check if ports 8765/8766 are in use:
netstat -tulpn | grep -E ":(8765|8766)"

# Kill conflicting processes:
sudo fuser -k 8765/tcp 8766/tcp
```

**Connection Issues:**
- Ensure both systems start within 5 seconds of each other
- Verify firewall allows localhost connections on ports 8765, 8766
- Check that no antivirus software is blocking WebSocket connections

**Silent Communication (Connected but No Messages):**
- Check AI analysis is generating insights (requires state changes)
- Ensure conversation_state is 'idle' between systems

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
2. Open an issue on the GitHub repository
