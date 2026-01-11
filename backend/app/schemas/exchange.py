"""
Exchange request schemas for input validation.
"""
from marshmallow import Schema, fields, validate


class ExchangeRequestCreateSchema(Schema):
    """Schema for exchange request creation validation"""
    book_id = fields.Int(required=True, validate=validate.Range(min=1))
    message = fields.Str(validate=validate.Length(max=1000), allow_none=True)


class ExchangeRequestUpdateSchema(Schema):
    """Schema for exchange request status update validation"""
    status = fields.Str(
        required=True,
        validate=validate.OneOf(['approved', 'rejected', 'completed'])
    )
    message = fields.Str(validate=validate.Length(max=1000), allow_none=True)


# Create schema instances
exchange_create_schema = ExchangeRequestCreateSchema()
exchange_update_schema = ExchangeRequestUpdateSchema()