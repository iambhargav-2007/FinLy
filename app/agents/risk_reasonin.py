# app/agents/risk_reasoning.py

import json
from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


# ---------------------------
# Utility: Safe JSON Parsing
# ---------------------------
def safe_json_parse(text: str) -> Dict[str, Any]:
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"\n❌ Invalid JSON returned by LLM.\n"
            f"Raw output:\n{text}\n"
        ) from e


# ---------------------------
# Step 1: Scenario Simulation
# ---------------------------
def simulate_scenarios(state: Dict[str, Any]) -> List[Dict[str, Any]]:
    total_salaries = sum(s["amount"] for s in state["salaries"])
    total_bills = sum(b["amount"] for b in state["fixed_bills"])

    return [
        {
            "name": "best_case",
            "description": "All clients pay on time",
            "net_cash": (
                state["cash_balance"]
                + sum(r["amount"] for r in state["receivables"])
                - total_salaries
                - total_bills
            )
        },
        {
            "name": "expected_case",
            "description": "One major client delays payment",
            "net_cash": (
                state["cash_balance"]
                + state["receivables"][1]["amount"]
                - total_salaries
                - total_bills
            )
        },
        {
            "name": "worst_case",
            "description": "Multiple delays and fixed costs hit together",
            "net_cash": (
                state["cash_balance"]
                - total_salaries
                - total_bills
            )
        }
    ]


# ---------------------------
# LLM Configuration (JSON-Forced)
# ---------------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3,
    model_kwargs={"response_format": {"type": "json_object"}}
)


# ---------------------------
# Prompt: Risk Reasoning
# ---------------------------
risk_prompt = ChatPromptTemplate.from_template("""
You are a financial risk reasoning agent.

You must reason under uncertainty and produce:
1. A quantitative risk assessment
2. A critical time window
3. The dominant source of financial risk
4. A REQUIRED financial sub-goal (desired outcome)

IMPORTANT RULES:
- The sub-goal MUST describe a desired financial state
- Do NOT suggest strategies
- Do NOT suggest actions
- Do NOT mention how the goal should be achieved
- Focus ONLY on what must be true to reduce risk

Return ONLY valid JSON in the EXACT structure below:

{{
  "risk_score": number,
  "critical_window": string,
  "dominant_risk": string,
  "confidence": "LOW" | "MEDIUM" | "HIGH",
  "sub_goal": {{
    "intent": string,
    "required_amount": number,
    "deadline_days": number,
    "reason": string
  }}
}}

Scenarios:
{scenarios}

Salary due in {salary_days} days.
""")



# ---------------------------
# Prompt: Sub-Goal Creation
# ---------------------------
goal_prompt = ChatPromptTemplate.from_template("""
You are an autonomous finance agent.

Given the risk analysis below, create a concrete financial sub-goal
that reduces risk before obligations hit.

Return ONLY valid JSON with:
- goal
- amount
- deadline_days
- reason

Risk analysis:
{risk_analysis}
""")


# ---------------------------
# LangGraph Node: Risk Reasoning Agent
# ---------------------------
def risk_reasoning_node(state: Dict[str, Any]) -> Dict[str, Any]:
    # Step 1: Simulate futures
    scenarios = simulate_scenarios(state)

    salary_days = min(s["due_in_days"] for s in state["salaries"])

    # Step 2: LLM risk reasoning
    risk_response = llm.invoke(
        risk_prompt.format_messages(
            scenarios=json.dumps(scenarios),
            salary_days=salary_days
        )
    )

    # print("\n--- RAW LLM OUTPUT (Risk Analysis) ---")
    # print(risk_response.content)

    risk_analysis = safe_json_parse(risk_response.content)

    # Step 3: LLM sub-goal creation
    goal_response = llm.invoke(
        goal_prompt.format_messages(
            risk_analysis=json.dumps(risk_analysis)
        )
    )

    # print("\n--- RAW LLM OUTPUT (Sub-Goal) ---")
    # print(goal_response.content)

    sub_goal = safe_json_parse(goal_response.content)

    # Step 4: Update shared LangGraph state
    state["scenarios"] = scenarios
    state["risk_analysis"] = risk_analysis
    state["sub_goal"] = sub_goal

    return state
