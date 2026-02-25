from flask import Blueprint, request
from flasgger import swag_from
from app.controllers.conference_room_controller import ConferenceRoomController
from app.utils import token_required

conference_room_bp = Blueprint("conference_room", __name__)

@conference_room_bp.route("/", methods=["POST"])
@token_required
@swag_from({
    'tags': ['Conference Rooms'],
    'summary': 'Create a new conference room',
    'description': 'Create a new conference room (HR/Admin only)',
    'security': [{'Bearer': []}],
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'required': ['name', 'capacity', 'location'],
            'properties': {
                'name': {'type': 'string', 'example': 'Conference Room A'},
                'capacity': {'type': 'integer', 'example': 10},
                'location': {'type': 'string', 'example': 'Floor 2'}
            }
        }
    }],
    'responses': {
        201: {'description': 'Conference room created successfully'},
        400: {'description': 'Bad request or validation error'},
        403: {'description': 'Access denied. HR or Admin role required'}
    }
})
def create_room():
    current_user_email = request.user.get("email")
    return ConferenceRoomController.create_room(current_user_email)

@conference_room_bp.route("/", methods=["GET"])
@token_required
@swag_from({
    'tags': ['Conference Rooms'],
    'summary': 'Get all conference rooms',
    'description': 'Get all conference rooms with filtering, search, sorting and pagination',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'is_active',
            'in': 'query',
            'type': 'string',
            'enum': ['true', 'false'],
            'description': 'Filter by active status: true=active only, false=inactive only, empty=all'
        },
        {
            'name': 'search',
            'in': 'query',
            'type': 'string',
            'description': 'Search by room name or location'
        },
        {
            'name': 'offset',
            'in': 'query',
            'type': 'integer',
            'default': 0,
            'description': 'Pagination offset'
        },
        {
            'name': 'limit',
            'in': 'query',
            'type': 'integer',
            'default': 10,
            'description': 'Number of items per page'
        },
        {
            'name': 'sort_by',
            'in': 'query',
            'type': 'string',
            'default': 'created_at',
            'enum': ['name', 'capacity', 'created_at'],
            'description': 'Sort by field'
        },
        {
            'name': 'order',
            'in': 'query',
            'type': 'string',
            'default': 'desc',
            'enum': ['asc', 'desc'],
            'description': 'Sort order'
        }
    ],
    'responses': {
        200: {
            'description': 'Conference rooms retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'total': {'type': 'integer'},
                    'offset': {'type': 'integer'},
                    'limit': {'type': 'integer'},
                    'rooms': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'name': {'type': 'string'},
                                'capacity': {'type': 'integer'},
                                'location': {'type': 'string'},
                                'is_active': {'type': 'boolean'},
                                'created_at': {'type': 'string'}
                            }
                        }
                    }
                }
            }
        }
    }
})
def get_all_rooms():
    return ConferenceRoomController.get_all_rooms()

@conference_room_bp.route("/<int:room_id>", methods=["GET"])
@token_required
@swag_from({
    'tags': ['Conference Rooms'],
    'summary': 'Get conference room by ID',
    'description': 'Get a specific conference room',
    'security': [{'Bearer': []}],
    'parameters': [{
        'name': 'room_id',
        'in': 'path',
        'type': 'integer',
        'required': True,
        'description': 'Conference room ID'
    }],
    'responses': {
        200: {'description': 'Conference room retrieved successfully'},
        404: {'description': 'Conference room not found'}
    }
})
def get_room(room_id):
    return ConferenceRoomController.get_room(room_id)

@conference_room_bp.route("/<int:room_id>", methods=["PUT"])
@token_required
@swag_from({
    'tags': ['Conference Rooms'],
    'summary': 'Update conference room',
    'description': 'Update a conference room (HR/Admin only)',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'room_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'Conference room ID'
        },
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'capacity': {'type': 'integer'},
                    'location': {'type': 'string'},
                    'is_active': {'type': 'boolean'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Conference room updated successfully'},
        400: {'description': 'Bad request'},
        403: {'description': 'Access denied. HR or Admin role required'},
        404: {'description': 'Conference room not found'}
    }
})
def update_room(room_id):
    current_user_email = request.user.get("email")
    return ConferenceRoomController.update_room(room_id, current_user_email)

@conference_room_bp.route("/<int:room_id>", methods=["DELETE"])
@token_required
@swag_from({
    'tags': ['Conference Rooms'],
    'summary': 'Delete conference room',
    'description': 'Delete a conference room (HR/Admin only)',
    'security': [{'Bearer': []}],
    'parameters': [{
        'name': 'room_id',
        'in': 'path',
        'type': 'integer',
        'required': True,
        'description': 'Conference room ID'
    }],
    'responses': {
        200: {'description': 'Conference room deleted successfully'},
        403: {'description': 'Access denied. HR or Admin role required'},
        404: {'description': 'Conference room not found'}
    }
})
def delete_room(room_id):
    current_user_email = request.user.get("email")
    return ConferenceRoomController.delete_room(room_id, current_user_email)
