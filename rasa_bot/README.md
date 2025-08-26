# Teacher1 Rasa Chatbot

This directory contains the Rasa chatbot integration for the Teacher1 educational project.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r ../requirements.txt
```

### 2. Train the Model
From the Teacher1 root directory:
```bash
cd rasa_bot
rasa train
```

### 3. Test the Chatbot
```bash
# Interactive chat with text-to-speech
python chatbot_integration.py

# Text-only mode
python chatbot_integration.py --no-tts

# With speech recognition (requires microphone)
python chatbot_integration.py --speech
```

### 4. Run Rasa Shell (Alternative)
```bash
rasa shell
```

## File Structure

- `config.yml` - Rasa pipeline and policy configuration
- `domain.yml` - Bot's domain including intents, entities, slots, and responses
- `data/` - Training data directory
  - `nlu.yml` - Natural Language Understanding training examples
  - `stories.yml` - Conversation flow training data
  - `rules.yml` - Rule-based conversation patterns
- `chatbot_integration.py` - Integration script with Teacher1 components
- `models/` - Trained models (created after running `rasa train`)

## Features

The chatbot is designed for early learners and includes:

### Supported Intents
- **Greetings**: Hello, hi, good morning
- **Goodbyes**: Bye, see you later, goodbye
- **Help requests**: Help, what can you do, I need help
- **Subject requests**: Math, reading, spelling, numbers lessons

### Educational Content
- **Math**: Simple addition, subtraction, counting
- **Reading**: Letter sounds, word recognition, phonics
- **Spelling**: Basic word spelling practice
- **Numbers**: Counting, number recognition, comparison

### Integration Features
- **Text-to-Speech**: Responses can be spoken aloud using the existing `text_to_speech.py`
- **Speech Recognition**: Input can be received via voice (using existing `speech_recognition.py`)
- **GUI Integration**: Can be integrated with the existing `big_text_gui.py`

## Training Data

The bot comes with basic training data suitable for early learners. You can extend the training data by:

1. Adding more examples to `data/nlu.yml`
2. Creating new stories in `data/stories.yml`
3. Adding new responses in `domain.yml`

## Customization

### Adding New Lessons
1. Add new intents to `domain.yml`
2. Add training examples to `data/nlu.yml`
3. Create stories in `data/stories.yml`
4. Add response templates to `domain.yml`

### Modifying Responses
Edit the `responses` section in `domain.yml` to customize what the bot says.

## Advanced Usage

### Custom Actions
To add custom actions (like integrating with the fractal AI components):

1. Create a `actions.py` file
2. Define custom action classes
3. Update `domain.yml` to include the actions
4. Run the action server: `rasa run actions`

### Integration with Fractal AI
The chatbot can potentially be integrated with the fractal AI system in `fractal_emergent_ai.py` for more advanced educational interactions.

## Troubleshooting

### Model Training Issues
- Ensure all dependencies are installed: `pip install -r ../requirements.txt`
- Check that training data files are properly formatted YAML
- Verify the config.yml pipeline is compatible with your Rasa version

### Speech Recognition Issues
- Ensure microphone permissions are granted
- Install required audio dependencies: `pip install pyaudio`
- Test the standalone speech recognition: `python ../speech_recognition.py`

### Text-to-Speech Issues
- Install pyttsx3 if not already installed: `pip install pyttsx3`
- Test standalone TTS: `python ../text_to_speech.py`

## Development

### Adding New Training Data
After modifying training data files, retrain the model:
```bash
rasa train
```

### Testing Changes
Use the Rasa shell to quickly test changes:
```bash
rasa shell
```

### Debugging
Enable debug logging:
```bash
rasa shell --debug
```