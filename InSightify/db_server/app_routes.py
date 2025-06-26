"""add all apis to here along with their routes. """
from InSightify.db_server.Flask_app import app, api
from InSightify.db_server.app_resources import *

# Register resources
api.add_resource(Foo, '/foo')
api.add_resource(Bar, '/bar')
api.add_resource(SignUp, '/signup')
api.add_resource(Login, '/login')
api.add_resource(WallForUser, '/user_wall')
api.add_resource(MySpaceWall, '/my_space_wall')
api.add_resource(VoteUpdate, '/vote_update')
api.add_resource(AddingIdea, '/add_idea')
api.add_resource(IdeaDisplay,"/idea_display")
print("Routes registered successfully")  # Debug print