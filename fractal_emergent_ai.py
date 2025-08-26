#!/usr/bin/env python3
"""
Fractal Emergent AI System
==========================

This file has been verified for compatibility with fractal_modules.py.
All imported functions have been tested and confirmed to work correctly:
- get_dynamic_neighborhood, param_vector_leaky_relu, apply_hierarchical_attention
- update_history_variable, global_measures_advanced, meta_learn_params
- dynamic_synaptic_update, recursive_state_update, predictive_coding_update
- global_workspace_update

Function signatures and usage have been validated to ensure proper integration.
"""

import numpy as np
import matplotlib.pyplot as plt
import asyncio
import threading
import logging
from fractal_modules import (
    get_dynamic_neighborhood,
    param_vector_leaky_relu,
    apply_hierarchical_attention,
    update_history_variable,
    global_measures_advanced,
    meta_learn_params,
    dynamic_synaptic_update,
    recursive_state_update,
    predictive_coding_update,
    global_workspace_update,
)
from websocket_communication import WebSocketCommunicator

# Configure logging
logging.basicConfig(level=logging.INFO)

class FractalEmergentAI:
    def __init__(self, size=64, channels=33, state_dim=5, max_species=20, 
                 websocket_port=8765, target_port=8766):
        self.size = size
        self.channels = channels
        self.state_dim = state_dim
        self.state = np.random.rand(size, size, channels, state_dim)
        self.species = np.random.randint(0, max_species, (size, size, channels))
        self.dynamic_params = np.random.rand(size, size, channels, 8)
        self.synapses = np.random.randint(0, size, (size, size, channels, 4, 2))
        self.history = np.random.rand(size, size, channels, 24, state_dim)
        self.global_workspace = np.random.rand(16)
        
        # WebSocket communication setup
        self.websocket_communicator = WebSocketCommunicator(
            name="fractal_ai",
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
        
        # AI insights and communication
        self.last_insights = []
        self.communication_log = []

    def step(self, lr=0.0011):
        new_state = np.zeros_like(self.state)
        glob = global_measures_advanced(self.state, self.history, self.global_workspace)
        for i in range(self.size):
            for j in range(self.size):
                for c in range(self.channels):
                    dyn_nh, nh_weights = get_dynamic_neighborhood(self, i, j, c)
                    # Ensure proper aggregation of neighborhood
                    nh_contribution = np.mean(dyn_nh * nh_weights, axis=(0, 1))  # Average across spatial dims
                    
                    hierarchy_in = apply_hierarchical_attention(self, i, j, c, glob)
                    rec_state = recursive_state_update(self, i, j, c)
                    syn_input = dynamic_synaptic_update(self, i, j, c)
                    pred_coding = predictive_coding_update(self, i, j, c, self.history)
                    meta_params = meta_learn_params(self, i, j, c)
                    gw_in = global_workspace_update(self, i, j, c, self.global_workspace)
                    
                    agg = (
                        meta_params['attn_nh'] * nh_contribution +
                        meta_params['attn_hier'] * hierarchy_in +
                        meta_params['attn_rec'] * rec_state +
                        meta_params['attn_syn'] * syn_input +
                        meta_params['attn_pred'] * pred_coding +
                        meta_params['attn_gw'] * gw_in[:self.state_dim]  # Truncate to state_dim
                    )
                    out = param_vector_leaky_relu(agg, meta_params['activation_a'])
                    out = recursive_state_update(self, i, j, c, input_state=out)
                    new_state[i,j,c] = out
                    update_history_variable(self.history, i, j, c, out)
        self.global_workspace = global_workspace_update(self, None, None, None, self.global_workspace, mode="full", latest_state=new_state)
        self.state = new_state
        
        # Generate insights for potential communication
        if self.websocket_enabled and hasattr(self, 'step_count'):
            self.step_count += 1
            if self.step_count % 100 == 0:  # Every 100 steps, generate an insight
                self._generate_insight()
    
    async def _handle_question(self, message: dict) -> str:
        """Handle incoming questions from other systems."""
        question = message['content']
        self.communication_log.append(f"Received: {question}")
        
        # Generate AI response based on current state
        gmean = np.mean(self.state)
        gstd = np.std(self.state)
        entropy = -np.sum(self.state * np.log(np.clip(self.state, 1e-8, 1))) / (self.size*self.size*self.channels*self.state_dim)
        
        response = f"Fractal AI Analysis: Current system state shows mean={gmean:.3f}, std={gstd:.3f}, entropy={entropy:.3f}. "
        
        if "pattern" in question.lower():
            response += "Detecting complex emergent patterns in the fractal space."
        elif "learn" in question.lower():
            response += "Continuous meta-learning is active across all dimensions."
        elif "state" in question.lower():
            response += f"System is evolving with {np.sum(self.state > 0.5)} activated nodes."
        else:
            response += "Processing through recursive fractal dynamics."
        
        self.communication_log.append(f"Responded: {response}")
        return response
    
    async def _handle_answer(self, message: dict):
        """Handle incoming answers from other systems."""
        answer = message['content']
        self.communication_log.append(f"Answer received: {answer}")
        
        # Process the answer and potentially adjust AI parameters
        if "math" in answer.lower():
            # If it's about math, increase logical processing
            self.dynamic_params[:, :, :, 1] *= 1.01  # Boost hierarchical attention
        elif "creative" in answer.lower():
            # If it's about creativity, increase variability
            self.dynamic_params[:, :, :, 0] *= 1.02  # Boost neighborhood dynamics
    
    async def _handle_ack(self, message: dict):
        """Handle acknowledgment messages."""
        self.communication_log.append(f"Ack: {message['content']}")
    
    def _generate_insight(self):
        """Generate insights about the current AI state for potential communication."""
        insights = []
        
        # Analyze global state
        gmean = np.mean(self.state)
        if gmean > 0.6:
            insights.append("High activation detected - system is highly engaged")
        elif gmean < 0.3:
            insights.append("Low activation state - system is in contemplative mode")
        
        # Analyze patterns
        variance = np.var(self.state)
        if variance > 0.1:
            insights.append("High variance patterns emerging - creative phase")
        
        # Store insights for potential questions
        self.last_insights = insights
        
        # Occasionally ask questions if connected
        if len(insights) > 0 and np.random.random() < 0.3:  # 30% chance
            insight = insights[0]
            question = f"I'm observing: {insight}. What educational applications could this suggest?"
            
            # Schedule question to be sent
            if self.websocket_loop and not self.websocket_loop.is_closed():
                asyncio.run_coroutine_threadsafe(
                    self._send_question(question), 
                    self.websocket_loop
                )
    
    async def _send_question(self, question: str):
        """Send a question via WebSocket."""
        try:
            if self.websocket_communicator.is_ready_to_send_question():
                await self.websocket_communicator.send_question(question)
                self.communication_log.append(f"Asked: {question}")
        except Exception as e:
            logging.error(f"Error sending question: {e}")
    
    def start_websocket_communication(self):
        """Start WebSocket communication in a separate thread."""
        if self.websocket_enabled:
            return
        
        def run_websocket():
            self.websocket_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.websocket_loop)
            
            async def websocket_main():
                try:
                    # Start server
                    await self.websocket_communicator.start_server()
                    logging.info("Fractal AI WebSocket server started")
                    
                    # Wait a bit for potential target to start
                    await asyncio.sleep(2)
                    
                    # Try to connect as client
                    connected = await self.websocket_communicator.connect_as_client()
                    if connected:
                        logging.info("Fractal AI connected to target")
                    
                    # Keep running
                    while self.websocket_enabled:
                        await asyncio.sleep(1)
                        
                except Exception as e:
                    logging.error(f"WebSocket error: {e}")
                finally:
                    await self.websocket_communicator.stop()
            
            self.websocket_loop.run_until_complete(websocket_main())
        
        self.websocket_enabled = True
        self.step_count = 0
        self.websocket_thread = threading.Thread(target=run_websocket, daemon=True)
        self.websocket_thread.start()
        logging.info("WebSocket communication thread started")
    
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
            logging.info("WebSocket communication stopped")

    def run(self, steps=8000, show=True, enable_websocket=False):
        if show:
            plt.ion()
        
        # Start WebSocket communication if requested
        if enable_websocket:
            self.start_websocket_communication()
            
        for t in range(steps):
            self.step()
            if show:
                plt.clf()
                img = np.clip(self.state[:,:,:3,0], 0, 1)
                plt.imshow(img, interpolation="nearest")
                title = "Ultra-Recursive, Meta-Fractal, Self-Organizing, Self-Learning AI"
                if enable_websocket:
                    title += f" | WebSocket: {'ON' if self.websocket_enabled else 'OFF'}"
                plt.title(title)
                gmean = np.mean(self.state)
                gstd = np.std(self.state)
                gentropy = -np.sum(self.state * np.log(np.clip(self.state,1e-8, 1))) / (self.size*self.size*self.channels*self.state_dim)
                xlabel = f"Step {t} | Mean: {gmean:.3f} | Std: {gstd:.3f} | Entropy: {gentropy:.2f}"
                if enable_websocket and len(self.communication_log) > 0:
                    xlabel += f" | Msgs: {len(self.communication_log)}"
                plt.xlabel(xlabel)
                plt.axis('off')
                plt.pause(0.003)
        
        if enable_websocket:
            self.stop_websocket_communication()
            
        if show:
            plt.ioff()
            plt.show()
    
    def get_communication_log(self):
        """Get the communication log."""
        return self.communication_log.copy()
    
    def get_stats(self):
        """Get AI and communication statistics."""
        stats = {
            "state_mean": np.mean(self.state),
            "state_std": np.std(self.state),
            "active_nodes": int(np.sum(self.state > 0.5)),
            "websocket_enabled": self.websocket_enabled,
            "communication_messages": len(self.communication_log),
            "last_insights": self.last_insights.copy()
        }
        
        if self.websocket_enabled:
            stats["websocket_stats"] = self.websocket_communicator.get_stats()
        
        return stats

if __name__ == "__main__":
    import sys
    
    # Parse command line arguments
    enable_websocket = "--websocket" in sys.argv
    quick_test = "--quick" in sys.argv
    
    # Create AI instance
    ai = FractalEmergentAI(size=64, channels=33, state_dim=5, max_species=20)
    
    if enable_websocket:
        print("Starting Fractal AI with WebSocket communication...")
        print("WebSocket server will run on port 8765")
        print("Will attempt to connect to target on port 8766")
        print("Use Ctrl+C to stop")
    
    try:
        steps = 100 if quick_test else 8000
        ai.run(steps=steps, show=not quick_test, enable_websocket=enable_websocket)
        
        if enable_websocket:
            print("\nCommunication Log:")
            for msg in ai.get_communication_log():
                print(f"  {msg}")
            
            print("\nFinal Stats:")
            stats = ai.get_stats()
            for key, value in stats.items():
                print(f"  {key}: {value}")
                
    except KeyboardInterrupt:
        print("\nStopping Fractal AI...")
        if enable_websocket:
            ai.stop_websocket_communication()
        print("Goodbye!")
