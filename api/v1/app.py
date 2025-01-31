#!/usr/bin/python3
""" Our HBnB app using api interfacing"""
from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def tearDowm(exception):
    """ close the storage engine"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Return errmsg `Not Found`."""
    response = {'error': 'Not found'}
    return jsonify(response), 404


if __name__ == "__main__":
    if os.getenv("HBNB_API_HOST") is None:
        HBNB_API_HOST = "0.0.0.0"
    else:
        HBNB_API_HOST = os.getenv("HBNB_API_HOST")
    if os.getenv("HBNB_API_PORT") is None:
        HBNB_API_PORT = "5000"
    else:
        HBNB_API_PORT = os.getenv("HBNB_API_PORT")
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
