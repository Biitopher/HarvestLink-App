#!/usr/bin/python3
""" Index file """

from api.v1.views import app_views
from api.v1.controllers.products import Products
from api.v1.controllers.user import User
from flask import jsonify, request

user = User()


@app_views.route('/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    email = data['email']
    password = data['password']

    user_data = user.auth_user(email, password)

    if user_data is None:
        return jsonify({"error": "User not found"}), 404
    else:
        return jsonify(user_data)


@app_views.route('/signup', methods=['POST'])
def create_user():
    data = request.get_json()
    created_user = user.create_user(data)
    if created_user == "Created":
        return jsonify({"status": "User created"}), 201
    elif created_user == "Wrong account type":
        return jsonify({"error": "Wrong account type"}), 401
    else:
        return jsonify({"error": created_user}), 401
