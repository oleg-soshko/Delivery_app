from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
config = {
    'username': 'username',
    'password': 1233456,
    'host': 'localhost',
    'port': 5432,
    'database': 'shop_db'
}

engine = create_engine(
    f"postgresql://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
)


class Shop(Base):
    __tablename__ = 'Shops'
    id = Column(Integer, primary_key=True, autoincrement=True)
    shop_name = Column(String, nullable=False)

    def __init__(self, shop_name):
        self.shop_name = shop_name


class Product(Base):
    __tablename__ = 'Products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    description = Column(Text, nullable=False)
    shop_id = Column(Integer, nullable=False)
    image = Column(String)

    def __init__(self, product_name: str, price: int, quantity: int, description: str, shop_id: int, image: str = ''):
        self.product_name = product_name
        self.price = price
        self.quantity = quantity
        self.description = description
        self.shop_id = shop_id
        self.image = image


class Order(Base):
    __tablename__ = 'Orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    city = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    date = Column(String, nullable=False)

    def __init__(self, name: str, email: str, city: str, phone: str, date: str):
        self.name = name
        self.email = email
        self.city = city
        self.phone = phone
        self.date = date


class OrderDetails(Base):
    __tablename__ = 'Order_Details'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, nullable=False)
    product_name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    order_id = Column(Integer, nullable=False)

    def __init__(self, product_id: int, product_name: str, price: int, quantity: int, order_id: int):
        self.product_id = product_id
        self.product_name = product_name
        self.price = price
        self.quantity = quantity
        self.order_id = order_id


class DataBase:
    def create_session(self, engine):
        Session = sessionmaker(bind=engine)
        session = Session()
        return session

    def add_product(self, product_name: str, price: int, quantity: int, description: str, shop_id: int, image: str):
        session = self.create_session(engine=engine)
        new_product = Product(product_name, price, quantity, description, shop_id, image)
        session.add(new_product)
        session.commit()

    def add_company(self, shop_name):
        session = self.create_session(engine=engine)
        new_company = Shop(shop_name)
        session.add(new_company)
        session.commit()

    def add_order(self, name, email, city, phone, date):
        session = self.create_session(engine=engine)
        order = Order(name, email, city, phone, date)
        session.add(order)
        session.commit()

    def add_order_details(self, product_id, product_name, price, quantity, order_id):
        session = self.create_session(engine=engine)
        order_details = OrderDetails(product_id, product_name, price, quantity, order_id)
        session.add(order_details)
        session.commit()

    def select_last_order(self):
        session = self.create_session(engine=engine)
        last_order = session.query(Order).order_by(Order.id.desc()).first().id
        return last_order

    def select_all_shops(self):
        session = self.create_session(engine=engine)
        all_shops = session.query(Shop).all()
        return all_shops

    def select_products_from_shop(self, shop_id):
        session = self.create_session(engine=engine)
        products_from_shop = session.query(Shop, Product).\
            join(Product, Shop.id == Product.shop_id).filter(Shop.id == shop_id).all()
        return products_from_shop

    def select_all_products(self):
        session = self.create_session(engine=engine)
        all_products = session.query(Shop, Product).\
            join(Product, Shop.id == Product.shop_id).all()
        return all_products

    def select_product_from_id(self, product_id):
        session = self.create_session(engine=engine)
        product = session.query(Shop, Product).\
            join(Product, Shop.id == Product.shop_id).filter(Product.id == product_id).first()
        return product

Base.metadata.create_all(engine)
