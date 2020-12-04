from jsonschema import validate
from jsonschema.exceptions import ValidationError

shipper_schema = {
    "type": "object",
    "properties": {
        "shipper_name": {
            "type": "string",
        },
        "shipper_link": {
            "type": "string"
        },
        "shipper_id": {
            "type": "integer"
        },
        "delete_flag": {
            "type": "boolean"
        }
    },
    "required": ["shipper_name", "shipper_link"]
}


def validate_shipper(data):
    try:
        validate(data, shipper_schema)
    except ValidationError as e:
        return {"isValid": False}
    return {"isValid": True}