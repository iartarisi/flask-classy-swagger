from flask import jsonify


SWAGGER_VERSION = '2.0'


def schema(title, version, base_path=None):
    schema = {"swagger": SWAGGER_VERSION,
              "paths": {},
              "info": {
                  "title": title,
                  "version": version}}
    if base_path is not None:
        schema['basePath'] = base_path
    return schema


def swaggerify(app, swagger_path, title, version, base_path=None):
    @app.route(swagger_path)
    def swagger():
        return jsonify(schema(title, version, base_path))
