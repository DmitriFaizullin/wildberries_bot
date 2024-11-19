import sqlite3
from contextlib import contextmanager


# Контекстный менеджер для открытия и закрытия соединения с базой данных SQLite
@contextmanager
def open_connection():
    conn = sqlite3.connect('products.db')
    try:
        yield conn
    finally:
        conn.commit()
        conn.close()


# Функция для выполнения запросов SELECT
def execute_query(query, params=()):
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return rows


# Функция для выполнения запросов INSERT, UPDATE, DELETE
def execute_commit(query, params=()):
    with open_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)


# Функция для создания таблицы products, если она не существует
def create_db():
    query = '''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER,
            min_price REAL,
            user_id INTEGER,
            product_url TEXT,
            PRIMARY KEY (id, user_id)
        )
    '''
    execute_commit(query)


# Функция для добавления товара в базу данных
def add_product_to_db(product_id, product_price, product_url, chat_id):
    query = '''
        INSERT INTO products (id, min_price, product_url, user_id)
        VALUES (?, ?, ?, ?)
    '''
    execute_commit(query, (product_id, product_price, product_url, chat_id))


# Функция для обновления минимальной цены товара в базе данных
def update_min_price(product_id, new_price):
    query = '''
        UPDATE products SET min_price = ? WHERE id = ?
    '''
    execute_commit(query, (new_price, product_id))


# Функция для получения списка всех товаров из базы данных
def get_ids_products_db():
    query = '''
        SELECT id, user_id, min_price FROM products
    '''
    rows = execute_query(query)
    return [
        {'id': row[0], 'user_id': row[1], 'min_price': row[2]} for row in rows]


# Функция для получения списка товаров пользователя из базы данных
def get_user_products(user_id):
    query = '''
        SELECT id, min_price, product_url FROM products WHERE user_id = ?
    '''
    rows = execute_query(query, (user_id,))
    return [
        {
            'id': row[0], 'min_price': row[1], 'product_url': row[2]
        } for row in rows]


# Функция для удаления товара из базы данных
def delete_product(user_id, product_id):
    query = '''
        DELETE FROM products WHERE user_id = ? AND id = ?
    '''
    execute_commit(query, (user_id, product_id))
