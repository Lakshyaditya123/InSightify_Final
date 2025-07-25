from sqlalchemy import and_
from InSightify.Common_files.base_crud import BaseCRUD
from InSightify.db_server.app_orm import Vote

class VoteCRUD(BaseCRUD):

    def __init__(self, db_session):
        super().__init__(Vote, db_session)

    def create_vote(self, user_id, vote_type, idea_id, merged_idea_id ,comment_id):
        return self.create(
            this_obj2users=user_id,
            vote_type=vote_type,
            this_obj2ideas=idea_id,
            this_obj2merged_ideas=merged_idea_id,
            this_obj2comments=comment_id
        )

    def get_user_vote(self, user_id, idea_id=None, comment_id=None, merged_idea_id=None):
        filters = [Vote.this_obj2users == user_id]
        votes = []

        if idea_id:
            filters.append(Vote.this_obj2ideas == idea_id)
            votes = self.get_by_fields(this_obj2ideas=idea_id)["obj"]
        elif comment_id:
            filters.append(Vote.this_obj2comments == comment_id)
            votes = self.get_by_fields(this_obj2comments=comment_id)["obj"]
        elif merged_idea_id:
            filters.append(Vote.this_obj2merged_ideas == merged_idea_id)
            votes = self.get_by_fields(this_obj2merged_ideas=merged_idea_id)["obj"]

        result = self.db_session.query(Vote).filter(*filters).first()

        if votes:
            upvotes = sum(1 for vote in votes if vote.vote_type > 0)
            downvotes = sum(1 for vote in votes if vote.vote_type < 0)

            final_result = {
                "user_vote_details":{
                "vote_id": result.id if result else None,
                "user_id": result.this_obj2users if result else None,
                "vote_type": result.vote_type if result else None,
                },
                "vote_details": {
                "upvotes": upvotes,
                "downvotes": downvotes,
                "total": upvotes - downvotes
            }
            }
            self.db_response.get_response(errCode=0, msg="Found Records!", obj={"vote_details":final_result})
        else:
            self.db_response.get_response(errCode=0, msg="Records not found", obj=None)

        return self.db_response.send_response()

    def update_vote(self,user_id, vote_type, idea_id = None, comment_id = None, merged_idea_id=None):
        existing_vote = self.get_user_vote(user_id, idea_id, comment_id, merged_idea_id)["obj"]
        if existing_vote:
            if existing_vote["vote_details"]["user_vote_details"]["user_id"]:
                return self.update(existing_vote["vote_details"]["user_vote_details"]["vote_id"], vote_type=vote_type)
        return self.create_vote(user_id, vote_type, idea_id, merged_idea_id, comment_id)

