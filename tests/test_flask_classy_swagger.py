from flask_classy_swagger import schema


class TestSchema(object):
    def test_required_params(self):
        assert schema('MyAPI', '1.0') == {
            'info': {
                'title': 'MyAPI',
                'version': '1.0'},
            'swagger': '2.0',
            'paths': {}}

    def test_base_path(self):
        assert schema('MyAPI', '1.0', base_path='/myswagger') == {
            'info': {
                'title': 'MyAPI',
                'version': '1.0'},
            'swagger': '2.0',
            'paths': {},
            'basePath': '/myswagger'}
