import sqlite3  # Импорт модуля для работы с базой данных SQLite.
import tkinter as tk  # Импорт библиотеки Tkinter для создания GUI.
from tkinter import messagebox, ttk  # Импорт компонентов MessageBox и ttk из библиотеки Tkinter.
from contextlib import closing  # Импорт функции closing из contextlib для управления ресурсами.


# Создание базы данных и таблицы, если их не существует.
def create_db():
    with closing(sqlite3.connect('products.db')) as conn:  # Открытие соединения с базой данных products.db.
        cursor = conn.cursor()  # Создание курсора для выполнения SQL-запросов.
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY, 
                user_id INTEGER, 
                min_price INTEGER
            )'''  # Создание таблицы products, если она не существует.
        )
        conn.commit()  # Сохранение изменений в базе данных.


# Получение списка всех товаров из базы данных.
def get_products():
    with closing(sqlite3.connect('products.db')) as conn:  # Открытие соединения с базой данных products.db.
        cursor = conn.cursor()  # Создание курсора для выполнения SQL-запросов.
        cursor.execute('SELECT id, user_id, min_price FROM products')  # Выполнение запроса на получение всех товаров.
        rows = cursor.fetchall()  # Получение всех строк результата запроса.
    return [{'id': row[0], 'user_id': row[1], 'min_price': row[2]} for row in rows]  # Преобразование строк в словари и возврат списка.


# Добавление нового товара в базу данных.
def add_product(product_id, user_id, min_price):
    with closing(sqlite3.connect('products.db')) as conn:  # Открытие соединения с базой данных products.db.
        cursor = conn.cursor()  # Создание курсора для выполнения SQL-запросов.
        cursor.execute(
            '''INSERT INTO products (id, user_id, min_price) VALUES (?, ?, ?)''',  # Вставка нового товара в таблицу.
            (product_id, user_id, min_price)  # Параметры для вставки.
        )
        conn.commit()  # Сохранение изменений в базе данных.


# Удаление товара из базы данных по его ID.
def delete_product(product_id):
    with closing(sqlite3.connect('products.db')) as conn:  # Открытие соединения с базой данных products.db.
        cursor = conn.cursor()  # Создание курсора для выполнения SQL-запросов.
        cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))  # Удаление товара по ID.
        conn.commit()  # Сохранение изменений в базе данных.


# Обновление списка товаров в интерфейсе.
def refresh_list():
    for row in listbox.get_children():  # Цикл по всем элементам списка.
        listbox.delete(row)  # Удаление текущего элемента списка.
    products = get_products()  # Получение актуального списка товаров из базы данных.
    for product in products:  # Цикл по всем товарам.
        listbox.insert("", "end", values=(product['id'], product['user_id'], product['min_price']))  # Вставка товара в список.


# Обработчик добавления нового товара.
def on_add():
    try:
        product_id = int(entry_id.get())  # Получение ID товара из поля ввода и преобразование в целое число.
        user_id = int(entry_user_id.get())  # Получение ID пользователя из поля ввода и преобразование в целое число.
        min_price = int(entry_min_price.get())  # Получение минимальной цены из поля ввода и преобразование в целое число.
        add_product(product_id, user_id, min_price)  # Добавление товара в базу данных.
        refresh_list()  # Обновление списка товаров в интерфейсе.
    except ValueError:
        messagebox.showerror("Ошибка ввода", "Пожалуйста, введите правильные значения.")  # Показ сообщения об ошибке, если введены некорректные данные.


# Обработчик удаления выбранного товара.
def on_delete():
    selected_item = listbox.selection()[0]  # Получение ID выбранного элемента в списке.
    product_id = listbox.item(selected_item, 'values')[0]  # Получение ID товара из выбранного элемента.
    delete_product(product_id)  # Удаление товара из базы данных.
    refresh_list()  # Обновление списка товаров в интерфейсе.


if __name__ == "__main__":
    # Создание графического интерфейса.
    root = tk.Tk()  # Создание главного окна приложения.
    root.title("Управление товарами")  # Установка заголовка окна.

    frame = tk.Frame(root)  # Создание фрейма для списка товаров.
    frame.pack(pady=10)  # Размещение фрейма с отступом по вертикали.

    listbox = ttk.Treeview(frame, columns=("ID", "User ID", "Min Price"), show="headings")  # Создание списка товаров.
    listbox.heading("ID", text="ID товара")  # Установка заголовка для колонки ID.
    listbox.heading("User ID", text="ID пользователя")  # Установка заголовка для колонки User ID.
    listbox.heading("Min Price", text="Минимальная цена")  # Установка заголовка для колонки Min Price.
    listbox.pack()  # Размещение списка товаров в фрейме.

    refresh_list()  # Первоначальное заполнение списка товаров.

    entry_frame = tk.Frame(root)  # Создание фрейма для полей ввода.
    entry_frame.pack(pady=10)  # Размещение фрейма с отступом по вертикали.

    tk.Label(entry_frame, text="ID товара").grid(row=0, column=0)  # Создание метки для поля ввода ID товара.
    entry_id = tk.Entry(entry_frame)  # Создание поля ввода ID товара.
    entry_id.grid(row=0, column=1)  # Размещение поля ввода.

    tk.Label(entry_frame, text="ID пользователя").grid(row=1, column=0)  # Создание метки для поля ввода ID пользователя.
    entry_user_id = tk.Entry(entry_frame)  # Создание поля ввода ID пользователя.
    entry_user_id.grid(row=1, column=1)  # Размещение поля ввода.

    tk.Label(entry_frame, text="Текущая цена").grid(row=2, column=0)  # Создание метки для поля ввода минимальной цены.
    entry_min_price = tk.Entry(entry_frame)  # Создание поля ввода минимальной цены.
    entry_min_price.grid(row=2, column=1)  # Размещение поля ввода.

    btn_add = tk.Button(root, text="Добавить товар", command=on_add)  # Создание кнопки для добавления товара.
    btn_add.pack(pady=5)  # Размещение кнопки с отступом по вертикали.

    btn_delete = tk.Button(root, text="Удалить товар", command=on_delete)  # Создание кнопки для удаления товара.
    btn_delete.pack(pady=5)  # Размещение кнопки с отступом по вертикали.

    create_db()  # Создание базы данных и таблицы (если они не существуют).
    root.mainloop()  # Запуск основного цикла обработки событий.
