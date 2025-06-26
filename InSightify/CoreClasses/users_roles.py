from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError

from InSightify.Common_files.base_crud import BaseCRUD
from InSightify.db_server.app_orm import UsersRoles


# class UsersRolesCRUD(BaseCRUD):
#
#     def __init__(self):
#         super().__init__(UsersRoles)
#
#     def assign_role_to_user(self, db: Session, user_id: int, role_id: int):
#         return self.create(db, id_users=user_id, id_roles=role_id)
#
#     def get_user_roles(self, db: Session, user_id: int):
#         return db.query(UsersRoles).filter(UsersRoles.id_users == user_id).all()
#
#     def get_users_with_role(self, db: Session, role_id: int):
#         return db.query(UsersRoles).filter(UsersRoles.id_roles == role_id).all()
#
#     def remove_role_from_user(self, db: Session, user_id: int, role_id: int):
#         assignment = db.query(UsersRoles).filter(
#             UsersRoles.id_users == user_id,
#             UsersRoles.id_roles == role_id
#         ).first()
#         if assignment:
#             db.delete(assignment)
#             db.commit()
#             return True
#         return False
#
#     def user_has_role(self, db: Session, user_id: int, role_id: int):
#         return db.query(UsersRoles).filter(
#             UsersRoles.id_users == user_id,
#             UsersRoles.id_roles == role_id
#         ).first() is not None



class UsersRolesCRUD(BaseCRUD):

    def __init__(self, db_session):
        super().__init__(UsersRoles, db_session)

    def assign_role_to_user(self, user_id, role_id):
        return self.create(
            id_users=user_id,
            id_roles=role_id
        )

    def get_user_roles(self, user_id):
        return self.get_by_fields(id_users=user_id)

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
            self.db_response.get_response(error_code=0, msg="Role removed from user !", obj=record)
        else:
            self.db_response.get_response(error_code=0, msg="Role not found !", obj=None)
        return self.db_response.send_response()

