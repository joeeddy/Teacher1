# WebSocket Communication System Documentation

## Overview

The Teacher1 project now includes a robust bidirectional WebSocket communication system that enables real-time interaction between the Fractal AI system and the Rasa chatbot. Both systems can initiate and respond to questions, creating a dynamic feedback loop for enhanced educational insights.

## Features

### ✅ Core Communication Features
- **Bidirectional Communication**: Both AI and chatbot can initiate conversations
- **Turn-taking Protocol**: Prevents message conflicts with proper conversation flow
- **Message Deduplication**: Prevents loops and spam using message ID caching
- **Structured JSON Messaging**: Standardized message format for reliable communication
- **Connection Resilience**: Automatic reconnection and error handling
- **Educational Context Integration**: Messages are processed with educational relevance

### ✅ Message Format

All WebSocket messages use this structured JSON format:

```json
{
  "message_id": "unique_uuid",
  "sender": "fractal_ai|chatbot",
  "type": "question|answer|ack",
  "content": "plain text message content",
  "in_reply_to": "message_id_of_original_question",
  "timestamp": "2024-01-01T12:00:00.000Z"
}
```

**Field Descriptions:**
- `message_id`: Unique identifier for deduplication and tracking
- `sender`: Identifies the system sending the message
- `type`: Message type for proper routing and response handling
- `content`: The actual message text content
- `in_reply_to`: Links answers to their original questions (null for new questions)
- `timestamp`: ISO8601 timestamp for message ordering and analysis

## System Architecture

### WebSocket Ports Configuration
- **Fractal AI**: Server on port 8765, connects to port 8766
- **Rasa Chatbot**: Server on port 8766, connects to port 8765

### Communication Flow
1. Both systems start their WebSocket servers
2. Each system connects as a client to the other's server
3. Either system can initiate questions when conversation state is "idle"
4. Receiving system sends acknowledgment and processes the question
5. Response is sent back with reference to original question ID
6. Conversation state returns to "idle" for next interaction

## Setup Instructions

### 1. Install Dependencies

```bash
# Core WebSocket dependency
pip install websockets>=12.0

# Fractal AI dependencies  
pip install numpy matplotlib

# Optional: Full Rasa installation for advanced chatbot features
pip install rasa>=3.6.0 rasa-sdk>=3.6.0
```

### 2. Basic Usage Examples

#### Run Test Communication (Recommended First Step)
```bash
# Test bidirectional communication with mock systems
python websocket_demo.py --test
```

#### Run Both Systems Together
```bash
# Start both Fractal AI and Rasa chatbot with WebSocket communication
python websocket_demo.py --both
```

#### Run Individual Systems

**Fractal AI with WebSocket:**
```bash
python fractal_emergent_ai.py --websocket --quick
```

**Rasa Chatbot with WebSocket:**
```bash
python personalized_chatbot.py
```

### 3. Advanced Configuration

#### Custom Ports
```python
# Create AI with custom WebSocket configuration
ai = FractalEmergentAI(websocket_port=8765, target_port=8766)

# Create chatbot with custom configuration  
chatbot = Teacher1ChatBot(websocket_port=8766, target_port=8765)
```

#### Programmatic Usage
```python
from websocket_communication import WebSocketCommunicator

# Create communicator
comm = WebSocketCommunicator(
    name="my_system",
    server_port=8767,
    target_host="localhost", 
    target_port=8768
)

# Set message handlers
comm.on_question_received = my_question_handler
comm.on_answer_received = my_answer_handler

# Start communication
await comm.start_server()
await comm.connect_as_client()

# Send a question
await comm.send_question("What patterns are you analyzing?")
```

## API Reference

### WebSocketCommunicator Class

#### Constructor
```python
WebSocketCommunicator(name, server_port, target_host="localhost", target_port=None)
```

#### Key Methods
```python
# Message creation
create_message(content, msg_type="question", in_reply_to=None)

# Communication
async start_server()
async connect_as_client()
async send_question(content, target_websocket=None)
async broadcast_message(message)
async stop()

# State checking
is_ready_to_send_question()
get_stats()
```

#### Message Handlers (Set These)
```python
comm.on_question_received = async_function  # Should return response string
comm.on_answer_received = async_function    # Process received answers
comm.on_ack_received = async_function       # Handle acknowledgments
```

### Fractal AI Integration

#### Enhanced Constructor
```python
FractalEmergentAI(size=64, channels=33, state_dim=5, max_species=20, 
                  websocket_port=8765, target_port=8766)
```

#### WebSocket Methods
```python
ai.start_websocket_communication()
ai.stop_websocket_communication() 
ai.get_communication_log()
ai.get_stats()  # Includes WebSocket statistics
```

#### Enhanced Run Method
```python
ai.run(steps=8000, show=True, enable_websocket=False)
```

### Rasa Chatbot Integration

#### Enhanced Constructor
```python
Teacher1ChatBot(model_path=None, websocket_port=8766, target_port=8765)
```

#### WebSocket Methods  
```python
chatbot.start_websocket_communication()
chatbot.stop_websocket_communication()
await chatbot.ask_ai_question(question)
chatbot.get_communication_log()
chatbot.get_stats()
```

#### Enhanced Chat Loop
```python
await chatbot.chat_loop(use_speech=False, use_tts=True, enable_websocket=False)
```

## Example Communication Scenarios

### 1. AI-Initiated Educational Insight
```
Fractal AI → Rasa: "I'm observing high-frequency learning patterns in mathematical sequences. How might this apply to student learning?"

Rasa → Fractal AI: "That's fascinating! We could use this for adaptive learning systems that adjust to student progress. Pattern recognition is fundamental to learning!"
```

### 2. Chatbot-Initiated Learning Query
```
Rasa → Fractal AI: "A student is struggling with multiplication tables. What cognitive patterns might help with memorization?"

Fractal AI → Rasa: "Analysis shows rhythmic repetition patterns with 0.7-second intervals optimize memory consolidation. Current neural pathway strength indicates visual-spatial learning preference."
```

### 3. Student Interaction with AI Insights
```
Student → Rasa: "Why is math so hard?"

Rasa → Student: "Math can feel challenging, but your brain is amazing at finding patterns!"

Rasa → Fractal AI: "Student expressing math difficulty. What learning patterns show best engagement strategies?"

Fractal AI → Rasa: "Detecting optimal learning occurs with game-based pattern recognition combined with immediate positive feedback loops."

Rasa → Student: "Let's try some fun math games that help your brain see the cool patterns in numbers!"
```

## Performance and Monitoring

### Message Statistics
```python
stats = communicator.get_stats()
print(f"Messages cached: {stats['cache_size']}")
print(f"Conversation state: {stats['conversation_state']}")
print(f"Connected clients: {stats['connected_clients']}")
```

### Communication Logs
```python
# Get recent communication history
log = ai.get_communication_log()
for message in log[-10:]:  # Last 10 messages
    print(message)
```

### Connection Health
```python
# Check if ready to send questions (turn-taking)
if communicator.is_ready_to_send_question():
    await communicator.send_question("Your question here")
    
# Check connection status
stats = communicator.get_stats()
has_connection = stats['has_client_connection']
```

## Troubleshooting

### Common Issues

#### Port Already in Use
```
Error: [Errno 98] Address already in use
```
**Solution**: Use different ports or stop existing processes:
```bash
# Check what's using the port
lsof -i :8765
lsof -i :8766

# Kill processes if needed
kill -9 <process_id>
```

#### Connection Refused
```
Error: [Errno 111] Connection refused
```
**Solution**: Ensure target system is running and ports are correct:
```bash
# Start systems in order
# Terminal 1: Start Fractal AI
python fractal_emergent_ai.py --websocket

# Terminal 2: Start Rasa (after AI is running)  
python personalized_chatbot.py
```

#### Import Errors
```
ModuleNotFoundError: No module named 'websockets'
```
**Solution**: Install required dependencies:
```bash
pip install websockets numpy matplotlib
```

### Debug Mode
Enable verbose logging for troubleshooting:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Security Considerations

### Current Implementation
- Communication is localhost-only by default
- No authentication mechanism implemented
- Messages are not encrypted

### Production Recommendations
- Add authentication tokens to message format
- Implement SSL/TLS for encrypted communication
- Add message rate limiting
- Validate message content before processing
- Use secure WebSocket connections (wss://)

## Future Enhancements

### Planned Features
- [ ] Multi-system communication (more than 2 participants)
- [ ] Message persistence and replay
- [ ] Real-time communication analytics dashboard
- [ ] Integration with external educational APIs
- [ ] Voice-to-WebSocket bridge for spoken interactions
- [ ] Visual communication flow diagrams

### Extensibility
The WebSocket system is designed to be extensible:
- Add new message types by extending the `type` field
- Create custom message handlers for domain-specific logic
- Integrate additional AI systems using the same protocol
- Build web interfaces that connect to the WebSocket servers

## Testing

### Automated Tests
```bash
# Run comprehensive communication test
python test_websocket_communication.py --duration 60

# Run with verbose output
python test_websocket_communication.py --duration 30 --verbose
```

### Manual Testing
```bash
# Test individual components
python websocket_demo.py --test

# Test full integration
python websocket_demo.py --both
```

## Support and Contributing

For issues, questions, or contributions related to the WebSocket communication system:

1. Check existing documentation and troubleshooting sections
2. Run the test suite to verify your setup
3. Review communication logs for debugging information
4. Create detailed bug reports with system information and logs

The WebSocket communication system enhances Teacher1's educational capabilities by enabling real-time collaboration between AI analysis and conversational interfaces, creating more responsive and insightful learning experiences.