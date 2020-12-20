from jsonschema import validate
from jsonschema import ValidationError

razorpay_paypal_cod_place_order = {
    "type": "object",
    "properties": {
        "amount": {
            "type": "string"
        },
        "displayAmount": {
            "type": "string"
        },
        "orderId": {
            "type": "integer"
        },
        "couponId": {
            "type": "integer"
        }
    },
    "required": ["amount","displayAmount", "orderId"]
}

razorpay_payment_success = {
    "type": "object",
    "properties": {
        "razorpayPaymentId": {
            "type": "string"
        },
        "razorpayOrderId": {
            "type": "string"
        },
        "razorpaySignature": {
            "type": "string"
        },
        "orderId": {
            "type": "integer"
        },
        "orderNumber": {
            "type": "string"
        },
        "addressId": {
            "type": ["integer", "string"]
        },
        "userAddress": {
            "type": "string"
        },
        "userName": {
            "type": "string"
        },
    },
    "required": ["razorpayPaymentId", "razorpayOrderId", "razorpaySignature", "orderId", "orderNumber", "addressId","userAddress","userName"]
}

paypal_payment_success = {
    "type": "object",
    "properties": {
        "paypalResponse": {
            "type": "object"
        },
        "orderId": {
            "type": "integer"
        },
        "addressId": {
            "type": "integer"
        },
        "isStandard": {
            "type": "boolean"
        },
        "couponId": {
            "type": "integer"
        },
        "quantity": {
            "type": "integer"
        },
        "userAddress": {
            "type": "string"
        },
        "userName": {
            "type": "string"
        },
    },
    "required": ["paypalResponse", "orderId","addressId","isStandard","quantity","userAddress","userName"]
}

cod_status = {
    "type": "object",
    "properties": {
        "otp": {
            "type": "string"
        },
        "orderId": {
            "type": "integer"
        },
        "addressId": {
            "type": ["integer", "string"]
        },
        "userAddress": {
            "type": "string"
        },
        "userName": {
            "type": "string"
        },
    },
    "required": ["otp", "orderId", "addressId","userAddress","userName"]
}

def validate_razorpay_paypal_cod_order(data):
    try:
        validate(data, razorpay_paypal_cod_place_order)
    except ValidationError as e:
        print(e)
        return {"isValid": False}
    return {"isValid": True}


def validate_razorpay_payment(data):
    try:
        validate(data, razorpay_payment_success)
    except ValidationError as e:
        print(e)
        return {"isValid": False}
    return {"isValid": True}


def validate_paypal_payment(data):
    try:
        validate(data, paypal_payment_success)
    except ValidationError as e:
        print(e)
        return {"isValid": False}
    return {"isValid": True}


def validate_cod_status(data):
    try:
        validate(data, cod_status)
    except ValidationError as e:
        print(e)
        return {"isValid": False}
    return {"isValid": True}