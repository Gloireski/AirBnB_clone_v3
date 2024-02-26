#!/usr/bin/python3
"""Module that handles Reviews"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=["GET", "POST"])
def reviews_place(place_id):
    """GET: Retrieves reviews of a place
       POST: Creates a new review in a place
    """

    place = storage.get("Review", place_id)
    if place is None:
        abort(404)

    if request.method == "GET":
        reviews = place.reviews
        reviews_list = [review.to_dict() for review in reviews]
        return jsonify(reviews_list)
    else:
        new_dict = request.get_json()
        if new_dict is None:
            abort(400, description="Not a JSON")
        if new_dict.get("user_id") is None:
            abort(400, description="Missing user_id")
        if new_dict.get("text") is None:
            abort(400, description="Missing text")

        new_review = Review(**new_dict)
        new_review.save()
        return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=["GET", "DELETE", "PUT"])
def reviews_getter(review_id):
    """Retrieves a city by its id"""

    review = storage.get("Review", review_id)
    if review is None:
        abort(404)

    if request.method == "GET":
        return jsonify(review.to_dict())
    elif request.method == "DELETE":
        review.delete()
        return {}, 200
    else:
        update_dict = request.get_json()
        if update_dict is None:
            abort(404, description="Not a JSON")
        else:
            review_dict = review.__dict__
            review.delete()
            ignored_keys = ["id", "state_id", "created_at", "updated_at"]

            for key, value in update_dict.items():
                if key in review_dict and key not in ignored_keys:
                    review.key = value
            review.save()
