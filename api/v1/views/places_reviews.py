#!/usr/bin/python3
"""Module that handles Reviews"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=["GET", "POST"])
def reviews_by_place(place_id):
    """GET: Retrieves reviews of a place
       POST: Creates a new review in a place
    """

    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if request.method == "GET":
        reviews_list = [review.to_dict() for review in place.reviews]
        return jsonify(reviews_list)
    else:
        new_dict = request.get_json()
        if not new_dict:
            abort(400, "Not a JSON")
        if new_dict.get("user_id") is None:
            abort(400, "Missing user_id")
        if new_dict.get("text") is None:
            abort(400, "Missing text")
        user = storage.get(User, new_dict['user_id'])
        if not user:
            abort(404)
        new_dict['place_id'] = place_id
        new_review = Review(**new_dict)
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=["GET", "DELETE", "PUT"])
def reviews_getter(review_id):
    """Retrieves a city by its id"""

    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if request.method == "GET":
        return jsonify(review.to_dict())
    elif request.method == "DELETE":
        storage.delete(review)
        storage.save()
        return {}, 200
    else:
        update_dict = request.get_json()
        if not update_dict:
            abort(400, "Not a JSON")
        else:
            ignored_keys = ["id", "state_id", "place_id", "created_at", "updated_at"]
            for key, value in update_dict.items():
                if key not in ignored_keys:
                    setattr(update_dict, key, value)
            review.save()
            return jsonify(review.to_dict()), 200
