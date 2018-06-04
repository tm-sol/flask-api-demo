import unittest
import flask
from app import app
import json


class TestPostersApi(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_check_poster_path(self):
        with app.test_request_context('/posters'):
            assert flask.request.path == '/posters'

    def test_get_posters(self):
        app.test_client()
        response = self.app.get('/poster')
        json_resp = json.loads(response.data.decode('utf-8'))
        self.assertTrue(len(json_resp[1]) == 2)

    def test_get_poster_by_name(self):
        app.test_client()
        response = self.app.get('/poster/'+"James")
        json_resp = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_resp[1]['name'] == 'James')


if __name__ == '__main__':
    unittest.main()

