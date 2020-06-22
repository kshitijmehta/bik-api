# from flask_jwt_extended import jwt_required
# from flask_restful import Resource
# from authserver import conn, bcrypt
# from flask import request
# from authserver.validation_schemas import userinfo
#


# class Userinfo(Resource):
#  @jwt_required
#  def post(self):
#     data = request.get_json()
#     user_validation = userinfo.validate_user(data)
#     if user_validation['isValid']:
#         try:
#             cur = conn.cursor()
#             first_name = data['first_name']
#             last_name = data['last_name']
#             address = data['address']
#             state = data['state']
#             country = data['country']
#
#             cur.execute(f'INSERT INTO public."user" (first_name, last_name, address, state, country) VALUES ('
#                             f"'{str(first_name)}', '{str(last_name)}', '{str(address)}', '{str(state)}','{str(country)}')")
#
#             conn.commit()
#             cur.close()
#             conn.close()
#             return {'message': 'user created successfully'}, 200
#
#         except Exception as e:
#                 print(e)
#                 return {'message': 'user insertion error'}, 500
#
#     else:
#         return {'message': 'information field validation error'}, 500
#
#  @jwt_required
#  def get(self):
#     try:
#         cur = conn.cursor()
#         cur.execute(f'SELECT * from public."user" WHERE first_name ='f"'kartik'")
#         select = cur.fetchone()
#         return select
#
#     except Exception as e:
#         print(e)
#         return {'message': 'user not found'}, 500
#
#
# class changepass(Resource):
#  @jwt_required
#  def post(self):
#     data = request.get_json()
#     try:
#         cur = conn.cursor()
#         password = data['password'].encode('utf-8')
#         cur.execute(f'SELECT password public."user" WHERE email ='f"'{email}'")
#         res =cur.fetchone()
#         if not res:
#            return {"message": "Invalid credentials"}, 500
#         if bcrypt.check_password_hash(res[0], password):
#            new_password = bcrypt.generate_password_hash(data['new_password']).decode('utf-8')
#
#            cur.execute(f'INSERT INTO public."user" (password) VALUES ('
#                 f"'{str(new_password)}')")
#     except Exception as e:
#           print(e)
#           return {'message': 'cant change passwrord'}