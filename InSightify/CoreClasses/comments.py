from InSightify.Common_files.base_crud import BaseCRUD
from InSightify.db_server.app_orm import Comment


# class CommentCRUD(BaseCRUD):
#
#     def __init__(self):
#         super().__init__(Comment)
#
#     def create_comment(self, db: Session, user_id: int, content: str,
#                        idea_id: int = None, merged_idea_id: int = None, parent_id: int = -1):
#         return self.create(
#             db, this__obj2users=user_id, content=content,
#             this_obj2ideas=idea_id, this_obj2merged_ideas=merged_idea_id,
#             parents=parent_id
#         )
#
#     def get_by_idea(self, db: Session, idea_id: int):
#         return db.query(Comment).filter(Comment.this_obj2ideas == idea_id).all()
#
#     def get_by_merged_idea(self, db: Session, merged_idea_id: int):
#         return db.query(Comment).filter(Comment.this_obj2merged_ideas == merged_idea_id).all()
#
#     def get_by_user(self, db: Session, user_id: int):
#         return db.query(Comment).filter(Comment.this__obj2users == user_id).all()
#
#     def get_replies(self, db: Session, parent_id: int):
#         return db.query(Comment).filter(Comment.parent_id == parent_id).all()
#
#     def get_root_comments(self, db: Session, idea_id: int = None, merged_idea_id: int = None):
#         query = db.query(Comment).filter(Comment.parent_id == -1)
#         if idea_id:
#             query = query.filter(Comment.this_obj2ideas == idea_id)
#         if merged_idea_id:
#             query = query.filter(Comment.this_obj2merged_ideas == merged_idea_id)
#         return query.all()

class CommentCRUD(BaseCRUD):

    def __init__(self, db_session):
        super().__init__(Comment, db_session)

    def create_comment(self, user_id, content, idea_id=None, merged_idea_id=None, parent_comment=-1):
        return self.create(
            this_obj2users=user_id,
            content=content,
            this_obj2ideas=idea_id,
            this_obj2merged_ideas=merged_idea_id,
            parent_comment=parent_comment
        )

    def get_by_idea(self, idea_id):
        return self.get_by_fields(this_obj2ideas=idea_id)

    def get_by_merged_idea(self, merged_idea_id):
        return self.get_by_fields(this_obj2merged_ideas=merged_idea_id)

    def get_by_user(self, user_id):
        return self.get_by_fields(this_obj2users=user_id)

    def get_replies(self, parent_comment_id):
        return self.get_by_fields(parent_comment=parent_comment_id)

