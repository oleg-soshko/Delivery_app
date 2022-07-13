from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, IntegerField


class AddCart(FlaskForm):
    id = HiddenField(label='ID')
    quantity = IntegerField(label='Quantity')


class Checkout(FlaskForm):
    name = StringField(label='Name')
    email = StringField(label='Email')
    city = StringField(label='City')
    telephone = StringField(label='Telephone')
