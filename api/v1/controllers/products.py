#!/usr/bin/python3
"""Manages and displays products alongside their images"""
from api.v1.controllers import db_storage
from models.farmers import Farmer
from models.products import Product
import re

images_list = ['maize', 'oranges', 'pineapples', 'apples', 'capsicum',
               'onions', 'raspberries', 'tomatoes', 'rice', 'watermelon',
               'melons', 'wheat', 'beef', 'cheese', 'fish', 'broiler chicken', 'kienyeji chicken', 'milk', 'eggs']
# Create a regex pattern using the keywords
pattern = re.compile('|'.join(images_list), re.IGNORECASE)


class Products:
    """Class to define product functions"""

    def list_all_products(self):
        """Lists all products"""
        products = (
            db_storage.get_session()
            .query(Product, Farmer)
            .join(Farmer, Product.farmer_id == Farmer.id)
            .all()
        )
        all_products = []

        for product, farmer in products:
            # Find the first match in the product name
            match = pattern.search(product.name)

            if match:
                image = match.group()
                product.image = image
            else:
                product.image = 'Logo'

            all_products.append({"id": product.id,
                                 "name": product.name,
                                 "category": product.category,
                                 "price": product.price,
                                 "location": product.location,
                                 "quantity": product.quantity,
                                 "farmer_id": farmer.id,
                                 "farmer": farmer.name,
                                 "product_image": product.image
                                 })
        return all_products
