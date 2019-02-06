import os
import sys
import requests
from flask import jsonify, request, make_response, send_from_directory
from app import app

# Port variable to run the server on. Taken from docker.
PORT = os.environ.get('PORT')


@app.route('/')
def index():
    """ serve static index file """
    folder = os.path.join('modules', 'app', 'dist')
    return send_from_directory(folder, 'index.html')


# Since the data will primarily be accessed by a machine,
#  responses will be in json form.
@app.errorhandler(404)
def page_not_found(error):
    """ error handler """
    LOG.error(error)
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/<path:path>')
def static_proxy(path):
    """ serve static route URIs """
    folder = os.path.join('modules', 'app', 'dist')
    fileName = path.split('/')[-1]
    dirName = os.path.join(folder, '/'.join(path.split('/')[:-1]))
    return send_from_directory(dir_name, file_name)


if __name__ == '__main__':
    app.logger.info('running environment: %s', os.environ.get('ENV'))
    # Debug mode if development env
    app.config['DEBUG'] = os.environ.get('ENV') == 'development'
    app.run(host='0.0.0.0', port=int(PORT))  # Run the app
