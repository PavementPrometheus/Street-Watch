from flask_testing import TestCase
from app import create_app as create_base_app
from app import mongo

class BaseTest(TestCase):

    def create_app(self):
        app = create_base_app()
        app.config['TESTING'] = True
        return app

    def setUp(self):
        mongo.db.create_collection('pavement')
        return

    def tearDown(self):
        mongo.db.drop_collection('pavement')
        return 