import os
import json
from dotenv import load_dotenv
from telebot import TeleBot, types
from product_management import check_prices, handle_product_id
from database_handlers import (
    create_db,
    get_user_products,
    delete_product
)

import threading
import time


load_dotenv()
token = os.getenv('TOKEN')


bot = TeleBot(token=token)


def price_monitoring():
    while True:
        check_prices(bot)
        time.sleep(600)


@bot.message_handler(commands=['start'])
def wake_up(message):
    chat = message.chat
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_myproducts = types.KeyboardButton('/myproducts')
    keyboard.add(button_myproducts)
    bot.send_message(
        chat_id=chat.id,
        text='Привет!',
        reply_markup=keyboard
    )


def create_delete_button(product_id):
    delete_callback_data = json.dumps({"action": "delete_selected", "id": product_id})
    delete_button = types.InlineKeyboardButton(text="Удалить", callback_data=delete_callback_data)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(delete_button)
    return keyboard


@bot.message_handler(commands=['myproducts'])
def my_products(message):
    chat_id = message.chat.id
    products = get_user_products(chat_id)
    if products:
        for product in products:
            keyboard = create_delete_button(product['id'])
            bot.send_photo(
                chat_id=chat_id,
                photo=product['product_url'],
                reply_markup=keyboard
            )
    else:
        bot.send_message(chat_id=chat_id, text="У вас нет добавленных товаров.")


def create_confirmation_buttons(product_id):
    confirm_callback_data = json.dumps({"action": "confirm_delete", "id": product_id})
    cancel_callback_data = json.dumps({"action": "cancel_delete", "id": product_id})
    confirm_button = types.InlineKeyboardButton(text="Подтвердить", callback_data=confirm_callback_data)
    cancel_button = types.InlineKeyboardButton(text="Отмена", callback_data=cancel_callback_data)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(confirm_button, cancel_button)
    return keyboard


@bot.callback_query_handler(func=lambda call: json.loads(call.data).get('action') == 'delete_selected')
def handle_delete_selected(call):
    user_id = call.message.chat.id
    data = json.loads(call.data)
    product_id = data['id']
    keyboard = create_confirmation_buttons(product_id)
    bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: json.loads(call.data).get('action') == 'confirm_delete')
def handle_confirm_delete(call):
    user_id = call.message.chat.id
    data = json.loads(call.data)
    product_id = data['id']
    delete_product(user_id, product_id)
    bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id, reply_markup=None)
    bot.send_message(chat_id=user_id, text="Товар удален.")


@bot.callback_query_handler(func=lambda call: json.loads(call.data).get('action') == 'cancel_delete')
def handle_cancel_delete(call):
    user_id = call.message.chat.id
    data = json.loads(call.data)
    product_id = data['id']
    keyboard = create_delete_button(product_id)
    bot.edit_message_reply_markup(chat_id=user_id, message_id=call.message.message_id, reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def receive_message(message):
    handle_product_id(message, bot)


if __name__ == '__main__':
    create_db()
    threading.Thread(target=price_monitoring, daemon=True).start()
    bot.polling(none_stop=True)
