from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from InSightify.Common_files.base_crud import BaseCRUD
from InSightify.db_server.app_orm import Idea


# class IdeaCRUD(BaseCRUD):
#
#     def __init__(self):
#         super().__init__(Idea)
#
#     def create_idea(self, db: Session, user_id: int, subject: str, content: str,
#                     status: int=-1, title: str = None, refine_content: str = None):
#         return self.create(
#             db, this_obj2users=user_id, title=title, subject=subject,
#             content=content, refine_content=refine_content, status=status
#         )
#
#     def get_by_user(self, db: Session, user_id: int):
#         return db.query(Idea).filter(Idea.this_obj2users == user_id).all()
#
#     def get_by_status(self, db: Session, status: int):
#         return db.query(Idea).filter(Idea.status == status).all()
#
#     def search_ideas(self, db: Session, search_term: str):
#         return db.query(Idea).filter(
#             (Idea.title.ilike(f"%{search_term}%")) |
#             (Idea.subject.ilike(f"%{search_term}%")) |
#             (Idea.content.ilike(f"%{search_term}%"))
#         ).all()
#
#     def update_status(self, db: Session, idea_id: int, status: int):
#         return self.update(db, idea_id, status=status)
#
#



class IdeaCRUD(BaseCRUD):

    def __init__(self, db_session):
        super().__init__(Idea, db_session)

    def create_idea(self, user_id, title, subject, content, tags_list, status=0, refine_content=None, link=None,
                    file_path=None, parent_idea=None):
        return self.create(
            this_obj2users=user_id,
            title=title,
            subject=subject,
            content=content,
            tags_list=tags_list,
            status=status,
            refine_content=refine_content,
            link=link,
            file_path=file_path,
            parent_idea=parent_idea
        )

    def get_by_user(self, user_id):
        return self.get_by_fields(this_obj2users=user_id)

    def get_by_status(self, status=1):
        return self.get_by_fields(status=status)

    def get_by_status_without_ver(self, status=1):
        return self.get_by_fields(status=status, parent_idea=-1)

    def get_by_tags(self, tag_ids):
        try:
            return self.db_session.query(self.model).filter(
                self.model.tags_list.op('&&')(tag_ids)
            ).all()
        except SQLAlchemyError as e:
            print(f"Error getting ideas by tags: {str(e)}")
            return []

    def update_status(self,idea_id, status):
        return self.update(idea_id, status=status)

    def search_ideas(self, search_term):
        try:
            return self.db_session.query(self.model).filter(
                or_(
                    self.model.title.ilike(f"%{search_term}%"),
                    self.model.subject.ilike(f"%{search_term}%"),
                    self.model.content.ilike(f"%{search_term}%")
                )
            ).all()
        except SQLAlchemyError as e:
            print(f"Error searching ideas: {str(e)}")
            return []

