import datetime
from flask_restful import Resource
from authserver import conn, bcrypt
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, \
    get_jwt_identity, get_raw_jwt
from authserver.validation_schemas import register, login


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
                cur.close()
                conn.close()
                return {'message': 'user created successfully'}, 200

            except Exception as e:
                print(e)
                return {'message': 'user insertion error'}, 500

        else:
            return {'message': 'register field validation error'}, 500


class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        user_login_validation = login.validate_user_login(data)
        if user_login_validation['isValid']:
            try:
                cur = conn.cursor()
                email = data['email']
                cur.execute(f'SELECT password, id, email from public."user" WHERE email ='
                            f"'{email}'")
                res = cur.fetchone()
                if not res:
                    return {"message": "Invalid credentials"}, 500
                password = data['password'].encode('utf-8')
                if bcrypt.check_password_hash(res[0], password):
                    access_token = create_access_token(identity={'email': res[2], 'id': res[1]},
                                                       expires_delta=datetime.timedelta(hour=1))
                    return {"message": 'Login successful', "access_token": access_token, "id": res[1]}, 200
                else:
                    return {"message": "Invalid credentials"}, 500

            except Exception as e:
                print(e)
                return {'message': 'user login error'}, 500
        else:
            return {'message': 'login field validation error'}, 500


class ProtectedRoute(Resource):
    """This is a test route to check jwt token"""
    @jwt_required
    def get(self):
        return {"message": "this is a protected route"}
