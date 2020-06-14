from authserver import app, pgresources, api

app.config['SECRET_KEY'] = 'test-app'

'''Resources'''
api.add_resource(pgresources.UserRegistration, '/registration')

