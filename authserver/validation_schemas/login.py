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


def validate_user_login(data):
    try:
        validate(data, user_login)
    except ValidationError as e:
        print(e)
        return {"isValid": False}
    return {"isValid": True}
