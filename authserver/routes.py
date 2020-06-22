from authserver import app, pgresources, pgresources1,api


"""Resources"""
api.add_resource(pgresources.UserRegistration, '/v1/registration')
api.add_resource(pgresources.UserLogin, '/v1/login')
# api.add_resource(pgresources1.Userinfo, '/v1/info')
api.add_resource(pgresources.ProtectedRoute, '/v1/protected')

