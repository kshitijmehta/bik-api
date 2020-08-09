from authserver import app, userlogin, userdetails, chgpassword, products, api


"""Resources"""
api.add_resource(userlogin.UserRegistration, '/v1/registration')
api.add_resource(userlogin.UserLogin, '/v1/login')
api.add_resource(userdetails.UserInfo, '/v1/userinfo')
api.add_resource(chgpassword.changepass, '/v1/passwordchange')
api.add_resource(products.Productsizeinsert, '/v1/productsize')
api.add_resource(products.Productinformation, '/v1/productinfo')
api.add_resource(products.Productsubcategoryinformation, '/v1/productypeinsert')
api.add_resource(products.Productcolourinsert, '/v1/productcolour')
api.add_resource(userlogin.ProtectedRoute, '/v1/protected')


