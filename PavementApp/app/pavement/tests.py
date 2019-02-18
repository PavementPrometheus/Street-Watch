from app.tests.test_base import BaseTest, mongo
from json import dumps

class PavementAPITests(BaseTest):

    def test_single_insert(self):
        request = dict(test='hey kids')
        response = self.client.post('/pavement', 
                                 data=dumps(request),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_single_get(self):
        request = dict(_id=12345, test='hey kids')
        mongo.db.pavement.insert_one(request)
        response = self.client.get('/pavement', 
                           data=dumps(request),
                           content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_single_remove(self):
        request = dict(_id=12345, test='hey kids')
        mongo.db.pavement.insert_one(request)
        response = self.client.delete('/pavement', 
                           data=dumps(request),
                           content_type='application/json')
        self.assertEqual(response.status_code, 200)