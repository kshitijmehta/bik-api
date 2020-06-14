from jsonschema import validate
from jsonschema.exceptions import ValidationError

user_schema = {
    "type": "object",
    "properties": {
        "username": {
            "type": "string"
        },
        "email": {
            "type": "string",
            "format": "email"
        },
        "phone_number": {
            "type": "number",
            "pattern": "[0-9]{10}"
        },
        "password": {
            "type": "string"
        }
    },
    "required": ["username", "email", "phone_number", "password"]
}


def validate_user(data):
    try:
        validate(data, user_schema)
    except ValidationError as e:
        return {"isValid": False}
    return {"isValid": True}
