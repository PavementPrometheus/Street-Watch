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

mongo = PyMongo()

def create_app():
    """
    Flask application factory that creates app instances.
    Every time this function is called, a new application instance is created. The reason
    why an application factory is needed is because we need to use different configurations
    for running our tests.
    :return Flask object: Returns a Flask application instance
    """
    # Create the flask object. We don't have instances yet
    app = Flask(__name__, instance_relative_config=False)

    # Add the mongo url to flask config so that
    # flask_pymongo can use it to make a connection
    app.config['MONGO_URI'] = os.environ.get('DB')

    # Use the modified encoder class to handle
    # ObjectId & datetime object while jsonifying the response.
    app.json_encoder = JSONTimeIDEncoder

    # Register the blueprint controllers for the API
    from app.pavement.controllers import pavement
    app.register_blueprint(pavement)
    
    # Initialize the database
    mongo.init_app(app)

    return app
