# 01 — FastAPI on EC2

A small FastAPI service deployed on an AWS EC2 instance.

Demonstrates the basic shape of every cloud-deployed Python web app:
build locally → push to Git → deploy on a server → expose via firewall rules → access from the internet.

## What it does

A REST API with 4 endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service info (name, version) |
| `/health` | GET | Health check + uptime (used by load balancers) |
| `/system` | GET | Server metadata (hostname, OS, Python version) |
| `/calc` | POST | Math operation: add / subtract / multiply / divide |

Interactive API docs are auto-generated at `/docs` (Swagger UI).

## Run locally

```bash