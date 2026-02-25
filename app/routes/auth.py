

from flask import Blueprint
from flasgger import swag_from
from app.controllers import AuthController

# Create blueprint
auth_bp = Blueprint("auth", __name__)


  #  POST /api/v1/auth/login
@auth_bp.route("/login", methods=["POST"])
@swag_from({
    'tags': ['Authentication'],
    'summary': 'User login',
    'description': 'Authenticate user and receive JWT tokens',
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'required': ['email', 'password'],
            'properties': {
                'email': {'type': 'string', 'example': 'admin@company.com'},
                'password': {'type': 'string', 'example': 'password123'}
            }
        }
    }],
    'responses': {
        200: {
            'description': 'Login successful',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'access_token': {'type': 'string'},
                    'refresh_token': {'type': 'string'},
                    'user': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'email': {'type': 'string'},
                            'name': {'type': 'string'},
                            'role': {'type': 'string', 'enum': ['Employee', 'HR', 'Admin']}
                        }
                    }
                }
            }
        },
        401: {'description': 'Invalid credentials'}
    }
})
def login():

    response, status_code = AuthController.login()
    return response, status_code


#    POST /api/v1/auth/refresh
@auth_bp.route("/refresh", methods=["POST"])
@swag_from({
    'tags': ['Authentication'],
    'summary': 'Refresh access token',
    'description': 'Get a new access token using refresh token',
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'required': ['refresh_token'],
            'properties': {
                'refresh_token': {'type': 'string', 'example': 'eyJ0eXAiOiJKV1QiLCJhbGc...'}
            }
        }
    }],
    'responses': {
        200: {
            'description': 'Token refreshed successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'access_token': {'type': 'string'}
                }
            }
        },
        401: {'description': 'Invalid or expired refresh token'}
    }
})
def refresh():

    response, status_code = AuthController.refresh()
    return response, status_code
