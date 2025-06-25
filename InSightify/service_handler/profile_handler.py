from InSightify.Common_files.response import ResponseHandler
from InSightify.CoreClasses.users import UserCRUD
from InSightify.db_server.Flask_app import dbsession


class ProfileHelper:
    def __init__(self):
        self.response = ResponseHandler()
        self.user_crud = UserCRUD(dbsession)
        self.session = dbsession

    def get_profile(self, user_id):
        user_rec=self.user_crud.get_by_id(**user_id)
        if type(user_rec)!=str:
            if user_rec:
                self.response.get_response(0,"Login Successful", data_rec=self.user_crud.convert_to_dict(user_rec)) #pass the token here
            else:
                self.response.get_response(2, "User not found")
        else:
            self.response.get_response(500, "Internal Server Error")
        return self.response.send_response()


