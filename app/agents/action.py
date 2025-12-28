# app/agents/action.py

from typing import Dict, Any
from tools.email_tool import send_payment_reminder


def action_execution_node(state: Dict[str, Any]) -> Dict[str, Any]:
    # print("\n⚙️ ENTERED ACTION EXECUTION AGENT")
    decision = state["decision"]
    sub_goal = state["sub_goal"]

    action_log = {}

    if decision["strategy"] == "COLLECT_RECEIVABLE":
        # 👇 Dummy recipient email (use your own email for testing)
        recipient_email = "tharunmoturu2007@gmail.com"

        result = send_payment_reminder(
            to_email=recipient_email,
            client_name=decision["target"],
            amount=decision["amount_goal"],
            deadline_days=sub_goal["deadline_days"]
        )

        action_log = {
            "action_taken": "EMAIL_PAYMENT_REMINDER",
            "result": result
        }

    else:
        action_log = {
            "action_taken": "NO_ACTION",
            "result": {"status": "SKIPPED"}
        }

    state["action_log"] = action_log
    return state
