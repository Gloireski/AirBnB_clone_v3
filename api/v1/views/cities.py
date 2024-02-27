#!/usr/bin/python3
"""Module that handles Cities"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=["GET", "POST"])
def state_cities(state_id):
    """GET: Retrieves cities in a state
       POST: Creates new city in the state
    """

    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    if request.method == "GET":
        st_cities = state.cities
        city_list = [city.to_dict() for city in st_cities]
        return jsonify(city_list)
    else:
        new_dict = request.get_json()
        if new_dict is None:
            abort(400, description="Not a JSON")
        if new_dict.get("name") is None:
            abort(400, description="Missing name")
        new_dict['state_id'] = state_id
        new_city = City(**new_dict)
        new_city.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=["GET", "DELETE", "PUT"])
def city_getter(city_id):
    """Retrieves a city by its id"""

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if request.method == "GET":
        return jsonify(city.to_dict())
    elif request.method == "DELETE":
        storage.delete(city)
        storage.save()
        return {}, 200
    else:
        update_dict = request.get_json()
        if update_dict is None:
            abort(404, description="Not a JSON")
        else:
            city_dict = city.__dict__
            city.delete()
            ignored_keys = ["id", "state_id", "created_at", "updated_at"]

            for key, value in update_dict.items():
                if key not in ignored_keys:
                    setattr(city, key, value)
            city.save()
            return jsonify(city.to_dict()), 200
