import psycopg2


def detect_category(subject: str, message: str) -> str:
    text = f"{subject} {message}".lower()

    if any(word in text for word in ["refund", "charged", "payment", "billing"]):
        return "billing"
    if any(word in text for word in ["login", "bug", "error", "crash", "password"]):
        return "technical"
    if any(word in text for word in ["feature", "request", "improvement", "dashboard"]):
        return "product"
    return "general"


def detect_priority(message: str) -> str:
    text = message.lower()

    if any(word in text for word in ["urgent", "immediately", "crash", "charged twice", "refund"]):
        return "high"
    if any(word in text for word in ["cannot", "problem", "issue", "delay"]):
        return "medium"
    return "low"


def detect_sentiment(message: str) -> str:
    text = message.lower()

    negative_words = ["cannot", "issue", "problem", "crash", "delay", "charged twice", "refund"]
    positive_words = ["great", "love", "thanks", "awesome"]

    if any(word in text for word in negative_words):
        return "negative"
    if any(word in text for word in positive_words):
        return "positive"
    return "neutral"


def build_summary(subject: str, message: str) -> str:
    short_message = message.strip()
    if len(short_message) > 80:
        short_message = short_message[:77] + "..."
    return f"{subject}: {short_message}"


def assign_team(category: str) -> str:
    mapping = {
        "billing": "billing",
        "technical": "engineering",
        "product": "product",
        "general": "support",
    }
    return mapping.get(category, "support")


def main() -> None:
    conn = psycopg2.connect(
        host="localhost",
        port="5435",
        database="support_analytics",
        user="support",
        password="support",
    )
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT ticket_id, subject, message
        FROM support_tickets
        """
    )
    tickets = cursor.fetchall()

    for ticket_id, subject, message in tickets:
        category = detect_category(subject, message)
        priority = detect_priority(message)
        sentiment = detect_sentiment(message)
        summary = build_summary(subject, message)
        assigned_team = assign_team(category)

        cursor.execute(
            """
            UPDATE support_tickets
            SET category = %s,
                priority = %s,
                sentiment = %s,
                summary = %s,
                assigned_team = %s
            WHERE ticket_id = %s
            """,
            (category, priority, sentiment, summary, assigned_team, ticket_id),
        )

    conn.commit()
    cursor.close()
    conn.close()

    print(f"{len(tickets)} tickets enrichis.")


if __name__ == "__main__":
    main()