from jsonschema import validate
from jsonschema.exceptions import ValidationError

Product_size_schema = {
    "type": "object",
    "properties": {
        "product_size": {
            "type": "string"
        },
        "product_size_code": {
            "type": "string",

        },
        "product_category": {
            "type": "integer",

        },

    },
    "required": ["product_size", "product_size_code", "product_category"
                 ]
}
Product_color_schema = {
    "type": "object",
    "properties": {
        "product_color_code": {
            "type": "string",
        },
        "product_color": {
            "type": "string",
        },

    },
    "required": ["product_color_code", "product_color"]
}
Product_schema = {
    "type": "object",
    "properties": {
        "product_INR_price": {
            "type": "integer",
        },
        "product_size_code": {
            "type": "integer",
        },
        "product_color_code": {
            "type": "integer",
        },
        "product_USD_price": {
            "type": "integer",
        },
        "product_Qty": {
            "type": "integer",
        },
        "product_image_id": {
            "type": "string"
        },
        "product_image_path": {
            "type": "string"
        },
        "product_image_name": {
            "type": "string"
        },

    },
    "required": ["product_desc", "product_INR_price",
                 "product_USD_price", "product_Qty", "product_image_id", "product_image_path",
                 "product_image_name", "product_size_code", "product_color_code"]
}
Product_subcategory_schema = {
    "type": "object",
    "properties": {
        "product_category_id": {
            "type": "string"
        },
        "product_name": {
            "type": "string",

        },
        "product_desc": {
            "type": "string",

        },

    },
    "required": ["product_category_id", "product_name", "product_desc"
                 ]
}


def validate_Product_size(data):
    try:
        validate(data, Product_size_schema)
    except ValidationError as e:
        return {"isValid": False}
    return {"isValid": True}


def validate_Product_colour(data):
    try:
        validate(data, Product_color_schema)
    except ValidationError as e:
        return {"isValid": False}
    return {"isValid": True}


def validate_Product(data):
    try:
        validate(data, Product_schema)
    except ValidationError as e:
        return {"isValid": False}
    return {"isValid": True}


def validate_Product_subcategory(data):
    try:
        validate(data, Product_subcategory_schema)
    except ValidationError as e:
        return {"isValid": False}
    return {"isValid": True}
