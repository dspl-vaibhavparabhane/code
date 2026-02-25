from flask import Blueprint, request
from flasgger import swag_from
from app.controllers.asset_controller import AssetController
from app.utils import token_required

# Create blueprint
asset_bp = Blueprint("asset", __name__)


# POST /api/v1/assets
@asset_bp.route("", methods=["POST"])
@token_required
@swag_from({
    'tags': ['Assets'],
    'summary': 'Create a new asset',
    'security': [{'Bearer': []}],
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'required': ['asset_code', 'asset_name'],
            'properties': {
                'asset_code': {'type': 'string', 'example': 'LAPTOP-001'},
                'asset_name': {'type': 'string', 'example': 'Dell Latitude 5420'},
                'asset_type': {'type': 'string', 'example': 'Laptop'}
            }
        }
    }],
    'responses': {
        201: {'description': 'Asset created successfully'},
        400: {'description': 'Invalid input'},
        401: {'description': 'Unauthorized'}
    }
})
def create_asset():
    """Create a new asset"""
    current_user_email = request.user.get("email")
    response, status_code = AssetController.create_asset(current_user_email)
    return response, status_code


# GET /api/v1/assets
@asset_bp.route("", methods=["GET"])
@token_required
@swag_from({
    'tags': ['Assets'],
    'summary': 'Get all assets',
    'security': [{'Bearer': []}],
    'parameters': [
        {'name': 'status', 'in': 'query', 'type': 'string', 'enum': ['available', 'assigned', 'maintenance']},
        {'name': 'asset_type', 'in': 'query', 'type': 'string'},
        {'name': 'offset', 'in': 'query', 'type': 'integer', 'default': 0},
        {'name': 'limit', 'in': 'query', 'type': 'integer', 'default': 10}
    ],
    'responses': {
        200: {'description': 'List of assets'},
        401: {'description': 'Unauthorized'}
    }
})
def get_all_assets():
    """Get all assets"""
    current_user_email = request.user.get("email")
    response, status_code = AssetController.get_all_assets(current_user_email)
    return response, status_code


# PUT /api/v1/assets/<asset_id>
@asset_bp.route("/<int:asset_id>", methods=["PUT"])
@token_required
@swag_from({
    'tags': ['Assets'],
    'summary': 'Update an asset',
    'security': [{'Bearer': []}],
    'parameters': [
        {'name': 'asset_id', 'in': 'path', 'type': 'integer', 'required': True},
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'asset_name': {'type': 'string'},
                    'asset_type': {'type': 'string'},
                    'status': {'type': 'string', 'enum': ['available', 'assigned', 'maintenance']}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Asset updated successfully'},
        401: {'description': 'Unauthorized'},
        404: {'description': 'Asset not found'}
    }
})
def update_asset(asset_id):
    """Update an asset"""
    current_user_email = request.user.get("email")
    response, status_code = AssetController.update_asset(asset_id, current_user_email)
    return response, status_code


# DELETE /api/v1/assets/<asset_id>
@asset_bp.route("/<int:asset_id>", methods=["DELETE"])
@token_required
@swag_from({
    'tags': ['Assets'],
    'summary': 'Delete an asset',
    'security': [{'Bearer': []}],
    'parameters': [{'name': 'asset_id', 'in': 'path', 'type': 'integer', 'required': True}],
    'responses': {
        200: {'description': 'Asset deleted successfully'},
        401: {'description': 'Unauthorized'},
        404: {'description': 'Asset not found'}
    }
})
def delete_asset(asset_id):
    """Delete an asset"""
    current_user_email = request.user.get("email")
    response, status_code = AssetController.delete_asset(asset_id, current_user_email)
    return response, status_code


# POST /api/v1/assets/<asset_id>/assign
@asset_bp.route("/<int:asset_id>/assign", methods=["POST"])
@token_required
@swag_from({
    'tags': ['Assets'],
    'summary': 'Assign asset to employee',
    'security': [{'Bearer': []}],
    'parameters': [
        {'name': 'asset_id', 'in': 'path', 'type': 'integer', 'required': True},
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['employee_id'],
                'properties': {
                    'employee_id': {'type': 'integer', 'example': 1}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Asset assigned successfully'},
        400: {'description': 'Invalid input'},
        401: {'description': 'Unauthorized'},
        404: {'description': 'Asset or employee not found'}
    }
})
def assign_asset(asset_id):
    """Assign an asset to an employee"""
    current_user_email = request.user.get("email")
    response, status_code = AssetController.assign_asset(asset_id, current_user_email)
    return response, status_code


# POST /api/v1/assets/<asset_id>/unassign
@asset_bp.route("/<int:asset_id>/unassign", methods=["POST"])
@token_required
@swag_from({
    'tags': ['Assets'],
    'summary': 'Unassign (return) an asset',
    'security': [{'Bearer': []}],
    'parameters': [{'name': 'asset_id', 'in': 'path', 'type': 'integer', 'required': True}],
    'responses': {
        200: {'description': 'Asset unassigned successfully'},
        401: {'description': 'Unauthorized'},
        404: {'description': 'Asset not found'}
    }
})
def unassign_asset(asset_id):
    """Unassign (return) an asset"""
    current_user_email = request.user.get("email")
    response, status_code = AssetController.unassign_asset(asset_id, current_user_email)
    return response, status_code


# GET /api/v1/employees/<employee_id>/assets
@asset_bp.route("/employees/<int:employee_id>/assets", methods=["GET"])
@token_required
@swag_from({
    'tags': ['Assets'],
    'summary': 'Get assets assigned to an employee',
    'security': [{'Bearer': []}],
    'parameters': [{'name': 'employee_id', 'in': 'path', 'type': 'integer', 'required': True}],
    'responses': {
        200: {'description': 'List of assigned assets'},
        401: {'description': 'Unauthorized'},
        404: {'description': 'Employee not found'}
    }
})
def get_employee_assets(employee_id):
    """Get assets assigned to an employee"""
    current_user_email = request.user.get("email")
    response, status_code = AssetController.get_employee_assets(employee_id, current_user_email)
    return response, status_code
