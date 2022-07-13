from flask import render_template, session, redirect, url_for
from datetime import datetime

from app import app
from app import data_base
from app import datas
from app import forms


@app.route('/', methods=['GET', 'POST'])
@app.route('/<int:shop_id>', methods=['GET', 'POST'])
def index(shop_id=None):
    if 'cart' not in session:
        session['cart'] = []
    cart_contents = datas.cart_contents(session['cart'])
    try:
        db = data_base.DataBase()
        shops = db.select_all_shops()
        if shop_id:
            products = db.select_products_from_shop(shop_id)
        elif len(cart_contents[0]) > 0:
            products = db.select_products_from_shop(cart_contents[0][0]['shop_id'])
        else:
            products = db.select_all_products()
    except Exception as e:
        products = []
        shops = []
    return render_template('index.html', products=products, shops=shops, cart_products=cart_contents[0],
                           to_pay=cart_contents[1], quantity_in_cart=cart_contents[2])


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    form = forms.AddCart()
    if form.validate_on_submit():
        datas.add_product_to_cart(session['cart'], form.id.data, form.quantity.data)
        session.modified = True
    cart_contents = datas.cart_contents(session['cart'])
    return render_template('cart.html', cart_products=cart_contents[0], to_pay=cart_contents[1],
                           quantity_in_cart=cart_contents[2])


@app.route('/quick-add-to_cart/<shop_id>_<product_id>')
def quick_add_to_cart(shop_id, product_id):
    if 'cart' not in session:
        session['cart'] = []
    datas.add_product_to_cart(session=session['cart'], product_id=product_id, shop_id=shop_id)
    session.modified = True
    return redirect(url_for('index'))


@app.route('/remove-from-cart/<index>')
def remove_from_cart(index):
    del session['cart'][int(index) - 1]
    session.modified = True
    return redirect(url_for('cart'))


@app.route('/remove-all_from-cart')
def remove_all_from_cart():
    session['cart'].clear()
    session.modified = True
    return redirect(url_for('index'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    form = forms.Checkout()
    cart_contents = datas.cart_contents(session['cart'])
    return render_template('checkout.html', form=form, cart_products=cart_contents[0],
                           to_pay=cart_contents[1], quantity_in_cart=cart_contents[2])


@app.route('/success', methods=['GET', 'POST'])
def success():
    db = data_base.DataBase()
    form = forms.Checkout()
    last_order_id = None
    now = datetime.now().strftime("%d.%m.%y")
    cart_contents = datas.cart_contents(session['cart'])
    if form.validate_on_submit():
        db.add_order(form.name.data, form.email.data, form.city.data, form.telephone.data, now)
        last_order_id = db.select_last_order()
        for product in cart_contents[0]:
            db.add_order_details(product['id'], product['name'], product['price'],
                                 product['quantity'], order_id=last_order_id)
        del session['cart']
        session.modified = True
    return render_template('success.html', form=form, now=now, cart_products=cart_contents[0],
                           to_pay=cart_contents[1], quantity_in_cart=cart_contents[2], order_id=last_order_id)
