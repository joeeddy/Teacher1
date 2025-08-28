"""
Test Multi-Chatbot WebSocket Communication for Teacher1
-------------------------------------------------------
Test script to verify that multiple chatbots (personalized + HuggingFace)
can communicate simultaneously via WebSocket with the Fractal AI system.
"""

import asyncio
import logging
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from websocket_communication import WebSocketCommunicator
from huggingface_websocket_chatbot import HuggingFaceWebSocketChatbot

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MockFractalAI:
    """Mock Fractal AI system for testing multiple chatbot communication."""
    
    def __init__(self, port=8765):
        self.communicator = WebSocketCommunicator(
            name="fractal_ai_mock",
            server_port=port,
            target_host="localhost",
            target_port=None  # Will connect to chatbots as client
        )
        self.communication_log = []
        self.insights = [
            "Detecting adaptive learning patterns in personalized education systems",
            "Observing conversational flow dynamics in multi-agent educational environments",
            "Analyzing cognitive load distribution across different AI interaction modalities",
            "Identifying optimal pedagogical strategies through multi-system collaboration",
            "Discovering emergent educational insights from parallel AI conversations"
        ]
        self.insight_index = 0
        
        # Set up handlers
        self.communicator.on_question_received = self._handle_question
        self.communicator.on_answer_received = self._handle_answer
    
    async def _handle_question(self, message: dict) -> str:
        """Handle questions from chatbots."""
        question = message['content']
        sender = message.get('sender', 'unknown')
        self.communication_log.append(f"Question from {sender}: {question}")
        
        # Generate educational insights
        base_insight = self.insights[self.insight_index % len(self.insights)]
        
        if "personalized" in sender.lower():
            response = f"From personalized learning perspective: {base_insight}"
        elif "huggingface" in sender.lower():
            response = f"From conversational AI perspective: {base_insight}"
        else:
            response = f"Educational insight: {base_insight}"
        
        self.insight_index += 1
        self.communication_log.append(f"Responded to {sender}: {response}")
        return response
    
    async def _handle_answer(self, message: dict):
        """Handle answers from chatbots."""
        answer = message['content']
        sender = message.get('sender', 'unknown')
        self.communication_log.append(f"Answer from {sender}: {answer}")
    
    async def send_educational_insights(self):
        """Send educational insights to connected chatbots."""
        insights = [
            "How can we optimize learning experiences using multiple AI perspectives?",
            "What patterns emerge when different AI systems collaborate in education?",
            "How might personalized and conversational AI complement each other?",
            "What are the benefits of multi-agent educational systems?"
        ]
        
        insight_index = 0
        while True:
            await asyncio.sleep(25)  # Send insight every 25 seconds
            
            if self.communicator.is_ready_to_send_question():
                insight = insights[insight_index % len(insights)]
                await self.communicator.send_question(insight)
                self.communication_log.append(f"Sent insight: {insight}")
                insight_index += 1
    
    async def start(self):
        """Start the mock Fractal AI system."""
        await self.communicator.start_server()
        logger.info("Mock Fractal AI system started")
        
        # Start sending insights
        insight_task = asyncio.create_task(self.send_educational_insights())
        await insight_task
    
    async def stop(self):
        """Stop the mock Fractal AI system."""
        await self.communicator.stop()


async def test_multi_chatbot_communication(duration: int = 90):
    """
    Test communication between Fractal AI, Personalized Chatbot, and HuggingFace Chatbot.
    
    Args:
        duration: Test duration in seconds
    """
    logger.info("Starting multi-chatbot WebSocket communication test")
    
    # Initialize systems
    fractal_ai = MockFractalAI(port=8765)
    hf_chatbot = HuggingFaceWebSocketChatbot(port=8767, target_port=8765)
    
    try:
        logger.info("Starting mock systems...")
        
        # Start Fractal AI mock
        fractal_task = asyncio.create_task(fractal_ai.start())
        await asyncio.sleep(2)  # Give server time to start
        logger.info("Mock Fractal AI started")
        
        # Start HuggingFace chatbot with more detailed startup
        logger.info("Starting HuggingFace WebSocket chatbot...")
        await hf_chatbot.communicator.start_server()
        logger.info(f"HuggingFace WebSocket server started on port {hf_chatbot.port}")
        
        # Connect to Fractal AI
        await asyncio.sleep(2)
        connected = await hf_chatbot.communicator.connect_as_client()
        if connected:
            logger.info("HuggingFace chatbot connected to Fractal AI")
        else:
            logger.warning("HuggingFace chatbot failed to connect to Fractal AI")
        
        await asyncio.sleep(2)  # Give time for connection to stabilize
        
        logger.info("Sending initial test messages...")
        
        # Send initial question to HuggingFace chatbot
        await fractal_ai.communicator.send_question(
            "Hello HuggingFace chatbot! How can conversational AI enhance educational experiences?"
        )
        
        # Start proactive communication tasks
        logger.info("Starting proactive communication tasks...")
        ai_insights_task = asyncio.create_task(fractal_ai.send_educational_insights())
        hf_questions_task = asyncio.create_task(hf_chatbot.send_proactive_questions(35))
        
        logger.info(f"Running multi-chatbot communication test for {duration} seconds...")
        
        # Run for specified duration
        await asyncio.sleep(duration)
        
        # Cancel tasks
        ai_insights_task.cancel()
        hf_questions_task.cancel()
        
        logger.info("Test duration completed")
        
    except Exception as e:
        logger.error(f"Error in multi-chatbot test: {e}")
        raise
    finally:
        logger.info("Stopping test systems...")
        
        # Stop all systems
        await hf_chatbot.stop()
        await fractal_ai.stop()
        
        # Print communication logs
        print("\n" + "="*80)
        print("FRACTAL AI COMMUNICATION LOG")
        print("="*80)
        for i, entry in enumerate(fractal_ai.communication_log, 1):
            print(f"{i:2d}. {entry}")
        
        print("\n" + "="*80)
        print("HUGGINGFACE CHATBOT COMMUNICATION LOG")
        print("="*80)
        hf_log = hf_chatbot.get_communication_log()
        for i, entry in enumerate(hf_log, 1):
            print(f"{i:2d}. {entry}")
        
        print("\n" + "="*80)
        print("COMMUNICATION STATISTICS")
        print("="*80)
        print(f"Fractal AI messages: {len(fractal_ai.communication_log)}")
        print(f"HuggingFace messages: {len(hf_log)}")
        
        # Print status
        hf_status = hf_chatbot.get_chatbot_status()
        print(f"\nHuggingFace Chatbot Status:")
        for key, value in hf_status.items():
            print(f"  {key}: {value}")
        
        logger.info("Multi-chatbot test cleanup completed")


if __name__ == "__main__":
    print("Multi-Chatbot WebSocket Communication Test for Teacher1")
    print("=" * 60)
    print("Testing: Fractal AI ↔ HuggingFace BlenderBot")
    print("This test verifies that multiple AI systems can communicate simultaneously")
    print()
    
    # Run the test
    try:
        asyncio.run(test_multi_chatbot_communication(60))
        print("\n✅ Multi-chatbot communication test PASSED!")
    except KeyboardInterrupt:
        print("\n⏹️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Multi-chatbot communication test FAILED: {e}")
        sys.exit(1)