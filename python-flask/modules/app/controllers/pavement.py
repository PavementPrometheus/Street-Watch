import os
from flask import request, jsonify
from app import app, mongo
from bson.objectid import ObjectId
import logger

ROOT_PATH = os.environ.get('ROOT_PATH')
LOG = logger.get_root_logger(
    __name__, filename=os.path.join(ROOT_PATH, 'output.log'))


@app.route('/pavement', methods=['POST'])
def create_data():
    """
    Function to add documents to the database
    """
    # Default return values
    result = {'error': 'Bad Request'}
    code   = 400
    try:
        data   = request.get_json()
        if(data is not None):
            record = mongo.db.pavement.insert(data)
            if isinstance(record, list):
                response = 'Inserted {} documents'.format(len(record))
                result = {'message': response, 'ids': [str(ID) for ID in record],
                 'hrefs': ["/pavement/" + str(ID) for ID in record]}
            else:
                response = 'Inserted 1 document'
                result = {'id': str(record)}
            code   = 201
    except:
        # Error while handling user request
        result = {'error': 'Server Error'}
        code   = 500
    return jsonify(result), code

@app.route('/pavement', methods=['GET'])
def retrieve_data():
    """
    Function to query the database
    """
    # Default return values
    result = {'error': 'Bad Request'}
    code   = 400
    try:
        query     = request.args
        documents = mongo.db.pavement.find(query)
        if documents.count() > 0:
            result = {'results': list(documents)}
            code   = 200
        else:
            # If the results from the query is empty
            result = {'error': 'Not found'}
            code   = 404
    except:
        # Error while handling user request
        result = {'error': 'Server Error'}
        code   = 500
    return jsonify(result), code

@app.route('/pavement/<_id>', methods=['GET'])
def retrieve_document(_id):
    """
    Function to query the database
    """
    # Default return values
    result = {'error': 'Bad Request'}
    code   = 400
    try:
        # We throw a 500 error if ObjectId doesn't parse the input correctly
        document = mongo.db.pavement.find({"_id": ObjectId(_id)})
        if document.count() > 0:
            result = {'result': document[0]}
            code   = 200
        else:
            # If the results from the query is empty
            result = {'error': 'Not found'}
            code   = 404
    except:
        # Error while handling user request
        result = {'error': 'Server Error'}
        code   = 500
    return jsonify(result), code

@app.route('/pavement', methods=['PATCH'])
def update_data():
    """
    Function to update documents in the database
    """
    # Default return values
    result = {'error': 'Bad Request'}
    code   = 400
    # TODO
    return jsonify(result), code

@app.route('/pavement/<_id>', methods=['PATCH'])
def update_document(_id):
    """
    Function to update a single document in the database
    """
    # Default return values
    result = {'error': 'Bad Request'}
    code   = 400
    try:
        data = request.get_json()
        if(data is not None):
            # We throw a 500 error if ObjectId doesn't parse the input correctly
            updated = mongo.db.pavement.update_one({"_id": ObjectId(_id)}, data)
            if updated.modified_count > 0:
                response = 'Updated _id: {}'.format(_id)
                result   = {'message': response}
                code     = 200
            else:
                # If the results from the query is empty
                result = {'error': 'Not found'}
                code   = 404
    except:
        # Error while handling user request
        result = {'error': 'Server Error'}
        code   = 500
    return jsonify(result), code

@app.route('/pavement', methods=['DELETE'])
def delete_data():
    """
    Function to remove documents from the database
    """
    # Default return values
    result = {'error': 'Bad Request'}
    code   = 400
    try:
        query    = request.get_json()
        deleted  = mongo.db.pavement.delete_many(query)
        count    = deleted.deleted_count
        if count > 0:
            response = 'Deleted {} result(s)'.format(count)
            result   = {'message': response}
            code     = 200
        else:
            # If the results from the query is empty
            result = {'error': 'Not found'}
            code   = 404
    except:
        # Error while handling user request
        result = {'error': 'Server Error'}
        code   = 500
    return jsonify(result), code

@app.route('/pavement/<_id>', methods=['DELETE'])
def remove_document(_id):
    """
    Function to remove a single document from the database
    """
    # Default return values
    result = {'error': 'Bad Request'}
    code   = 400
    try:
        deleted  = mongo.db.pavement.delete_one({"_id": ObjectId(_id)})
        if deleted.deleted_count > 0:
            response = 'Deleted _id: {}'.format(_id)
            result   = {'message': response}
            code     = 200
        else:
            # If the results from the query is empty
            result = {'error': 'Not found'}
            code   = 404
    except:
        # Error while handling user request
        result = {'error': 'Server Error'}
        code   = 500
    return jsonify(result), code
