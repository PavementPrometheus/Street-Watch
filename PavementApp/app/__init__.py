import os
import json
import datetime
from bson.objectid import ObjectId
from flask import Flask
from flask_pymongo import PyMongo


class JSONTimeIDEncoder(json.JSONEncoder):
    ''' extend json-encoder class'''

    # Will give a false positive from pylint since we are overriding "default"
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, datetime.datetime):
            return str(o)
        else:
            return json.JSONEncoder.default(self, o)

# Create the flask object
app = Flask(__name__)

# Add the mongo url to flask config so that
# flask_pymongo can use it to make a connection
app.config['MONGO_URI'] = os.environ.get('DB')
mongo = PyMongo(app)

# Use the modified encoder class to handle
# ObjectId & datetime object while jsonifying the response.
app.json_encoder = JSONTimeIDEncoder

from app.pavement import *
