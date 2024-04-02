#!/usr/bin/python3
"""Consumer controller definitions"""
import uuid

from sqlalchemy.exc import SQLAlchemyError
from api.v1.controllers import db_storage
from models.cart import Cart
from models.orders import Order
from models.products import Product


class Consumer:
    """Handles consumer api functions"""
    """show_cart_items, edit_cart_items, delete_cart_items"""

    def add_item(self, u_id, consumer_id, product_id, quantity, created_at,
                 updated_at):
        """Adds item to cart"""
        try:
            if Cart.add_item(db_storage.get_session(), u_id=u_id,
                             product_id=product_id,
                             consumer_id=consumer_id,
                             quantity=quantity,
                             created_at=created_at,
                             updated_at=updated_at):
                return True
            else:
                return False
        except SQLAlchemyError as e:
            return False

    def show_cart_items(self, consumer_id):
        """Returns a json of all cart items for the logged in consumer"""
        cart_details = []
        items = []
        try:
            cart_items = (
                db_storage.get_session()
                .query(Cart, Product)
                .join(Product, Cart.product_id == Product.id)
                .filter(Cart.consumer_id == consumer_id)
                .all()
            )

            """get the total quantity and total cost of items in the cart"""
            total_quantity = sum(
                cart_item.quantity for cart_item, _ in cart_items)
            total_cost = sum(
                cart_item.quantity * product.price for cart_item, product in
                cart_items)

            for cart_item, product in cart_items:
                items.append({
                    "product_id": cart_item.product_id,
                    "quantity": cart_item.quantity,
                    "name": product.name,
                    "price": product.price,
                    "category": product.category,
                    "cart_item_id": cart_item.id
                })

            cart_details.append({"cart_items": items,
                                 "total_cost": total_cost})
            return cart_details
        except SQLAlchemyError as e:
            return None

    def edit_cart_item(self, consumer_id, product_id, new_quantity):
        """Handles the quantity update feature"""
        try:
            if Cart.edit_quantity(db_storage.get_session(), product_id,
                                  consumer_id, new_quantity):
                return True
            else:
                return False
        except SQLAlchemyError as e:
            return False

    def delete_cart_item(self, item_id, consumer_id):
        """Handles delete cart item api endpoint"""
        try:
            if Cart.delete_item(db_storage.get_session(), item_id,
                                consumer_id):
                return True
            else:
                return False
        except SQLAlchemyError as e:
            return False

    def place_order(self, consumer_id, consumer_location):
        """Handles order api operations"""
        u_id = str(uuid.uuid4())
        try:
            if Order.place_order(db_storage.get_session(), u_id,
                                 consumer_id,
                                 consumer_location):
                return True
            else:
                return False
        except SQLAlchemyError as e:
            return False

    def get_all_orders(self, consumer_id):
        """Fetch all orders"""
        orders = []
        try:
            my_orders = Order.view_orders(db_storage.get_session(),
                                          consumer_id)
            for my_order in my_orders:
                orders.append({
                    "checkout_id": my_order.checkout_id,
                    "product_id": my_order.product_id,
                    "consumer_id": my_order.consumer_id,
                    "farmer_id": my_order.farmer_id,
                    "product_name": my_order.product_name,
                    "quantity": my_order.quantity,
                    "price": my_order.price,
                    "category": my_order.category,
                    "location": my_order.location,
                    "status": my_order.status,
                    "order_id": my_order.id

                })
            return orders
        except SQLAlchemyError as e:
            return None

    def cancel_order(self, consumer_id, order_id):
        """Cancels a consumer's order"""
        try:
            if Order.cancel_order(db_storage.get_session(), order_id,
                                  consumer_id):
                return True
            return False
        except SQLAlchemyError as e:
            return False
