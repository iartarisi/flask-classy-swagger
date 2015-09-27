import json

from flask import Flask
from flask.ext.classy import FlaskView

import mock

from flask_classy_swagger import (
    generate_docs,
    get_path,
    schema,
    swaggerify,
)


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


class TestSwaggerify(object):
    def test_empty(self):
        app = Flask('test')
        swaggerify(app, TITLE, VERSION)
        client = app.test_client()

        response = client.get('/swagger.json')
        assert json.loads(response.data) == BASIC_SCHEMA


class TestGenerateDocs(object):
    def test_post_route(self):
        class Balloons(FlaskView):
            def post(self, foo):
                return foo

        app = Flask('test')
        Balloons.register(app)

        assert (
            generate_docs(app, TITLE, VERSION) ==
            dict(BASIC_SCHEMA,
                 **{'paths': {
                     '/balloons': {
                         'post': {
                             'tags': ['Balloons']}}}}))

    def test_index_route(self):
        class Balloons(FlaskView):
            def index(self):
                return "Oi"

        app = Flask('test')
        Balloons.register(app)

        assert (
            generate_docs(app, TITLE, VERSION) ==
            dict(BASIC_SCHEMA,
                 **{'paths': {
                     '/balloons': {
                         'get': {
                             'tags': ['Balloons']}}}}))


class TestGetPath(object):
    def test_root_path(self):
        assert _get_path('/') == '/'

    def test_simple_paths(self):
        assert _get_path('/foo/') == '/foo'
        assert _get_path('/foo.json') == '/foo.json'
        assert _get_path('/foo') == '/foo'

    def test_path_with_one_arg(self):
        assert _get_path('/foo/<bar>') == '/foo'


def _get_path(rule_rule):
    """Helper for creating a (mocked) rule object with the given `rule` attr"""
    rule = mock.Mock()
    rule.rule = rule_rule
    return get_path(rule)
