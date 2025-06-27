from sqlalchemy import and_
from InSightify.Common_files.base_crud import BaseCRUD
from InSightify.db_server.app_orm import Vote

class VoteCRUD(BaseCRUD):

    def __init__(self, db_session):
        super().__init__(Vote, db_session)

    def create_vote(self, user_id, vote_type, idea_id=None, comment_id=None):
        return self.create(
            this_obj2users=user_id,
            vote_type=vote_type,
            this_obj2ideas=idea_id,
            this_obj2comments=comment_id
        )

    def get_user_vote_for_idea_or_comment(self, user_id, idea_id, comment_id):
        if comment_id:
            result= self.db_session.query(self.model).filter(
                and_(
                    self.model.this_obj2users == user_id,
                    self.model.this_obj2ideas == idea_id
                )
            ).first()
        elif idea_id:
            result= self.db_session.query(self.model).filter(
                and_(
                    self.model.this_obj2users == user_id,
                    self.model.this_obj2comments == idea_id
                )
            )
        else:
            result=None
        if result:
            self.db_response.get_response(errCode=0, msg="Found Records !", obj=result)
        else:
            self.db_response.get_response(errCode=0, msg="Records not found", obj=None)
        return self.db_response.send_response()

    def get_vote_count(self,idea_id=None, comment_id=None):
        get_vote= idea_id if idea_id is not None else comment_id
        votes = self.get_by_fields(this_obj2ideas=get_vote)["obj"]
        upvotes = sum(1 for vote in votes if vote.vote_type > 0)
        downvotes = sum(1 for vote in votes if vote.vote_type < 0)
        result= {"upvotes": upvotes, "downvotes": downvotes, "total": upvotes-downvotes}
        if sum(result.values())>0:
            self.db_response.get_response(errCode=0, msg="Found Records !", obj=result)
        else:
            self.db_response.get_response(errCode=0, msg="Records not found", obj=None)
        return self.db_response.send_response()


    def get_user_vote(self, user_id , idea_id = None, comment_id= None):
        query = self.db_session.query(Vote).filter(Vote.this_obj2users == user_id)
        if idea_id:
            query = query.filter(Vote.this_obj2ideas == idea_id)
        if comment_id:
            query = query.filter(Vote.this_obj2comments == comment_id)
        result=query.first()
        if result:
            self.db_response.get_response(errCode=0, msg="Found Records !", obj=result)
        else:
            self.db_response.get_response(errCode=0, msg="Records not found", obj=None)
        return self.db_response.send_response()

    def update_vote(self,user_id, vote_type, idea_id = None, comment_id = None):
        existing_vote = self.get_user_vote(user_id, idea_id, comment_id)["obj"]
        if existing_vote:
            return self.update(existing_vote.id, vote_type=vote_type)
        else:
            return self.create_vote(user_id, vote_type, idea_id, comment_id)

