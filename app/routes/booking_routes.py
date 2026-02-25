from flask import Blueprint, request
from flasgger import swag_from
from app.controllers.booking_controller import BookingController
from app.utils import token_required

booking_bp = Blueprint("booking", __name__)

@booking_bp.route("/", methods=["POST"])
@token_required
@swag_from({
    'tags': ['Bookings'],
    'summary': 'Create a new booking',
    'description': 'Create a new conference room booking',
    'security': [{'Bearer': []}],
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'required': ['room_id', 'start_time', 'end_time', 'purpose'],
            'properties': {
                'room_id': {'type': 'integer', 'example': 8},
                'start_time': {'type': 'string', 'format': 'date-time', 'example': '2026-02-21T12:00:00'},
                'end_time': {'type': 'string', 'format': 'date-time', 'example': '2026-02-21T13:00:00'},
                'purpose': {'type': 'string', 'example': 'Team Meeting'}
            }
        }
    }],
    'responses': {
        201: {'description': 'Booking confirmed successfully'},
        400: {'description': 'Bad request or validation error'}
    }
})
def create_booking():
    current_user_email = request.user.get("email")
    return BookingController.create_booking(current_user_email)

@booking_bp.route("/my-bookings", methods=["GET"])
@token_required
@swag_from({
    'tags': ['Bookings'],
    'summary': 'Get current user bookings',
    'description': 'Get bookings for the authenticated user',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'upcoming_only',
            'in': 'query',
            'type': 'string',
            'default': 'false',
            'enum': ['true', 'false'],
            'description': 'Filter by upcoming bookings only'
        },
        {
            'name': 'status',
            'in': 'query',
            'type': 'string',
            'enum': ['confirmed', 'complete', 'cancelled'],
            'description': 'Filter by booking status'
        }
    ],
    'responses': {
        200: {
            'description': 'Bookings retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'data': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'room_id': {'type': 'integer'},
                                'room_name': {'type': 'string'},
                                'user_id': {'type': 'integer'},
                                'start_time': {'type': 'string', 'format': 'date-time'},
                                'end_time': {'type': 'string', 'format': 'date-time'},
                                'purpose': {'type': 'string'},
                                'status': {'type': 'string'},
                                'duration_minutes': {'type': 'integer'}
                            }
                        }
                    },
                    'total': {'type': 'integer'},
                    'offset': {'type': 'integer'},
                    'limit': {'type': 'integer'}
                }
            }
        },
        401: {'description': 'Unauthorized - Invalid or missing token'}
    }
})
def get_my_bookings():
    current_user_email = request.user.get("email")
    return BookingController.get_my_bookings(current_user_email)

@booking_bp.route("/all", methods=["GET"])
@token_required
@swag_from({
    'tags': ['Bookings'],
    'summary': 'Get all bookings',
    'description': 'Get all bookings (HR/Admin only). Use upcoming_only=true for upcoming, false for all. Use status parameter for completed/cancelled.',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'upcoming_only',
            'in': 'query',
            'type': 'string',
            'default': 'false',
            'enum': ['true', 'false'],
            'description': 'true = upcoming only, false = all bookings'
        },
        {
            'name': 'status',
            'in': 'query',
            'type': 'string',
            'enum': ['confirmed', 'complete', 'cancelled'],
            'description': 'Filter by status'
        }
    ],
    'responses': {
        200: {'description': 'Bookings retrieved successfully'},
        403: {'description': 'Access denied. HR or Admin role required'}
    }
})
def get_all_bookings():
    current_user_email = request.user.get("email")
    return BookingController.get_all_bookings(current_user_email)

@booking_bp.route("/<int:booking_id>/cancel", methods=["PUT"])
@token_required
@swag_from({
    'tags': ['Bookings'],
    'summary': 'Cancel a booking',
    'description': 'Cancel a confirmed booking. Only the booking owner or admin can cancel. Cannot cancel past bookings.',
    'security': [{'Bearer': []}],
    'parameters': [{
        'name': 'booking_id',
        'in': 'path',
        'type': 'integer',
        'required': True,
        'description': 'ID of the booking to cancel',
        'example': 1
    }],
    'responses': {
        200: {
            'description': 'Booking cancelled successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Booking cancelled successfully'}
                }
            }
        },
        400: {
            'description': 'Bad request - Booking already cancelled or cannot cancel past bookings',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Booking is already cancelled'}
                }
            }
        },
        403: {
            'description': 'Forbidden - You can only cancel your own bookings',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'You can only cancel your own bookings'}
                }
            }
        },
        404: {
            'description': 'Booking not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Booking not found'}
                }
            }
        },
        401: {'description': 'Unauthorized - Invalid or missing token'}
    }
})
def cancel_booking(booking_id):
    current_user_email = request.user.get("email")
    return BookingController.cancel_booking(booking_id, current_user_email)

@booking_bp.route("/availability", methods=["GET"])
@token_required
@swag_from({
    'tags': ['Bookings'],
    'summary': 'Get room availability',
    'description': 'Get room availability for a date range',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'room_id',
            'in': 'query',
            'type': 'integer',
            'required': True,
            'description': 'Conference room ID'
        },
        {
            'name': 'start_date',
            'in': 'query',
            'type': 'string',
            'format': 'date-time',
            'required': True,
            'description': 'Start date (ISO 8601 format)'
        },
        {
            'name': 'end_date',
            'in': 'query',
            'type': 'string',
            'format': 'date-time',
            'required': True,
            'description': 'End date (ISO 8601 format)'
        }
    ],
    'responses': {
        200: {'description': 'Room availability retrieved successfully'},
        400: {'description': 'Bad request'}
    }
})
def get_room_availability():
    return BookingController.get_room_availability()
