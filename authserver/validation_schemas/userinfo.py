from jsonschema import validate
from jsonschema.exceptions import ValidationError

user_schema = {
    "type": "object",
    "properties": {
        "firstName": {
            "type": "string"
        },
        "lastName": {
            "type": "string",
        },
        "dob ": {
            "type": "string",
        },
        "mobile": {
            "type": "string",
            "pattern": "^((\+)(\d{1,4}[-]))(\d{10}){1}?$"
        },
        "gender": {
            "type": "string",
        },
        "addressLineOne": {
            "type": "string",
        },
        "addressLineTwo": {
            "type": "string",
        },
        "addressLineThree": {
            "type": "string",
        },
        "city": {
            "type": "string",
        },
        "state": {
            "type": "string",
        },
        "country": {
            "type": "string"
        }
    },
    "required": ["firstName", "lastName", "mobile", "addressLineOne", "city", "state", "country"]
}

discount_schema = {
    "type": "object",
    "properties": {
        "discount": {
            "type": "string"
        },
        "email": {
            "type": "string"
        },
    },
    "required": ["discount","email"]
}


def validate_user(data):
    try:
        validate(data, user_schema)
    except ValidationError as e:
        print(e)
        return {"isValid": False}
    return {"isValid": True}


def validate_user_discount(data):
    try:
        validate(data, discount_schema)
    except ValidationError as e:
        print(e)
        return {"isValid": False}
    return {"isValid": True}
