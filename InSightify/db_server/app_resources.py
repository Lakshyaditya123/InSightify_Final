"""Define all the classes here for each page element"""
from InSightify.service_handler.tags_handler import TagHelper
from InSightify.db_server.resource_decorator import Resource
from InSightify.service_handler import *
from flask import request

class Foo(Resource):
    @staticmethod
    def get():
        return {'errCode': 0, 'msg': 'IN FOO Function.'}

class Bar(Resource):
    @staticmethod
    def post():
        _payload = request.get_json()
        return {'errCode': 0, 'msg': 'In BAR Function', 'datarec': _payload}

    @staticmethod
    def get():
        return {'errCode': 0, 'msg': 'BAR GET method working'}

class SignUp(Resource):
    @staticmethod
    def post():
        signup = SignupHelper()
        data = request.get_json()
        return signup.signup(data)

class Login(Resource):
    @staticmethod
    def post():
        login = LoginHelper()
        data = request.get_json()
        return login.login(data)

class VoteUpdate(Resource):
    @staticmethod
    def post():
        vote = VoteHelper()
        data = request.get_json()
        return vote.update_vote(data)

    @staticmethod
    def get():
        vote = VoteHelper()
        data = request.get_json()  # {"idea_id","comment_id"}
        return vote.vote_display(data)

class UserMainWall(Resource):
    @staticmethod
    def get():
        wall = WallHelper()
        return wall.load_wall()

class AdminMainWall(Resource):
    @staticmethod
    def get():
        wall = WallHelper()
        return wall.load_wall(user="admin")

class MySpaceWall(Resource):
    @staticmethod
    def get():
        wall = WallHelper()
        data = request.get_json()
        return wall.load_my_space(data)

class AddingIdea(Resource):
    @staticmethod
    def post():
        idea = IdeaHelper()
        data = request.get_json()
        return idea.add_idea(data)

class IdeaDisplay(Resource):
    @staticmethod
    def get():
        idea = IdeaHelper()
        data = request.get_json()
        return idea.idea_display(data)

class TagCreation(Resource):
    @staticmethod
    def post():
        tag = TagHelper()
        data = request.get_json()
        return tag.add_tag(data)

class TagUpdate(Resource):
    @staticmethod
    def post():
        tag = TagHelper()
        data = request.get_json()
        return tag.update_tag(data)

class TagDisplay(Resource):
    @staticmethod
    def get():
        tag = TagHelper()
        data = request.get_json()
        return tag.tag_display(data)

class TagDelete(Resource):
    @staticmethod
    def post():
        tag=TagHelper()
        data=request.json()
        return tag.tag_delete(data)

class UserProfile(Resource):
    @staticmethod
    def get():
        user = ProfileHelper()
        data = request.get_json()
        return user.get_profile(data)

class UserProfileUpdate(Resource):
    @staticmethod
    def post():
        user = ProfileHelper()
        data = request.get_json()
        return user.update_profile(data)

class AddComment(Resource):
    @staticmethod
    def post():
        comment = CommentHelper()
        data = request.get_json()
        return comment.add_comment(data)

class CommentDisplay(Resource):
    @staticmethod
    def get():
        comment = CommentHelper()
        data = request.get_json()
        return comment.comment_display(data)

class RefineIdeas(Resource):
    @staticmethod
    def get():
        ai_help= AiHelper()
        data=request.get_json()
        return ai_help.refine_idea(data)

class ForgotPassswd(Resource):
    @staticmethod
    def post():
        login = LoginHelper()
        data=request.get_json()
        return login.forgot_passwd(data)

class UpdateIdeaStatus(Resource):
    @staticmethod
    def post():
        idea = IdeaHelper()
        data=request.get_json()
        return idea.update_idea_status(data)

