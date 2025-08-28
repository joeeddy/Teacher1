"""
Teacher1 BlenderBot Chatbot Integration
--------------------------------------
This script provides integration between the Teacher1 project and a child-friendly BlenderBot.
It allows the chatbot to work with existing Teacher1 components like text-to-speech
and speech recognition, plus WebSocket communication with the Fractal AI system.
"""

import os
import sys
import asyncio
import logging
import threading
import random
import re
from typing import Optional, List

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

try:
    from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
    import torch
    BLENDERBOT_AVAILABLE = True
except ImportError:
    BLENDERBOT_AVAILABLE = False
    print("BlenderBot (transformers) not installed. Please run: pip install transformers torch")

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

# Import WebSocket communication
try:
    from websocket_communication import WebSocketCommunicator
    WEBSOCKET_AVAILABLE = True
except ImportError:
    WEBSOCKET_AVAILABLE = False
    print("WebSocket communication not available.")


class Teacher1ChatBot:
    """
    Integration class that combines BlenderBot chatbot with Teacher1 components
    and WebSocket communication with the Fractal AI system.
    """
    
    def __init__(self, model_path: Optional[str] = None, websocket_port: int = 8766, 
                 target_port: int = 8765):
        """
        Initialize the Teacher1 ChatBot.
        
        Args:
            model_path: Model name for BlenderBot (e.g., 'facebook/blenderbot-400M-distill')
            websocket_port: Port for WebSocket server
            target_port: Port of target WebSocket server (Fractal AI)
        """
        self.tokenizer = None
        self.model = None
        self.model_name = model_path or "facebook/blenderbot-400M-distill"
        
        # Child-friendly content filtering
        self.inappropriate_words = {
            'violence', 'kill', 'death', 'die', 'hurt', 'pain', 'blood', 'weapon',
            'stupid', 'dumb', 'hate', 'angry', 'mad', 'bad words', 'curse',
            'scary', 'frightening', 'nightmare', 'monster', 'ghost'
        }
        
        # Educational response templates for fallback
        self.educational_responses = {
            'math': [
                "Math is so much fun! Let's practice counting or simple addition.",
                "Numbers are everywhere! Can you count to 10 with me?",
                "Let's solve a fun math puzzle together!"
            ],
            'reading': [
                "Reading opens up magical worlds! What's your favorite story?",
                "Let's practice reading together. Can you tell me about a book you like?",
                "Reading is like going on adventures! What would you like to read about?"
            ],
            'spelling': [
                "Spelling helps us write amazing stories! Let's practice some fun words.",
                "Letters make words, and words make stories! What word should we spell?",
                "Spelling is like a puzzle with letters! Want to try spelling your name?"
            ],
            'numbers': [
                "Numbers help us understand the world! Let's count something fun.",
                "Numbers are like friends - they help us with so many things!",
                "Let's explore numbers together! What's your favorite number?"
            ],
            'general': [
                "That's a great question! Learning is always an adventure.",
                "I love helping you learn new things! What interests you most?",
                "You're such a curious learner! That's wonderful!",
                "Learning together is so much fun! What would you like to explore?"
            ]
        }
        
        # WebSocket communication setup
        if WEBSOCKET_AVAILABLE:
            self.websocket_communicator = WebSocketCommunicator(
                name="blenderbot_chatbot",
                server_port=websocket_port,
                target_host="localhost", 
                target_port=target_port
            )
            
            # Set up message handlers
            self.websocket_communicator.on_question_received = self._handle_question
            self.websocket_communicator.on_answer_received = self._handle_answer
            self.websocket_communicator.on_ack_received = self._handle_ack
            
            # Communication state
            self.websocket_enabled = False
            self.websocket_thread = None
            self.websocket_loop = None
            self.communication_log = []
            self.educational_context = {
                "current_topic": None,
                "difficulty_level": "beginner",
                "learning_goals": []
            }
        else:
            self.websocket_communicator = None
        
        if BLENDERBOT_AVAILABLE:
            self._load_model()
        else:
            print("BlenderBot is not available. Using educational fallback responses.")
    
    def _load_model(self):
        """Load the BlenderBot model and tokenizer."""
        try:
            print(f"Loading BlenderBot model: {self.model_name}")
            self.tokenizer = BlenderbotTokenizer.from_pretrained(self.model_name)
            self.model = BlenderbotForConditionalGeneration.from_pretrained(self.model_name)
            
            # Use CPU for lighter processing (can be changed to GPU if available)
            device = "cuda" if torch.cuda.is_available() else "cpu"
            self.model.to(device)
            self.device = device
            
            print("BlenderBot model loaded successfully!")
        except Exception as e:
            print(f"Error loading BlenderBot model: {e}")
            print("Falling back to educational response templates.")
            self.tokenizer = None
            self.model = None
    
    def _filter_inappropriate_content(self, text: str) -> bool:
        """
        Check if text contains inappropriate content for children.
        
        Args:
            text: Text to check
            
        Returns:
            True if content is appropriate, False if inappropriate
        """
        text_lower = text.lower()
        
        # Check for inappropriate words
        for word in self.inappropriate_words:
            if word in text_lower:
                return False
        
        # Check for overly complex or adult themes
        adult_topics = ['politics', 'religion', 'dating', 'romance', 'marriage']
        for topic in adult_topics:
            if topic in text_lower:
                return False
        
        return True
    
    def _make_child_friendly(self, text: str) -> str:
        """
        Make the response more child-friendly and educational.
        
        Args:
            text: Original response text
            
        Returns:
            Child-friendly version of the text
        """
        # Remove any inappropriate content patterns
        text = re.sub(r'\b(um|uh|er)\b', '', text, flags=re.IGNORECASE)
        
        # Make it more encouraging and positive
        if any(word in text.lower() for word in ['bad', 'wrong', 'error', 'fail']):
            text = "That's okay! Learning means trying new things. " + text
        
        # Add educational encouragement
        encouraging_endings = [
            " Keep up the great learning!",
            " You're doing wonderfully!",
            " Learning is so much fun!",
            " Great question!",
            " You're so curious - I love that!"
        ]
        
        if len(text) < 100 and not text.endswith(('!', '?', '.')):
            text += random.choice(encouraging_endings)
        
        return text.strip()
    
    def _get_educational_response(self, message: str) -> str:
        """
        Generate an educational response based on the message content.
        
        Args:
            message: User message
            
        Returns:
            Educational response
        """
        message_lower = message.lower()
        
        # Detect educational topics
        if any(word in message_lower for word in ['math', 'add', 'subtract', 'count', 'number']):
            return random.choice(self.educational_responses['math'])
        elif any(word in message_lower for word in ['read', 'book', 'story', 'letter']):
            return random.choice(self.educational_responses['reading'])
        elif any(word in message_lower for word in ['spell', 'write', 'word']):
            return random.choice(self.educational_responses['spelling'])
        elif any(word in message_lower for word in ['number', 'count', 'digit']):
            return random.choice(self.educational_responses['numbers'])
        else:
            return random.choice(self.educational_responses['general'])
    
    async def get_response(self, message: str, sender_id: str = "user") -> str:
        """
        Get response from the chatbot.
        
        Args:
            message: User input message
            sender_id: Unique identifier for the user
            
        Returns:
            Bot response text
        """
        try:
            # First check if BlenderBot is available and loaded
            if self.model and self.tokenizer:
                return await self._get_blenderbot_response(message)
            else:
                # Use educational fallback responses
                return self._get_educational_response(message)
                
        except Exception as e:
            print(f"Error getting response: {e}")
            return "I'm sorry, let me try to help you with something else. What would you like to learn about?"
    
    async def _get_blenderbot_response(self, message: str) -> str:
        """
        Get response from BlenderBot model.
        
        Args:
            message: User input message
            
        Returns:
            BlenderBot response (filtered for child-friendliness)
        """
        try:
            # Create educational context for the prompt
            educational_prompt = f"You are a friendly, patient teacher for young children. A child says: '{message}'. Respond in a simple, encouraging, and educational way."
            
            # Tokenize input
            inputs = self.tokenizer(educational_prompt, return_tensors="pt").to(self.device)
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=150,
                    num_beams=3,
                    no_repeat_ngram_size=2,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Remove the original prompt from the response
            if educational_prompt in response:
                response = response.replace(educational_prompt, "").strip()
            
            # Filter and make child-friendly
            if self._filter_inappropriate_content(response):
                response = self._make_child_friendly(response)
            else:
                # If content is inappropriate, use educational fallback
                response = self._get_educational_response(message)
            
            return response
            
        except Exception as e:
            print(f"Error with BlenderBot generation: {e}")
            # Fallback to educational response
            return self._get_educational_response(message)
    
    async def _handle_question(self, message: dict) -> str:
        """Handle incoming questions from the Fractal AI system."""
        question = message['content']
        self.communication_log.append(f"AI Question: {question}")
        
        # Process the question through BlenderBot if available
        try:
            # Get response from the chatbot
            response = await self.get_response(question, sender_id="fractal_ai")
            
            # Enhance response with educational context
            if "pattern" in question.lower():
                response += " From an educational perspective, pattern recognition is fundamental to learning mathematics and reading."
            elif "learn" in question.lower():
                response += " In education, we use scaffolded learning to build knowledge progressively."
            elif "creative" in question.lower():
                response += " Creativity in learning helps students develop problem-solving skills."
            
            self.communication_log.append(f"BlenderBot Response: {response}")
            return response
            
        except Exception as e:
            logging.error(f"Error processing AI question: {e}")
        
        # Fallback educational response
        fallback_responses = {
            "pattern": "I see you're analyzing patterns! In education, pattern recognition helps students understand sequences, mathematics, and reading comprehension.",
            "learn": "Learning is fascinating! I focus on adaptive, personalized education that meets each student where they are.",
            "state": "System states remind me of how learners have different cognitive states - sometimes focused, sometimes creative, always growing!",
            "creative": "Creativity is essential in education! It helps students think outside the box and approach problems from multiple angles."
        }
        
        for keyword, response in fallback_responses.items():
            if keyword in question.lower():
                self.communication_log.append(f"Fallback Response: {response}")
                return response
        
        default_response = "That's an interesting observation from your AI analysis! How might we apply this insight to help students learn more effectively?"
        self.communication_log.append(f"Default Response: {default_response}")
        return default_response
    
    async def _handle_answer(self, message: dict):
        """Handle incoming answers from the Fractal AI system."""
        answer = message['content'] 
        self.communication_log.append(f"AI Answer: {answer}")
        
        # Extract educational insights from AI answers
        if "pattern" in answer.lower():
            self.educational_context["current_topic"] = "pattern_recognition"
        elif "math" in answer.lower():
            self.educational_context["current_topic"] = "mathematics"
        elif "creative" in answer.lower():
            self.educational_context["current_topic"] = "creative_thinking"
        
        # Log the educational context update
        self.communication_log.append(f"Context updated: {self.educational_context['current_topic']}")
    
    async def _handle_ack(self, message: dict):
        """Handle acknowledgment messages."""
        self.communication_log.append(f"AI Ack: {message['content']}")
    
    async def ask_ai_question(self, question: str):
        """Ask a question to the Fractal AI system."""
        if not self.websocket_communicator or not self.websocket_enabled:
            return
        
        try:
            if self.websocket_communicator.is_ready_to_send_question():
                await self.websocket_communicator.send_question(question)
                self.communication_log.append(f"Asked AI: {question}")
        except Exception as e:
            logging.error(f"Error asking AI question: {e}")
    
    def start_websocket_communication(self):
        """Start WebSocket communication in a separate thread."""
        if not WEBSOCKET_AVAILABLE or self.websocket_enabled:
            return
        
        def run_websocket():
            self.websocket_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.websocket_loop)
            
            async def websocket_main():
                try:
                    # Start server
                    await self.websocket_communicator.start_server()
                    logging.info("BlenderBot WebSocket server started")
                    
                    # Wait a bit then try to connect as client
                    await asyncio.sleep(2)
                    connected = await self.websocket_communicator.connect_as_client()
                    if connected:
                        logging.info("BlenderBot connected to Fractal AI")
                        
                        # Send an initial educational question
                        await asyncio.sleep(1)
                        await self.ask_ai_question("Hello! I'm the educational chatbot. What learning patterns are you currently analyzing?")
                    
                    # Keep running
                    while self.websocket_enabled:
                        await asyncio.sleep(1)
                        
                except Exception as e:
                    logging.error(f"BlenderBot WebSocket error: {e}")
                finally:
                    await self.websocket_communicator.stop()
            
            self.websocket_loop.run_until_complete(websocket_main())
        
        self.websocket_enabled = True
        self.websocket_thread = threading.Thread(target=run_websocket, daemon=True)
        self.websocket_thread.start()
        logging.info("BlenderBot WebSocket communication thread started")
    
    def stop_websocket_communication(self):
        """Stop WebSocket communication."""
        if self.websocket_enabled:
            self.websocket_enabled = False
            if self.websocket_loop and not self.websocket_loop.is_closed():
                asyncio.run_coroutine_threadsafe(
                    self.websocket_communicator.stop(),
                    self.websocket_loop
                )
            if self.websocket_thread:
                self.websocket_thread.join(timeout=5)
            logging.info("BlenderBot WebSocket communication stopped")
    
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
    
    async def chat_loop(self, use_speech: bool = False, use_tts: bool = True, 
                       enable_websocket: bool = False):
        """
        Run the main chat loop.
        
        Args:
            use_speech: Whether to use speech recognition for input
            use_tts: Whether to use text-to-speech for output
            enable_websocket: Whether to enable WebSocket communication with Fractal AI
        """
        print("Teacher1 ChatBot is ready! Type 'quit' to exit.")
        
        # Start WebSocket communication if requested
        if enable_websocket and WEBSOCKET_AVAILABLE:
            self.start_websocket_communication()
            print("WebSocket communication with Fractal AI enabled!")
        
        greeting = "Hello! I'm your learning assistant. How can I help you today?"
        if enable_websocket:
            greeting += " I'm also connected to our advanced AI system for enhanced insights!"
        
        if use_tts:
            self.speak_response(greeting)
        else:
            print(f"Bot: {greeting}")
        
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
                    # Regular chatbot response
                    response = await self.get_response(user_input, sender_id)
                    
                    # If WebSocket is enabled, possibly ask AI for insights
                    if enable_websocket and self.websocket_enabled:
                        # Check if this is a complex educational question
                        if any(word in user_input.lower() for word in ['why', 'how', 'explain', 'teach', 'learn']):
                            # Ask the AI for additional insights
                            ai_question = f"A student asked: '{user_input}'. What learning patterns or insights could help with this educational query?"
                            await self.ask_ai_question(ai_question)
                    
                    if use_tts:
                        self.speak_response(response)
                    else:
                        print(f"Bot: {response}")
                
                # Show communication log if WebSocket is active
                if enable_websocket and len(self.communication_log) > 0:
                    recent_messages = self.communication_log[-3:]  # Show last 3 messages
                    for msg in recent_messages:
                        if msg not in getattr(self, '_shown_messages', set()):
                            print(f"  [AI Communication] {msg}")
                            if not hasattr(self, '_shown_messages'):
                                self._shown_messages = set()
                            self._shown_messages.add(msg)
                        
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error in chat loop: {e}")
        
        # Cleanup
        if enable_websocket:
            self.stop_websocket_communication()
    
    def get_communication_log(self):
        """Get the communication log."""
        if hasattr(self, 'communication_log'):
            return self.communication_log.copy()
        return []
    
    def get_stats(self):
        """Get chatbot and communication statistics.""" 
        stats = {
            "blenderbot_available": BLENDERBOT_AVAILABLE,
            "websocket_available": WEBSOCKET_AVAILABLE,
            "websocket_enabled": getattr(self, 'websocket_enabled', False),
            "communication_messages": len(getattr(self, 'communication_log', [])),
            "educational_context": getattr(self, 'educational_context', {}),
            "model_loaded": self.model is not None and self.tokenizer is not None
        }
        
        if hasattr(self, 'websocket_communicator') and self.websocket_communicator:
            stats["websocket_stats"] = self.websocket_communicator.get_stats()
        
        return stats


def main():
    """Main function to run the chatbot."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Teacher1 BlenderBot Chatbot")
    parser.add_argument("--no-tts", action="store_true", 
                       help="Disable text-to-speech")
    parser.add_argument("--speech", action="store_true",
                       help="Enable speech recognition")
    parser.add_argument("--model-name", type=str,
                       help="BlenderBot model name (default: facebook/blenderbot-400M-distill)")
    parser.add_argument("--websocket", action="store_true",
                       help="Enable WebSocket communication with Fractal AI")
    parser.add_argument("--websocket-port", type=int, default=8766,
                       help="WebSocket server port (default: 8766)")
    parser.add_argument("--target-port", type=int, default=8765,
                       help="Target WebSocket port for Fractal AI (default: 8765)")
    
    args = parser.parse_args()
    
    # Create chatbot instance
    chatbot = Teacher1ChatBot(
        model_path=args.model_name,
        websocket_port=args.websocket_port,
        target_port=args.target_port
    )
    
    if args.websocket:
        print(f"WebSocket enabled - Server on port {args.websocket_port}, Target on port {args.target_port}")
    
    # Run chat loop
    try:
        asyncio.run(chatbot.chat_loop(
            use_speech=args.speech,
            use_tts=not args.no_tts,
            enable_websocket=args.websocket
        ))
    except KeyboardInterrupt:
        print("\nShutting down...")
        if args.websocket:
            chatbot.stop_websocket_communication()


if __name__ == "__main__":
    main()