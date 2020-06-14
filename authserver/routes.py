from authserver import app, pgresources, api


"""Resources"""
api.add_resource(pgresources.UserRegistration, '/v1/registration')
api.add_resource(pgresources.UserLogin, '/v1/login')
api.add_resource(pgresources.ProtectedRoute, '/v1/protected')

