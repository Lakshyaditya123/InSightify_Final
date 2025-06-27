"""add all apis to here along with their routes. """
from InSightify.db_server.Flask_app import app, api,app_logger
from InSightify.db_server.app_resources import *


api.add_resource(Foo, '/foo')
api.add_resource(Bar, '/bar')
api.add_resource(SignUp, '/signup')
api.add_resource(Login, '/login')
api.add_resource(WallForUserIdea, '/user_wall')
api.add_resource(MySpaceWall, '/my_space_wall')
api.add_resource(VoteUpdate, '/vote_update')
api.add_resource(AddingIdea, '/add_idea')
api.add_resource(IdeaDisplay,"/idea_display")
api.add_resource(TagCreation, "/tag_creation")
api.add_resource(TagDisplay, "/tag_display")
api.add_resource(UserProfile, "/user_profile")
api.add_resource(AddComment, "/add_comment")
api.add_resource(CommentDisplay, "/comment_display")
app_logger.info("Routes registered successfully")