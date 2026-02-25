

from flask import Blueprint, request
from flasgger import swag_from

from app.controllers.user_controller import UserController
from app.utils import token_required, role_required

# Create blueprint
user_bp = Blueprint("user", __name__)


# POST /api/v1/users
@user_bp.route("", methods=["POST"])
@token_required
@swag_from({
    'tags': ['User Management'],
    'summary': 'Create a new user',
    'description': 'Create a new user (Admin/HR only). HR can only create Employee users.',
    'security': [{'Bearer': []}],
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'required': ['email', 'password'],
            'properties': {
                'email': {'type': 'string', 'example': 'newuser@company.com'},
                'password': {'type': 'string', 'example': 'password123'},
                'name': {'type': 'string', 'example': 'Jane Doe'},
                'role': {'type': 'string', 'enum': ['Employee', 'HR', 'Admin'], 'example': 'Employee'},
                'join_date': {'type': 'string', 'format': 'date', 'example': '2024-01-01'},
                'status': {'type': 'string', 'enum': ['active', 'separated'], 'example': 'active'}
            }
        }
    }],
    'responses': {
        201: {'description': 'User created successfully'},
        400: {'description': 'Bad request or validation error'},
        403: {'description': 'Insufficient permissions'}
    }
})
def create_user():

    current_user_email = request.user.get("email")
    response, status_code = UserController.create_user(current_user_email)
    return response, status_code


#GET /api/v1/users
@user_bp.route("", methods=["GET"])
@token_required
@swag_from({
    'tags': ['User Management'],
    'summary': 'Get users list',
    'description': 'Get users with filtering, pagination, and sorting. Admin sees all, HR sees only Employees.',
    'security': [{'Bearer': []}],
    'parameters': [
        {'name': 'role', 'in': 'query', 'type': 'string', 'enum': ['Employee', 'HR', 'Admin'], 'description': 'Filter by role'},
        {'name': 'name', 'in': 'query', 'type': 'string', 'description': 'Filter by name (partial match)'},
        {'name': 'email', 'in': 'query', 'type': 'string', 'description': 'Filter by email (partial match)'},
        {'name': 'offset', 'in': 'query', 'type': 'integer', 'default': 0, 'description': 'Pagination offset'},
        {'name': 'limit', 'in': 'query', 'type': 'integer', 'default': 10, 'description': 'Pagination limit (max 100)'},
        {'name': 'sort_by', 'in': 'query', 'type': 'string', 'enum': ['name', 'email', 'created_at'], 'default': 'created_at'},
        {'name': 'order', 'in': 'query', 'type': 'string', 'enum': ['asc', 'desc'], 'default': 'desc'}
    ],
    'responses': {
        200: {
            'description': 'Users list retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'total': {'type': 'integer'},
                    'offset': {'type': 'integer'},
                    'limit': {'type': 'integer'},
                    'users': {'type': 'array', 'items': {'type': 'object'}}
                }
            }
        },
        403: {'description': 'Insufficient permissions'}
    }
})
def get_users():

    current_user_email = request.user.get("email")
    response, status_code = UserController.get_users(current_user_email)
    return response, status_code


#    GET /api/v1/users/<user_id>
@user_bp.route("/<int:user_id>", methods=["GET"])
@token_required
@swag_from({
    'tags': ['User Management'],
    'summary': 'Get user by ID',
    'description': 'Get user details by ID. Employees can only view their own details.',
    'security': [{'Bearer': []}],
    'parameters': [{
        'name': 'user_id',
        'in': 'path',
        'type': 'integer',
        'required': True,
        'description': 'User ID'
    }],
    'responses': {
        200: {
            'description': 'User details retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'user': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'email': {'type': 'string'},
                            'name': {'type': 'string'},
                            'role': {'type': 'string'},
                            'join_date': {'type': 'string'},
                            'status': {'type': 'string'}
                        }
                    }
                }
            }
        },
        403: {'description': 'Access denied'},
        404: {'description': 'User not found'}
    }
})
def get_user_by_id(user_id):

    current_user_email = request.user.get("email")
    
    response, status_code = UserController.get_user_by_id(
        user_id, current_user_email
    )
    return response, status_code



#    PUT /api/v1/users/<user_id>
@user_bp.route("/<int:user_id>", methods=["PUT"])
@token_required
@swag_from({
    'tags': ['User Management'],
    'summary': 'Update user',
    'description': 'Update user details. Admin can update all fields including role. HR can only update Employee users (except role).',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'User ID'
        },
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'email': {'type': 'string'},
                    'role': {'type': 'string', 'enum': ['Employee', 'HR', 'Admin']},
                    'join_date': {'type': 'string', 'format': 'date'},
                    'separation_date': {'type': 'string', 'format': 'date'},
                    'status': {'type': 'string', 'enum': ['active', 'separated']}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'User updated successfully'},
        400: {'description': 'Bad request or validation error'},
        403: {'description': 'Insufficient permissions'},
        404: {'description': 'User not found'}
    }
})
def update_user(user_id):

    current_user_email = request.user.get("email")
    response, status_code = UserController.update_user(user_id, current_user_email)
    return response, status_code




#    DELETE /api/v1/users/<user_id>
@user_bp.route("/<int:user_id>", methods=["DELETE"])
@token_required
@swag_from({
    'tags': ['User Management'],
    'summary': 'Delete user',
    'description': 'Delete user by ID (Admin only)',
    'security': [{'Bearer': []}],
    'parameters': [{
        'name': 'user_id',
        'in': 'path',
        'type': 'integer',
        'required': True,
        'description': 'User ID'
    }],
    'responses': {
        200: {'description': 'User deleted successfully'},
        400: {'description': 'Bad request'},
        403: {'description': 'Admin role required'},
        404: {'description': 'User not found'}
    }
})
def delete_user(user_id):

    current_user_email = request.user.get("email")
    response, status_code = UserController.delete_user(user_id, current_user_email)
    return response, status_code
