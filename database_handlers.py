import sqlite3


# Функция для добавления товара в базу данных
def add_product_to_db(product_id, product_price):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY)''')
    cursor.execute('''INSERT INTO products (id, min_price) VALUES (?, ?)''', (product_id, product_price))
    conn.commit()
    conn.close()


def update_min_price(product_id, new_price):
    conn = sqlite3.connect('products.db')
    cursor = conn.cursor()
    cursor.execute(
        ''' UPDATE products SET min_price = ? WHERE id = ? ''',
        (new_price, product_id))
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
