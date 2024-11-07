import sqlite3
import requests


# Создание базы данных и таблицы
def create_db():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute(
        ''' CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY, user_id INTEGER, min_price INTEGER
        )
        ''')
    conn.commit()
    conn.close()


# Добавление товара в базу данных
def add_product(product_id, user_id, min_price):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute(
        ''' INSERT INTO products (id, user_id, min_price) VALUES (?, ?, ?) ''',
        (product_id, user_id, min_price))
    conn.commit()
    conn.close()


# Получение товаров из базы данных
def get_products():
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, user_id, min_price FROM products')
    rows = cursor.fetchall()
    conn.close()
    products = []
    for row in rows:
        product = {'id': row[0], 'user_id': row[1], 'min_price': row[2]}
        products.append(product)
    return products


# Получение каталога товаров с сайта
def get_catalog(ids):
    params = {
        'dest': 1,
        'nm': ';'.join(map(str, ids))
    }
    url = 'https://card.wb.ru/cards/v2/detail'
    response = requests.get(url=url, params=params)
    return response.json()


# Форматирование данных о товарах
def format_items(response):
    products = {}
    products_raw = response.get('data', {}).get('products', None)

    if products_raw is not None and len(products_raw) > 0:
        for product in products_raw:
            sizes = product.get('sizes', None)[0]
            price = sizes.get('price', None).get('total', None)
            products[product.get('id', None)] = price
    return products


# Обновление минимальной цены в базе данных
def update_min_price(product_id, new_price):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute(
        ''' UPDATE products SET min_price = ? WHERE id = ? ''',
        (new_price, product_id))
    conn.commit()
    conn.close()


# Проверка цен и уведомление о снижении
def check_prices():
    products = get_products()
    ids = [prod['id'] for prod in products]
    response = get_catalog(ids)
    items = format_items(response)
    for product in products:
        price_wb = items.get(product['id'])
        price_db = product.get('min_price')
        if price_wb < price_db:
            update_min_price(product['id'], price_wb)
            print(f"Цена на товар {product['id']} снизилась с {price_db} до {price_wb}!")


create_db()
# add_product(71906089, 1, 1000)
# add_product(221799727, 1, 2000)
check_prices()
