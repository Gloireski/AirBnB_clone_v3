#!/usr/bin/python3
"""amenity"""
from api.v1.views import app_views
from models.amenity import Amenity
from flask import jsonify, abort, request
from models import storage


@app_views.route('/amenities/', methods=['GET'], strict_slashes=False)
def getAmenityList():
    """Retrieves the list of all Amenity objects"""
    amenity_list = [obj.to_dict() for obj in storage.all("Amenity").values()]
    return jsonify(amenity_list)

@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves an Amenity object"""
    obj = storage.get(Amenity, amenity_id)
    if obj:
        return jsonify(obj.to_dict())
    else:
        abort(404)

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an Amenity object"""
    obj = storage.get(Amenity, amenity_id)
    if obj:
        #print(obj.to_dict())
        storage.delete(obj)
        storage.save()
        return jsonify({}), '200'
    abort(404)

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates an Amenity"""
    if not request.get_json():
        abort(404, 'Not a JSON')
    if 'name' not in request.get_json():
        return abort(400, 'Missing name')
    newAmenity = Amenity(name=request.json['name'])
    storage.new(newAmenity)
    storage.save()
    return jsonify(newAmenity.to_dict()), 201

@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an Amenity"""
    obj = storage.get(Amenity, amenity_id)
    if obj is not None:
        if not request.get_json():
            abort('404', 'Not a JSON')
        obj.name = request.json['name']
        storage.save()
        return jsonify(obj.to_dict()), '200'
    abort(404)
