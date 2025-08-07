"""add all apis to here along with their routes. """
from InSightify.db_server.Flask_app import app, api,app_logger
from InSightify.db_server.app_resources import *


api.add_resource(Foo, '/foo') #Done
api.add_resource(Bar, '/bar') #Done
api.add_resource(SignUp, '/signup') #Done
api.add_resource(Login, '/login') #Done
api.add_resource(AdminMainWall, '/admin/main_wall') #Done
api.add_resource(UserMainWall, '/user/main_wall') #Done
api.add_resource(VoteUpdate, '/user/vote_update') #Done
api.add_resource(AddingIdea, '/user/add_idea') #Done
api.add_resource(UpdateIdeaStatus, '/admin/update_idea_status')
api.add_resource(IdeaDisplay,"/idea_display") #Done
api.add_resource(TagCreation, "/admin/add_tag") #Mostly redundant but can be used by admin to create new tags
api.add_resource(TagUpdate, "/admin/tag_update")
api.add_resource(TagDelete, "/admin/tag_delete")
api.add_resource(TagDisplay, "/admin/tag_display")  #Done
api.add_resource(UserProfile, "/user_profile") #Done
api.add_resource(UserProfileUpdate, "/user_profile_update") #Done
api.add_resource(AddComment, "/user/add_comment") #Done
api.add_resource(CommentDisplay, "/user/comment_display") #Done
api.add_resource(RefineIdeas, "/user/refine_idea") #Done
api.add_resource(ForgotPassswd, "/forgot_password") #Done
api.add_resource(BulkMerge, "/admin/remerge_ideas") #Done

# Test left for merging with merged ideas
app_logger.info("Routes registered successfully")