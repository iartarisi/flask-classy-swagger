import re
from collections import defaultdict

from flask import jsonify


SWAGGER_VERSION = '2.0'
SWAGGER_PATH = '/swagger.json'
IGNORED_RULES = ['/static', SWAGGER_PATH]


def schema(title, version, base_path=None):
    schema = {"swagger": SWAGGER_VERSION,
              "paths": {},
              "info": {
                  "title": title,
                  "version": version}}
    if base_path is not None:
        schema['basePath'] = base_path
    return schema


def resolve_method(rule):
    # trying to get over rule.methods like: set(['HEAD', 'OPTIONS', 'GET'])
    for m in rule.methods:
        if m in ['GET', 'POST', 'PUT', 'DELETE']:
            return m.lower()


def is_ignored(rule):
    # TODO app.static_url_path
    for ignored in IGNORED_RULES:
        if rule.rule.startswith(ignored):
            return True
    else:
        return False


def get_path(rule):
    # swagger spec is very clear about wanting paths to start with a slash
    assert rule.rule.startswith('/')

    if rule.rule == '/':
        return '/'

    # try to strip the end of the path which are usually parameters
    reversed = rule.rule[::-1]
    return re.sub(r'(>\w+\</)', '', reversed, count=1)[::-1].rstrip('/')


def make_tags(rule):
    return [rule.endpoint.split(":")[0]]


def get_docs(function):
    """Return (summary, description) tuple from the passed in function"""
    try:
        return re.match(
            r"""
            (.+?$) # first (summary) line, non-greedy MULTILINE $
            \n?    # maybe a newline
            \s*    # maybe indentation to the beginning of the next line
            (.*)   # maybe multiple other lines DOTALL
            """,
            function.func_doc.strip(),
            re.MULTILINE | re.DOTALL | re.VERBOSE
        ).groups()
    except AttributeError, TypeError:
        return '', ''


def generate_docs(app, title, version, base_path=None):
    paths = defaultdict(dict)
    for rule in app.url_map.iter_rules():
        if is_ignored(rule):
            continue

        path = get_path(rule)

        path_item_name = resolve_method(rule)
        func = app.view_functions[rule.endpoint]
        summary, description = get_docs(func)
        path_item_object = {
            "summary": summary,
            "description": description,
            "tags": make_tags(rule)}
        paths[path][path_item_name] = path_item_object

    docs = schema(title, version, base_path)
    docs['paths'] = paths
    return docs


def swaggerify(
        app, title, version, swagger_path=SWAGGER_PATH, base_path=None):
    @app.route(swagger_path)
    def swagger():
        docs = generate_docs(app, title, version, base_path)
        return jsonify(docs)
