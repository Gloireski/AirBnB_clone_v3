#!/usr/bin/python3
""" Our HBnB app using api interfacing"""
from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
#app.register_blueprint(app_views)


@app.teardown_appcontext
def tearDowm(self):
    """ close the storage engine"""
    storage.close()


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
