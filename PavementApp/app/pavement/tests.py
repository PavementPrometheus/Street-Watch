from app.tests.test_base import BaseTest, mongo
from json import dumps

class PavementAPITests(BaseTest):

    def test_single_insert(self):
        request = dict(test='hey kids')
        response = self.client.post('/pavement', 
                                    data=dumps(request),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        documentNum = mongo.db.pavement.count_documents({})
        self.assertEqual(documentNum, 1)

    def test_multiple_insert(self):
        request = [dict(test='hey kids'), 
                   dict(test='it\'s kids')]
        response = self.client.post('/pavement', 
                                    data=dumps(request),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)
        documentNum = mongo.db.pavement.count_documents({})
        self.assertEqual(documentNum, 2)

    def test_single_base_get(self):
        request = dict(_id=12345, test='hey kids')
        mongo.db.pavement.insert_one(request)
        response = self.client.get('/pavement', 
                                   data=dumps(request),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_multiple_get(self):
        docs = [dict(same=True, test='hey kids'), 
                dict(same=True, test='it\'s kids')]
        mongo.db.pavement.insert_many(docs)
        request = dict(same=True)
        response = self.client.get('/pavement', 
                                   data=dumps(request),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        jsonData = response.get_json()
        resultsLength = len(jsonData['results'])
        self.assertEqual(resultsLength, 2)

    def test_single_base_delete(self):
        request = dict(_id=12345, test='hey kids')
        mongo.db.pavement.insert_one(request)
        response = self.client.delete('/pavement', 
                                      data=dumps(request),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_multiple_delete(self):
        docs = [dict(same=True, test='hey kids'), 
                dict(same=True, test='it\'s kids')]
        mongo.db.pavement.insert_many(docs)
        request = dict(same=True)
        response = self.client.delete('/pavement', 
                                      data=dumps(request),
                                      content_type='application/json')
        self.assertEqual(response.status_code, 200)
        documentNum = mongo.db.pavement.count_documents({})
        self.assertEqual(documentNum, 0)


    def test_single_id_get(self):
        request = dict(test='hey kids')
        record = mongo.db.pavement.insert_one(request)
        url = '/pavement/' + str(record.inserted_id)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_single_id_delete(self):
        request = dict(test='hey kids')
        record = mongo.db.pavement.insert_one(request)
        url = '/pavement/' + str(record.inserted_id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)