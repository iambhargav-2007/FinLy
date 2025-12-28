# app/agents/decision.py

import json
from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# ---------------------------
# LLM (JSON forced)
# ---------------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
    model_kwargs={"response_format": {"type": "json_object"}},
    request_timeout=20
)

# ---------------------------
# Available Strategy Space
# ---------------------------
AVAILABLE_STRATEGIES = [
    "COLLECT_RECEIVABLE",
    "PARTIAL_COLLECTION",
    "DELAY_VENDOR_PAYMENT",
    "MAINTAIN_STATUS_QUO",
    "ALERT_FOUNDER"
]

# ---------------------------
# Prompt
# ---------------------------
decision_prompt = ChatPromptTemplate.from_template("""
You are a financial decision-making agent (The Strategist).

Your task is to select the BEST strategic action to achieve the sub-goal.

METHODOLOGY:
1. **OBLIGATIONS ANALYSIS**:
   - Combine **Bills** and **Salaries** into a single list of "Obligations".
   - **Loop through EACH Obligation** (sorted by urgency).

2. **FUNDING WATERFALL (STRICT ORDER)**:
   
   **STEP 1: CHECK RECEIVABLES (POOLING)**
   - For the specific Obligation, look for **ALL** Receivables where:
     - `Receivable due_in_days` <= `Obligation due_in_days`?
     - **CRITICAL**: If `due_in_days` are EQUAL, it is a MATCH.
   - **SUM** the amounts of all matching receivables.
   
   **STEP 2: EVALUATE COVERAGE (Receivables + Cash)**
   - **CASE A: Receivables >= Obligation**
     - **ACTION**: "COLLECT_RECEIVABLE".
     - **TARGET**: List all contributing clients.
     - **REASON**: "Pooled receivables ({{total_rec}}) fully cover Obligation ({{amount}}). Preserving Cash."
     - **AMOUNT**: Set `amount_goal` = Total Receivable Amount.

   - **CASE B: (Receivables + Cash Balance) >= Obligation**
     - **ACTION**: "COLLECT_RECEIVABLE" (if receivables > 0) OR "MAINTAIN_STATUS_QUO" (if only cash used).
     - **REASON**: "Pooled receivables ({{total_rec}}) + Cash Balance ({{cash}}) covers Obligation ({{amount}})."
     - **AMOUNT**: Set `amount_goal` = Total Receivable Amount (collect what we can).

   - **CASE C: DEFICIT (Receivables + Cash < Obligation)**
     - **ACTION**: "DELAY_VENDOR_PAYMENT".
     - **TARGET**: The Vendor for this bill (if applicable).
     - **REASON**: "Insufficient funds (Cash + Recs) to cover Obligation by due date."
     - **AMOUNT**: Set `amount_goal` = Deficit Amount.

3. **Delay Strategy**:
   - NEVER delay Salaries (`preference.dont_delay_salaries`).
   - Only delay Bills if `due_in_days` > 2.

Context:
- Sub-goal: {sub_goal}
- Cash Balance: {cash_balance}

Output Requirement:
1. Perform a visible Chain of Thought (in "rationale").
2. Select ONE strategy and target(s).

Return ONLY valid JSON in the EXACT structure below:

{{
  "strategy": "COLLECT_RECEIVABLE" | "DELAY_VENDOR_PAYMENT" | "MAINTAIN_STATUS_QUO" | "ALERT_FOUNDER",
  "target": ["Name 1", "Name 2"] or "Vendor Name" or "None",
  "rationale": "Step-by-step reasoning...",
  "amount_goal": number,
  "execution_params": {{
    "tone": "FIRM" | "POLITE" | "URGENT" | "NONE",
    "channel": "EMAIL" | "SLACK" | "NONE"
  }}
}}

AVAILABLE STRATEGIES:
{strategies}

Financial Context:
Receivables: {receivables}
Obligations (Bills + Salaries): {obligations}
Client Profiles: {client_profiles}
Preferences: {preferences}
Financial Metrics: {financial_metrics}
""")

# ---------------------------
# LangGraph Node
# ---------------------------
def decision_agent_node(state: Dict[str, Any]) -> Dict[str, Any]:
    # Extract inputs
    sub_goal = state.get("sub_goal", {})
    receivables = state.get("receivables", [])
    bills = state.get("fixed_bills", [])
    salaries = state.get("salaries", [])
    
    # Combine obligations for context
    obligations = bills + salaries
    
    client_profiles = state.get("client_profiles", {})
    preferences = state.get("preferences", {})
    cash_balance = state.get("cash_balance", 0)
    
    # Invoke LLM
    metrics = state.get("financial_metrics", {})
    response = llm.invoke(
        decision_prompt.format_messages(
            strategies=json.dumps(AVAILABLE_STRATEGIES),
            sub_goal=json.dumps(sub_goal),
            receivables=json.dumps(receivables),
            obligations=json.dumps(obligations),
            client_profiles=json.dumps(client_profiles),
            preferences=json.dumps(preferences),
            financial_metrics=json.dumps(metrics),
            cash_balance=cash_balance
        )
    )
    
    try:
        decision = json.loads(response.content)
    except json.JSONDecodeError:
        # Fallback
        fallback_amt = bills[0]["amount"] if bills else 0
        decision = {
            "strategy": "ALERT_FOUNDER",
            "target": "Admin",
            "rationale": "LLM failed to output valid JSON",
            "amount_goal": fallback_amt,
            "execution_params": {"tone": "URGENT"}
        }

    # Update state
    state["decision"] = decision
    return state
