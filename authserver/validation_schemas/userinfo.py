from jsonschema import validate
from jsonschema.exceptions import ValidationError

user_schema = {
    "type": "object",
    "properties": {
        "f_name": {
            "type": "string"
        },
        "l_name": {
            "type": "string",

        },
        "gender": {
            "type": "string",

        },
         "dob ": {
            "type": "string",
        },
         "line1": {
            "type": "string",
        },
        "line2": {
            "type": "string",
        },
        "line3": {
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
    "required": ["f_name", "l_name", "gender", "DOB", "typecode" , "line1", "line2", "line3", "city", "state", "country"]
}


def validate_user(data):
    try:
        validate(data, user_schema)
    except ValidationError as e:
        return {"isValid": False}
    return {"isValid": True}
