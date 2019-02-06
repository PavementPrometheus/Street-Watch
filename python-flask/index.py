import os
import sys
import requests
from flask import jsonify, request, make_response, send_from_directory

# Change the root path for execution to the modules folder
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
os.environ.update({'ROOT_PATH': ROOT_PATH})
sys.path.append(os.path.join(ROOT_PATH, 'modules'))

# TODO: Reorder this file and make the logger tied to the app
import logger
from app import app

# Create a logger object
LOG = logger.get_root_logger(os.environ.get(
    'ROOT_LOGGER', 'root'), filename=os.path.join(ROOT_PATH, 'output.log'))

# Port variable to run the server on.
PORT = os.environ.get('PORT')


# Since the data will primarily be accessed by a machine,
#  responses will be in json form.
@app.errorhandler(404)
def page_not_found(error):
    """ error handler """
    LOG.error(error)
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/')
def index():
    """ serve static index files """
    return send_from_directory('dist', 'index.html')


@app.route('/<path:path>')
def static_proxy(path):
    """ serve static route URIs """
    file_name = path.split('/')[-1]
    dir_name = os.path.join('dist', '/'.join(path.split('/')[:-1]))
    return send_from_directory(dir_name, file_name)


if __name__ == '__main__':
    LOG.info('running environment: %s', os.environ.get('ENV'))
    # Debug mode if development env
    app.config['DEBUG'] = os.environ.get('ENV') == 'development'
    app.run(host='0.0.0.0', port=int(PORT))  # Run the app
