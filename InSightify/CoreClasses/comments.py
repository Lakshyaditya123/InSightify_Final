from InSightify.Common_files.base_crud import BaseCRUD
from InSightify.db_server.app_orm import Comment


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

