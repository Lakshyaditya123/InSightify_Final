"""Define all the classes here for each page element"""
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
            app_logger.error(f"Error in SignUp POST: {str(e)}")

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
            app_logger.error(f"Error in Login POST: {str(e)}")

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
    @staticmethod
    def get():
        app_logger.info("VoteUpdate GET method called")
        vote = VoteHelper()
        data = request.get_json()
        return vote.update_vote(vote.vote_display(data))


class WallForUser(Resource):
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






