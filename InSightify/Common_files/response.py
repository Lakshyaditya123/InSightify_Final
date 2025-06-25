from flask import jsonify
class ResponseHandler:
    def __init__(self):
        self.errCode = None
        self.response = dict()
    def get_response(self,error_code, msg, data=None, data_rec=None):
        self.response = {"error_code": error_code, "msg": msg if msg else "No Message", "data": data if data else [],"datarec": data_rec if data_rec else {}}

    def send_response(self):
        return jsonify(self.response)

#