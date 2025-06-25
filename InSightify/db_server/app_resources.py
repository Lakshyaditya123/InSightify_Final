"""Define all the classes here for each page element"""
# app_resources.py - UPDATED VERSION
"""Define all the classes here for each page element"""
from InSightify.db_server.resource_decorator import Resource
from flask import request
import json


class Foo(Resource):
    @staticmethod
    def get():
        print("FOO GET method called")  # Debug print
        return {'errCode': 0, 'msg': 'IN FOO Function.'}


class Bar(Resource):
    @staticmethod
    def post():
        print("BAR POST method called")  # Debug print
        try:
            _payload = request.get_json()
            print(f"Received payload: {_payload}")  # Debug print
            return {'errCode': 0, 'msg': 'In BAR Function', 'datarec': _payload}
        except Exception as e:
            print(f"Error in BAR POST: {str(e)}")  # Debug print
            return {'errCode': 1, 'msg': f'Error: {str(e)}'}

    @staticmethod
    def get():
        print("BAR GET method called")  # Debug print
        return {'errCode': 0, 'msg': 'BAR GET method working'}