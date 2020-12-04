from jsonschema import validate
from jsonschema import ValidationError

user_login = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string"
        },
        "password": {
            "type": "string"
        }
    },
    "required": ["email", "password"]
}

reset_pass = {
    "type": "object",
    "properties": {
        "email": {
            "type": "string"
        }
    },
    "required": ["email"]
}


def validate_reset_password(data):
    try:
        validate(data, reset_pass)
    except ValidationError as e:
        print(e)
        return {"isValid": False}
    return {"isValid": True}


def validate_user_login(data):
    try:
        validate(data, user_login)
    except ValidationError as e:
        print(e)
        return {"isValid": False}
    return {"isValid": True}
