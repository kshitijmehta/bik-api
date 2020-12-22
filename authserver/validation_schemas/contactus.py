from jsonschema import validate
from jsonschema.exceptions import ValidationError

contact_us_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
        },
        "email": {
            "type": "string"
        },
        "message": {
            "type": "string"
        }
    },
    "required": ["name", "email", "message"]
}


def validate_contact_us(data):
    try:
        validate(data, contact_us_schema)
    except ValidationError as e:
        return {"isValid": False}
    return {"isValid": True}
