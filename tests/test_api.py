import unittest
import json
import re
from base64 import b64encode
from flask import url_for
from app import create_app, db
from app.models.user import User
from app.models.role import Role
from app.models.post import Post
from app.models.comment import Comment


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context().push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self, username, password):
        return {
            'Authorization': 'Basic ' + b64encode(
                (username + ':' + password).encode()).decode(),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_token_auth(self):
        r = Role.query.filter_by(name='User').first()
        u = User(email='testtest@bora.com', password='testtest', confirmed=True, role=r)
        db.session.add(u)
        db.session.commit()

        response = self.client.get(url_for('api.get_posts'), headers=self.get_api_headers('bad-token', ''))
        self.assertTrue(response.status_code == 401)

        response = self.client.get(url_for('api.get_token'), headers=self.get_api_headers('testtest@bora.com', 'testtest'))
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(response.data.decode())
        self.assertIsNotNone(json_response.get('token'))
        token = json_response['token']

        response = self.client.get(url_for('api.get_post'), headers=self.get_api_headers(token, ''))
        self.assertTrue(response.status_code == 200)