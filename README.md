# Flask Classy Swagger

Generate [Swagger](http://swagger.io/) API representations from [Flask Classy](https://pythonhosted.org/Flask-Classy/) views.

## Quickstart

NOTE: This only works with python2 so far (mainly due to flask-classy itself only working with python2).

TODO: create python package

```python
from flask import Flask
from flask.ext.classy import FlaskView
from flask_classy_swagger import generate_docs

class BaloonsView(FlaskView):
    def index(self):
        return ['b1, 'b2']


app = Flask(__name__)
BaloonsView.register(app)
swaggerify(app, 'MyApp', '0.1.0', swagger_path='/swagger.json')
```


## Testing

```
$ pip install -requirement requirements-dev.txt
$ py.test tests
```

## License

Copyright (c) 2015-2016, Ionuț Arțăriși

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE
