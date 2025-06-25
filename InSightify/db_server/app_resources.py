"""Define all the classes here for each page element"""
# app_resources.py - UPDATED VERSION
"""Define all the classes here for each page element"""
from InSightify.db_server.resource_decorator import Resource, app_logger
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
            return {'errCode': 0, 'msg': 'In SignUp Function', 'datarec': request.get_json()}
        except Exception as e:
            app_logger.error(f"Error in SignUp POST: {str(e)}")
            return {'errCode': 1, 'msg': f'Error: {str(e)}'}

    @staticmethod
    def get():
        app_logger.info("SignUp GET method called")
        return {'errCode': 0, 'msg': 'SignUp GET method working'}
