"""add all apis to here along with their routes. """
from InSightify.db_server.Flask_app import app, api
from InSightify.db_server.app_resources import Foo, Bar

# Register resources
api.add_resource(Foo, '/foo')
api.add_resource(Bar, '/bar')

print("Routes registered successfully")  # Debug print