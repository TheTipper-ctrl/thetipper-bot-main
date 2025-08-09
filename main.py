import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_FOOTBALL_KEY = os.getenv("API_FOOTBALL_KEY")  # optional for predictions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🕴️ Welcome to The Tipper — your underworld plug for high‑odds football predictions.\n"
        "Commands:\n"
        "/start - Welcome message\n"
        "/ping - Check bot is alive\n"
        "/predict <league_id> <fixture_id> - Get predictions (requires API key)\n"
    )

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Pong! ✅")

def fetch_prediction(league_id, fixture_id):
    if not API_FOOTBALL_KEY:
        return None, 'API key not configured.'
    url = f"https://v3.api-football.com/predictions?league={league_id}&fixture={fixture_id}"
    headers = {"x-apisports-key": API_FOOTBALL_KEY}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        data = r.json()
        return data, None
    except Exception as e:
        return None, str(e)

async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        await update.message.reply_text("Usage: /predict <league_id> <fixture_id>")
        return
    league_id, fixture_id = context.args
    data, err = fetch_prediction(league_id, fixture_id)
    if err:
        await update.message.reply_text(f"Prediction error: {err}")
        return
    # Basic formatting (depends on API response)
    try:
        resp = data.get('response', [])
        if not resp:
            await update.message.reply_text('No prediction data returned.')
            return
        p = resp[0].get('predictions', {})
        message = '*Predictions*\n'
        for k, v in p.items():
            message += f"{k}: {v}\n"
        await update.message.reply_text(message, parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f'Error parsing prediction: {e}')

def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not set. Exiting.")
        return
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ping", ping))
    app.add_handler(CommandHandler("predict", predict))
    logger.info("Bot starting...")
    app.run_polling()

if __name__ == '__main__':
    main()
