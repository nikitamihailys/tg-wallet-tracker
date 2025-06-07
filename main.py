import logging
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.ext import AIORateLimiter
from telegram.ext.webhookhandler import WebhookServer

from web3 import Web3
from flask import Flask, request

TELEGRAM_TOKEN = "7872098214:AAEcVXZJIh6fHhIFCfaO5Gku6gvbwxRHzCA"
ETH_ADDRESS = "0xb1b51b15125e688aea7b919eca7a4eb94aab8f17"
WEBHOOK_URL = "https://tg-wallet-tracker.onrender.com/webhook"

INFURA_HTTP = "https://mainnet.infura.io/v3/84842078b09946638c03157f83405213"
w3 = Web3(Web3.HTTPProvider(INFURA_HTTP))

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Бот запущен через Webhook.\nКоманда /balance покажет текущий баланс ETH.")

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    balance_wei = w3.eth.get_balance(ETH_ADDRESS)
    balance_eth = w3.fromWei(balance_wei, 'ether')
    await update.message.reply_text(f"💰 Баланс Ethereum-кошелька:\n{balance_eth:.4f} ETH")

app = Flask(__name__)

@app.route('/')
def index():
    return "✅ Бот работает"

@app.route('/webhook', methods=['POST'])
def webhook():
    request_data = request.get_json(force=True)
    application.update_queue.put_nowait(Update.de_json(data=request_data, bot=application.bot))
    return "ok"

if __name__ == '__main__':
    application = Application.builder().token(TELEGRAM_TOKEN).rate_limiter(AIORateLimiter()).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("balance", balance))
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.delete_webhook()
    bot.set_webhook(WEBHOOK_URL)
    app.run(host="0.0.0.0", port=10000)
