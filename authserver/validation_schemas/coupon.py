from jsonschema import validate
from jsonschema.exceptions import ValidationError

coupon_schema = {
    "type": "object",
    "properties": {
        "coupon_code": {
            "type": "string",
        },
        "coupon_value": {
            "type": "string"
        },
        "coupon_id": {
            "type": "integer"
        },
        "isDelete": {
            "type": "boolean"
        }
    },
    "required": ["coupon_id", "coupon_code", "coupon_value", "isDelete"]
}


def validate_coupon(data):
    try:
        validate(data, coupon_schema)
    except ValidationError as e:
        return {"isValid": False}
    return {"isValid": True}
