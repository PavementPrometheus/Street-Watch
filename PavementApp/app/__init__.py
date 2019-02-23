import os
import json
import datetime

from bson.objectid import ObjectId
from flask import Flask, jsonify, make_response
from flask_pymongo import PyMongo


class JSONTimeIDEncoder(json.JSONEncoder):
    """ extends json-encoder class """

    # Will give a false positive from pylint since we are overriding "default"
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, datetime.datetime):
            return str(o)
        else:
            return json.JSONEncoder.default(self, o)

mongo = PyMongo()


# Since the data will primarily be accessed by a machine,
# responses will be in json form.
# TODO: This should most likely be pulled into its own file
def bad_request(error):
    """ 400 error handler """
    return make_response(jsonify({'error': 'Bad Request'}), 400)


def page_not_found(error):
    """ 404 error handler """
    return make_response(jsonify({'error': 'Not found'}), 404)


def create_app():
    """ Creates a Flask app instance

    Creates the app and loads it with the pavement controllers as
    well as loading the app with the mongodb database instance taken 
    from the local environment. This comes from the docker settings.

    Args:
        none

    Returns:
        A flask app using the pavement controllers for a restful API
        interface.  

    Raises:
        none
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
    from app.pavement.controllers import pavementAPI
    app.register_blueprint(pavementAPI)

    # Resister error handlers
    app.register_error_handler(400, bad_request)
    app.register_error_handler(404, page_not_found)

    # Initialize the database
    mongo.init_app(app)

    return app
