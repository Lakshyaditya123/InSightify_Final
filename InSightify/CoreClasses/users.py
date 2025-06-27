from InSightify.Common_files.base_crud import BaseCRUD
from InSightify.db_server.app_orm import User

# class UserCRUD(BaseCRUD):
#
#     def __init__(self):
#         super().__init__(User)
#
#     def create_user(self, db: Session, name: str, email: str, mob_number: str,
#                     password: str, profile_picture: str, bio: str = None):
#         return self.create(
#             db, name=name, email=email, mob_number=mob_number,
#             password=password, profile_picture=profile_picture, bio=bio
#         )
#
#     def get_by_email(self, db: Session, email: str):
#         return db.query(User).filter(User.email == email).first()
#
#     def get_by_mobile(self, db: Session, mob_number: str):
#         return db.query(User).filter(User.mob_number == mob_number).first()
#
#     def update_profile(self, db: Session, user_id: int, **kwargs):
#         return self.update(db, user_id, **kwargs)
#
#     def search_users(self, db: Session, search_term: str):
#         return db.query(User).filter(
#             (User.name.ilike(f"%{search_term}%")) |
#             (User.email.ilike(f"%{search_term}%"))
#         ).all()

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

    def get_by_mobile(self, mobile):
        return self.get_by_field("mobile", mobile)

    def update_profile(self, user_id, **kwargs):
        return self.update(user_id, **kwargs)


