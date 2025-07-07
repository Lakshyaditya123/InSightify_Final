from InSightify.Common_files.response import ResponseHandler
from InSightify.CoreClasses.users import UserCRUD
from InSightify.db_server.Flask_app import dbsession

class SignupHelper:
    def __init__(self):
        self.response = ResponseHandler()
        self.user_crud = UserCRUD(dbsession)
        self.session = dbsession

    def signup(self, data):
        data.setdefault('security_question_id',1)
        data.setdefault('security_answer',"lakshya")
        data.setdefault('profile_picture', "/static/img/profile_picture.png")
        data.setdefault('bio', "No bio available")
        # Check if all required fields are provided
        if  data['name'] and data['email'] and data['mobile'] and data['password'] and  data['security_question_id'] and data['security_answer'] and data['profile_picture']:
            user_rec=self.user_crud.get_by_email(data['email'])["obj"]
            if user_rec:
                self.response.get_response(3, "User already exists with this email")
            else:
                self.user_crud.create_user(**data)
                if self.user_crud.commit_it()["errCode"]:
                    self.response.get_response(500, "Internal Server Error")
                else:
                    self.response.get_response(0, "User created successfully")
        return self.response.send_response()
# have to email, mobile number, sec answer