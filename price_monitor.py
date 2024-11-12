import requests
from database_handlers import add_product_to_db, update_min_price, get_products


# Получение каталога товаров с сайта
def get_catalog(ids):
    params = {
        'dest': 1,
        'nm': ';'.join(map(str, ids))
    }
    url = 'https://card.wb.ru/cards/v2/detail'
    response = requests.get(url=url, params=params)
    return response.json()


def get_product_cart(product):
    sizes = product.get('sizes', None)[0]
    price = sizes.get('price', None).get('product', None)
    product_cart = {
        'price': price,
        'brand': product.get('brand', None),
        'name': product.get('name', None),
        'product_url': f"https://www.wildberries.ru/catalog/{product.get('id', None)}/detail.aspx"
    }
    return product_cart


# Форматирование данных о товарах
def get_products(response):
    products = {}
    products_raw = response.get('data', {}).get('products', None)
    if products_raw is not None and len(products_raw) > 0:
        for product in products_raw:
            product_cart = get_product_cart(product)
            products[product.get('id', None)] = product_cart
    return products


def check_prices(bot, chat_id):
    products_db = get_products()
    products_ids = [product['id'] for product in products_db]
    products_from_server_wb = get_catalog(products_ids)
    products_wb = get_products(products_from_server_wb)
    for product_db in products_db:
        product_wb = products_wb.get(product_db['id'])
        price_wb = product_wb.get('price')
        price_db = product_db.get('min_price')
        if price_wb < price_db:
            message = (
                f'Снизилась цена на товар!\n'
                f"Была: {product_db.get('min_price') // 100} руб.\n"
                f"Стала: {product_wb.get('price') // 100} руб.\n"
                f"{product_wb.get('product_url')}\n"
            )
            bot.send_message(chat_id, message)
            update_min_price(product_db['id'], price_wb)


def handle_product_id(message, bot):
    try:
        product_id = int(message.text)
        response = get_catalog([product_id])
        product = response.get('data', {}).get('products', None)[0]
        product_cart = get_product_cart(product)
        product_price = product_cart.get('price')
        add_product_to_db(product_id, product_price)
        text = (
            f'Твар добавлен!\n'
            f"Цена: {product_price // 100} руб.\n"
            f"{product_cart.get('product_url')}\n"
        )
        bot.send_message(message.chat.id, text)
    except ValueError:
        bot.send_message(message.chat.id, 'ID товара должно быть числом. Пожалуйста, попробуйте снова.')
