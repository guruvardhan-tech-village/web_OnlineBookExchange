"""
Book schemas for input validation.
"""
from marshmallow import Schema, fields, validate, ValidationError


class BookCreateSchema(Schema):
    """Schema for book creation validation"""
    title = fields.Str(required=True, validate=validate.Length(min=1, max=200))
    author = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    isbn = fields.Str(validate=validate.Length(max=20), allow_none=True)
    category = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    condition = fields.Str(
        required=True, 
        validate=validate.OneOf(['new', 'like_new', 'good', 'fair', 'poor'])
    )
    description = fields.Str(validate=validate.Length(max=1000), allow_none=True)
    image_url = fields.Str(validate=validate.Length(max=255), allow_none=True)


class BookUpdateSchema(Schema):
    """Schema for book update validation"""
    title = fields.Str(validate=validate.Length(min=1, max=200))
    author = fields.Str(validate=validate.Length(min=1, max=100))
    isbn = fields.Str(validate=validate.Length(max=20), allow_none=True)
    category = fields.Str(validate=validate.Length(min=1, max=50))
    condition = fields.Str(
        validate=validate.OneOf(['new', 'like_new', 'good', 'fair', 'poor'])
    )
    description = fields.Str(validate=validate.Length(max=1000), allow_none=True)
    image_url = fields.Str(validate=validate.Length(max=255), allow_none=True)
    available = fields.Bool()


# Create schema instances
book_create_schema = BookCreateSchema()
book_update_schema = BookUpdateSchema()