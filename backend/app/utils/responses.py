"""
Utility functions for consistent API responses
"""
from flask import jsonify
from typing import Any, Dict, Optional, List


def success_response(data: Any = None, message: str = "Success", status_code: int = 200) -> tuple:
    """
    Create a standardized success response
    
    Args:
        data: The response data
        message: Success message
        status_code: HTTP status code
        
    Returns:
        Tuple of (response, status_code)
    """
    response = {
        'success': True,
        'message': message
    }
    
    if data is not None:
        response['data'] = data
        
    return jsonify(response), status_code


def error_response(message: str, status_code: int = 400, details: Optional[Dict] = None) -> tuple:
    """
    Create a standardized error response
    
    Args:
        message: Error message
        status_code: HTTP status code
        details: Additional error details
        
    Returns:
        Tuple of (response, status_code)
    """
    response = {
        'success': False,
        'error': get_error_type(status_code),
        'message': message
    }
    
    if details:
        response['details'] = details
        
    return jsonify(response), status_code


def validation_error_response(errors: Dict, message: str = "Validation failed") -> tuple:
    """
    Create a standardized validation error response
    
    Args:
        errors: Validation error details
        message: Error message
        
    Returns:
        Tuple of (response, status_code)
    """
    return error_response(
        message=message,
        status_code=400,
        details=errors
    )


def paginated_response(items: List, page: int, per_page: int, total: int, 
                      message: str = "Success") -> tuple:
    """
    Create a standardized paginated response
    
    Args:
        items: List of items for current page
        page: Current page number
        per_page: Items per page
        total: Total number of items
        message: Success message
        
    Returns:
        Tuple of (response, status_code)
    """
    total_pages = (total + per_page - 1) // per_page
    
    data = {
        'items': items,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
    }
    
    return success_response(data=data, message=message)


def get_error_type(status_code: int) -> str:
    """
    Get error type based on status code
    
    Args:
        status_code: HTTP status code
        
    Returns:
        Error type string
    """
    error_types = {
        400: 'Bad Request',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found',
        405: 'Method Not Allowed',
        409: 'Conflict',
        422: 'Unprocessable Entity',
        500: 'Internal Server Error'
    }
    
    return error_types.get(status_code, 'Unknown Error')


def not_found_response(resource: str = "Resource") -> tuple:
    """
    Create a standardized not found response
    
    Args:
        resource: Name of the resource that was not found
        
    Returns:
        Tuple of (response, status_code)
    """
    return error_response(
        message=f"{resource} not found",
        status_code=404
    )


def unauthorized_response(message: str = "Authentication required") -> tuple:
    """
    Create a standardized unauthorized response
    
    Args:
        message: Unauthorized message
        
    Returns:
        Tuple of (response, status_code)
    """
    return error_response(
        message=message,
        status_code=401
    )


def forbidden_response(message: str = "Access denied") -> tuple:
    """
    Create a standardized forbidden response
    
    Args:
        message: Forbidden message
        
    Returns:
        Tuple of (response, status_code)
    """
    return error_response(
        message=message,
        status_code=403
    )


def conflict_response(message: str, details: Optional[Dict] = None) -> tuple:
    """
    Create a standardized conflict response
    
    Args:
        message: Conflict message
        details: Additional conflict details
        
    Returns:
        Tuple of (response, status_code)
    """
    return error_response(
        message=message,
        status_code=409,
        details=details
    )