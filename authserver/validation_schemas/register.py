from jsonschema import validate
from jsonschema.exceptions import ValidationError

user_schema = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "format": "email"
        },
        "mobile": {
            "type": "string",
            "pattern": "^((\+)(\d{1,4}[-]))(\d{10}){1}?$"
        },
        "password": {
            "type": "string"
        }
    },
    "required": ["email", "mobile", "password"]
}


def validate_user(data):
    try:
        validate(data, user_schema)
    except ValidationError as e:
        return {"isValid": False}
    return {"isValid": True}
