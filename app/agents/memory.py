# app/agents/memory.py

import json
import os
from typing import Dict, Any, List

# Define the path for the persistent memory store
MEMORY_FILE = os.path.join(os.path.dirname(__file__), "../data/client_memory.json")

def load_memory() -> Dict[str, Any]:
    """Load the persistent memory from JSON file."""
    if not os.path.exists(MEMORY_FILE):
        return {}
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_memory(memory: Dict[str, Any]):
    """Save the memory to the JSON file."""
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

def get_client_context(client_id: str) -> Dict[str, Any]:
    """
    Retrieves past behavior for a specific client to be injected into the Risk/Decision agents.
    Returns default neutral profile if new client.
    """
    memory = load_memory()
    return memory.get(client_id, {
        "risk_score_modifier": 1.0,  # 1.0 = Neutral, >1.0 = Higher Risk, <1.0 = Reliable
        "interaction_history": [],
        "last_strategy": None,
        "last_outcome": None
    })

def update_client_profile(client_id: str, strategy: str, action_taken: str, result: str):
    """
    Updates the client's behavior profile based on the action and its result.
    Implements 'Recursive Improvement' by adjusting risk modifiers.
    """
    memory = load_memory()
    
    if client_id not in memory:
        memory[client_id] = {
            "risk_score_modifier": 1.0,
            "interaction_history": [],
            "last_strategy": None,
            "last_outcome": None
        }
    
    # Recursive Improvement Logic
    # Update risk modifier based on simplistic outcome analysis
    current_modifier = memory[client_id]["risk_score_modifier"]
    
    # Example logic: If we chased them and it worked, they might be "Forgetful but Solvable" (Risk slightly down)
    # If we chased and they ignored, Risk UP.
    if result == "PAID":
        current_modifier = max(0.5, current_modifier - 0.1)
    elif result == "IGNORED" or result == "FAILED":
        current_modifier = min(2.0, current_modifier + 0.2)
        
    memory[client_id]["risk_score_modifier"] = round(current_modifier, 2)
    memory[client_id]["last_strategy"] = strategy
    memory[client_id]["last_outcome"] = result
    
    interaction_entry = {
        "strategy": strategy,
        "action": action_taken,
        "result": result,
        # In a real app, add timestamp here
    }
    memory[client_id]["interaction_history"].append(interaction_entry)
    
    save_memory(memory)
    return memory[client_id]

def memory_agent_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    LangGraph Node: Memory & Learning Agent (The Historian)
    Watches the delta between 'Action' and 'Result' and updates the database.
    """
    # print("\n🧠 ENTERED MEMORY AGENT")
    
    decision = state.get("decision", {})
    action_log = state.get("action_log", {})
    
    # If no decision was made or no action taken, skip
    if not decision or not action_log:
        return state

    target_client = decision.get("target")
    strategy = decision.get("strategy")
    
    # In this simulation, the 'result' comes immediately from the Action Agent (e.g. 'EMAIL_SENT').
    # For the feedback loop, we assume the Action Agent might return simulated outcomes like "PAID" or "IGNORED" 
    # for testing purposes, or we just log the attempt.
    
    # Extract the result status
    # Assuming action_log format: {"action_taken": "...", "result": {"status": "..."}}
    result_data = action_log.get("result", {})
    if isinstance(result_data, dict):
        result_status = result_data.get("status", "UNKNOWN")
    else:
        result_status = str(result_data)

    if target_client:
        updated_profile = update_client_profile(
            client_id=target_client,
            strategy=strategy,
            action_taken=action_log.get("action_taken"),
            result=result_status
        )
        
        # Inject the updated context back into state for the NEXT loop (or just for visibility)
        if "memory_updates" not in state:
            state["memory_updates"] = {}
        state["memory_updates"][target_client] = updated_profile

    return state
