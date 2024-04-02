#!/usr/bin/python3
""" Index file """
import uuid
from datetime import datetime
from api.v1.views import app_views
from api.v1.controllers.farmer import Farmer
from flask import jsonify, request

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

farmer = Farmer()

"""Products CRUD Operations"""


@app_views.route('/products', methods=['GET'])
def view_all_products():
    """Fetch all products for the farmer"""
    if request.method == 'GET':
        if len(request.args.keys()) == 0:
            farmer_id = request.get_json()['farmer_id']
        else:
            farmer_id = request.args.get('farmer_id')

        farmer_products = farmer.view_products(farmer_id)
        if farmer_products is None:
            return jsonify({"error": "Could not fetch products"}), 404

        return jsonify(farmer_products), 200


@app_views.route('/products/add', methods=['POST'])
def add_new_product():
    """Adds new product"""
    if request.method == 'POST':
        data = request.get_json()

        added_product = farmer.add_new_product(data)
        if added_product:
            return jsonify({"status": "Product added successfully"}), 201
        return jsonify({"error": "Error adding product"}), 401


@app_views.route('/products/update', methods=['POST'])
def update_product():
    """Update the product"""
    if request.method == 'POST':
        data = request.get_json()
        farmer_id = data['farmer_id']
        product_id = data['product_id']
        new_product_details = {
            "price": float(data['price']),
            "quantity": int(data['quantity']),
        }

        updated_product = farmer.update_product(farmer_id, product_id,
                                                new_product_details)
        if updated_product:
            return jsonify({"status": "Product updated successfully"}), 200
        return jsonify({"error": "Error updating product"}), 404


@app_views.route('/products/delete', methods=['DELETE'])
def delete_product():
    """Delete a product"""
    if request.method == 'DELETE':
        data = request.get_json()
        farmer_id = data['farmer_id']
        product_id = data['product_id']

        deleted_product = farmer.delete_product(farmer_id, product_id)
        if deleted_product:
            return jsonify({"status": "Deleted product successfully"}), 200
        return jsonify({"error": "Error deleting product"}), 404


"""Orders CRUD Operations"""


@app_views.route('/farmer/orders', methods=['GET'])
def view_all_orders():
    """Show all orders"""
    if request.method == 'GET':
        if len(request.args.keys()) == 0:
            farmer_id = request.get_json()['farmer_id']
        else:
            farmer_id = request.args.get('farmer_id')

        orders = farmer.get_all_orders(farmer_id)

        if orders is None:
            return jsonify({"error": "Could not fetch orders"}), 404
        return jsonify(orders), 200


@app_views.route('/farmer/orders/accept', methods=['POST'])
def accept_order():
    """Accept order"""
    if request.method == 'POST':
        data = request.get_json()
        farmer_id = data['farmer_id']
        order_id = data['order_id']
        accepted_order = farmer.accept_order(farmer_id, order_id)
        if accepted_order:
            return jsonify({"status": "Order accepted"}), 200
        return jsonify({"error": "Error accepting order"}), 404


@app_views.route('/farmer/orders/deliver', methods=['POST'])
def deliver_order():
    """deliver order"""
    if request.method == 'POST':
        data = request.get_json()
        farmer_id = data['farmer_id']
        order_id = data['order_id']
        print(farmer_id)
        print(order_id)
        delivered_order = farmer.deliver_order(farmer_id, order_id)
        if delivered_order:
            return jsonify({"status": "Order delivered"}), 200
        return jsonify({"error": "Error delivering order"}), 404


@app_views.route('/farmer/orders/decline', methods=['POST'])
def decline_order():
    """decline order"""
    if request.method == 'POST':
        data = request.get_json()
        farmer_id = data['farmer_id']
        order_id = data['order_id']

        declined_order = farmer.decline_order(farmer_id, order_id)
        if declined_order:
            return jsonify({"status": "Order declined"}), 200
        return jsonify({"error": "Error declining order"}), 404
