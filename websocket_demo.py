#!/usr/bin/env python3
"""
Teacher1 WebSocket Communication Demo
====================================

This script demonstrates the bidirectional WebSocket communication between
the Fractal AI system and the Rasa chatbot. It shows how both systems can
initiate and respond to questions in real-time.

Usage Examples:
    # Run both AI and chatbot with WebSocket communication
    python websocket_demo.py --both
    
    # Run only Fractal AI with WebSocket enabled
    python websocket_demo.py --ai-only
    
    # Run only Rasa chatbot with WebSocket enabled
    python websocket_demo.py --chatbot-only
    
    # Test with mock systems
    python websocket_demo.py --test
"""

import asyncio
import logging
import sys
import os
import threading
import time
from typing import Optional

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def run_fractal_ai():
    """Run the Fractal AI system with WebSocket communication."""
    try:
        from fractal_emergent_ai import FractalEmergentAI
        
        print("🧠 Starting Fractal AI with WebSocket communication...")
        print("   Server: localhost:8765")
        print("   Target: localhost:8766 (Rasa chatbot)")
        
        ai = FractalEmergentAI()
        
        try:
            # Run with WebSocket enabled, quick mode for demo
            ai.run(steps=200, show=False, enable_websocket=True)
            
            print("\n📊 Fractal AI Communication Summary:")
            stats = ai.get_stats()
            print(f"   Messages exchanged: {stats['communication_messages']}")
            print(f"   Last insights: {stats['last_insights']}")
            if 'websocket_stats' in stats:
                ws_stats = stats['websocket_stats']
                print(f"   Connected clients: {ws_stats['connected_clients']}")
                print(f"   Client connection: {ws_stats['has_client_connection']}")
            
            print("\n💬 Communication Log:")
            for i, msg in enumerate(ai.get_communication_log()[-10:], 1):  # Last 10 messages
                print(f"   {i:2d}. {msg}")
                
        except KeyboardInterrupt:
            print("\n⏹️  Stopping Fractal AI...")
            ai.stop_websocket_communication()
            
    except ImportError as e:
        print(f"❌ Error importing Fractal AI: {e}")
        print("   Please ensure numpy and matplotlib are installed")


def run_personalized_chatbot():
    """Run the personalized chatbot."""
    try:
        from personalized_chatbot import PersonalizedKindergartenChatbot
        
        print("🤖 Starting Personalized Chatbot...")
        print("   Interactive educational chat")
        print("   Type messages to chat, or 'quit' to exit")
        
        chatbot = PersonalizedKindergartenChatbot()
        
        try:
            chatbot.interactive_session()
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
        except Exception as e:
            print(f"Error during chat: {e}")
    except ImportError as e:
        print(f"❌ Error: Could not import personalized chatbot: {e}")
        print("   Please ensure the personalized_chatbot.py module is available")


async def run_both_systems():
    """Run both systems simultaneously with WebSocket communication."""
    print("🚀 Starting both Fractal AI and Rasa chatbot with WebSocket communication...")
    print("   This will run both systems in parallel")
    print("   Press Ctrl+C to stop both systems")
    
    # Run Fractal AI in a separate thread
    ai_thread = threading.Thread(target=run_fractal_ai, daemon=True)
    ai_thread.start()
    
    # Give AI time to start
    await asyncio.sleep(3)
    
    # Run personalized chatbot in main thread
    run_personalized_chatbot()


async def run_test_mode():
    """Run test mode with mock systems."""
    print("🧪 Running test mode with mock systems...")
    
    from test_websocket_communication import test_bidirectional_communication
    
    try:
        await test_bidirectional_communication(duration=30)
        print("✅ Test completed successfully!")
    except Exception as e:
        print(f"❌ Test failed: {e}")


def print_usage():
    """Print usage instructions."""
    print("""
📚 Teacher1 WebSocket Communication Demo
========================================

This demo shows bidirectional WebSocket communication between the Fractal AI
system and the Rasa chatbot. Both systems can ask and answer questions in real-time.

Available Commands:
  --both      Run both AI and chatbot together (recommended)
  --ai-only   Run only Fractal AI with WebSocket enabled  
  --chatbot-only Run only personalized chatbot
  --test      Run test mode with mock systems
  --help      Show this help message

WebSocket Configuration:
  - Fractal AI runs server on port 8765, connects to port 8766
  - Chatbot runs as interactive educational system
  
Message Format:
  {
    "message_id": "unique_id",
    "sender": "fractal_ai|chatbot",
    "type": "question|answer|ack", 
    "content": "message text",
    "in_reply_to": "replied_message_id",
    "timestamp": "ISO8601_timestamp"
  }

Features Demonstrated:
  ✅ Bidirectional communication (both can initiate)
  ✅ Turn-taking (wait for answer before next question)  
  ✅ Message deduplication (prevents loops/spam)
  ✅ Structured JSON messaging
  ✅ Educational context integration
  ✅ Real-time insights sharing

Prerequisites:
  - Python 3.7+
  - websockets library: pip install websockets
  - numpy, matplotlib: pip install numpy matplotlib
  - Optional: Rasa for full chatbot functionality

Examples:
  python websocket_demo.py --both
  python websocket_demo.py --test
  python websocket_demo.py --ai-only
""")


async def main():
    """Main demo function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Teacher1 WebSocket Communication Demo")
    parser.add_argument("--both", action="store_true", 
                       help="Run both AI and chatbot together")
    parser.add_argument("--ai-only", action="store_true",
                       help="Run only Fractal AI with WebSocket")
    parser.add_argument("--chatbot-only", action="store_true", 
                       help="Run only personalized chatbot")
    parser.add_argument("--test", action="store_true",
                       help="Run test mode with mock systems")
    
    args = parser.parse_args()
    
    if not any([args.both, args.ai_only, args.chatbot_only, args.test]):
        print_usage()
        return
    
    print("🎓 Teacher1 WebSocket Communication Demo")
    print("=" * 50)
    
    try:
        if args.test:
            await run_test_mode()
        elif args.both:
            await run_both_systems()
        elif args.ai_only:
            run_fractal_ai()
        elif args.chatbot_only:
            run_personalized_chatbot()
            
    except KeyboardInterrupt:
        print("\n👋 Demo stopped by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())