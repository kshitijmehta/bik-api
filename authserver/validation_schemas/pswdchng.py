from jsonschema import validate
from jsonschema.exceptions import ValidationError

user_schema = {
    "type": "object",
    "properties": {
        "currentPassword": {
            "type": "string"
        },
        "newPassword": {
            "type": "string"
        }
    },
    "required": ["currentPassword", "newPassword"]
}


def validate_user(data):
    try:
        validate(data, user_schema)
    except ValidationError as e:
        return {"isValid": False}
    return {"isValid": True}