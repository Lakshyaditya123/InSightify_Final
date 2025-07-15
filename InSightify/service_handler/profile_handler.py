
from InSightify.Common_files.response import ResponseHandler
from InSightify.CoreClasses.users import UserCRUD
from InSightify.db_server.Flask_app import dbsession, app_logger


class ProfileHelper:
    def __init__(self):
        self.response = ResponseHandler()
        self.user_crud = UserCRUD(dbsession)
        self.session = dbsession

    def get_profile(self, user_id):
        user_id=user_id.get("user_id")
        user_rec=self.user_crud.get_by_id(id=user_id)
        if user_rec["obj"]:
            self.response.get_response(0,"Profile found Successful", data_rec=self.user_crud.convert_to_dict(user_rec["obj"])) #pass the token here
        else:
            self.response.get_response(2, "User not found")

        return self.response.send_response()

    def update_profile(self, data):
        user_id = data.get("user_id")
        user_rec = self.user_crud.get_by_id(id=user_id)
        if user_rec["obj"]:
            if data.get("mobile") or data.get("name") or data.get("email"):
                self.response.get_response(1,"Access Denied to change mobile, email or name")
            else:
                result=self.user_crud.update_profile(user_id=user_rec["obj"].id, **data)["obj"]
                if self.user_crud.commit_it()["errCode"]:
                    self.response.get_response(500, "Internal Server Error")
                else:
                    self.response.get_response(0,"Profile updated Successful", data_rec=self.user_crud.convert_to_dict(result))
        return self.response.send_response()







