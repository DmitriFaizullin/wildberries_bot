import requests
import sqlite3
from database_handlers import (
    add_product_to_db, update_min_price, update_max_price, get_ids_products_db)


# Получение каталога товаров с сайта Wildberries
def get_catalog_wb(ids):
    geo_info = requests.get(
        url='https://user-geo-data.wildberries.ru/get-geo-info').json()
    destination = geo_info['destinations'][-1]
    params = {
        'dest': destination,
        'nm': ';'.join(map(str, ids))
    }
    response = requests.get(
        url='https://card.wb.ru/cards/v2/detail', params=params)
    return response.json()


# Создание карточки товара с необходимыми данными
def create_product_cart(product):
    sizes = product.get('sizes', [])
    for size in sizes:
        prices = size.get('price', None)
        if prices:
            price = prices.get('product', None)
            break
    return {
        'price': price,
        'brand': product.get('brand', None),
        'name': product.get('name', None),
        'product_url': (
            f'https://www.wildberries.ru/catalog/{product["id"]}/'
            f'detail.aspx')
    }


# Создание словаря товаров (key - id товара)
def get_products(response):
    products = {}
    products_raw = response.get('data', {}).get('products', [])
    for product in products_raw:
        product_cart = create_product_cart(product)
        products[product['id']] = product_cart
    return products


# Проверка цен на товары и уведомление при снижении цены
def check_prices(bot):
    products_db = get_ids_products_db()
    products_ids = [product['id'] for product in products_db]
    products_wb = get_products(get_catalog_wb(products_ids))
    for product_db in products_db:
        product_wb = products_wb.get(product_db['id'])
        price_wb = product_wb.get('price')
        min_price_db = product_db.get('min_price')
        max_price_db = product_db.get('max_price')
        if price_wb < min_price_db:
            message = (
                f'Минимальная цена товара!\n'
                f"Была: {min_price_db // 100} руб.\n"
                f"Стала: {price_wb // 100} руб.\n"
                f"Максимальная: {max_price_db // 100} руб.\n"
                f"{product_wb['product_url']}\n"
            )
            bot.send_message(product_db['user_id'], message)
            update_min_price(product_db['id'], price_wb)
        elif price_wb > max_price_db:
            message = (
                f'Максимальная цена товара!\n'
                f"Была: {max_price_db // 100} руб.\n"
                f"Стала: {price_wb // 100} руб.\n"
                f"Минимальная: {min_price_db // 100} руб.\n"
                f"{product_wb['product_url']}\n"
            )
            bot.send_message(product_db['user_id'], message)
            update_max_price(product_db['id'], price_wb)


# Получение данных о товаре с сервера Wildberries по ID
def get_product_data(product_id):
    response = get_catalog_wb([product_id])
    products = response.get('data', {}).get('products', [])
    if not products:
        raise ValueError('Такой товар не найден на сервере')
    product_cart = create_product_cart(products[0])
    return product_cart['price'], product_cart['product_url']


# Обработка введенного ID товара и добавление в базу данных
def handle_product_id(message, bot):
    try:
        product_id = int(message.text)
    except ValueError:
        bot.send_message(
            message.chat.id,
            'ID товара должно быть числом. Пожалуйста, попробуйте снова.'
        )
        return
    product_price, product_url = get_product_data(product_id)
    try:
        add_product_to_db(
            product_id, product_price, product_url, message.chat.id)
    except ValueError:
        bot.send_message(message.chat.id, 'Ошибка добавления товара.')
        return
    except sqlite3.IntegrityError:
        bot.send_message(message.chat.id, 'Такой товар уже добавлен.')
        return

    text = (
        f'Товар добавлен!\n'
        f"Цена: {product_price // 100} руб.\n"
        f"{product_url}\n"
    )
    bot.send_message(message.chat.id, text)
