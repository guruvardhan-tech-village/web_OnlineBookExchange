"""
Authentication schemas for input validation.
"""
from marshmallow import Schema, fields, validate, ValidationError
import re


def validate_email(email):
    """Custom email validation"""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        raise ValidationError('Invalid email format')


def validate_password(password):
    """Custom password validation"""
    if len(password) < 8:
        raise ValidationError('Password must be at least 8 characters long')
    
    if not re.search(r'[A-Za-z]', password):
        raise ValidationError('Password must contain at least one letter')
    
    if not re.search(r'\d', password):
        raise ValidationError('Password must contain at least one number')


class UserRegistrationSchema(Schema):
    """Schema for user registration validation"""
    email = fields.Email(required=True, validate=validate_email)
    password = fields.Str(required=True, validate=validate_password)
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=50))


class UserLoginSchema(Schema):
    """Schema for user login validation"""
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=1))


# Create schema instances
registration_schema = UserRegistrationSchema()
login_schema = UserLoginSchema()