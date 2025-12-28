# app/agents/action.py

from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.tools.email_tool import send_payment_reminder

# ---------------------------
# LLM for Dynamic Content Generation
# ---------------------------
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7, # Higher temperature for creative tone adaptation
    request_timeout=20
)

draft_prompt = ChatPromptTemplate.from_template("""
You are an Action Execution Agent.

Draft a payment reminder email.

Context:
- Client: {client_name}
- Amount: ₹{amount}
- Deadline: {deadline_days} days
- Tone: {tone} (Must be strictly followed)

Instructions:
- If tone is FIRM: Use professional, direct language. Mention consequences if appropriate.
- If tone is POLITE: Be courteous, assume it's an oversight.
- If tone is URGENT: Emphasize the immediate deadline.

Output only the email body text.
""")

deferral_prompt = ChatPromptTemplate.from_template("""
You are an Action Execution Agent.
Draft a polite email to a vendor asking for a payment extension.

Context:
- Vendor: {client_name}
- Amount: ₹{amount}
- Current Tone: {tone}

Instructions:
- Apologize for the delay.
- Propose a new date (implied +7 days).
- Emphasize long-term partnership value.

Output only the email body text.
""")

def action_execution_node(state: Dict[str, Any]) -> Dict[str, Any]:
    # print("\n⚙️ ENTERED ACTION EXECUTION AGENT")
    decision = state.get("decision", {})
    sub_goal = state.get("sub_goal", {})
    strategy = decision.get("strategy")
    
    # Target details
    target_client = decision.get("target")
    amount = decision.get("amount_goal", 0)
    params = decision.get("execution_params", {})
    tone = params.get("tone", "POLITE")

    action_log = {}

    if strategy == "COLLECT_RECEIVABLE" or strategy == "DELAY_VENDOR_PAYMENT":
        # Handle single vs list target
        targets = target_client if isinstance(target_client, list) else [target_client]
        
        all_results = []
        
        for t in targets:
            if not t or t == "None": continue
            
            # Determine Prompt & Subject
            if strategy == "COLLECT_RECEIVABLE":
                prompt = draft_prompt
                # If multiple targets, split amount evenly or logic? For simplicity, we use total amount for context 
                # but ideally we should look up specific receivable amount. 
                # Agent instruction said "Amount: Set amount_goal = Total Receivable Amount".
                # We will just mention the total required in the email for now or generic.
                # BETTER: Look up the specific receivable amount for this client from state.
                
                specific_amount = amount # Default
                for r in state.get("receivables", []):
                    if r.get("client") == t:
                        specific_amount = r.get("amount")
                        break
                
                current_amount = specific_amount
                deadline_days = sub_goal.get("deadline_days", 7)
            else:
                prompt = deferral_prompt
                current_amount = amount
                deadline_days = 7 # Standard deferral
            
            # 1. Draft Email via LLM
            email_body_response = llm.invoke(
                prompt.format(
                    client_name=t,
                    amount=current_amount,
                    deadline_days=deadline_days,
                    tone=tone
                )
            )
            email_body = email_body_response.content
            
            # Find recipient email from state
            recipient_email = None
            for r in state.get("receivables", []):
                if r.get("client") == t:
                    recipient_email = r.get("email") 
                    break
            
            if not recipient_email:
                if strategy == "DELAY_VENDOR_PAYMENT":
                    recipient_email = "vendor_contact@example.com"
                else:
                    recipient_email = "client_contact@example.com"

            # 2. Execute Action (Send)
            result = send_payment_reminder(
                to_email=recipient_email,
                client_name=t,
                amount=current_amount,
                deadline_days=deadline_days,
                body=email_body
            )
            
            all_results.append({
                "target": t,
                "email": recipient_email,
                "result": result
            })

        # 3. Log Action for 'Contextual Traceability'
        action_log = {
            "action_taken": "EMAIL_PAYMENT_REMINDER_MULTI" if strategy == "COLLECT_RECEIVABLE" else "PAYMENT_EXTENSION_REQUEST",
            "targets_processed": all_results,
            "tone_used": tone
        }

    elif strategy == "MAINTAIN_STATUS_QUO":
        action_log = {
            "action_taken": "MONITORING_ONLY",
            "target": "N/A",
            "recipient_email": "N/A",
            "tone_used": "NEUTRAL",
            "content_draft": "Cash flow is within safe limits. No immediate action required.",
            "result": {"status": "OPTIMAL"}
        }

    else:
        action_log = {
            "action_taken": "NO_ACTION",
            "reason": strategy,
            "result": {"status": "SKIPPED"}
        }

    state["action_log"] = action_log
    return state
