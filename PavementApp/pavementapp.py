import os
import sys

import requests
from flask import render_template

from app import create_app


# Port variable to run the server on. Taken from docker's env.
PORT = os.environ.get('PORT')

app = create_app()


@app.route('/')
@app.route('/index')
def index():
    """ serves static index file """
    return render_template('index.html',
                           title='Pavement Prometheus',
                           body='Group 9 - Pavement Prometheus')

def main():
    app.logger.info('running environment: %s', os.environ.get('FLASK_ENV'))
    # Debug mode if development env
    debugVal = os.environ.get('FLASK_ENV') == 'development'
    currentHost = os.environ.get('FLASK_RUN_HOST')
    app.run(host=currentHost, port=int(PORT), debug=debugVal)  # Run the app

if __name__ == '__main__':
   main()
