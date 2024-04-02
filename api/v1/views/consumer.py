#!/usr/bin/python3
""" Index file """
import uuid
from datetime import datetime
from api.v1.views import app_views
from api.v1.controllers.consumer import Consumer
from flask import jsonify, request

consumer = Consumer()


@app_views.route('/cart/add', methods=['POST'])
def add_to_cart():
    """Handles add to cart api endpoint"""
    if request.method == 'POST':
        data = request.get_json()
        u_id = str(uuid.uuid4())
        product_id = data['product_id']
        quantity = int(data['quantity'])
        consumer_id = data['consumer_id']
        created_at = datetime.now()
        updated_at = datetime.now()

        added_to_cart = consumer.add_item(u_id, consumer_id, product_id,
                                          quantity, created_at, updated_at)

        if added_to_cart:
            return jsonify({"status": "Added item to cart"}), 200
        return jsonify({"error": "Unable to add to cart"}), 401


@app_views.route('/cart', methods=['GET', 'POST'])
def view_cart():
    """Handles cart operations"""
    if request.method == 'GET':
        if len(request.args.keys()) == 0:
            consumer_id = request.get_json()['consumer_id']
        else:
            consumer_id = request.args.get('consumer_id')
        cart_details = consumer.show_cart_items(consumer_id)
        if cart_details is None:
            return jsonify({"error": "User not logged in"}), 401
        return jsonify(cart_details)

    if request.method == 'POST':
        if len(request.args.keys()) == 0:
            data = request.get_json()
            consumer_id = data['consumer_id']
            product_id = data['product_id']
            new_quantity = int(data['new_quantity'])
        else:
            consumer_id = request.args.get('consumer_id')
            product_id = request.args.get('product_id')
            new_quantity = int(request.args.get('new_quantity'))

        update_quantity = consumer.edit_cart_item(consumer_id, product_id,
                                                  new_quantity)
        if update_quantity:
            return jsonify({"status": "Quantity updated"}), 200
        return jsonify({"error": "Error updating quantity"}), 401


@app_views.route('/cart/delete', methods=['DELETE'])
def delete_item():
    """Deletes item from the cart"""
    if request.method == 'DELETE':
        print("Here")
        data = request.get_json()
        cart_item_id = data['cart_item_id']
        consumer_id = data['consumer_id']

        deleted_item = consumer.delete_cart_item(cart_item_id, consumer_id)

        if deleted_item:
            return jsonify({"status": "Item deleted successfully"}), 200
        return jsonify({"error": "Error deleting item"}), 404


@app_views.route('/place_order', methods=['POST'])
def place_order():
    """Places and order"""
    if request.method == 'POST':
        data = request.get_json()
        consumer_id = data['consumer_id']
        consumer_location = data['consumer_location']

        placed_order = consumer.place_order(consumer_id, consumer_location)
        if placed_order:
            return jsonify({"status": "Order placed successfully"}), 200
        return jsonify({"error": "Error placing an order"}), 401


@app_views.route('/orders', methods=['GET'])
def get_all_orders():
    """Show all orders"""
    if len(request.args.keys()) == 0:
        consumer_id = request.get_json()['consumer_id']
    else:
        consumer_id = request.args.get('consumer_id')
    orders = consumer.get_all_orders(consumer_id)
    if orders is None:
        return jsonify({"error": "Error fetching orders"})
    return jsonify(orders)


@app_views.route('/orders/cancel', methods=['POST'])
def cancel_order():
    """Updates the status of an order"""
    if request.method == 'POST':
        data = request.get_json()
        consumer_id = data['consumer_id']
        order_id = data['order_id']

        cancelled_order = consumer.cancel_order(consumer_id, order_id)
        if cancelled_order:
            return jsonify({"status": "Order cancelled"}), 200
        return jsonify({"error": "Failed to cancel order"}), 401

