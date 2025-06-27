"""Define all the classes here for each page element"""
from InSightify.service_handler.tags_handler import TagHelper

# app_resources.py - UPDATED VERSION
"""Define all the classes here for each page element"""
from InSightify.db_server.resource_decorator import Resource, app_logger
from InSightify.service_handler import *
from flask import request
import json


class Foo(Resource):
    @staticmethod
    def get():
        app_logger.info("FOO GET method called")
        return {'errCode': 0, 'msg': 'IN FOO Function.'}

class Bar(Resource):
    @staticmethod
    def post():
        app_logger.info("BAR POST method called")
        try:
            _payload = request.get_json()
            print(f"Received payload: {_payload}")  # Debug print
            return {'errCode': 0, 'msg': 'In BAR Function', 'datarec': _payload}
        except Exception as e:
            print(f"Error in BAR POST: {str(e)}")  # Debug print
            return {'errCode': 1, 'msg': f'Error: {str(e)}'}

    @staticmethod
    def get():
        app_logger.info("BAR GET method called")
        return {'errCode': 0, 'msg': 'BAR GET method working'}

class SignUp(Resource):
    @staticmethod
    def post():
        try:
            app_logger.info("SignUp POST method called")
            signup= SignupHelper()
            data=request.get_json()
            return signup.signup(data)
        except Exception as e:
            app_logger.error(f"Error in VoteUpdate POST: {str(e)}")
            return {'errCode': 1, 'msg': f'Error: {str(e)}'}

    @staticmethod
    def get():
        app_logger.info("SignUp GET method called")
        return {'errCode': 0, 'msg': 'SignUp GET method working'}

class Login(Resource):
    @staticmethod
    def post():
        app_logger.info("Login POST method called")
        try:
            login= LoginHelper()
            data=request.get_json()
            return login.login(data)
        except Exception as e:
            app_logger.error(f"Error in VoteUpdate POST: {str(e)}")
            return {'errCode': 1, 'msg': f'Error: {str(e)}'}

    @staticmethod
    def get():
        app_logger.info("Login GET method called")
        return {'errCode': 0, 'msg': 'Login GET method working'}

class VoteUpdate(Resource):
    @staticmethod
    def post():
        app_logger.info("VoteUpdate POST method called")
        try:
            vote=VoteHelper()
            data=request.get_json()
            return vote.update_vote(data)
        except Exception as e:
            app_logger.error(f"Error in VoteUpdate POST: {str(e)}")
            return {'errCode': 1, 'msg': f'Error: {str(e)}'}

    @staticmethod
    def get():
        app_logger.info("VoteUpdate GET method called")
        vote = VoteHelper()
        data = request.get_json() #{"idea_id","comment_id"}
        return vote.vote_display(data)


class WallForUserIdea(Resource):
    @staticmethod
    def get():
        app_logger.info("WallForUser GET method called")
        try:
            wall = WallHelper()
            data=request.get_json()
            return wall.load_wall_with_child(data)
        except Exception as e:
            app_logger.error(f"Error in WallForUser GET: {str(e)}")

class MySpaceWall(Resource):
    @staticmethod
    def get():
        app_logger.info("MySpaceWall GET method called")
        try:
            wall = WallHelper()
            data=request.get_json()
            return wall.load_my_space(data)
        except Exception as e:
            app_logger.error(f"Error in MySpaceWall GET: {str(e)}")

class AddingIdea(Resource):
    @staticmethod
    def post():
        app_logger.info("AddingIdea POST method called")
        try:
            idea=IdeaHelper()
            data=request.get_json()
            return idea.add_idea(data)
        except Exception as e:
            app_logger.error(f"Error in AddingIdea POST: {str(e)}")
            return {'errCode': 1, 'msg': f'Error: {str(e)}'}

    def get(self):
        app_logger.info("AddingIdea GET method called")
        return {'errCode': 0, 'msg': 'AddingIdea GET method working'}

class IdeaDisplay(Resource):
    @staticmethod
    def get():
        app_logger.info("IdeaDisplay GET method called")
        try:
            idea=IdeaHelper()
            data=request.get_json()
            return idea.idea_display(data)
        except Exception as e:
            app_logger.error(f"Error in IdeaDisplay GET: {str(e)}")
            return {'errCode': 1, 'msg': f'Error: {str(e)}'}

class TagCreation(Resource):
    @staticmethod
    def post():
        app_logger.info("TagCreation POST method called")
        try:
            tag=TagHelper()
            data=request.get_json()
            return tag.add_tag(data)
        except Exception as e:
            app_logger.error(f"Error in TagCreation POST: {str(e)}")
            return {'errCode': 1, 'msg': f'Error: {str(e)}'}

    def get(self):
        app_logger.info("TagCreation GET method called")
        return {'errCode': 0, 'msg': 'TagCreation GET method working'}

class TagDisplay(Resource):
    @staticmethod
    def get():
        app_logger.info("TagDisplay GET method called")
        try:
            tag=TagHelper()
            data=request.get_json()
            return tag.tag_display(data)
        except Exception as e:
            app_logger.error(f"Error in TagDisplay GET: {str(e)}")
            return {'errCode': 1, 'msg': f'Error: {str(e)}'}

class UserProfile(Resource):
    @staticmethod
    def get():
        try:
            app_logger.info("UserProfile GET method called")
            user=ProfileHelper()
            data = request.get_json()
            return user.get_profile(data)
        except Exception as e:
            app_logger.error(f"Error in UserProfile GET: {str(e)}")
            return {'errCode': 1, 'msg': f'Error: {str(e)}'}
class AddComment(Resource):
    @staticmethod
    def post():
        try:
            app_logger.info("AddComment POST method called")
            comment=CommentHelper()
            data=request.get_json()
            return comment.add_comment(data)
        except Exception as e:
            app_logger.error(f"Error in AddComment POST: {str(e)}")
            return {'errCode': 1, 'msg': f'Error: {str(e)}'}

class CommentDisplay(Resource):
    @staticmethod
    def get():
        app_logger.info("CommentDisplay GET method called")
        try:
            comment=CommentHelper()
            data=request.get_json()
            return comment.comment_display(data)
        except Exception as e:
            app_logger.error(f"Error in CommentDisplay GET: {str(e)}")
            return {'errCode': 1, 'msg': f'Error: {str(e)}'}







