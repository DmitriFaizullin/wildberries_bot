# Telegram Price Monitoring Bot

Этот проект представляет собой бота для Telegram, который мониторит цены на товары с сайта Wildberries и уведомляет пользователей о снижении цен.

## Установка

1. Клонируйте репозиторий:
    ```sh
    git clone git@github.com:DmitriFaizullin/wildberries_bot.git
    ```
2. Установите и активируйте виртуальное окружение:
    ```sh
    python3 -m venv venv
    ```
    для Linux/MacOS:
    ```
    source venv/bin/activate
    ```
    для Windows:
    ```
    source venv/Scripts/activate
    ```
3. Установите зависимости:
    ```sh
    pip install -r requirements.txt
    ```

4. Создайте файл `.env` в корневом каталоге проекта и добавьте следующие строки:
    ```env
    TOKEN=ваш_токен_бота_telegram
    ALLOWED_USERS=список_разрешенных_id_пользователей_через_запятую
    ```

## Использование

1. Запустите бота:
    ```sh
    python bot_price_monitor.py
    ```

2. В Telegram отправьте команду `/start`, чтобы начать использование бота.

3. Для добавления товара в мониторинг отправьте его id с сайта Wildberries.

4. Для просмотра добавленных товаров используйте команду `/myproducts`.

## Описание файлов

- `bot_price_monitor.py` - Основной файл бота, содержащий логику обработки команд и сообщений.
- `product_management.py` - Модуль, отвечающий за проверку цен и управление товарами.
- `database_handlers.py` - Модуль для взаимодействия с базой данных.

## Зависимости

- `telebot`
- `requests`
- `decouple`

Все зависимости перечислены в файле `requirements.txt`.

## Авторы

Файзуллин Дмитрий Андреевич
[Мой Telegram](https://t.me/DmitriFn)
