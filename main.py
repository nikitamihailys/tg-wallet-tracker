import asyncio
import requests
from web3 import Web3
from telegram import Bot
from telegram.ext import Updater, CommandHandler

TELEGRAM_TOKEN = "7872098214:AAEcVXZJIh6fHhIFCfaO5Gku6gvbwxRHzCA"
ETH_ADDRESS = "0xb1b51b15125e688aea7b919eca7a4eb94aab8f17"

INFURA_WS = "wss://mainnet.infura.io/ws/v3/84842078b09946638c03157f83405213"
w3 = Web3(Web3.WebsocketProvider(INFURA_WS))

bot = Bot(token=TELEGRAM_TOKEN)

async def watch_eth_transactions():
    print("Подключение к Ethereum...")
    while True:
        try:
            pending_filter = w3.eth.filter('pending')
            while True:
                for tx_hash in pending_filter.get_new_entries():
                    tx = w3.eth.get_transaction(tx_hash)
                    if tx and tx.to and tx.to.lower() == ETH_ADDRESS.lower():
                        message = f"💸 Входящая транзакция в Ethereum\n\nС адреса: `{tx['from']}`\nСумма: {w3.fromWei(tx['value'], 'ether')} ETH"
                        bot.send_message(chat_id=827200392, text=message, parse_mode='Markdown')
                await asyncio.sleep(2)
        except Exception as e:
            print(f"Ошибка: {e}")
            await asyncio.sleep(5)

def start(update, context):
    update.message.reply_text("👋 Привет! Я отслеживаю адреса и сообщаю о транзакциях.\n\nДоступные команды:\n/balance — баланс кошелька\n/start — перезапуск\n/help — помощь")

def help_command(update, context):
    update.message.reply_text("💡 Я отслеживаю транзакции на адресах.\n\n/balance — баланс ETH\n/start — запуск\n/help — помощь")

def balance(update, context):
    balance_wei = w3.eth.get_balance(ETH_ADDRESS)
    balance_eth = w3.fromWei(balance_wei, 'ether')
    update.message.reply_text(f"💰 Баланс Ethereum-кошелька:\n{balance_eth:.4f} ETH")

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("balance", balance))
    loop = asyncio.get_event_loop()
    loop.create_task(watch_eth_transactions())
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
