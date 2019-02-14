import os
import sys
import requests
from flask import render_template
from app import create_app


# Port variable to run the server on. Taken from docker.
PORT = os.environ.get('PORT')

app = create_app()


@app.route('/')
@app.route('/index')
def index():
    """ serve static index file """
    return render_template('index.html',
                           title='Placeholder',
                           body='Placeholder')


if __name__ == '__main__':
    app.logger.info('running environment: %s', os.environ.get('ENV'))
    # Debug mode if development env
    debugVal = os.environ.get('ENV') == 'development'
    app.run(host='0.0.0.0', port=int(PORT), debug=debugVal)  # Run the app