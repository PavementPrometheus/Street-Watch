from flask import request, jsonify, Blueprint
from bson.objectid import ObjectId
from bson.errors import InvalidId
from werkzeug.exceptions import BadRequest
from pymongo.errors import BulkWriteError

from app import mongo


pavementAPI = Blueprint('pavementAPI', __name__, url_prefix='/pavement')


@pavementAPI.route('', methods=['POST'])
def create_data():
    """ Creates a number of documents in the mongo database

    Takes user's JSON from an HTTP POST request and adds the data 
    to the database.

    Args:
        None directly, takes JSON data from the request

    Returns:
        A pair (JSON: response, Int: response code)
        which tells the user if their request was correct and tells
        the user where their data can be accessed from.

        Examples:
        ({
         "message":"Inserted 2 documents",
         "id":["507f1f77bcf86cd799439011", "507f1f77bcf86cd799439012"],
         "href":["/pavement/507f1f77bcf86cd799439011", "/pavement/507f1f77bcf86cd799439012"]
        }, 201)
        ({
         "message":"Inserted 1 document",
         "id":"507f1f77bcf86cd799439013",
         "href":"/pavement/507f1f77bcf86cd799439013"
        }, 201)

        If the user asked to put multiple documents in the database, 
        then the function does and tells the user how many were
        added.

    Raises:
        none
    """
    # Default return values
    result = {'error': 'Bad Request'}
    code = 400
    try:
        data = request.get_json()
        if(data is not None):
            record = mongo.db.pavement.insert(data)
            if isinstance(record, list):
                response = 'Inserted {} documents'.format(len(record))
                result = {'message': response,
                          'id': [str(ID) for ID in record],
                          'href': ["/pavement/" + str(ID) for ID in record]}
            else:
                response = 'Inserted 1 document'
                result = {'message': response,
                          'id': str(record),
                          'href': "/pavement/" + str(record)}
            code = 201
    except (BadRequest, BulkWriteError):
        pass
    except Exception as inst:
        # Error while handling user request
        result = {'error': 'Server Error ' + str(type(inst)) + ' ' + str(inst)}
        code = 500
    return jsonify(result), code


@pavementAPI.route('', methods=['GET'])
def retrieve_data():
    """ Queries the database for a specified kind of document

    Takes user's query from an HTTP GET request and searches the
    database for matching data. If any are found, return them to 
    the user.

    Args:
        None directly, takes query data from the request

    Returns:
        A pair (JSON: response, Int: response code)
        which tells the user if their request was correct and 
        gives the user the documents matching their query.

        Example:
        ({"results":[{_id:1, cars:3, time:7884848}, {_id:2, cars:4, time:9823492}]}, 200)

    Raises:
        none
    """
    # Default return values
    result = {'error': 'Bad Request'}
    code = 400
    try:
        query = request.args
        documents = mongo.db.pavement.find(query)
        if documents.count() > 0:
            result = {'results': list(documents)}
            code = 200
        else:
            # If the results from the query is empty
            result = {'error': 'Resources not found'}
            code = 404
    except BadRequest:
        pass
    except Exception as inst:
        # Error while handling user request
        result = {'error': 'Server Error ' + str(type(inst)) + ' ' + str(inst)}
        code = 500
    return jsonify(result), code


@pavementAPI.route('', methods=['DELETE'])
def delete_data():
    """ Removes documents in the mongo database matching a query

    Takes user's query from an HTTP DELETE request and searches the
    database for matching data. If any are found, delete them.

    Args:
        None directly, takes query data from the request

    Returns:
        A pair (JSON: response, Int: response code)
        which tells the user if their request was correct and 
        gives the user the number of deleted documents.

        Examples:
        ({"message":"Deleted 3 result(s)}, 200)
        ({"error":"Not found"}, 404)

    Raises:
        none
    """
    # Default return values
    result = {'error': 'Bad Request'}
    code = 400
    try:
        query = request.get_json()
        deleted = mongo.db.pavement.delete_many(query)
        count = deleted.deleted_count
        if count > 0:
            response = 'Deleted {} result(s)'.format(count)
            result = {'message': response}
            code = 200
        else:
            # If the results from the query is empty
            result = {'error': 'Not found'}
            code = 404
    except BadRequest:
        pass
    except Exception as inst:
        # Error while handling user request
        result = {'error': 'Server Error ' + str(type(inst)) + ' ' + str(inst)}
        code = 500
    return jsonify(result), code


@pavementAPI.route('/<_id>', methods=['GET'])
def retrieve_document(_id):
    """ Queries the database for a specified document by ID and
        returns it if found.

    Takes an object's ID from the URL where a get request is sent
    and searches the database for matching data. If it is found,
    returns it to the user.

    Args:
        None directly, takes the ID of the object from the URL

    Returns:
        A pair (JSON: response, Int: response code)
        which tells the user if their request was correct and 
        gives the user the document matching their query.

        Example:
        ({"result":{_id:1, cars:3, time:7884848}}, 200)

    Raises:
        none
    """
    # Default return values
    result = {'error': 'Bad Request'}
    code = 400
    try:
        document = mongo.db.pavement.find_one({"_id": ObjectId(_id)})
        if document is not None:
            result = {'result': document}
            code = 200
        else:
            # If the results from the query is empty
            response = 'Resource {} not found'.format(_id)
            result = {'error': response}
            code = 404
    except BadRequest:
        pass
    except InvalidId:
        # Ill formed object id
        response = 'Resource {} not found'.format(_id)
        result = {'error': response}
        code = 404
    except Exception as inst:
        # Error while handling user request
        result = {'error': 'Server Error ' + str(type(inst)) + ' ' + str(inst)}
        code = 500
    return jsonify(result), code


@pavementAPI.route('/<_id>', methods=['PATCH'])
def update_document(_id):
    """ Queries the database for a specified document by ID and 
        updates it if found.

    Takes an object's ID from the URL where a get request is sent
    and searches the database for matching data. If it is found,
    update the internal data for that object based off of the 
    user's JSON sent in the request.

    Args:
        None directly, takes the ID of the object from the URL
                       also takes JSON from the request

    Returns:
        A pair (JSON: response, Int: response code)
        which tells the user if their request was correct and 
        if the document is updated, tells the user where their 
        data can be accessed from. 

        Example:
        ({
         "id":"507f1f77bcf86cd799439013",
         "href":"/pavement/507f1f77bcf86cd799439013"
        }, 200)

    Raises:
        none
    """
    # Default return values
    result = {'error': 'Bad Request'}
    code = 400
    try:
        data = request.get_json()
        if(data is not None):
            updated = mongo.db.pavement.update_one({"_id": ObjectId(_id)},
                                                   data)
            if updated.modified_count > 0:
                result = {'id': str(_id),
                          'href': "/pavement/" + str(_id)}
                code = 200
            else:
                # If the results from the query is empty
                response = 'Resource {} not found'.format(_id)
                result = {'error': response}
                code = 404
    except BadRequest:
        pass
    except InvalidId:
        # Ill formed object id
        response = 'Resource {} not found'.format(_id)
        result = {'error': response}
        code = 404
    except Exception as inst:
        # Error while handling user request
        result = {'error': 'Server Error ' + str(type(inst)) + ' ' + str(inst)}
        code = 500
    return jsonify(result), code


@pavementAPI.route('/<_id>', methods=['DELETE'])
def delete_document(_id):
    """ Queries the database for a specified document by ID and
        removes it if found.

    Takes an object's ID from the URL where a get request is sent
    and searches the database for matching data. If it is found,
    deletes the object.

    Args:
        None directly, takes the ID of the object from the URL

    Returns:
        A pair (JSON: response, Int: response code)
        which tells the user if their request was correct and 
        tells the user the ID of the deleted object.

        Example:
        ({
         "message":"Deleted _id: 507f1f77bcf86cd799439013"
        },200)

    Raises:
        none
    """
    # Default return values
    result = {'error': 'Bad Request'}
    code = 400
    try:
        deleted = mongo.db.pavement.delete_one({"_id": ObjectId(_id)})
        if deleted.deleted_count > 0:
            response = 'Deleted _id: {}'.format(_id)
            result = {'message': response}
            code = 200
        else:
            # If the results from the query is empty
            response = 'Resource {} not found'.format(_id)
            result = {'error': response}
            code = 404
    except BadRequest:
        pass
    except InvalidId:
        # Ill formed object id
        response = 'Resource {} not found'.format(_id)
        result = {'error': response}
        code = 404
    except Exception as inst:
        # Error while handling user request
        result = {'error': 'Server Error ' + str(type(inst)) + ' ' + str(inst)}
        code = 500
    return jsonify(result), code
