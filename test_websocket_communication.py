#!/usr/bin/env python3
"""
WebSocket Communication Test for Teacher1
=========================================

This script tests the bidirectional WebSocket communication between 
the Fractal AI system and chatbot components.
"""

import asyncio
import logging
import time
import sys
import os

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from websocket_communication import WebSocketCommunicator

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MockFractalAI:
    """Mock Fractal AI for testing WebSocket communication."""
    
    def __init__(self, port=8765, target_port=8766):
        self.communicator = WebSocketCommunicator(
            name="fractal_ai_mock",
            server_port=port,
            target_host="localhost",
            target_port=target_port
        )
        self.communication_log = []
        self.insights = [
            "Detecting high-frequency learning patterns in mathematical sequences",
            "Observing emergent creativity patterns in problem-solving approaches", 
            "Analyzing cognitive load distribution across different learning modalities",
            "Identifying optimal spacing intervals for knowledge retention"
        ]
        self.current_insight = 0
        
        # Set up handlers
        self.communicator.on_question_received = self._handle_question
        self.communicator.on_answer_received = self._handle_answer
        
    async def _handle_question(self, message: dict) -> str:
        """Handle questions from chatbot."""
        question = message['content']
        self.communication_log.append(f"Received: {question}")
        
        # Generate AI-like responses
        if "pattern" in question.lower():
            response = f"Current analysis shows {self.insights[self.current_insight % len(self.insights)]}"
        elif "learn" in question.lower():
            response = "My neural networks are continuously adapting through recursive feedback loops and meta-learning algorithms"
        elif "educational" in question.lower():
            response = "Educational applications include personalized learning paths, adaptive difficulty adjustment, and real-time comprehension assessment"
        else:
            response = f"Processing query through fractal analysis... {self.insights[self.current_insight % len(self.insights)]}"
        
        self.current_insight += 1
        self.communication_log.append(f"Responded: {response}")
        return response
    
    async def _handle_answer(self, message: dict):
        """Handle answers from chatbot."""
        answer = message['content']
        self.communication_log.append(f"Answer: {answer}")
    
    async def start(self):
        """Start the mock Fractal AI system."""
        await self.communicator.start_server()
        logger.info("Mock Fractal AI server started")
        
        # Try to connect to chatbot
        await asyncio.sleep(2)
        connected = await self.communicator.connect_as_client()
        if connected:
            logger.info("Mock Fractal AI connected to chatbot")
        
        return connected
    
    async def send_periodic_insights(self):
        """Send periodic insights to test proactive communication."""
        while True:
            await asyncio.sleep(15)  # Send insight every 15 seconds
            
            if self.communicator.is_ready_to_send_question():
                insight = self.insights[self.current_insight % len(self.insights)]
                question = f"I'm observing: {insight}. How might this apply to student learning?"
                
                await self.communicator.send_question(question)
                self.communication_log.append(f"Sent insight: {question}")
                self.current_insight += 1
    
    async def stop(self):
        """Stop the mock system."""
        await self.communicator.stop()


class MockChatBot:
    """Mock chatbot for testing WebSocket communication."""
    
    def __init__(self, port=8766, target_port=8765):
        self.communicator = WebSocketCommunicator(
            name="chatbot_mock",
            server_port=port,
            target_host="localhost",
            target_port=target_port
        )
        self.communication_log = []
        self.educational_responses = [
            "That's fascinating! We could use this for adaptive learning systems that adjust to student progress",
            "This insight could help create personalized learning experiences for different cognitive styles",
            "We might apply this to develop better assessment tools that measure true understanding",
            "This pattern could inform how we design collaborative learning environments"
        ]
        self.response_index = 0
        
        # Set up handlers
        self.communicator.on_question_received = self._handle_question
        self.communicator.on_answer_received = self._handle_answer
    
    async def _handle_question(self, message: dict) -> str:
        """Handle questions from Fractal AI."""
        question = message['content']
        self.communication_log.append(f"Received: {question}")
        
        # Generate educational responses
        base_response = self.educational_responses[self.response_index % len(self.educational_responses)]
        
        if "pattern" in question.lower():
            response = f"{base_response} Pattern recognition is fundamental to learning!"
        elif "creative" in question.lower():
            response = f"{base_response} Creativity enhances problem-solving skills in students!"
        elif "cognitive" in question.lower():
            response = f"{base_response} Understanding cognitive load helps optimize learning!"
        else:
            response = f"{base_response} This could revolutionize educational technology!"
        
        self.response_index += 1
        self.communication_log.append(f"Responded: {response}")
        return response
    
    async def _handle_answer(self, message: dict):
        """Handle answers from Fractal AI."""
        answer = message['content']
        self.communication_log.append(f"Answer: {answer}")
    
    async def start(self):
        """Start the mock chatbot system."""
        await self.communicator.start_server()
        logger.info("Mock chatbot server started")
        
        # Try to connect to Fractal AI
        await asyncio.sleep(2)
        connected = await self.communicator.connect_as_client()
        if connected:
            logger.info("Mock chatbot connected to Fractal AI")
        
        return connected
    
    async def send_educational_questions(self):
        """Send educational questions to test proactive communication."""
        questions = [
            "What learning patterns are most effective for mathematical concepts?",
            "How can we identify when students are struggling with comprehension?",
            "What insights do you have about optimal learning sequences?",
            "How might your analysis help with personalized education?"
        ]
        
        question_index = 0
        while True:
            await asyncio.sleep(20)  # Send question every 20 seconds
            
            if self.communicator.is_ready_to_send_question():
                question = questions[question_index % len(questions)]
                await self.communicator.send_question(question)
                self.communication_log.append(f"Asked: {question}")
                question_index += 1
    
    async def stop(self):
        """Stop the mock system."""
        await self.communicator.stop()


async def test_bidirectional_communication(duration: int = 60):
    """
    Test bidirectional WebSocket communication between mock systems.
    
    Args:
        duration: Test duration in seconds
    """
    logger.info("Starting bidirectional WebSocket communication test")
    
    # Create mock systems
    fractal_ai = MockFractalAI()
    chatbot = MockChatBot()
    
    try:
        # Start both systems
        logger.info("Starting mock systems...")
        await fractal_ai.start()
        await chatbot.start()
        
        # Give connections time to establish
        await asyncio.sleep(3)
        
        # Start periodic communication tasks
        ai_task = asyncio.create_task(fractal_ai.send_periodic_insights())
        chatbot_task = asyncio.create_task(chatbot.send_educational_questions())
        
        # Send initial test messages
        logger.info("Sending initial test messages...")
        
        # Fractal AI asks first question
        await fractal_ai.communicator.send_question(
            "Hello Chatbot! I'm analyzing learning patterns. What educational insights would you like?"
        )
        
        await asyncio.sleep(2)
        
        # Chatbot asks a question back
        await chatbot.communicator.send_question(
            "Hello Fractal AI! Can you analyze patterns for improving student engagement?"
        )
        
        # Let the systems communicate
        logger.info(f"Running communication test for {duration} seconds...")
        await asyncio.sleep(duration)
        
        # Cancel periodic tasks
        ai_task.cancel()
        chatbot_task.cancel()
        
        # Print communication logs
        print("\n" + "="*60)
        print("FRACTAL AI COMMUNICATION LOG:")
        print("="*60)
        for i, msg in enumerate(fractal_ai.communication_log, 1):
            print(f"{i:2d}. {msg}")
        
        print("\n" + "="*60)
        print("CHATBOT COMMUNICATION LOG:")
        print("="*60)
        for i, msg in enumerate(chatbot.communication_log, 1):
            print(f"{i:2d}. {msg}")
        
        # Print statistics
        print("\n" + "="*60)
        print("COMMUNICATION STATISTICS:")
        print("="*60)
        
        ai_stats = fractal_ai.communicator.get_stats()
        chatbot_stats = chatbot.communicator.get_stats()
        
        print(f"Fractal AI: {len(fractal_ai.communication_log)} messages, {ai_stats['cache_size']} cached")
        print(f"Chatbot: {len(chatbot.communication_log)} messages, {chatbot_stats['cache_size']} cached")
        print(f"AI Server Clients: {ai_stats['connected_clients']}")
        print(f"Chatbot Server Clients: {chatbot_stats['connected_clients']}")
        print(f"AI Client Connected: {ai_stats['has_client_connection']}")
        print(f"Chatbot Client Connected: {chatbot_stats['has_client_connection']}")
        
        logger.info("Test completed successfully!")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        raise
    finally:
        # Cleanup
        await fractal_ai.stop()
        await chatbot.stop()
        logger.info("Test cleanup completed")


async def main():
    """Main test function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test WebSocket communication")
    parser.add_argument("--duration", type=int, default=60,
                       help="Test duration in seconds (default: 60)")
    parser.add_argument("--verbose", action="store_true",
                       help="Enable verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    try:
        await test_bidirectional_communication(duration=args.duration)
        print("\n✅ WebSocket communication test PASSED!")
    except Exception as e:
        print(f"\n❌ WebSocket communication test FAILED: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())