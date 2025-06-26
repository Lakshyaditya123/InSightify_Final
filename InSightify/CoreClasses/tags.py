from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from InSightify.Common_files.base_crud import BaseCRUD
from InSightify.db_server.app_orm import Tag


# class TagCRUD(BaseCRUD):
#
#     def __init__(self):
#         super().__init__(Tag)
#
#     def create_tag(self, db: Session, name: str, tag_desc: str, status: int, generated_by: str):
#         return self.create(
#             db, name=name, tag_desc=tag_desc, status=status, generated_by=generated_by
#         )
#
#     def get_by_name(self, db: Session, name: str):
#         return db.query(Tag).filter(Tag.name == name).first()
#
#     def get_by_status(self, db: Session, status: int):
#         return db.query(Tag).filter(Tag.status == status).all()
#
#     def search_tags(self, db: Session, search_term: str):
#         return db.query(Tag).filter(
#             (Tag.name.ilike(f"%{search_term}%")) |
#             (Tag.tag_desc.ilike(f"%{search_term}%"))
#         ).all()


class TagCRUD(BaseCRUD):

    def __init__(self, db_session):
        super().__init__(Tag, db_session)

    def create_tag(self, name, tag_desc, status=1, generated_by="user"):
        return self.create(
            name=name,
            tag_desc=tag_desc,
            status=status,
            generated_by=generated_by)

    def get_by_name(self, name):
        return self.get_by_field("name", name)

    def get_by_generated_by(self, generated_by):
        return self.get_by_field("generated_by", generated_by)

    def get_active_tags(self):
        return self.get_by_fields(status=1)

    def search_tags(self, search_term):
        result=self.db_session.query(self.model).filter(
            or_(
                self.model.name.ilike(f"%{search_term}%"),
                self.model.tag_desc.ilike(f"%{search_term}%")
            )
        ).all()
        if result:
            self.db_response.get_response(error_code=0, msg="Found Records !", obj=result)
        else:
            self.db_response.get_response(error_code=0, msg="Records not found", obj=None)
        return self.db_response.send_response()

