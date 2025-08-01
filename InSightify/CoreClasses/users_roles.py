from sqlalchemy import and_
from InSightify.Common_files.base_crud import BaseCRUD
from InSightify.db_server.app_orm import UsersRoles

class UsersRolesCRUD(BaseCRUD):

    def __init__(self, db_session):
        super().__init__(UsersRoles, db_session)

    def assign_role_to_user(self, user_id, role_id):
        return self.create(id_users=user_id,id_roles=role_id)

    def get_user_roles(self, user_id):
        return self.get_by_field("id_users",user_id)

    def get_users_with_role(self, role_id):
        return self.get_by_fields(id_roles=role_id)

    def remove_role_from_user(self, user_id, role_id):
        record = self.db_session.query(self.model).filter(
            and_(
                self.model.id_users == user_id,
                self.model.id_roles == role_id
            )
        ).first()

        if record:
            self.db_session.delete(record)
            self.db_response.get_response(errCode=0, msg="Role removed from user !", obj=record)
        else:
            self.db_response.get_response(errCode=0, msg="Role not found !", obj=None)
        return self.db_response.send_response()

