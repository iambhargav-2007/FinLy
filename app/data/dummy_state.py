# app/data/dummy_state.py

finance_state = {
    "cash_balance": 150000,  # ₹1.5L available

    "salaries": [
        {"employee": "Dev", "amount": 60000, "due_in_days": 15},
        {"employee": "Designer", "amount": 40000, "due_in_days": 15}
    ],

    "fixed_bills": [
        {"type": "AWS", "amount": 20000, "due_in_days": 10},
        {"type": "Office Rent", "amount": 30000, "due_in_days": 18}
    ],

    "receivables": [
        {"client": "Client A", "amount": 120000, "due_in_days": 12},
        {"client": "Client B", "amount": 80000, "due_in_days": 20}
    ],

    "preferences": {
        "dont_delay_salaries": True,
        "avoid_vendor_damage": True
    }
}
