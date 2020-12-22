from flask import request
from flask_restful import Resource

from authserver import app
from authserver.utils.send_email import send_email
from authserver.validation_schemas.contactus import validate_contact_us
from secrets import secrets


class SendContactUs(Resource):
    def post(self):
        try:
            data = request.get_json()
            validation = validate_contact_us(data)
            if validation['isValid']:
                send_email(secrets['CUSTOMER_CONTACT_QUERY'], {
                    "to_email": secrets['ADMIN_EMAIL'],
                    "variables": {
                        "NAME": data['name'],
                        "EMAIL": data['email'],
                        "MESSAGE": data['message'],
                    }
                })
                return {'message': 'Email sent to support team!'}, 200
            else:
                return {'message': 'Please enter valid data to the form'}, 500
        except Exception as e:
            app.logger.debug(e)
            return {'message': 'Error occurred try again'}, 500