import json

from flask import Flask
import pytest

from flask_classy_swagger import schema, swaggerify


TITLE = 'MyTestAPI'
VERSION = '0.9'
BASIC_SCHEMA = {
    'info': {
        'title': TITLE,
        'version': VERSION},
    'swagger': '2.0',
    'paths': {}}


class TestSchema(object):
    def test_required_params(self):
        assert schema(TITLE, VERSION) == BASIC_SCHEMA

    def test_base_path(self):
        assert (
            schema(TITLE, VERSION, base_path='/myswagger') ==
            dict(BASIC_SCHEMA, **{'basePath': '/myswagger'}))


@pytest.fixture
def app():
    app = Flask('test')
    swaggerify(app, TITLE, VERSION)
    return app.test_client()


class TestSwaggerify(object):
    def test_empty(self, app):
        response = app.get('/swagger.json')
        assert json.loads(response.data) == BASIC_SCHEMA
