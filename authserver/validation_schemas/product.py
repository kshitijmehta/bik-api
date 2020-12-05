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
    "required": ["product_size", "product_size_code", "product_category"]
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
            "type": "string",
        },
        "product_USD_price": {
            "type": "string",
        },
        "product_name": {
            "type": "string"
        },
        "product_desc": {
            "type": "string"
        },
        "product_subcategory_id": {
            "type": "string"
        },
        "size_colour_quantity_combo": {
            "type": "string"
        }

    },
    "required": ["product_INR_price", "product_USD_price", "size_colour_quantity_combo",
                 "product_desc", "product_name", "product_subcategory_id"]
}
Product_subcategory_schema = {
    "type": "object",
    "properties": {
        "product_category_id": {
            "type": "integer",
        },
        "product_name": {
            "type": "string",
        },
        "product_desc": {
            "type": "string",
        },
        "subcategory_id": {
            "type": "string",
        }

    },
    "required": ["product_category_id", "product_name", "product_desc","subcategory_id"]
}

returns_schema = {
    "type": "object",
    "properties": {
        "order_detail_id": {
            "type": "integer",
            },

        "return_status": {
            "type": "string"
            },

        "payment_status": {
            "type": "string"
            },

    },
    "required": ["order_detail_id"]
}

customer_return_schema = {
    "type": "object",
    "properties": {
        "orderDetailsId": {
            "type": "integer",
            },

        "returnReason": {
            "type": "string"
            },
        "orderNumber": {
            "type": "string",
            },
        "productName": {
            "type": "string"
            },
        "userName": {
            "type": "string"
            }
    },
    "required": ["orderDetailsId", "returnReason", "orderNumber", "productName", "userName"]
}

product_related = {
    "type": "object",
    "properties": {
        "subcategoryId": {
            "type": "integer",
            },
        "productId": {
            "type": "integer"
        }
    },
    "required": ["subcategoryId", "productId"]
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


def validate_returns(data):
    try:
        validate(data, returns_schema)
    except ValidationError as e:
        return {"isValid": False}
    return {"isValid": True}


def customer_returns(data):
    try:
        validate(data, customer_return_schema)
    except ValidationError as e:
        return {"isValid": False}
    return {"isValid": True}


def product_related_check(data):
    try:
        validate(data, product_related)
    except ValidationError as e:
        return {"isValid": False}
    return {"isValid": True}