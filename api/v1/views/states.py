#!/usr/bin/python3
"""state"""
from api.v1.views import app_views
from models.state import State
from flask import jsonify, abort, request, make_response
from models import storage


@app_views.route('/states', methods=['GET'])
def getList():
    """Retrieves the list of all State objects"""
    state_list = [obj.to_dict() for obj in storage.all("State").values()]
    return jsonify(state_list)

@app_views.route('/states/<state_id>', methods=['GET'])
def get(state_id):
    """Retrieves a State object"""
    obj = storage.get(State, state_id)
    if obj:
        return jsonify(obj.to_dict())
    else:
        abort(404)

@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete(state_id):
    """Deletes a State object"""
    obj = storage.get(State, state_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), '200'
        #return jsonify(obj.to_dict())
    abort(404)

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create():
    """Creates a State"""
    if not request.get_json():
        abort(404, 'Not a JSON')
    if 'name' not in request.get_json():
        return abort(400, 'Missing name')
    newState = State(name=request.json['name'])
    storage.new(newState)
    storage.save()
    return jsonify(newState.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'])
def update(state_id):
    """Updates a State"""
    obj = storage.get(State, state_id)
    if obj is not None:
        if not request.get_json():
            abort('404', 'Not a JSON')
        obj.name = request.json['name']
        storage.save()
        return jsonify(obj.to_dict()), '200'
    abort(404)
