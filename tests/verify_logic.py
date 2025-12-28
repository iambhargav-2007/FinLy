
import sys
import os
import json
from dotenv import load_dotenv

# Add app root to sys path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.agents.risk_reasoning import risk_reasoning_node
from app.agents.decision import decision_agent_node

load_dotenv()

def run_test_scenario(scenario_name, state):
    print(f"\n--- Running Scenario: {scenario_name} ---")
    
    # 1. Pre-process like server.py
    total_inflow = sum(r.get("amount", 0) for r in state.get("receivables", []))
    total_outflow = sum(s.get("amount", 0) for s in state.get("salaries", [])) + \
                    sum(b.get("amount", 0) for b in state.get("fixed_bills", []))
    current_cash = state.get("cash_balance", 0)
    
    projected_balance = current_cash - total_outflow
    liquidity_status = "SURPLUS" if projected_balance >= 0 else "DEFICIT"
    net_position = current_cash + total_inflow - total_outflow
    
    state["financial_metrics"] = {
        "total_inflow": total_inflow,
        "total_outflow": total_outflow,
        "projected_balance": projected_balance,
        "liquidity_status": liquidity_status,
        "net_position": net_position
    }
    
    print(f"Metrics: Balance={projected_balance}, Status={liquidity_status}")

    # 2. Run Risk Agent
    print("Running Risk Agent...")
    state = risk_reasoning_node(state)
    sub_goal = state.get("sub_goal", {})
    
    print(f"Risk Reason: {sub_goal.get('reason')}")

    # 3. Run Decision Agent
    state["sub_goal"] = sub_goal
    print("Running Decision Agent...")
    state = decision_agent_node(state)
    decision = state.get("decision", {})
    
    print(f"Strategy: {decision.get('strategy')}")
    print(f"Rationale: {decision.get('rationale')}")
    print(f"Financial Target (Amount Goal): {decision.get('amount_goal')}")

if __name__ == "__main__":
    # SCENARIO: Same Day Match
    # Cash 0. Bill 100k (10d). Rec 100k (10d).
    # Logic: 10d <= 10d. Match.
    # Expect: COLLECT_RECEIVABLE. Amount: 100000.
    
    same_day_scenario = {
        "cash_balance": 0,
        "fixed_bills": [{"type": "Salaries", "amount": 100000, "due_in_days": 10}],
        "salaries": [],
        "receivables": [{"client": "Acme", "amount": 100000, "due_in_days": 10}],
        "client_profiles": {},
        "preferences": {"dont_delay_salaries": True}
    }
    run_test_scenario("Same Day (10d vs 10d)", same_day_scenario)
