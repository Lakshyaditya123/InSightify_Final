from flask import jsonify
class ResponseHandler:
    def __init__(self):
        self.errCode = None
        self.response = dict()
    def get_response(self,errCode, msg, data=None, data_rec=None):
        self.response = {"errCode": errCode, "message": msg if msg else "No Message", "data": data if data else [],"datarec": data_rec if data_rec else {}}

    def send_response(self):
        return self.response

class DatabaseResponse:
    def __init__(self):
        self.errCode = None
        self.response = dict()
    def get_response(self,errCode, msg, obj=None):
        self.response = {"errCode": errCode, "msg": msg if msg else "No Message", "obj": obj}
    def send_response(self):
        return self.response
