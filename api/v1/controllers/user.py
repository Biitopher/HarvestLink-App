#!/usr/bin/python3
"""User controller definitions"""
import uuid

from api.v1.controllers import db_storage
from models.consumers import add_consumer
from models.farmers import Farmer
from web.harvestlink import authenticate_farmer, authenticate_consumer


class User:
    """Consumer class definition"""
    def auth_user(self, email, password):
        """Login consumer"""
        user_details = []
        consumer_data = authenticate_consumer(email, password)
        if consumer_data is None:
            farmer_data = authenticate_farmer(email, password)
            if farmer_data is None:
                return None
            else:
                user_details.append({
                    "user_type": "farmer",
                    "id": farmer_data.id,
                    "name": farmer_data.name,
                    "email": farmer_data.email,
                    "phone": farmer_data.phone,
                    "location": farmer_data.location
                })
        else:
            user_details.append({
                "user_type": "consumer",
                "id": consumer_data.id,
                "name": consumer_data.name,
                "email": consumer_data.email,
                "phone": consumer_data.phone,
                "location": consumer_data.location
            })

        return user_details

    def create_user(self, user_details):
        """Creates a user and saves to DB"""
        u_id = str(uuid.uuid4())
        acc = user_details['account_type']
        name = user_details['name']
        email = user_details['email']
        phone = user_details['phone']
        location = user_details['location']
        password = user_details['password']

        # Create a session to interact with the database
        session = db_storage.get_session()

        if acc == "farmer":
            # Add the farmer to the 'farmers' table
            try:
                Farmer.add_farmer(session, u_id, name, email, phone,
                                  location, password)
            except Exception as e:
                return "User already exists"
            return "Created"
        elif acc == "consumer":
            # Add the consumer to the 'consumers' table
            try:
                add_consumer(session, u_id, name, email, phone,
                             location, password)
            except Exception as e:
                return "User already exists"
            return "Created"
        else:
            return "Wrong account type"
