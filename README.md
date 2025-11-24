# SecretShare-Py

Ephemeral secret sharing app built with Flask and HTMX.

## Features
- Create one-time secrets with expiration
- HTMX for dynamic interactions
- In-memory storage (resets on restart)

## Setup
1. `pip install -r requirements.txt`
2. `python app.py`
3. Visit `http://127.0.0.1:5000`

## Docker
- `docker build -t secretshare-py .`
- `docker run -p 5000:5000 secretshare-py`