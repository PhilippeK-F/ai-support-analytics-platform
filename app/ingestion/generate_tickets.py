import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

OUTPUT_PATH = Path("data/raw/support_tickets.csv")

CHANNELS = ["email", "chat", "phone", "web"]
STATUSES = ["open", "open", "open", "closed", "pending"]

BILLING_SUBJECTS = [
    "Refund request",
    "Payment issue",
    "Double charge",
    "Invoice problem",
    "Subscription billing issue",
]
BILLING_MESSAGES = [
    "I was charged twice for my subscription and I need a refund.",
    "My payment failed but the money was still debited.",
    "I have not received my refund after several days.",
    "The invoice amount looks incorrect on my account.",
    "Please help me fix this billing problem quickly.",
]

TECH_SUBJECTS = [
    "Login problem",
    "Bug report",
    "Password reset issue",
    "Export button not working",
    "Dashboard crash",
]
TECH_MESSAGES = [
    "I cannot log into my account after resetting my password.",
    "The export button crashes every time I click on it.",
    "There seems to be a bug when I try to open the dashboard.",
    "The application is slow and sometimes throws an error.",
    "I am unable to access a feature that worked yesterday.",
]

PRODUCT_SUBJECTS = [
    "Feature request",
    "Dark mode suggestion",
    "Dashboard improvement",
    "Need better filtering",
    "Suggestion for export options",
]
PRODUCT_MESSAGES = [
    "It would be great to have dark mode in the dashboard.",
    "I would like more filtering options in reports.",
    "A CSV export with more columns would be very useful.",
    "Please consider improving the dashboard usability.",
    "This is not urgent but I have a product suggestion.",
]

GENERAL_SUBJECTS = [
    "General question",
    "Need information",
    "Account question",
    "Support request",
    "Clarification needed",
]
GENERAL_MESSAGES = [
    "I have a general question about how the platform works.",
    "Can someone help me understand a feature in my account?",
    "I need more information before continuing.",
    "This is not urgent, I just need clarification.",
    "Could your support team guide me on the next steps?",
]

CUSTOMER_IDS = [f"CUST-{1000+i}" for i in range(1, 301)]


def pick_category() -> str:
    return random.choices(
        population=["billing", "technical", "product", "general"],
        weights=[30, 35, 20, 15],
        k=1,
    )[0]


def subject_and_message(category: str) -> tuple[str, str]:
    if category == "billing":
        return random.choice(BILLING_SUBJECTS), random.choice(BILLING_MESSAGES)
    if category == "technical":
        return random.choice(TECH_SUBJECTS), random.choice(TECH_MESSAGES)
    if category == "product":
        return random.choice(PRODUCT_SUBJECTS), random.choice(PRODUCT_MESSAGES)
    return random.choice(GENERAL_SUBJECTS), random.choice(GENERAL_MESSAGES)


def detect_priority(category: str, message: str) -> str:
    text = message.lower()
    if category in ["billing", "technical"] and any(
        word in text for word in ["charged twice", "refund", "cannot", "crashes", "error"]
    ):
        return random.choices(["high", "medium"], weights=[70, 30], k=1)[0]
    if category == "product":
        return random.choices(["low", "medium"], weights=[80, 20], k=1)[0]
    return random.choices(["low", "medium"], weights=[60, 40], k=1)[0]


def detect_sentiment(message: str) -> str:
    text = message.lower()
    if any(word in text for word in ["cannot", "issue", "problem", "crash", "error", "refund", "charged twice"]):
        return random.choices(["negative", "neutral"], weights=[85, 15], k=1)[0]
    if any(word in text for word in ["great", "useful", "love"]):
        return random.choices(["positive", "neutral"], weights=[70, 30], k=1)[0]
    return random.choices(["neutral", "positive"], weights=[80, 20], k=1)[0]


def build_summary(subject: str, message: str) -> str:
    short_message = message[:90].strip()
    if len(message) > 90:
        short_message += "..."
    return f"{subject}: {short_message}"


def assign_team(category: str) -> str:
    mapping = {
        "billing": "billing",
        "technical": "engineering",
        "product": "product",
        "general": "support",
    }
    return mapping[category]


def random_created_at(days_back: int = 60) -> datetime:
    now = datetime.now()
    delta_days = random.randint(0, days_back)
    delta_hours = random.randint(0, 23)
    delta_minutes = random.randint(0, 59)
    return now - timedelta(days=delta_days, hours=delta_hours, minutes=delta_minutes)


def generate_ticket(i: int) -> dict:
    category = pick_category()
    subject, message = subject_and_message(category)
    priority = detect_priority(category, message)
    sentiment = detect_sentiment(message)
    assigned_team = assign_team(category)

    return {
        "ticket_id": f"TCK-{i:04d}",
        "created_at": random_created_at().strftime("%Y-%m-%d %H:%M:%S"),
        "customer_id": random.choice(CUSTOMER_IDS),
        "channel": random.choice(CHANNELS),
        "subject": subject,
        "message": message,
        "category": category,
        "priority": priority,
        "status": random.choice(STATUSES),
        "sentiment": sentiment,
        "summary": build_summary(subject, message),
        "assigned_team": assigned_team,
    }


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    rows = [generate_ticket(i) for i in range(1, 401)]

    with OUTPUT_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "ticket_id",
                "created_at",
                "customer_id",
                "channel",
                "subject",
                "message",
                "category",
                "priority",
                "status",
                "sentiment",
                "summary",
                "assigned_team",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"{len(rows)} tickets générés dans {OUTPUT_PATH}")


if __name__ == "__main__":
    main()