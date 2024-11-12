import os
from dotenv import load_dotenv
from telebot import TeleBot, types
from price_monitor import check_prices, handle_product_id

import threading
import time


load_dotenv()
token = os.getenv('TOKEN')
chat_id = os.getenv('CHAT_ID')


bot = TeleBot(token=token)


def price_monitoring():
    while True:
        check_prices(bot, chat_id)
        time.sleep(600)


@bot.message_handler(content_types=['text'])
def receive_message(message):
    handle_product_id(message, bot)


@bot.message_handler(commands=['start'])
def wake_up(message):
    chat = message.chat
    name = message.chat.first_name
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_addproduct = types.KeyboardButton('/add_product')
    keyboard.add(button_addproduct)
    bot.send_message(
        chat_id=chat.id,
        text=f'Привет, {name}, добавь id товара!',
        reply_markup=keyboard
    )


if __name__ == '__main__':
    threading.Thread(target=price_monitoring, daemon=True).start()
    bot.polling(none_stop=True)
