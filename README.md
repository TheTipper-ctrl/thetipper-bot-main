# thetipper-bot-main

Simple Telegram bot "The Tipper" — ready to deploy to Render.

Files:
- main.py : bot code (uses BOT_TOKEN and optional API_FOOTBALL_KEY environment variables)
- requirements.txt

Commands:
- /start
- /ping
- /predict <league_id> <fixture_id>  (requires API_FOOTBALL_KEY to be set)

Deployment (Render):
1. Connect GitHub and create new Web Service from this repo.
2. Build command: `pip install -r requirements.txt`
3. Start command: `python main.py`
4. Add environment variable `BOT_TOKEN` (your Telegram token) and optional `API_FOOTBALL_KEY`.
