"""
HuggingFace BlenderBot Chatbot for Teacher1
-------------------------------------------
A conversational AI chatbot using HuggingFace's BlenderBot model for open-ended,
natural conversation in educational contexts.

This module provides a chatbot interface compatible with the Teacher1 system
using state-of-the-art conversational AI from HuggingFace transformers.
"""

import os
import sys
import logging
import time
import warnings
from typing import Optional, Dict, List, Tuple
from datetime import datetime

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import transformers, handle gracefully if not available
HUGGINGFACE_AVAILABLE = False
try:
    from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
    import torch
    HUGGINGFACE_AVAILABLE = True
    logger.info("HuggingFace transformers available - BlenderBot ready")
except ImportError as e:
    logger.warning(f"HuggingFace transformers not available: {e}")
    logger.warning("Install with: pip install transformers torch")


class HuggingFaceBlenderBotChatbot:
    """
    HuggingFace BlenderBot-based chatbot for natural conversation.
    
    This chatbot provides open-ended conversational AI capabilities using
    Facebook's BlenderBot model, designed to complement the educational
    features of Teacher1 with natural dialogue capabilities.
    """
    
    def __init__(self, model_name: str = "facebook/blenderbot-400M-distill"):
        """
        Initialize the HuggingFace BlenderBot chatbot.
        
        Args:
            model_name: HuggingFace model identifier for BlenderBot
        """
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.current_student = None
        self.current_session_id = None
        self.session_start_time = None
        self.conversation_history = []
        self.max_history_length = 10  # Keep last 10 exchanges
        
        # Educational context prompts
        self.educational_context = {
            "system_prompt": (
                "You are a friendly AI assistant helping with educational conversations. "
                "You should be encouraging, age-appropriate, and supportive of learning. "
                "Keep responses conversational but educational when appropriate."
            ),
            "fallback_responses": [
                "That's really interesting! Tell me more about what you're thinking.",
                "I love learning new things with you! What would you like to explore?",
                "You have such great ideas! What else are you curious about?",
                "That's a wonderful question! Let's think about that together.",
                "I enjoy our conversations! What would you like to talk about next?"
            ]
        }
        
        # Initialize the model if available
        self._initialize_model()
    
    def _initialize_model(self) -> bool:
        """
        Initialize the BlenderBot model and tokenizer.
        
        Returns:
            bool: True if initialization successful, False otherwise
        """
        if not HUGGINGFACE_AVAILABLE:
            logger.warning("HuggingFace transformers not available - using fallback responses")
            return False
        
        try:
            logger.info(f"Loading BlenderBot model: {self.model_name}")
            
            # Suppress some warnings during model loading
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                
                # Load tokenizer and model
                self.tokenizer = BlenderbotTokenizer.from_pretrained(self.model_name)
                self.model = BlenderbotForConditionalGeneration.from_pretrained(self.model_name)
                
                # Move to GPU if available
                if torch.cuda.is_available():
                    self.model = self.model.cuda()
                    logger.info("Model loaded on GPU")
                else:
                    logger.info("Model loaded on CPU")
            
            logger.info("BlenderBot model initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize BlenderBot model: {e}")
            logger.warning("Falling back to simple response generation")
            return False
    
    def start_session(self, student_name: str) -> str:
        """
        Start a new conversation session.
        
        Args:
            student_name: Name of the student
            
        Returns:
            str: Welcome message
        """
        self.current_student = student_name
        self.current_session_id = f"hf_session_{int(time.time())}"
        self.session_start_time = datetime.now()
        self.conversation_history = []
        
        # Generate personalized greeting
        greeting = self._generate_personalized_greeting()
        logger.info(f"Started HuggingFace BlenderBot session for {student_name}")
        return greeting
    
    def _generate_personalized_greeting(self) -> str:
        """Generate a personalized greeting for the student."""
        if self.current_student:
            greeting_input = f"Hello {self.current_student}! I'm an AI assistant here to chat and help with learning."
            
            if self.model and self.tokenizer:
                try:
                    response = self._generate_response(greeting_input, is_greeting=True)
                    return response
                except Exception as e:
                    logger.warning(f"Error generating greeting with model: {e}")
            
            # Fallback greeting
            return f"Hello {self.current_student}! I'm your AI conversation partner. I'm here to chat, answer questions, and help with learning. What would you like to talk about today?"
        
        return "Hello! I'm an AI chatbot ready to have a conversation with you. What's on your mind?"
    
    def get_response(self, user_input: str) -> Tuple[str, Dict]:
        """
        Generate a response to user input.
        
        Args:
            user_input: The user's message
            
        Returns:
            Tuple[str, Dict]: Response message and metadata
        """
        if not user_input.strip():
            return "I'm listening! What would you like to talk about?", {}
        
        start_time = time.time()
        
        try:
            # Check for session end
            if any(phrase in user_input.lower() for phrase in ['bye', 'goodbye', 'see you', 'quit', 'exit']):
                return self.end_session(), {"type": "session_end"}
            
            # Generate response using model or fallback
            response = self._generate_response(user_input)
            
            # Add to conversation history
            self._update_conversation_history(user_input, response)
            
            response_time = time.time() - start_time
            
            metadata = {
                "type": "conversation",
                "response_time": response_time,
                "model_used": self.model_name if self.model else "fallback",
                "conversation_length": len(self.conversation_history)
            }
            
            return response, metadata
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            fallback = self._get_fallback_response()
            return fallback, {"type": "error", "error": str(e)}
    
    def _generate_response(self, user_input: str, is_greeting: bool = False) -> str:
        """
        Generate response using BlenderBot model or fallback.
        
        Args:
            user_input: User's input message
            is_greeting: Whether this is a greeting exchange
            
        Returns:
            str: Generated response
        """
        if not self.model or not self.tokenizer:
            return self._get_fallback_response()
        
        try:
            # Prepare conversation context
            context = self._prepare_conversation_context(user_input, is_greeting)
            
            # Tokenize input
            inputs = self.tokenizer(context, return_tensors="pt", truncation=True, max_length=512)
            
            # Move to same device as model
            if torch.cuda.is_available() and self.model.device.type == 'cuda':
                inputs = {k: v.cuda() for k, v in inputs.items()}
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs["input_ids"],
                    max_length=150,
                    min_length=10,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.9,
                    pad_token_id=self.tokenizer.eos_token_id,
                    no_repeat_ngram_size=3
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Clean up response (remove input echo if present)
            if context in response:
                response = response.replace(context, "").strip()
            
            # Ensure response is appropriate and not empty
            if not response or len(response.strip()) < 3:
                return self._get_fallback_response()
            
            # Apply educational filtering
            response = self._filter_educational_content(response)
            
            return response
            
        except Exception as e:
            logger.warning(f"Error in model generation: {e}")
            return self._get_fallback_response()
    
    def _prepare_conversation_context(self, user_input: str, is_greeting: bool = False) -> str:
        """
        Prepare conversation context including history.
        
        Args:
            user_input: Current user input
            is_greeting: Whether this is a greeting
            
        Returns:
            str: Formatted context for the model
        """
        if is_greeting:
            return f"{self.educational_context['system_prompt']} {user_input}"
        
        # Build context with recent conversation history
        context_parts = [self.educational_context['system_prompt']]
        
        # Add recent conversation history (last few exchanges)
        recent_history = self.conversation_history[-4:]  # Last 2 exchanges
        for exchange in recent_history:
            context_parts.append(f"Student: {exchange['user']}")
            context_parts.append(f"Assistant: {exchange['bot']}")
        
        # Add current input
        context_parts.append(f"Student: {user_input}")
        context_parts.append("Assistant:")
        
        return " ".join(context_parts)
    
    def _filter_educational_content(self, response: str) -> str:
        """
        Filter response to ensure educational appropriateness.
        
        Args:
            response: Raw model response
            
        Returns:
            str: Filtered response
        """
        # Basic filtering - ensure response is appropriate
        # Remove potentially inappropriate content, keep educational focus
        
        # Ensure response length is reasonable
        sentences = response.split('. ')
        if len(sentences) > 3:
            response = '. '.join(sentences[:3]) + '.'
        
        # Ensure positive, educational tone
        if any(word in response.lower() for word in ['stupid', 'dumb', 'bad', 'wrong', 'hate']):
            return self._get_fallback_response()
        
        return response.strip()
    
    def _update_conversation_history(self, user_input: str, bot_response: str):
        """Update conversation history with new exchange."""
        self.conversation_history.append({
            "user": user_input,
            "bot": bot_response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only recent history
        if len(self.conversation_history) > self.max_history_length:
            self.conversation_history = self.conversation_history[-self.max_history_length:]
    
    def _get_fallback_response(self) -> str:
        """Get a fallback response when model is unavailable."""
        import random
        return random.choice(self.educational_context["fallback_responses"])
    
    def end_session(self) -> str:
        """End the current conversation session."""
        if self.current_student:
            goodbye_msg = f"It was great chatting with you, {self.current_student}! I enjoyed our conversation. Feel free to come back anytime you want to chat or learn something new!"
        else:
            goodbye_msg = "Thanks for the conversation! Come back anytime you want to chat or explore new ideas!"
        
        # Reset session
        self.current_student = None
        self.current_session_id = None
        self.session_start_time = None
        self.conversation_history = []
        
        return goodbye_msg
    
    def get_student_progress_summary(self) -> Dict:
        """Get a summary of the current conversation session."""
        if not self.current_student:
            return {}
        
        session_duration = 0
        if self.session_start_time:
            session_duration = (datetime.now() - self.session_start_time).seconds
        
        return {
            "student_name": self.current_student,
            "session_id": self.current_session_id,
            "conversation_length": len(self.conversation_history),
            "session_duration_seconds": session_duration,
            "model_name": self.model_name,
            "model_available": self.model is not None,
            "last_exchange": self.conversation_history[-1] if self.conversation_history else None
        }
    
    def is_model_available(self) -> bool:
        """Check if the HuggingFace model is available and loaded."""
        return self.model is not None and self.tokenizer is not None


# Example usage and testing
if __name__ == "__main__":
    print("HuggingFace BlenderBot Chatbot for Teacher1")
    print("=" * 50)
    
    # Initialize chatbot
    print("Initializing BlenderBot chatbot...")
    chatbot = HuggingFaceBlenderBotChatbot()
    
    if not chatbot.is_model_available():
        print("\nNote: HuggingFace model not available. Install requirements:")
        print("pip install transformers torch")
        print("Running in fallback mode with simple responses.\n")
    
    # Start a test session
    print("\nStarting test conversation:")
    greeting = chatbot.start_session("Alex")
    print(f"Bot: {greeting}")
    
    # Test conversation examples
    test_inputs = [
        "Hi! I'm excited to chat with you today!",
        "Can you tell me about space?",
        "What's your favorite subject to talk about?",
        "I like learning about animals",
        "Do you know any fun facts?",
        "bye"
    ]
    
    for user_input in test_inputs:
        print(f"\nStudent: {user_input}")
        response, metadata = chatbot.get_response(user_input)
        print(f"Bot: {response}")
        
        if metadata.get("type") == "session_end":
            break
    
    # Show session summary
    summary = chatbot.get_student_progress_summary()
    if summary:
        print(f"\nSession Summary:")
        print(f"- Student: {summary.get('student_name', 'Unknown')}")
        print(f"- Exchanges: {summary.get('conversation_length', 0)}")
        print(f"- Duration: {summary.get('session_duration_seconds', 0)} seconds")
        print(f"- Model: {summary.get('model_name', 'Unknown')}")