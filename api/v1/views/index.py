#!/usr/bin/python3
""" Index file """

from api.v1.views import app_views
from api.v1.controllers.products import Products
from flask import jsonify

products = Products()


@app_views.route('/status', methods=['GET'])
def get_status():
    """ Return status"""
    return jsonify({"status": "OK"})


@app_views.route('/products')
@app_views.route('/', methods=['GET'])
def home():
    """Display all products in the market"""
    all_products = products.list_all_products()
    return jsonify(all_products)

