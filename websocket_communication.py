"""
WebSocket Communication Module for Teacher1
==========================================

This module provides bidirectional WebSocket communication capabilities between
the Fractal AI system and the Rasa chatbot. It implements structured JSON messaging,
turn-taking, message tracking, and deduplication.

Message Format:
{
    "message_id": "unique_id",
    "sender": "fractal_ai|rasa_bot", 
    "type": "question|answer|ack",
    "content": "plain text message",
    "in_reply_to": "message_id_being_replied_to",
    "timestamp": "ISO8601_timestamp"
}
"""

import asyncio
import json
import logging
import time
import uuid
from datetime import datetime, timezone
from typing import Dict, Optional, Callable, Set
import websockets
from websockets.exceptions import ConnectionClosed, WebSocketException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebSocketCommunicator:
    """
    Handles bidirectional WebSocket communication with message tracking,
    turn-taking, and deduplication.
    """
    
    def __init__(self, name: str, server_port: int, target_host: str = "localhost", target_port: int = None):
        """
        Initialize WebSocket communicator.
        
        Args:
            name: Identifier for this communicator (e.g., "fractal_ai", "rasa_bot")
            server_port: Port to run WebSocket server on
            target_host: Host of the target WebSocket server
            target_port: Port of the target WebSocket server
        """
        self.name = name
        self.server_port = server_port
        self.target_host = target_host
        self.target_port = target_port
        
        # Connection management
        self.server = None
        self.client_websocket = None
        self.connected_clients: Set = set()
        
        # Message tracking and deduplication
        self.message_cache: Set[str] = set()
        self.pending_questions: Dict[str, dict] = {}  # message_id -> message
        self.conversation_state = "idle"  # idle, waiting_for_answer, processing
        
        # Message handlers
        self.message_handlers: Dict[str, Callable] = {
            "question": self._handle_question,
            "answer": self._handle_answer,
            "ack": self._handle_ack
        }
        
        # Custom message handlers (to be set by integrating systems)
        self.on_question_received: Optional[Callable] = None
        self.on_answer_received: Optional[Callable] = None
        self.on_ack_received: Optional[Callable] = None
        
        # Deduplication cache size limit
        self.max_cache_size = 1000
        
    def create_message(self, content: str, msg_type: str = "question", 
                      in_reply_to: Optional[str] = None) -> dict:
        """
        Create a structured message.
        
        Args:
            content: The message content
            msg_type: Type of message (question/answer/ack)
            in_reply_to: Message ID this is replying to
            
        Returns:
            Structured message dictionary
        """
        message = {
            "message_id": str(uuid.uuid4()),
            "sender": self.name,
            "type": msg_type,
            "content": content,
            "in_reply_to": in_reply_to,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        return message
    
    def _is_duplicate_message(self, message_id: str) -> bool:
        """Check if message has been seen before."""
        if message_id in self.message_cache:
            return True
        
        # Add to cache and manage size
        self.message_cache.add(message_id)
        if len(self.message_cache) > self.max_cache_size:
            # Remove oldest entries (simple approach - could be improved with LRU)
            oldest_entries = list(self.message_cache)[:100]
            for entry in oldest_entries:
                self.message_cache.discard(entry)
        
        return False
    
    async def _handle_message(self, websocket, message_data: dict):
        """
        Handle incoming message with deduplication and routing.
        """
        try:
            message_id = message_data.get("message_id")
            if not message_id:
                logger.warning("Received message without message_id")
                return
            
            # Check for duplicates
            if self._is_duplicate_message(message_id):
                logger.info(f"Ignoring duplicate message: {message_id}")
                return
            
            msg_type = message_data.get("type", "").lower()
            handler = self.message_handlers.get(msg_type)
            
            if handler:
                await handler(websocket, message_data)
            else:
                logger.warning(f"Unknown message type: {msg_type}")
                
        except Exception as e:
            logger.error(f"Error handling message: {e}")
    
    async def _handle_question(self, websocket, message: dict):
        """Handle incoming question."""
        logger.info(f"Received question from {message['sender']}: {message['content']}")
        
        # Send acknowledgment
        ack_msg = self.create_message(
            content=f"Question received: {message['message_id']}",
            msg_type="ack",
            in_reply_to=message["message_id"]
        )
        await self._send_to_websocket(websocket, ack_msg)
        
        # Call custom handler if set
        if self.on_question_received:
            try:
                response = await self.on_question_received(message)
                if response:
                    answer_msg = self.create_message(
                        content=response,
                        msg_type="answer",
                        in_reply_to=message["message_id"]
                    )
                    await self._send_to_websocket(websocket, answer_msg)
            except Exception as e:
                logger.error(f"Error in question handler: {e}")
    
    async def _handle_answer(self, websocket, message: dict):
        """Handle incoming answer."""
        logger.info(f"Received answer from {message['sender']}: {message['content']}")
        
        # Update conversation state
        in_reply_to = message.get("in_reply_to")
        if in_reply_to and in_reply_to in self.pending_questions:
            del self.pending_questions[in_reply_to]
            self.conversation_state = "idle"
        
        # Send acknowledgment
        ack_msg = self.create_message(
            content=f"Answer received: {message['message_id']}",
            msg_type="ack",
            in_reply_to=message["message_id"]
        )
        await self._send_to_websocket(websocket, ack_msg)
        
        # Call custom handler if set
        if self.on_answer_received:
            try:
                await self.on_answer_received(message)
            except Exception as e:
                logger.error(f"Error in answer handler: {e}")
    
    async def _handle_ack(self, websocket, message: dict):
        """Handle acknowledgment message."""
        logger.info(f"Received ack from {message['sender']}: {message['content']}")
        
        # Call custom handler if set
        if self.on_ack_received:
            try:
                await self.on_ack_received(message)
            except Exception as e:
                logger.error(f"Error in ack handler: {e}")
    
    async def _send_to_websocket(self, websocket, message: dict):
        """Send message to specific websocket."""
        try:
            await websocket.send(json.dumps(message))
            logger.info(f"Sent {message['type']} to {websocket.remote_address}")
        except ConnectionClosed:
            logger.warning("Connection closed while sending message")
        except Exception as e:
            logger.error(f"Error sending message: {e}")
    
    async def broadcast_message(self, message: dict):
        """Broadcast message to all connected clients."""
        if not self.connected_clients:
            logger.warning("No connected clients to broadcast to")
            return
        
        disconnected_clients = set()
        for client in self.connected_clients:
            try:
                await self._send_to_websocket(client, message)
            except ConnectionClosed:
                disconnected_clients.add(client)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected_clients.add(client)
        
        # Clean up disconnected clients
        self.connected_clients -= disconnected_clients
    
    async def send_question(self, content: str, target_websocket = None) -> str:
        """
        Send a question and track it for turn-taking.
        
        Args:
            content: Question content
            target_websocket: Specific websocket to send to (if None, broadcasts)
            
        Returns:
            Message ID of the sent question
        """
        if self.conversation_state == "waiting_for_answer":
            logger.warning("Already waiting for an answer, cannot send another question")
            return None
        
        question_msg = self.create_message(content, msg_type="question")
        
        # Track the question
        self.pending_questions[question_msg["message_id"]] = question_msg
        self.conversation_state = "waiting_for_answer"
        
        if target_websocket:
            await self._send_to_websocket(target_websocket, question_msg)
        else:
            await self.broadcast_message(question_msg)
        
        return question_msg["message_id"]
    
    async def send_via_client(self, message: dict):
        """Send message via client connection."""
        if not self.client_websocket:
            logger.error("No client connection available")
            return
        
        try:
            await self.client_websocket.send(json.dumps(message))
            logger.info(f"Sent {message['type']} via client connection")
        except Exception as e:
            logger.error(f"Error sending via client: {e}")
    
    async def _server_handler(self, websocket, *args):
        """Handle WebSocket server connections."""
        logger.info(f"New client connected from {websocket.remote_address}")
        self.connected_clients.add(websocket)
        
        try:
            async for message in websocket:
                try:
                    message_data = json.loads(message)
                    await self._handle_message(websocket, message_data)
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON received: {message}")
                except Exception as e:
                    logger.error(f"Error processing message: {e}")
        except ConnectionClosed:
            logger.info(f"Client {websocket.remote_address} disconnected")
        finally:
            self.connected_clients.discard(websocket)
    
    async def start_server(self):
        """Start the WebSocket server."""
        try:
            self.server = await websockets.serve(
                self._server_handler,
                "localhost",
                self.server_port
            )
            logger.info(f"{self.name} WebSocket server started on port {self.server_port}")
        except Exception as e:
            logger.error(f"Failed to start server: {e}")
            raise
    
    async def connect_as_client(self) -> bool:
        """Connect to target WebSocket server as client."""
        if not self.target_port:
            logger.warning("No target port specified for client connection")
            return False
        
        try:
            uri = f"ws://{self.target_host}:{self.target_port}"
            self.client_websocket = await websockets.connect(uri)
            logger.info(f"{self.name} connected as client to {uri}")
            
            # Start listening for messages
            asyncio.create_task(self._client_message_handler())
            return True
        except Exception as e:
            logger.error(f"Failed to connect as client: {e}")
            return False
    
    async def _client_message_handler(self):
        """Handle messages received as client."""
        try:
            async for message in self.client_websocket:
                try:
                    message_data = json.loads(message)
                    await self._handle_message(self.client_websocket, message_data)
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON received: {message}")
                except Exception as e:
                    logger.error(f"Error processing client message: {e}")
        except ConnectionClosed:
            logger.info("Client connection closed")
            self.client_websocket = None
        except Exception as e:
            logger.error(f"Client message handler error: {e}")
            self.client_websocket = None
    
    async def stop(self):
        """Stop the communicator."""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
            logger.info(f"{self.name} server stopped")
        
        if self.client_websocket:
            await self.client_websocket.close()
            logger.info(f"{self.name} client disconnected")
    
    def is_ready_to_send_question(self) -> bool:
        """Check if ready to send a new question (turn-taking)."""
        return self.conversation_state == "idle"
    
    def get_stats(self) -> dict:
        """Get communication statistics."""
        return {
            "name": self.name,
            "server_port": self.server_port,
            "connected_clients": len(self.connected_clients),
            "has_client_connection": self.client_websocket is not None,
            "conversation_state": self.conversation_state,
            "pending_questions": len(self.pending_questions),
            "cache_size": len(self.message_cache)
        }


async def create_communicator_pair(ai_port: int = 8765, rasa_port: int = 8766):
    """
    Helper function to create a pair of communicators for testing.
    
    Args:
        ai_port: Port for Fractal AI WebSocket server
        rasa_port: Port for Rasa WebSocket server
        
    Returns:
        Tuple of (ai_communicator, rasa_communicator)
    """
    ai_comm = WebSocketCommunicator(
        name="fractal_ai",
        server_port=ai_port,
        target_host="localhost",
        target_port=rasa_port
    )
    
    rasa_comm = WebSocketCommunicator(
        name="rasa_bot",
        server_port=rasa_port,
        target_host="localhost",
        target_port=ai_port
    )
    
    return ai_comm, rasa_comm


if __name__ == "__main__":
    # Example usage
    async def test_communication():
        """Test the WebSocket communication system."""
        ai_comm, rasa_comm = await create_communicator_pair()
        
        # Set up simple handlers for testing
        async def ai_question_handler(message):
            return f"AI processed: {message['content']}"
        
        async def rasa_question_handler(message):
            return f"Rasa processed: {message['content']}"
        
        ai_comm.on_question_received = ai_question_handler
        rasa_comm.on_question_received = rasa_question_handler
        
        # Start servers
        await ai_comm.start_server()
        await rasa_comm.start_server()
        
        # Give servers time to start
        await asyncio.sleep(1)
        
        # Connect as clients
        await ai_comm.connect_as_client()
        await rasa_comm.connect_as_client()
        
        # Give connections time to establish
        await asyncio.sleep(1)
        
        # Test sending messages
        await ai_comm.send_question("Hello from Fractal AI!")
        await asyncio.sleep(2)
        
        await rasa_comm.send_question("Hello from Rasa!")
        await asyncio.sleep(2)
        
        # Print stats
        print("AI Stats:", ai_comm.get_stats())
        print("Rasa Stats:", rasa_comm.get_stats())
        
        # Cleanup
        await ai_comm.stop()
        await rasa_comm.stop()
    
    # Run the test
    asyncio.run(test_communication())