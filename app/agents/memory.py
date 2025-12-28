import json
import os
from typing import Dict, Any
from datetime import datetime

MEMORY_FILE = "app/data/memory.json"


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {
            "clients": {},
            "strategies": {},
            "flags": {"escalations": []}
        }
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def memory_agent_node(state: Dict[str, Any]) -> Dict[str, Any]:
    memory = load_memory()

    decision = state["decision"]
    action_log = state["action_log"]

    client = decision.get("target")
    strategy = decision.get("strategy")
    status = action_log["result"]["status"]

    now = datetime.utcnow().isoformat()

    # ---- Client learning ----
    client_mem = memory["clients"].get(client, {
        "success": 0,
        "failure": 0,
        "risk_weight": "MEDIUM",
        "last_contact": None
    })

    if status == "SENT":
        client_mem["success"] += 1
    else:
        client_mem["failure"] += 1

    if client_mem["failure"] >= 2:
        client_mem["risk_weight"] = "HIGH"
    elif client_mem["success"] >= 1:
        client_mem["risk_weight"] = "LOW"

    client_mem["last_contact"] = now
    memory["clients"][client] = client_mem

    # ---- Strategy learning ----
    strat_mem = memory["strategies"].get(strategy, {
        "success": 0,
        "failure": 0,
        "confidence": 0.7
    })

    if status == "SENT":
        strat_mem["success"] += 1
        strat_mem["confidence"] = min(1.0, strat_mem["confidence"] + 0.1)
    else:
        strat_mem["failure"] += 1
        strat_mem["confidence"] = max(0.0, strat_mem["confidence"] - 0.2)

    memory["strategies"][strategy] = strat_mem

    save_memory(memory)

    state["memory_update"] = {
        "client": client,
        "strategy": strategy,
        "status": status,
        "risk_weight": client_mem["risk_weight"],
        "strategy_confidence": strat_mem["confidence"]
    }

    return state
