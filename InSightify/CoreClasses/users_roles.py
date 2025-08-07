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

