from app import ma
from marshmallow import fields, validate, post_load
from app.models import User

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ("password_hash",)

    password = fields.String(load_only=True, required=True, validate=validate.Length(min=6))