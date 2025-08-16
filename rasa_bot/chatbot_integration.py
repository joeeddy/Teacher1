"""
Teacher1 Rasa Chatbot Integration
---------------------------------
This script provides integration between the Teacher1 project and the Rasa chatbot.
It allows the chatbot to work with existing Teacher1 components like text-to-speech
and speech recognition.
"""

import os
import sys
import asyncio
import logging
from typing import Optional

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

try:
    from rasa.core.agent import Agent
    from rasa.core.interpreter import RasaNLUInterpreter
    RASA_AVAILABLE = True
except ImportError:
    RASA_AVAILABLE = False
    print("Rasa not installed. Please run: pip install -r requirements.txt")

# Import existing Teacher1 components
try:
    from text_to_speech import speak
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("Text-to-speech not available. Install pyttsx3 if needed.")

try:
    from speech_recognition import listen_and_print
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False
    print("Speech recognition not available. Install speechrecognition if needed.")


class Teacher1ChatBot:
    """
    Integration class that combines Rasa chatbot with Teacher1 components.
    """
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the Teacher1 ChatBot.
        
        Args:
            model_path: Path to trained Rasa model. If None, uses default path.
        """
        self.agent = None
        self.model_path = model_path or os.path.join(
            os.path.dirname(__file__), "models"
        )
        
        if RASA_AVAILABLE:
            self._load_agent()
        else:
            print("Rasa is not available. Text-only mode.")
    
    def _load_agent(self):
        """Load the Rasa agent."""
        try:
            if os.path.exists(self.model_path):
                self.agent = Agent.load(self.model_path)
                print("Rasa agent loaded successfully!")
            else:
                print(f"No trained model found at {self.model_path}")
                print("Please train the model first using: rasa train")
        except Exception as e:
            print(f"Error loading Rasa agent: {e}")
    
    async def get_response(self, message: str, sender_id: str = "user") -> str:
        """
        Get response from the chatbot.
        
        Args:
            message: User input message
            sender_id: Unique identifier for the user
            
        Returns:
            Bot response text
        """
        if not self.agent:
            return "I'm sorry, the chatbot is not available right now."
        
        try:
            response = await self.agent.handle_text(message, sender_id=sender_id)
            if response and len(response) > 0:
                return response[0]["text"]
            else:
                return "I'm not sure how to respond to that. Can you try asking differently?"
        except Exception as e:
            print(f"Error getting response: {e}")
            return "I encountered an error. Please try again."
    
    def speak_response(self, text: str):
        """
        Use text-to-speech to speak the response.
        
        Args:
            text: Text to speak
        """
        if TTS_AVAILABLE:
            try:
                speak(text)
            except Exception as e:
                print(f"Error with text-to-speech: {e}")
                print(f"Bot: {text}")
        else:
            print(f"Bot: {text}")
    
    async def chat_loop(self, use_speech: bool = False, use_tts: bool = True):
        """
        Run the main chat loop.
        
        Args:
            use_speech: Whether to use speech recognition for input
            use_tts: Whether to use text-to-speech for output
        """
        print("Teacher1 ChatBot is ready! Type 'quit' to exit.")
        
        if use_tts:
            self.speak_response("Hello! I'm your learning assistant. How can I help you today?")
        else:
            print("Bot: Hello! I'm your learning assistant. How can I help you today?")
        
        sender_id = "user_session"
        
        while True:
            try:
                if use_speech and SR_AVAILABLE:
                    print("\nListening... (or type your message)")
                    user_input = input("You: ").strip()
                else:
                    user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    farewell = "Goodbye! Keep learning and have fun!"
                    if use_tts:
                        self.speak_response(farewell)
                    else:
                        print(f"Bot: {farewell}")
                    break
                
                if user_input:
                    response = await self.get_response(user_input, sender_id)
                    if use_tts:
                        self.speak_response(response)
                    else:
                        print(f"Bot: {response}")
                        
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error in chat loop: {e}")


def main():
    """Main function to run the chatbot."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Teacher1 Rasa Chatbot")
    parser.add_argument("--no-tts", action="store_true", 
                       help="Disable text-to-speech")
    parser.add_argument("--speech", action="store_true",
                       help="Enable speech recognition")
    parser.add_argument("--model-path", type=str,
                       help="Path to Rasa model directory")
    
    args = parser.parse_args()
    
    # Create chatbot instance
    chatbot = Teacher1ChatBot(model_path=args.model_path)
    
    # Run chat loop
    asyncio.run(chatbot.chat_loop(
        use_speech=args.speech,
        use_tts=not args.no_tts
    ))


if __name__ == "__main__":
    main()