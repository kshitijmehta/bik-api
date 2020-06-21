from jsonschema import validate
from jsonschema.exceptions import ValidationError

user_schema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "format": "email"
        },
        "phone_number": {
            "type": "string",
            "length": 10
        },
        "password": {
            "type": "string"
        }
    },
    "required": ["email", "phone_number", "password"]
}


def validate_user(data):
    try:
        validate(data, user_schema)
    except ValidationError as e:
        return {"isValid": False}
    return {"isValid": True}
