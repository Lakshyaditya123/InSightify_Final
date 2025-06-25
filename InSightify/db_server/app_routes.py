"""add all apis to here along with their routes. """
from InSightify.db_server.Flask_app import app, api
from InSightify.db_server.app_resources import *

# Register resources
api.add_resource(Foo, '/foo')
api.add_resource(Bar, '/bar')
api.add_resource(SignUp, '/signup')
print("Routes registered successfully")  # Debug print