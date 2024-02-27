#!/usr/bin/python3
"""Module that handles Users"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET", "POST"])
def all_users():
    """Retrieves all users or posts a new user"""

    if request.method == "GET":
        users = storage.all(User).values()
        user_list = [user.to_dict() for user in users]
        return jsonify(user_list)
    else:
        params = request.get_json()
        if params is None:
            abort(400, "Not a JSON")
        if params.get("email") is None:
            abort(400, "Missing name")
        if params.get("password") is None:
            abort(400, "Missing password")

        new_user = User(**(params))
        new_user.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=["GET", "DELETE", "PUT"])
def user_getter(user_id):
    """Gets, deletes or updates a user by its id"""

    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if request.method == "GET":
        return jsonify(user.to_dict())
    elif request.method == "DELETE":
        storage.delete(user)
        storage.save()
        return {}, 200
    else:
        update_dict = request.get_json()
        if update_dict is None:
            abort(404, "Not a JSON")
        else:
            ignored_keys = ["id", "email", "created_at", "updated_at"]

            for key, value in update_dict.items():
                if key not in ignored_keys:
                    setattr(user, key, value)
            user.save()
            return jsonify(user.to_dict()), 200
