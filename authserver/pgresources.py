from flask_restful import Resource
from authserver import conn, bcrypt
from flask import request
from authserver.validation_schemas import register


class UserRegistration(Resource):
    def post(self):
        data = request.get_json()
        user_validation = register.validate_user(data)
        if user_validation['isValid']:
            try:
                cur = conn.cursor()
                username = data['username']
                email = data['email']
                phone_number = data['phone_number']
                password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

                cur.execute(f'INSERT INTO public."user" (username, email, phone_number, password) VALUES ('
                            f"'{str(username)}', '{str(email)}', {phone_number}, '{str(password)}')")

                conn.commit()
                return {'message': 'user created successfully'}, 200

            except Exception as e:
                return {'message': 'user insertion error'}, 500

        else:
            return {'message': 'field validation error'}, 500

