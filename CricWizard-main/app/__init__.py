import os
from typing import Mapping, Any

from flask import Flask
from flask_assets import Bundle, Environment

from . import main


def create_app(test_config: Mapping[str, Any] | None = None) -> Flask:
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # bundle and add assets to flask app
    assets = Environment(app)
    css = Bundle("src/input.css", output="dist/output.css")

    assets.register("css", css)
    css.build()

    # register the blueprint from the factory
    app.register_blueprint(main.bp)

    return app
