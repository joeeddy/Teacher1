"""
HuggingFace BlenderBot WebSocket Integration for Teacher1
--------------------------------------------------------
WebSocket-enabled HuggingFace BlenderBot chatbot that can communicate with
other AI components in the Teacher1 system via the WebSocket communication protocol.

This module integrates the HuggingFace BlenderBot with the Teacher1 WebSocket
communication system, allowing real-time bidirectional communication between
the conversational AI and other system components.
"""

import asyncio
import logging
import sys
import os
from typing import Dict, Optional

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from websocket_communication import WebSocketCommunicator
from huggingface_chatbot import HuggingFaceBlenderBotChatbot

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HuggingFaceWebSocketChatbot:
    """
    WebSocket-enabled HuggingFace BlenderBot for Teacher1 system integration.
    
    This class wraps the HuggingFace BlenderBot chatbot with WebSocket communication
    capabilities, allowing it to participate in real-time conversations with other
    AI components in the Teacher1 ecosystem.
    """
    
    def __init__(self, port: int = 8767, target_port: int = 8765, 
                 target_host: str = "localhost", model_name: str = "facebook/blenderbot-400M-distill"):
        """
        Initialize the WebSocket-enabled HuggingFace chatbot.
        
        Args:
            port: Port for this chatbot's WebSocket server
            target_port: Port of the target WebSocket server (e.g., Fractal AI)
            target_host: Host of the target WebSocket server
            model_name: HuggingFace model identifier for BlenderBot
        """
        self.port = port
        self.target_port = target_port
        self.target_host = target_host
        
        # Initialize WebSocket communicator
        self.communicator = WebSocketCommunicator(
            name="huggingface_blenderbot",
            server_port=port,
            target_host=target_host,
            target_port=target_port
        )
        
        # Initialize HuggingFace chatbot
        self.chatbot = HuggingFaceBlenderBotChatbot(model_name=model_name)
        
        # Communication tracking
        self.communication_log = []
        self.active_conversations = {}  # conversation_id -> context
        
        # Set up WebSocket message handlers
        self.communicator.on_question_received = self._handle_question
        self.communicator.on_answer_received = self._handle_answer
        self.communicator.on_ack_received = self._handle_ack
        
        logger.info(f"HuggingFace WebSocket chatbot initialized on port {port}")
        logger.info(f"Model available: {self.chatbot.is_model_available()}")
    
    async def _handle_question(self, message: dict) -> str:
        """
        Handle questions received from other AI components.
        
        Args:
            message: WebSocket message dictionary
            
        Returns:
            str: Response to the question
        """
        question = message['content']
        sender = message.get('sender', 'unknown')
        message_id = message.get('message_id', 'unknown')
        
        self.communication_log.append(f"Question from {sender}: {question}")
        logger.info(f"Received question from {sender}: {question}")
        
        try:
            # Use chatbot to generate response
            response, metadata = self.chatbot.get_response(question)
            
            # Log the interaction
            self.communication_log.append(f"Responded to {sender}: {response}")
            logger.info(f"Generated response for {sender}: {response[:100]}...")
            
            # Store conversation context if needed
            conversation_id = f"{sender}_{message_id}"
            self.active_conversations[conversation_id] = {
                "last_question": question,
                "last_response": response,
                "metadata": metadata
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Error handling question from {sender}: {e}")
            fallback_response = "I'm having trouble processing that right now. Could you try asking in a different way?"
            self.communication_log.append(f"Error response to {sender}: {fallback_response}")
            return fallback_response
    
    async def _handle_answer(self, message: dict):
        """
        Handle answers received from other AI components.
        
        Args:
            message: WebSocket message dictionary
        """
        answer = message['content']
        sender = message.get('sender', 'unknown')
        in_reply_to = message.get('in_reply_to')
        
        self.communication_log.append(f"Answer from {sender}: {answer}")
        logger.info(f"Received answer from {sender}: {answer}")
        
        # Could process the answer and potentially ask follow-up questions
        # For now, just log the interaction
        
        # If this is an educational context, we might want to acknowledge learning
        if any(keyword in answer.lower() for keyword in ['learn', 'teach', 'student', 'education']):
            logger.info(f"Educational answer received from {sender}")
    
    async def _handle_ack(self, message: dict):
        """
        Handle acknowledgments from other AI components.
        
        Args:
            message: WebSocket message dictionary
        """
        sender = message.get('sender', 'unknown')
        logger.debug(f"Received acknowledgment from {sender}")
    
    async def send_proactive_questions(self, interval: int = 30):
        """
        Send proactive educational questions to stimulate conversation.
        
        Args:
            interval: Seconds between proactive questions
        """
        educational_questions = [
            "What learning patterns are you observing in student interactions?",
            "How can we make educational content more engaging for different learning styles?",
            "What insights do you have about effective teaching methods?",
            "How might we personalize learning experiences better?",
            "What are some creative ways to assess student understanding?",
            "How can we encourage more collaborative learning?",
            "What role does storytelling play in education?",
            "How can we make learning more fun and interactive?"
        ]
        
        question_index = 0
        
        while True:
            await asyncio.sleep(interval)
            
            # Only send if ready and connected
            if self.communicator.is_ready_to_send_question():
                question = educational_questions[question_index % len(educational_questions)]
                
                try:
                    await self.communicator.send_question(question)
                    self.communication_log.append(f"Proactive question sent: {question}")
                    logger.info(f"Sent proactive question: {question}")
                    question_index += 1
                    
                except Exception as e:
                    logger.error(f"Error sending proactive question: {e}")
    
    async def start(self):
        """Start the WebSocket chatbot server and client connections."""
        try:
            logger.info("Starting HuggingFace WebSocket chatbot...")
            
            # Start WebSocket server
            await self.communicator.start_server()
            logger.info(f"WebSocket server started on port {self.port}")
            
            # Start WebSocket client (connect to other components)
            connected = await self.communicator.connect_as_client()
            if connected:
                logger.info(f"Connected to target server at {self.target_host}:{self.target_port}")
            else:
                logger.warning(f"Failed to connect to target server at {self.target_host}:{self.target_port}")
                logger.info("Running in server-only mode")
            
            # Start proactive question sending (optional)
            proactive_task = asyncio.create_task(self.send_proactive_questions(45))
            
            logger.info("HuggingFace WebSocket chatbot is running...")
            
            # Keep running
            await proactive_task
            
        except Exception as e:
            logger.error(f"Error starting HuggingFace WebSocket chatbot: {e}")
            raise
    
    async def stop(self):
        """Stop the WebSocket chatbot and cleanup."""
        logger.info("Stopping HuggingFace WebSocket chatbot...")
        await self.communicator.stop()
        logger.info("HuggingFace WebSocket chatbot stopped")
    
    def get_communication_log(self) -> list:
        """Get the communication log for debugging/monitoring."""
        return self.communication_log.copy()
    
    def get_chatbot_status(self) -> dict:
        """Get status information about the chatbot."""
        return {
            "model_available": self.chatbot.is_model_available(),
            "model_name": self.chatbot.model_name,
            "active_conversations": len(self.active_conversations),
            "communication_log_length": len(self.communication_log),
            "websocket_ready": self.communicator.conversation_state == "idle",
            "current_student": self.chatbot.current_student
        }


async def run_huggingface_chatbot(port: int = 8767, target_port: int = 8765, 
                                 duration: int = None):
    """
    Run the HuggingFace WebSocket chatbot for testing.
    
    Args:
        port: Port for the chatbot server
        target_port: Port of the target server to connect to
        duration: How long to run (None = indefinitely)
    """
    chatbot = HuggingFaceWebSocketChatbot(port=port, target_port=target_port)
    
    try:
        if duration:
            # Run for specified duration
            await asyncio.wait_for(chatbot.start(), timeout=duration)
        else:
            # Run indefinitely
            await chatbot.start()
            
    except asyncio.TimeoutError:
        logger.info(f"Test completed after {duration} seconds")
    except KeyboardInterrupt:
        logger.info("Chatbot stopped by user")
    except Exception as e:
        logger.error(f"Error running chatbot: {e}")
    finally:
        await chatbot.stop()
        
        # Print final status
        status = chatbot.get_chatbot_status()
        log = chatbot.get_communication_log()
        
        print("\n" + "="*60)
        print("HUGGINGFACE CHATBOT FINAL STATUS")
        print("="*60)
        for key, value in status.items():
            print(f"{key}: {value}")
        
        print(f"\nCOMMUNICATION LOG ({len(log)} entries):")
        print("-"*40)
        for i, entry in enumerate(log[-10:], 1):  # Show last 10 entries
            print(f"{i:2d}. {entry}")


if __name__ == "__main__":
    print("HuggingFace BlenderBot WebSocket Integration for Teacher1")
    print("=" * 60)
    
    # Check command line arguments
    import argparse
    parser = argparse.ArgumentParser(description="Run HuggingFace WebSocket Chatbot")
    parser.add_argument("--port", type=int, default=8767, help="WebSocket server port")
    parser.add_argument("--target-port", type=int, default=8765, help="Target server port")
    parser.add_argument("--duration", type=int, default=60, help="Test duration in seconds")
    
    args = parser.parse_args()
    
    print(f"Starting HuggingFace chatbot on port {args.port}")
    print(f"Will connect to target server on port {args.target_port}")
    print(f"Test duration: {args.duration} seconds")
    print()
    
    # Run the chatbot
    asyncio.run(run_huggingface_chatbot(
        port=args.port,
        target_port=args.target_port,
        duration=args.duration
    ))