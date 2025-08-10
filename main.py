import os
import telebot
from flask import Flask
import threading

# Create Flask app (dummy server for Render)
app = Flask(__name__)

@app.route('/')
def home():
    return "Tipper Bot is alive!"

# Start the Telegram bot
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found. Please set BOT_TOKEN in environment variables.")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I’m your Tipper Bot 🤖. How can I assist you today?")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

def run_bot():
    bot.polling(none_stop=True)

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

# Run both Flask and Telegram bot in parallel
if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    run_flask()
