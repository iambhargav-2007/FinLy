# app/agents/decision.py

import json
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate


# ---------------------------
# LLM (JSON forced)
# ---------------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
    model_kwargs={"response_format": {"type": "json_object"}}
)


# ---------------------------
# Available Strategy Space
# ---------------------------
AVAILABLE_STRATEGIES = [
    "COLLECT_RECEIVABLE",
    "PARTIAL_COLLECTION",
    "DELAY_VENDOR_PAYMENT",
    "ALERT_FOUNDER"
]


# ---------------------------
# Prompt
# ---------------------------
decision_prompt = ChatPromptTemplate.from_template("""
You are a financial decision-making agent.

Your task is to choose the BEST strategy from the AVAILABLE STRATEGIES
to achieve the required sub-goal.

IMPORTANT RULES:
- Evaluate each available strategy mentally
- Choose ONE strategy only
- Do NOT execute actions
- Do NOT describe steps

Return ONLY valid JSON in the EXACT structure below:

{{
  "strategy": string,
  "target": string,
  "amount_goal": number,
  "reason": string
}}

AVAILABLE STRATEGIES:
{strategies}

Sub-goal:
{sub_goal}

Receivables:
{receivables}

Bills:
{bills}

Preferences:
{preferences}
""")

# ---------------------------
# LangGraph Node
# ---------------------------
def decision_agent_node(state: Dict[str, Any]) -> Dict[str, Any]:
    response = llm.invoke(
        decision_prompt.format_messages(
            strategies=json.dumps(AVAILABLE_STRATEGIES),
            sub_goal=json.dumps(state["sub_goal"]),
            receivables=json.dumps(state["receivables"]),
            bills=json.dumps(state["fixed_bills"]),
            preferences=json.dumps(state.get("preferences", {}))
        )
    )

    # print("\n--- RAW LLM OUTPUT (Decision Agent) ---")
    # print(response.content)

    decision = json.loads(response.content)

    state["decision"] = decision
    return state
