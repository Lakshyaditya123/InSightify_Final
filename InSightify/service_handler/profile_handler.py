import os
from InSightify.Common_files.response import ResponseHandler
from InSightify.CoreClasses import UserCRUD, RoleCRUD, UsersRolesCRUD
from InSightify.db_server.Flask_app import dbsession, app_logger
from InSightify.Common_files.config import config

class ProfileHelper:
    def __init__(self):
        self.response = ResponseHandler()
        self.user_crud = UserCRUD(dbsession)
        self.user_role_crud = UsersRolesCRUD(dbsession)
        self.role_crud = RoleCRUD(dbsession)
        self.session = dbsession

    def get_profile(self, data):
        user_id=data.get("user_id")
        user_rec=self.user_crud.get_by_id(id=user_id)["obj"]
        if user_rec:
            user_role_id = self.user_role_crud.get_user_roles(user_id=user_rec.id)["obj"]
            user_role = self.role_crud.get_role_id(user_role_id.id_roles)["obj"].roles
            output = {
                "user_id": user_rec.id,
                "user_name": user_rec.name,
                "user_email": user_rec.email,
                "user_mobile": user_rec.mobile,
                "user_profile_picture": user_rec.profile_picture,
                "user_bio": user_rec.bio,
                "user_role": user_role
            }
            self.response.get_response(0,"Profile found Successful", data_rec=output) #pass the token here
        else:
            self.response.get_response(2, "User not found")

        return self.response.send_response()

    def update_profile(self, user_id, bio, file):
        user_rec = self.user_crud.get_by_id(id=user_id)
        if user_rec["obj"]:
            if file and file.filename.lower().endswith('.png'):
                user_folder = os.path.join(config.PROFILE_PIC_PATH, str(user_id))
                os.makedirs(user_folder, exist_ok=True)

                filepath = os.path.join(user_folder, "profile_picture.png")
                file.save(filepath)

                profile_picture_url = f"{config.PROFILE_PIC_URL_PREFIX}/{user_id}/profile_picture.png"
            else:
                profile_picture_url = user_rec["obj"].profile_picture

            result=self.user_crud.update_profile(user_id=user_rec["obj"].id, bio=bio, profile_picture=profile_picture_url)["obj"]
            if self.user_crud.commit_it()["errCode"]:
                self.response.get_response(500, "Internal Server Error")
            else:
                self.response.get_response(0,"Profile updated Successful", data_rec=self.user_crud.convert_to_dict(result))
        return self.response.send_response()







