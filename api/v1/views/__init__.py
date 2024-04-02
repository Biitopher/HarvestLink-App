#!/usr/bin/python3
""" Creates init file """
from flask import Blueprint


app_views = Blueprint('app_views', __name__, template_folder='views')
from api.v1.views.index import *
from api.v1.views.user import *
from api.v1.views.consumer import *
from api.v1.views.farmer import *