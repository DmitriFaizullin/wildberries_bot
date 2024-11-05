import requests


def get_catalog():
    ids = [
        71906089,
        221799727,
    ]
    params = {
        'dest': 1,
        'nm': ';'.join(map(str, ids))
    }
    url = 'https://card.wb.ru/cards/v2/detail'
    response = requests.get(url=url, params=params)
    return response.json()


def format_items(response):
    products = []
    products_raw = response.get('data', {}).get('products', None)

    if products_raw != None and len(products_raw) > 0:
        for product in products_raw:
            sizes = product.get('sizes', None)[0]
            price = sizes.get('price', None).get('total', None)
            products.append({
                'brand': product.get('brand', None),
                'name': product.get('name', None),
                'id': product.get('id', None),
                'price': price,
            })
    return products


format_items(get_catalog())
