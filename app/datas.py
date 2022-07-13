from app import data_base


def cart_contents(session):
    db = data_base.DataBase()
    products = []
    to_pay = 0
    index = 0
    for item in session:
        product = db.select_product_from_id(product_id=item['id'])
        total = item['quantity'] * product[1].price
        to_pay += total
        index += 1
        products.append(
            {'id': product[1].id,
             'name': product[1].product_name,
             'price': product[1].price,
             'quantity': item['quantity'],
             'total': total,
             'index': index,
             'shop_name': product[0].shop_name,
             'shop_id': item['shop_id'],
             'image': product[1].image
             }
        )
    products_in_cart = len(products)
    return products, to_pay, products_in_cart


def add_product_to_cart(session, shop_id: int, product_id: int, product_quantity: int = 1):
    dict_keys = []
    for item in session:
        dict_keys.append(int(item['id']))
    if int(product_id) in dict_keys:
        for item in session:
            if int(product_id) == item['id']:
                item['quantity'] += 1
    else:
        session.append({'id': int(product_id), 'quantity': product_quantity, 'shop_id': int(shop_id)})
