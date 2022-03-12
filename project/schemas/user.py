from marshmallow import fields, Schema


class UserSchema(Schema):
    id = fields.Int(required=True, dump_only=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    name = fields.Str()
    surname = fields.Str()
    favorite_genre = fields.Str()