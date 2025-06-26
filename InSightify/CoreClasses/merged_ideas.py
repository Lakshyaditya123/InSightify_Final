from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from InSightify.Common_files.base_crud import BaseCRUD
from InSightify.db_server.app_orm import MergedIdea, Idea


class MergedIdeaCRUD(BaseCRUD):

    def __init__(self, db_session):
        super().__init__(MergedIdea, db_session)

    def create_merged_idea(self, title, subject, content):
        return self.create(
            title=title,
            subject=subject,
            content=content
        )

    def search_merged_ideas(self, search_term):
        result=self.db_session.query(self.model).filter(
            or_(
                self.model.title.ilike(f"%{search_term}%"),
                self.model.subject.ilike(f"%{search_term}%"),
                self.model.content.ilike(f"%{search_term}%")
            )
        ).all()
        if result:
            self.db_response.get_response(error_code=0, msg="Found Records !", obj=result)
        else:
            self.db_response.get_response(error_code=0, msg="Records not found", obj=None)
        return self.db_response.send_response()

    def get_merged_ideas_with_users(self):
        merged_ideas = (
            self.db_session.query(MergedIdea)
            .options(
                joinedload(MergedIdea.ideas).joinedload(Idea.user)
            )
            .all()
        )
        if merged_ideas:
            result = []
            for merged_idea in merged_ideas:
                users_set = set()
                users_list = []

                for idea in merged_idea.ideas:
                    user = idea.user
                    if user and user.id not in users_set:
                        users_set.add(user.id)
                        users_list.append({
                            "id": user.id,
                            "name": user.name,
                            "email": user.email,
                            "mob_number": user.mob_number,
                            "bio": user.bio,
                            "profile_picture": user.profile_picture
                        })

                merged_idea_dict = {
                    "id": merged_idea.id,
                    "title": merged_idea.title,
                    "subject": merged_idea.subject,
                    "content": merged_idea.content,
                    "created_at": merged_idea.create_datetime,
                    "last_modified": merged_idea.lastchange_datetime
                }

                result.append({
                    "users": users_list,
                    "merged_idea": merged_idea_dict
                })

                self.db_response.get_response(error_code=0, msg="Found Records !", obj=result)
        else:
            self.db_response.get_response(error_code=0, msg="Records not found", obj=None)

        return self.db_response.send_response()





# class MergedIdeaCRUD(BaseCRUD):
#
#     def __init__(self):
#         super().__init__(MergedIdea)
#
#     def create_merged_idea(self, db: Session, subject: str, content: str, title: str = None):
#         return self.create(db, title=title, subject=subject, content=content)
#
#     def search_merged_ideas(self, db: Session, search_term: str):
#         return db.query(MergedIdea).filter(
#             (MergedIdea.title.ilike(f"%{search_term}%")) |
#             (MergedIdea.subject.ilike(f"%{search_term}%")) |
#             (MergedIdea.content.ilike(f"%{search_term}%"))
#         ).all()
#