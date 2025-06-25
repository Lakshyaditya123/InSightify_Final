from InSightify.Common_files.response import ResponseHandler
from InSightify.CoreClasses.users import UserCRUD
from InSightify.db_server.Flask_app import dbsession

class SignupHelper:
    def __init__(self):
        self.response = ResponseHandler()
        self.user_crud = UserCRUD(dbsession)
        self.session = dbsession

    def signup(self, data):
        data['security_question_id']= data['security_question_id'] if data.get('security_question_id') else 1
        data['security_answer'] = data['security_answer'] if data.get('security_answer') else "lakshya"
        data['profile_picture'] = data['profile_picture'] if data.get('profile_picture') else "/static/img/profile_picture.png"
        # Check if all required fields are provided
        if  data['name'] and data['email'] and data['mobile'] and data['password'] and  data['security_question_id'] and data['security_answer'] and data['profile_picture']:
            user_rec=self.user_crud.get_by_email(data['email'])
            if type(user_rec)!=str:
                if user_rec:
                    self.response.get_response(3, "Try logging in or forgot password")
                else:
                    check=self.user_crud.create_user(**data)
                    if type(check) !=str:
                        self.response.get_response(0,"User created successfully")
                    else:
                        self.response.get_response(500, "Internal Server Error")
            else:
                self.response.get_response(500, "Internal Server Error")
        else:
            self.response.get_response(2, "email, mobile, password, security_question and security_answer are required")
        self.response.send_response()
# have to encrypt password, email, mobile number, sec answer