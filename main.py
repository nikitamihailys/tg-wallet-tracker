from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler
import os

TOKEN = "7872098214:AAEcVXZJIh6fHhIFCfaO5Gku6gvbwxRHzCA"
bot = Bot(token=TOKEN)
app = Flask(__name__)
dispatcher = Dispatcher(bot=bot, update_queue=None, workers=4, use_context=True)

# Команды
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="✅ Бот работает через Webhook!")

def balance(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="💰 Баланс скоро будет здесь...")

# Регистрация
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("balance", balance))

# Webhook обработчик
@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

@app.route('/')
def home():
    return "✅ TG Wallet Tracker работает"

if __name__ == '__main__':
    bot.set_webhook(url="https://tg-wallet-tracker.onrender.com/webhook")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))