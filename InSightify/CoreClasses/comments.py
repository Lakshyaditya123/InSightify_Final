from sqlalchemy.orm import joinedload

from InSightify.Common_files.base_crud import BaseCRUD
from InSightify.db_server.app_orm import Comment, User, Vote


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

    def get_by_idea(self, user_id, idea_id=None, merged_idea_id=None):
        query = self.db_session.query(Comment).options(
            joinedload(Comment.user),
            joinedload(Comment.votes)
        )

        if idea_id:
            query = query.filter(Comment.this_obj2ideas == idea_id)
        else:
            query = query.filter(Comment.this_obj2merged_ideas == merged_idea_id)

        comments = query.all()  # ✅ Only call `.all()` once here

        comments_send = [{
            "comment_id": comment.id,
            "user_id": comment.this_obj2users,
            "user_name": comment.user.name,
            "user_profile_picture":comment.user.profile_picture,
            "idea_id": comment.this_obj2ideas,
            "merged_idea_id": comment.this_obj2merged_ideas,
            "content": comment.content,
            "parent_comment": comment.parent_comment,
            "likes": sum(1 for vote in comment.votes if vote.vote_type == 1),
            "user_vote": next((vote.vote_type for vote in comment.votes if vote.this_obj2users == user_id), None),
            "created_at": comment.create_datetime.isoformat()
        } for comment in comments]

        if not comments_send:
            self.db_response.get_response(errCode=0, msg="No comments found for the specified idea", obj=None)
        else:
            self.db_response.get_response(errCode=0, msg="Found all comments!", obj=comments_send)

        return self.db_response.send_response()

    def get_by_user(self, user_id):
        return self.get_by_fields(this_obj2users=user_id)

    def get_replies(self, parent_comment_id):
        return self.get_by_fields(parent_comment=parent_comment_id)

