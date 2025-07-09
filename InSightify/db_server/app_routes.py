"""add all apis to here along with their routes. """
from InSightify.db_server.Flask_app import app, api,app_logger
from InSightify.db_server.app_resources import *


api.add_resource(Foo, '/foo') #Done
api.add_resource(Bar, '/bar') #Done
api.add_resource(SignUp, '/signup') #Done
api.add_resource(Login, '/login') #Done
api.add_resource(MainWall, '/main_wall') #Done
api.add_resource(MySpaceWall, '/my_space_wall') #Done
api.add_resource(VoteUpdate, '/vote_update') #Done
api.add_resource(AddingIdea, '/add_idea') #Done
api.add_resource(IdeaDisplay,"/idea_display") #Done
api.add_resource(TagCreation, "/tag_creation") #Mostly redundant but can be used by admin to create new tags
api.add_resource(TagDisplay, "/tag_display")  #Done
api.add_resource(UserProfile, "/user_profile") #Done
api.add_resource(UserProfileUpdate, "/user_profile_update") #Done
api.add_resource(AddComment, "/add_comment") #Done
api.add_resource(CommentDisplay, "/comment_display") #Done
api.add_resource(RefineIdeas, "/refine_idea") #Done
api.add_resource(ForgotPassswd, "/forgot_password") #Done

# Test left for merging with merged ideas
app_logger.info("Routes registered successfully")