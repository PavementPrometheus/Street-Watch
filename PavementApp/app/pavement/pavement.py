import os
from flask import request, jsonify
from app import app, mongo
from bson.objectid import ObjectId


@app.route('/pavement', methods=['POST'])
def create_data():
    """
    Function to add documents to the database
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
                          'ids': [str(ID) for ID in record],
                          'hrefs': ["/pavement/" + str(ID) for ID in record]}
            else:
                response = 'Inserted 1 document'
                result = {'message': response,
                          'id': str(record),
                          'href': "/pavement/" + str(record)}
            code = 201
    except Exception as inst:  # TODO Sometimes catches 400 errors.
        # Error while handling user request
        result = {'error': 'Server Error ' + str(type(inst)) + ' ' + str(inst)}
        code = 500
    return jsonify(result), code


@app.route('/pavement', methods=['GET'])
def retrieve_data():
    """
    Function to query the database
    """
    # TODO: Change this to format responses like
    # multiple retrieve_document calls
    # Will return a 207
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
    except Exception as inst:  # TODO Sometimes catches 400 errors.
        # Error while handling user request
        result = {'error': 'Server Error ' + str(type(inst)) + ' ' + str(inst)}
        code = 500
    return jsonify(result), code


@app.route('/pavement/<_id>', methods=['GET'])
def retrieve_document(_id):
    """
    Function to query the database
    """
    # Default return values
    result = {'error': 'Bad Request'}
    code = 400
    try:
        # We throw a 500 error if ObjectId doesn't parse the input correctly
        document = mongo.db.pavement.find({"_id": ObjectId(_id)})
        if document.count() > 0:
            result = {'result': document[0]}
            code = 200
        else:
            # If the results from the query is empty
            response = 'Resource {} not found'.format(_id)
            result = {'error': response}
            code = 404
    except Exception as inst:  # TODO Sometimes catches 400 errors.
        # Error while handling user request
        result = {'error': 'Server Error ' + str(type(inst)) + ' ' + str(inst)}
        code = 500
    return jsonify(result), code


@app.route('/pavement', methods=['PATCH'])
def update_data():
    """
    Function to update documents in the database
    """
    # Will return a 207
    # Default return values
    result = {'error': 'Bad Request'}
    code = 400
    # TODO
    return jsonify(result), code


@app.route('/pavement/<_id>', methods=['PATCH'])
def update_document(_id):
    """
    Function to update a single document in the database
    """
    # Default return values
    result = {'error': 'Bad Request'}
    code = 400
    try:
        data = request.get_json()
        if(data is not None):
            # We throw a 500 error if ObjectId
            # doesn't parse the input correctly
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
    except Exception as inst:  # TODO Sometimes catches 400 errors.
        # Error while handling user request
        result = {'error': 'Server Error ' + str(type(inst)) + ' ' + str(inst)}
        code = 500
    return jsonify(result), code


@app.route('/pavement', methods=['DELETE'])
def delete_data():
    """
    Function to remove documents from the database
    """
    # TODO: Change this to format responses like multiple delete_document calls
    # Will return a 207
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
    except Exception as inst:  # TODO Sometimes catches 400 errors.
        # Error while handling user request
        result = {'error': 'Server Error ' + str(type(inst)) + ' ' + str(inst)}
        code = 500
    return jsonify(result), code


@app.route('/pavement/<_id>', methods=['DELETE'])
def delete_document(_id):
    """
    Function to remove a single document from the database
    """
    # Default return values
    result = {'error': 'Bad Request'}
    code = 400
    try:
        # We throw a 500 error if ObjectId doesn't parse the input correctly
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
    except Exception as inst:  # TODO Sometimes catches 400 errors.
        # Error while handling user request
        result = {'error': 'Server Error ' + str(type(inst)) + ' ' + str(inst)}
        code = 500
    return jsonify(result), code
