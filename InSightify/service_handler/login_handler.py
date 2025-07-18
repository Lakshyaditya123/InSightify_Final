from InSightify.Common_files.response import ResponseHandler
from InSightify.CoreClasses import UsersRolesCRUD, RoleCRUD
from InSightify.CoreClasses.users import UserCRUD
from InSightify.db_server.Flask_app import dbsession, app_logger


class LoginHelper:
    def __init__(self):
        self.response = ResponseHandler()
        self.user_crud = UserCRUD(dbsession)
        self.user_role_crud = UsersRolesCRUD(dbsession)
        self.role_crud = RoleCRUD(dbsession)
        self.session = dbsession

    def login(self, data):
        # Check if both username and password are provided
        if data.get('email') and data.get('password'):
            user_rec=self.user_crud.get_by_email(data.get('email'))["obj"]
            output={
                "user_id": user_rec.id,
                "user_name": user_rec.name,
                "user_email": user_rec.email,
                "user_mobile": user_rec.mobile,
                "user_profile_picture": user_rec.profile_picture,
                "user_bio": user_rec.bio,
                "user_role": [self.role_crud.get_role_id(role.id_roles)["obj"].roles for role in self.user_role_crud.get_user_roles(user_id=user_rec.id)["obj"]]
            }
            if user_rec:
                if user_rec.password == data['password']:
                    #token = create_access_token(identity={"user_name": self.username, "user_id": self.user_rec.id}, expires_delta=timedelta(days=1))
                    self.response.get_response(0,"Login Successful", data_rec=output) #pass the token here
                else:
                    self.response.get_response(1,"Username or password is incorrect")
            else:
                self.response.get_response(404, "User not found")
        else:
            self.response.get_response(100, "Username and password are required")
        return self.response.send_response()

    def forgot_passwd(self, data):
        if data.get('email') and data.get('security_question_id') and data.get('security_answer'):
            user_rec=self.user_crud.get_by_email(data['email'])["obj"]
            if user_rec:
                app_logger.info(f"User found: {data['security_question_id']}=={user_rec.this_obj2security_ques}:{data["security_answer"].strip()}=={user_rec.security_ques_answer}")
                if user_rec.this_obj2security_ques == data['security_question_id'] and user_rec.security_ques_answer == data['security_answer'].strip():
                    self.response.get_response(0, "Yupp you are the one...")
                    self.reset_password(data, user_rec)
                else:
                    self.response.get_response(1,"Security_question or answer is incorrect")
            else:
                self.response.get_response(404,"User not found")
        else:
            self.response.get_response(400, "email, security_question_id and security_answer are required")
        return self.response.send_response()

    def reset_password(self, data, user_rec):
        new_password = data.get("new_password")
        if new_password:
            self.user_crud.update_profile(user_rec.id, password=new_password)
            if self.user_crud.commit_it()["errCode"]:
                self.response.get_response(500, "Internal Server Error")
            else:
                self.response.get_response(0, "Password reset successfully")
        else:
            self.response.get_response(400, "new_password are required")
        return self.response.send_response()







