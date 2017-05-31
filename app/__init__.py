# -*- coding: utf-8 -*-
from flask import Flask, request, session, render_template, flash, abort
import importlib


def create_app():
    """Create an application."""
    app = Flask(__name__)
    app.config.from_object('app.settings')
    load_modules(app)
    return app


def load_modules(app):
    # start page
    from app.views.main import mod as main_blueprint

    app.register_blueprint(main_blueprint)

    # load and register enabled modules
    for mod_name in app.config['ENABLED_MODULES']:
        module = importlib.import_module('app.views.' + mod_name)
        app.register_blueprint(module.mod, url_prefix='/' + mod_name)


app = create_app()
