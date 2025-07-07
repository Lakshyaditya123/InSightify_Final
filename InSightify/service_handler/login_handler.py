from InSightify.Common_files.response import ResponseHandler
from InSightify.CoreClasses.users import UserCRUD
from InSightify.db_server.Flask_app import dbsession


class LoginHelper:
    def __init__(self):
        self.response = ResponseHandler()
        self.user_crud = UserCRUD(dbsession)
        self.session = dbsession

    def login(self, data):
        # Check if both username and password are provided
        if data['email'] and data['password']:
            user_rec=self.user_crud.get_by_email(data['email'])["obj"]
            if user_rec:
                if user_rec.password == data['password']:
                    #token = create_access_token(identity={"user_name": self.username, "user_id": self.user_rec.id}, expires_delta=timedelta(days=1))
                    self.response.get_response(0,"Login Successful", data_rec=self.user_crud.convert_to_dict(user_rec)) #pass the token here
                else:
                    self.response.get_response(1,"Username or password is incorrect")
            else:
                self.response.get_response(404, "User not found")
        else:
            self.response.get_response(400, "Username and password are required")
        return self.response.send_response()

    def forgot_passwd(self, data):
        if data['email'] and data['sec_ques'] and data['answer'] in data:
            user_rec=self.user_crud.get_by_email(data['email'])["obj"]
            if user_rec:
                if user_rec.sec_ques == data['sec_ques'] and user_rec.answer == data['answer']:
                    self.response.get_response(0, "Yupp you are the one...")
                    self.reset_password(data)
                else:
                    self.response.get_response(1,"Security_question or answer is incorrect")
            else:
                self.response.get_response(404,"User not found")
        else:
            self.response.get_response(400, "email and sec_ques and answer are required")
        return self.response.send_response()

    def reset_password(self, data):
        user_rec=self.user_crud.get_by_email(data['email'])["obj"]
        if user_rec:
            self.user_crud.update_profile(user_id=user_rec.id, password=data['password'])
            #have to commit here:)
            if self.user_crud.commit_it()["errCode"]:
                self.response.get_response(500, "Internal Server Error")
            else:
                self.response.get_response(0, "Password updated successfully")
        else:
            self.response.get_response(2,"User not found")
        return self.response.send_response()









