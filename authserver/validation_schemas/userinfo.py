from jsonschema import validate
from jsonschema.exceptions import ValidationError

user_schema = {
    "type": "object",
    "properties": {
        "first_name": {
            "type": "string"
        },
        "last_name": {
            "type": "string",

        },
        "address": {
            "type": "string",

        },
         "state": {
            "type": "string",
        },
        "country": {
            "type": "string"
        }
    },
    "required": ["first_name", "last_name", "address", "state", "country"]
}


def validate_user(data):
    try:
        validate(data, user_schema)
    except ValidationError as e:
        return {"isValid": False}
    return {"isValid": True}
