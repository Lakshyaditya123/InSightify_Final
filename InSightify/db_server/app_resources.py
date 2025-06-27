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

    @staticmethod
    def get():
        return {'errCode': 0, 'msg': 'SignUp GET method working'}

class Login(Resource):
    @staticmethod
    def post():
        login = LoginHelper()
        data = request.get_json()
        return login.login(data)

    @staticmethod
    def get():
        return {'errCode': 0, 'msg': 'Login GET method working'}

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

class WallForUserIdea(Resource):
    @staticmethod
    def get():
        wall = WallHelper()
        data = request.get_json()
        return wall.load_wall_with_child(data)

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

    @staticmethod
    def get():
        return {'errCode': 0, 'msg': 'AddingIdea GET method working'}

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

    @staticmethod
    def get():
        return {'errCode': 0, 'msg': 'TagCreation GET method working'}

class TagDisplay(Resource):
    @staticmethod
    def get():
        tag = TagHelper()
        data = request.get_json()
        return tag.tag_display(data)

class UserProfile(Resource):
    @staticmethod
    def get():
        user = ProfileHelper()
        data = request.get_json()
        return user.get_profile(data)

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