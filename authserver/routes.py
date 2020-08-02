from authserver import app, userlogin, userdetails, chgpassword, products, api


"""Resources"""
api.add_resource(userlogin.UserRegistration, '/v1/registration')
api.add_resource(userlogin.UserLogin, '/v1/login')
api.add_resource(userdetails.UserInfo, '/v1/userinfo')
api.add_resource(chgpassword.changepass, '/v1/passwordchange')
api.add_resource(products.Productinfoinsert, '/v1/productinfoinsert')
api.add_resource(products.Productinfouppdate, '/v1/productinfoupdate')
api.add_resource(products.Productsubcategoryinsert, '/v1/productypeinsert')
api.add_resource(products.Productsubcategoryupdate, '/v1/producttypeupdate')
api.add_resource(userlogin.ProtectedRoute, '/v1/protected')

