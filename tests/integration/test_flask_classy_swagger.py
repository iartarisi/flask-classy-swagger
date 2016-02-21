from flask import Flask

from flask_classy import FlaskView

from flask_classy_swagger import generate_everything

from ..const import TITLE, VERSION


def swagger(resource):
    """Generate an app having this sole resource and return the swagger dict"""
    app = Flask('test')
    resource.register(app)

    return generate_everything(app, TITLE, VERSION)


class TestPaths(object):
    def test_index(self):
        class Balloons(FlaskView):
            def index(self):
                """Show all the balloons

                Detailed instructions for what to do with balloons
                """
                pass

        assert swagger(Balloons)['paths'] == {
            '/balloons': {
                'get': {
                    'summary': 'Show all the balloons',
                    'description':
                    'Detailed instructions for what to do with balloons',
                    'parameters': [],
                    'tags': ['Balloons']}}}

    def test_post_route(self):
        class Balloons(FlaskView):
            def post(self, balloon):
                """Create a new balloon

                Detailed instructions for creating a balloon
                """
                return balloon

        assert swagger(Balloons)['paths'] == {
            '/balloons/{balloon}': {
                'post': {
                    'summary': 'Create a new balloon',
                    'description':
                    'Detailed instructions for creating a balloon',
                    'parameters': [{
                        'name': "balloon",
                        'in': 'path',
                        'type': 'string',
                        'required': True}],
                    'tags': ['Balloons']}}}


class TestTags(object):
    def test_no_class_docstring(self):
        class Balloons(FlaskView):
            def index(self):
                return

        assert swagger(Balloons)['tags'] == [
            {'name': "Balloons", 'description': ""}]

    def test_simple(self):
        class Balloons(FlaskView):
            """Real Balloons"""
            def index(self):
                return

        assert swagger(Balloons)['tags'] == [
            {'name': "Balloons", 'description': "Real Balloons"}]


class TestParams(object):
    def test_index_no_params(self):
        class Balloons(FlaskView):
            def index(self):
                return []

        assert swagger(Balloons)[
            'paths']['/balloons']['get']['parameters'] == []

    def test_post_params_in_path(self):
        class Balloons(FlaskView):
            def post(self, balloon, string, color='red', helium=True):
                return balloon

        assert swagger(Balloons)[
            'paths'][
                '/balloons/{balloon}/{string}/{color}/{helium}'
            ]['post']['parameters'] == (
                [{
                    'name': "balloon",
                    'required': True,
                    'in': 'path',
                    'type': 'string',
                }, {
                    'name': "string",
                    'in': 'path',
                    'type': 'string',
                    'required': True
                }, {
                    'name': "color",
                    'in': 'path',
                    'type': 'string',
                    'required': False
                }, {
                    'name': "helium",
                    'in': 'path',
                    'type': 'string',
                    'required': False}])

    def test_put_params_extend_route_base(self):
        class Balloons(FlaskView):
            route_base = '/<int:balloon_id>/balloon'

            def put(self, balloon_id, color):
                return

        assert swagger(Balloons)['paths'][
            '/{balloon_id}/balloon/{color}'
        ]['put']['parameters'] == (
            [{
                'name': 'balloon_id',
                'in': 'path',
                'type': 'integer',
                'format': 'int32',
                'required': True},
             {
                 'name': 'color',
                 'in': 'path',
                 'type': 'string',
                 'required': True}])
