from flask_restful import Resource, reqparse
from authserver.models import UserModel
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt


parser = reqparse.RequestParser()
parser.add_argument('username', help='This field is required', required=True)
parser.add_argument('password', help='This field is required', required=True)


class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": f"User {data['username']} already exists"}, 500

        new_user = UserModel(
            username=data['username'],
            password=UserModel.generate_hash(data['password'])
        )
        try:
            new_user.save_to_db()
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                "message": f"User {data['username']} was created",
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        except:
            return {
                       "message": "Something went wrong"
                   }, 500


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = UserModel.find_by_username(data['username'])
        if not current_user:
            return {
                "message": f"User {data['username']} does not exists"
            }, 500

        if UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                "message": f"Logged in as {data['username']}",
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200
        else:
            return {
                "message": "Wrong Credentials"
            }, 500


class UserLogoutAccess(Resource):
    def post(self):
        return {'message': 'User logout'}


class UserLogoutRefresh(Resource):
    def post(self):
        return {'message': 'User logout'}


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}


class AllUsers(Resource):
    def get(self):
        return UserModel.return_all()

    def delete(self):
        return UserModel.delete_all()


class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {'answer': 42}
