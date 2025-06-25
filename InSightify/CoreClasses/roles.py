from InSightify.Common_files.base_crud import BaseCRUD
from InSightify.db_server.app_orm import Role


# class RoleCRUD(BaseCRUD):
#
#     def __init__(self):
#         super().__init__(Role)
#
#     def create_role(self, db: Session, role: str, description: str):
#         return self.create(db, roles=role, description=description)
#
#     def get_by_role(self, db: Session, role_char: str):
#         return db.query(Role).filter(Role.roles == role_char).first()


class RoleCRUD(BaseCRUD):

    def __init__(self, db_session):
        super().__init__(Role, db_session)

    def get_by_role_name(self, role_name):
        return self.get_by_field("roles", role_name)

    def create_role(self, role_name, description):
        return self.create(roles=role_name, description=description)