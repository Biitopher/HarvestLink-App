#!/usr/bin/python3
"""Farmer controller definitions"""
import uuid
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError
from api.v1.controllers import db_storage
from models.cart import Cart
from models.orders import Order
from models.products import Product
from api.v1.controllers.products import Products

"""
Products
    View products
    Add products
    Update products
    Delete products
Orders
    View orders
    Accept orders
    Deliver orders
    Decline orders
"""

products = Products()


class Farmer:
    """Handles all farmer operations"""
    """Products"""

    def view_products(self, farmer_id):
        """Fetch all products of the farmer"""
        try:
            farmer_products = products.list_farmer_products(farmer_id)
            return farmer_products
        except SQLAlchemyError as e:
            return None

    def add_new_product(self, product_details):
        u_id = str(uuid.uuid4())
        name = product_details['name']
        category = product_details['category']
        price = product_details['price']
        location = product_details['location']
        quantity = product_details['quantity']
        farmer_id = product_details['farmer_id']
        created_at = datetime.now()
        updated_at = datetime.now()

        """Create a session"""
        session = db_storage.get_session()
        try:
            added_product = Product.add_product(session, u_id, name, category,
                                                price, location, quantity,
                                                farmer_id, created_at,
                                                updated_at)
            if added_product:
                return True
        except SQLAlchemyError as e:
            print(e)
            return False

    def update_product(self, farmer_id, product_id, product_details):
        """Updates the farmer product"""
        session = db_storage.get_session()
        try:
            updated_product = Product.update_product(session,
                                                     product_id,
                                                     farmer_id, product_details)
            if updated_product:
                return True
            return False
        except SQLAlchemyError as e:
            return False

    def delete_product(self, farmer_id, product_id):
        """Deletes a product"""
        session = db_storage.get_session()
        try:
            deleted_product = Product.delete_product(session, product_id,
                                                     farmer_id)
            if deleted_product:
                return True
            return False
        except SQLAlchemyError as e:
            return False

    """Orders"""

    def get_all_orders(self, farmer_id):
        """Fetch all order for the farmer"""
        orders = []
        session = db_storage.get_session()
        try:
            my_orders = Order.get_orders(session, farmer_id)
            for my_order, consumer in my_orders:
                orders.append({
                    "order_id": my_order.id,
                    "checkout_id": my_order.checkout_id,
                    "product_id": my_order.product_id,
                    "consumer_id": my_order.consumer_id,
                    "consumer_name": consumer.name,
                    "consumer_phone": consumer.phone,
                    "farmer_id": my_order.farmer_id,
                    "product_name": my_order.product_name,
                    "quantity": my_order.quantity,
                    "price": my_order.price,
                    "category": my_order.category,
                    "location": my_order.location,
                    "status": my_order.status
                })
            return orders
        except SQLAlchemyError as e:
            return None

    def accept_order(self, farmer_id, order_id):
        """Accept order"""
        session = db_storage.get_session()
        try:
            try:
                accepted = Order.accept_order(session, order_id, farmer_id)
                if accepted:
                    return True
                return False
            except Exception as exc:
                print(exc)
                return False
        except SQLAlchemyError as e:
            print(e)
            return False

    def deliver_order(self, farmer_id, order_id):
        """deliver order"""
        session = db_storage.get_session()
        try:
            try:
                delivered = Order.deliver_order(session, order_id, farmer_id)
                if delivered:
                    return True
                return False
            except Exception as exc:
                return False
        except SQLAlchemyError as e:
            return False

    def decline_order(self, farmer_id, order_id):
        """decline order"""
        session = db_storage.get_session()
        try:
            try:
                declined = Order.decline_order(session, order_id, farmer_id)
                if declined:
                    return True
                return False
            except Exception as exc:
                return False
        except SQLAlchemyError as e:
            return False
