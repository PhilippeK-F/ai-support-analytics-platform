CREATE TABLE IF NOT EXISTS support_tickets (
    ticket_id TEXT PRIMARY KEY,
    created_at TIMESTAMP,
    customer_id TEXT,
    channel TEXT,
    subject TEXT,
    message TEXT,
    category TEXT,
    priority TEXT,
    status TEXT,
    sentiment TEXT,
    summary TEXT,
    assigned_team TEXT
);