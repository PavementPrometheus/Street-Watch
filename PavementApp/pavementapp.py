import os
import sys
import requests
from flask import jsonify, request, make_response, render_template, send_from_directory
from app import app

# Port variable to run the server on. Taken from docker.
PORT = os.environ.get('PORT')


@app.route('/')
@app.route('/index')
def index():
    """ serve static index file """
    return render_template('index.html', 
                           title='Placeholder', 
                           body='Placeholder')


# Since the data will primarily be accessed by a machine,
#  responses will be in json form.
@app.errorhandler(404)
def page_not_found(error):
    """ error handler """
    app.logger.error(error)
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.logger.info('running environment: %s', os.environ.get('ENV'))
    # Debug mode if development env
    debugVal = os.environ.get('ENV') == 'development'
    app.run(host='0.0.0.0', port=int(PORT), debug=debugVal)  # Run the app
