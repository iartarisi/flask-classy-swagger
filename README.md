# Flask Classy Swagger

[![Build Status](https://travis-ci.org/mapleoin/flask-classy-swagger.svg?branch=master)](https://travis-ci.org/mapleoin/flask-classy-swagger)

Generate [Swagger](http://swagger.io/) API representations from [Flask Classy](https://pythonhosted.org/Flask-Classy/) views.

## Quickstart

NOTE: This only works with python2 so far (mainly due to flask-classy itself only working with python2).

TODO: create python package

Put this in a file, e.g. `app.py`:

```python
from flask import Flask
from flask_classy import FlaskView
from flask_classy_swagger import swaggerify


class BaloonsView(FlaskView):
    """I love balloons"""

    def get(self, balloon_id):
        """Bloons!

        Get all your balloons here.

        """
        return balloon_id


app = Flask(__name__)
BaloonsView.register(app)
swaggerify(app, 'BalloonApp', '0.1.0', swagger_path='/swagger.json')


if __name__ == "__main__":
    app.run()
```

Run the server:

```
$ python app.py
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Curl it:

```json
$ curl http://127.0.0.1:5000/swagger.json
{
  "info": {
    "title": "BalloonApp",
    "version": "0.1.0"
  },
  "paths": {
    "/baloons/{balloon_id}": {
      "get": {
        "description": "Get all your balloons here.",
        "parameters": [
          {
            "in": "path",
            "name": "balloon_id",
            "required": true,
            "type": "string"
          }
        ],
        "summary": "Bloons!",
        "tags": [
          "BaloonsView"
        ]
      }
    }
  },
  "swagger": "2.0",
  "tags": [
    {
      "description": "I love balloons",
      "name": "BaloonsView"
    }
  ]
}
```

## Testing

```
$ pip install --requirement requirements-dev.txt
$ py.test tests
```

## License

Copyright (c) 2015-2016, Ionuț Arțăriși

Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE
