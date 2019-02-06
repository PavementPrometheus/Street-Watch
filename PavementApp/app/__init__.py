import os
import json
import datetime
from bson.objectid import ObjectId
from flask import Flask
from flask_pymongo import PyMongo


# Create the flask object
app = Flask(__name__)

# Add the mongo url to flask config so that
# flask_pymongo can use it to make a connection
app.config['MONGO_URI'] = os.environ.get('DB')
mongo = PyMongo(app)

from app.pavement import *
