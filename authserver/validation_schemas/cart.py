from jsonschema import validate
from jsonschema.exceptions import ValidationError

order_schema = {
    "type": "object",
    "properties": {
        "user_id": {
            "type": "Integer",
            },

        "product_id": {
            "type": "Integer"
        },
        "order_price": {
            "type": "Integer"
        },
        "price_id": {
            "type": "Integer"
        },
        "order_quantity": {
            "type": "Integer"
        },
    },

    "required": ["prod_id", "orderdetail_qty",  "orderdetail_price", "price_id", "order_quantity"]
}


def validate_order(data):
    try:
        validate(data, order_schema)
    except ValidationError as e:
        return {"isValid": False}
    return {"isValid": True}
