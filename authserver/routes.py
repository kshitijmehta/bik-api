from authserver import app, pgresources, userdetails, chgpassword, products, api


"""Resources"""
api.add_resource(pgresources.UserRegistration, '/v1/registration')
api.add_resource(pgresources.UserLogin, '/v1/login')
api.add_resource(userdetails.Userinfo, '/v1/userinfo')
api.add_resource(chgpassword.changepass, '/v1/passwordchange')
api.add_resource(products.Productinfoinsert, '/v1/productinfoinsert')
api.add_resource(products.Productinfouppdate, '/v1/productinfoupdate')
api.add_resource(products.Producttypeinsert, '/v1/productypeinsert')
api.add_resource(products.Producttypeupdate, '/v1/producttypeupdate')
api.add_resource(pgresources.ProtectedRoute, '/v1/protected')

