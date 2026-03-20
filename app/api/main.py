from fastapi import FastAPI
from sqlalchemy import create_engine, text

app = FastAPI(title="AI Support Analytics Platform")

DATABASE_URL = "postgresql+psycopg2://support:support@localhost:5435/support_analytics"
engine = create_engine(DATABASE_URL)


@app.get("/")
def root():
    return {"message": "AI Support Analytics Platform API is running"}


@app.get("/tickets")
def get_tickets():
    query = text(
        """
        SELECT
            ticket_id,
            created_at,
            customer_id,
            channel,
            subject,
            message,
            category,
            priority,
            status,
            sentiment,
            summary,
            assigned_team
        FROM support_tickets
        ORDER BY created_at DESC
        """
    )

    with engine.connect() as conn:
        rows = conn.execute(query)
        return [dict(row._mapping) for row in rows]


@app.get("/tickets/stats")
def get_ticket_stats():
    query = text(
        """
        SELECT
            COUNT(*) AS total_tickets,
            COUNT(*) FILTER (WHERE priority = 'high') AS high_priority_tickets,
            COUNT(*) FILTER (WHERE sentiment = 'negative') AS negative_tickets,
            COUNT(*) FILTER (WHERE status = 'open') AS open_tickets
        FROM support_tickets
        """
    )

    with engine.connect() as conn:
        row = conn.execute(query).fetchone()
        return dict(row._mapping)


@app.get("/tickets/by-category")
def get_tickets_by_category():
    query = text(
        """
        SELECT category, COUNT(*) AS total
        FROM support_tickets
        GROUP BY category
        ORDER BY total DESC
        """
    )

    with engine.connect() as conn:
        rows = conn.execute(query)
        return [dict(row._mapping) for row in rows]


@app.get("/tickets/by-priority")
def get_tickets_by_priority():
    query = text(
        """
        SELECT priority, COUNT(*) AS total
        FROM support_tickets
        GROUP BY priority
        ORDER BY total DESC
        """
    )

    with engine.connect() as conn:
        rows = conn.execute(query)
        return [dict(row._mapping) for row in rows]