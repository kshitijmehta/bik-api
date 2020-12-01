from jsonschema import validate
from jsonschema.exceptions import ValidationError

shipment_schema = {
    "type": "object",
    "properties": {
        "shipmentId": {
            "type": ["string", "integer"],
        },
        "shipper": {
            "type": "string",
        },
        "trackingNumber": {
            "type": "string"
        },
        "shippingDate": {
            "type": ["string", "null"]
        },
        "deliveryDate": {
            "type": ["string", "null"]
        },
        "returnStatus": {
            "type": "string"
        },
        "paymentReturned": {
            "type": "string"
        },
        "orderDetailId": {
            "type": "integer"
        },
        "deleteFlag": {
            "type": "boolean"
        }
    }
}


def validate_shipment(data):
    try:
        validate(data, shipment_schema)
    except ValidationError as e:
        return {"isValid": False}
    return {"isValid": True}