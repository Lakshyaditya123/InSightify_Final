from InSightify.Common_files.base_crud import BaseCRUD
from InSightify.db_server.app_orm import User

class UserCRUD(BaseCRUD):

    def __init__(self, db_session):
        super().__init__(User, db_session)

    def create_user(self, name, email, mobile, password, security_question_id, security_answer, profile_picture,
                    bio):
        return self.create(
            name=name,
            email=email,
            mobile=mobile,
            password=password,
            this_obj2security_ques=security_question_id,
            security_ques_answer=security_answer,
            profile_picture=profile_picture,
            bio=bio)

    def get_by_email(self, email):
        return self.get_by_field("email", email)

    def update_profile(self, user_id, **kwargs):
        return self.update(user_id, **kwargs)


