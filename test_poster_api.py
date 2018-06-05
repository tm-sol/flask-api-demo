import unittest
import flask
from pymongo import MongoClient
import app as webapp
from app import app
import json


class TestPostersApi(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.TESTING = True

        # Inject test database into application
        db = MongoClient('localhost', 27017).TestDB

        # Drop collection (faster than dropping entire db)
        if 'FirstCollection' in db.collection_names():
            db.drop_collection('FirstCollection')
        webapp.db = db

        new_posters = [{"name": "James", "url": "my_url"}, {"name": "James", "url": "my_url"}]
        webapp.db.FirstCollection.insert_many(new_posters)

    def tearDown(self):
        webapp.db.drop_collection('FirstCollection')

    def test_check_poster_path(self):
        with app.test_request_context('/posters'):
            assert flask.request.path == '/posters'

    def test_get_posters(self):
        app.test_client()
        response = self.app.get('/poster')
        json_resp = json.loads(response.data.decode('utf-8'))
        self.assertTrue(len(json_resp[1]) == 2)

    def test_add_poster(self):
        app.test_client()
        response = self.app.post('/poster', json={"name": "test", "url": "my_url"})
        json_resp = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_resp[1]['name'] == 'test')
        self.assertTrue(json_resp[1]['url'] == 'my_url')

    def test_get_poster_by_name(self):
        app.test_client()
        response = self.app.get('/poster/{}'.format("James"))
        json_resp = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_resp[1]['name'] == 'James')


if __name__ == '__main__':
    unittest.main()

