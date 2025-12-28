# app/tools/email_tool.py

import smtplib
import os
from email.message import EmailMessage
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def send_payment_reminder(
    to_email: str,
    client_name: str,
    amount: int,
    deadline_days: int
) -> dict:
    """
    Sends a real email using SMTP (Gmail).
    """

    sender_email = os.getenv("SMTP_EMAIL")
    sender_password = os.getenv("SMTP_PASSWORD")
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT"))

    print("SMTP_EMAIL:", sender_email)
    print("SMTP_HOST:", smtp_host)
    print("SMTP_PORT:", smtp_port)
    print("SMTP_PASSWORD loaded:", bool(sender_password))

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = "Payment Reminder – FinLy Finance Assistant"

    msg.set_content(
        f"""
Dear {client_name},

This is a gentle reminder regarding an outstanding payment of ₹{amount}.

To avoid any disruptions, we kindly request the payment within {deadline_days} days.

Thank you for your cooperation.

Regards,
FinLy – Autonomous Finance Assistant
"""
    )

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)

        print("\n📧 REAL EMAIL SENT SUCCESSFULLY")
        print(f"➡️ To: {to_email}")

        return {
            "status": "SENT",
            "to": to_email,
            "amount": amount,
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        print("\n❌ EMAIL FAILED")
        print(str(e))

        return {
            "status": "FAILED",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }
