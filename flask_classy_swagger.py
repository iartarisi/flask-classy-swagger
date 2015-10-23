import re
from collections import defaultdict

from flask import jsonify

from flask_classy import FlaskView


SWAGGER_VERSION = '2.0'
SWAGGER_PATH = '/swagger.json'
IGNORED_RULES = ['/static', SWAGGER_PATH]


def schema(title, version, base_path=None):
    schema = {"swagger": SWAGGER_VERSION,
              "paths": {},
              "tags": [],
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


def get_tag(rule):
    return rule.endpoint.split(":")[0]


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
    except (AttributeError, TypeError):
        return '', ''


def get_flask_classy_class(method):
    # XXX might not work on python3
    if method.func_closure is None:
        return

    for cell in method.func_closure:
        try:
            if issubclass(cell.cell_contents.im_class, FlaskView):
                return cell.cell_contents.im_class
        except AttributeError:
            pass
    else:
        return


def get_tag_description(func):
    klass = get_flask_classy_class(func)
    if klass:
        return klass.__doc__ or ''


def get_parameters(func):
    return []


def generate_everything(app, title, version, base_path=None):
    """Build the whole swagger JSON tree for this app"""
    paths = defaultdict(dict)
    tags = dict()
    for rule in app.url_map.iter_rules():
        if is_ignored(rule):
            continue

        path = get_path(rule)

        path_item_name = resolve_method(rule)
        func = app.view_functions[rule.endpoint]
        summary, description = get_docs(func)
        parameters = get_parameters(func)

        tag = get_tag(rule)
        if tag not in tags:
            tags[tag] = get_tag_description(func)

        path_item_object = {
            "summary": summary,
            "description": description,
            "tags": [tag],
            "parameters": parameters
        }
        paths[path][path_item_name] = path_item_object

    docs = schema(title, version, base_path)
    docs['paths'] = paths
    docs['tags'] = [{'name': k, 'description': v}
                    for k, v in tags.items()]
    return docs


def swaggerify(
        app, title, version, swagger_path=SWAGGER_PATH, base_path=None):
    @app.route(swagger_path)
    def swagger():
        docs = generate_everything(app, title, version, base_path)
        return jsonify(docs)
