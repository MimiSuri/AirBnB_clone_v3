#!/usr/bin/python3
"""
    Manage the RESTfull API for states
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/states", strict_slashes=False, methods=['GET'])
def states():
    """Display all the states saved"""
    return jsonify([state.to_dict() for state in storage.all(State).values()])


@app_views.route("/states/<state_id>", strict_slashes=False, methods=['GET'])
def get_state_id(state_id):
    """Display the state matched by id"""
    state_by_id = storage.get(State, state_id)
    if state_by_id is not None:
        return jsonify(state_by_id.to_dict())
    abort(404)


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=['DELETE'])
def delete_state_id(state_id):
    """Delete the state matched by id"""
    state_by_id = storage.get(State, state_id)
    if state_by_id is not None:
        storage.delete(state_by_id)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/states", strict_slashes=False, methods=['POST'])
def post_state():
    """Create a new state"""
    try:
        request.get_json()
    except:
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    new_state = State()
    new_state.name = request.get_json()["name"]
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", strict_slashes=False, methods=['PUT'])
def put_state_id(state_id):
    """Update a state in database"""
    state_by_id = storage.get(State, state_id)
    if state_by_id is not None:
        try:
            request.get_json()
        except:
            abort(400, 'Not a JSON')
        for attr, value in request.get_json().items():
            setattr(state_by_id, attr, value)
        storage.save()
        return jsonify(state_by_id.to_dict()), 200
    abort(404)
