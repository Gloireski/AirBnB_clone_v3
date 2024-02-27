#!/usr/bin/python3
"""Place"""
from api.v1.views import app_views
from models.place import Place
from models.city import City
from flask import jsonify, abort, request
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city():
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(amenity_id):
    """Retrieves an Place object"""
    obj = storage.get(Place, place_id)
    if obj:
        return jsonify(obj.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes an Place object"""
    obj = storage.get(Place, place_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), '200'
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place():
    """Creates a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(404, 'Not a JSON')
    data = request.get_json()
    if 'name' not in data:
        return abort(400, 'Missing name')
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Updates a place"""
    obj = storage.get(Place, place_id)
    if obj is not None:
        if not request.get_json():
            abort('404', 'Not a JSON')
        obj.name = request.json['name']
        storage.save()
        return jsonify(obj.to_dict()), '200'
    abort(404)
