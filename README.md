# 🚀 AI Support Analytics Platform

A small data project to simulate how support tickets can be ingested, analyzed and monitored.

The goal is to build a simple end-to-end pipeline: from raw data to actionable insights.

---

## Stack

* Python (Pandas, SQLAlchemy)
* FastAPI
* PostgreSQL (Docker)
* Grafana
* Docker Compose

---

## Project Goal

This project simulates a support analytics platform:

* load support tickets into a database
* expose them via an API
* build dashboards to analyze trends
* highlight critical issues
* trigger alerts when things go wrong

It’s designed to be simple but close to real-world use cases.

---

## Architecture

```text
CSV → Python ingestion → PostgreSQL → API → Grafana
```

---

## Features

* Ticket ingestion pipeline (CSV → PostgreSQL)
* API endpoints to explore tickets
* Dashboard with:

  * tickets over time
  * distribution by priority / category / sentiment
  * assigned teams
  
* 🔥 Top critical tickets (actionable view)
* 🚨 Criticality score (global risk indicator)
* Alert when criticality gets too high

---

## Criticality Score

A simple scoring logic to identify risky situations:

* +3 → high priority
* +2 → negative sentiment
* +2 → not resolved

This gives a global score that helps prioritize support workload.

---

## Run the project

Start services:

```bash
docker compose up -d
```

Generate data:

```bash
python app/ingestion/generate_tickets.py
```

Load data:

```bash
python app/ingestion/load_tickets.py
```

---

## Access

* API → http://localhost:8000
* Grafana → http://localhost:3000

---

## Notes

This project focuses on:

* structuring a small data pipeline
* building useful dashboards
* thinking in terms of business value (not just data)

---

## Possible improvements

* better classification (ML / NLP)
* real-time ingestion
* SLA tracking
* anomaly detection
* orchestration (Airflow)

---

## Author

Philippe Kirstetter-Fender
