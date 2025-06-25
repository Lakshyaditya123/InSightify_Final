from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from InSightify.Common_files.base_crud import BaseCRUD
from InSightify.db_server.app_orm import Vote


# class VoteCRUD(BaseCRUD):
#
#     def __init__(self):
#         super().__init__(Vote)
#
#     def create_vote(self, db: Session, user_id: int, vote_type: int,
#                     idea_id: int = None, comment_id: int = None):
#         return self.create(
#             db, this_obj2users=user_id, vote_type=vote_type,
#             this_obj2ideas=idea_id, this_obj2comments=comment_id
#         )
#
#     def get_user_vote(self, db: Session, user_id: int, idea_id: int = None, comment_id: int = None):
#         query = db.query(Vote).filter(Vote.this_obj2users == user_id)
#         if idea_id:
#             query = query.filter(Vote.this_obj2ideas == idea_id)
#         if comment_id:
#             query = query.filter(Vote.this_obj2comments == comment_id)
#         return query.first()
#
#     def get_votes_by_idea(self, db: Session, idea_id: int):
#         return db.query(Vote).filter(Vote.this_obj2ideas == idea_id).all()
#
#     def get_votes_by_comment(self, db: Session, comment_id: int):
#         return db.query(Vote).filter(Vote.this_obj2comments == comment_id).all()
#
#     def count_votes(self, db: Session, idea_id: int = None, comment_id: int = None, vote_type: int = None):
#         query = db.query(Vote)
#         if idea_id:
#             query = query.filter(Vote.this_obj2ideas == idea_id)
#         if comment_id:
#             query = query.filter(Vote.this_obj2comments == comment_id)
#         if vote_type is not None:
#             query = query.filter(Vote.vote_type == vote_type)
#         return query.count()
#
#     def update_vote(self, db: Session, user_id: int, vote_type: int,
#                     idea_id: int = None, comment_id: int = None):
#         existing_vote = self.get_user_vote(db, user_id, idea_id, comment_id)
#         if existing_vote:
#             return self.update(db, existing_vote.id, vote_type=vote_type)
#         else:
#             return self.create_vote(db, user_id, vote_type, idea_id, comment_id)


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

    def get_user_vote_for_idea(self, user_id, idea_id):
        try:
            return self.db_session.query(self.model).filter(
                and_(
                    self.model.this_obj2users == user_id,
                    self.model.this_obj2ideas == idea_id
                )
            ).first()
        except SQLAlchemyError as e:
            print(f"Error getting user vote for idea: {str(e)}")
            return None

    def get_user_vote_for_comment(self, user_id, comment_id):
        try:
            return self.db_session.query(self.model).filter(
                and_(
                    self.model.this_obj2users == user_id,
                    self.model.this_obj2comments == comment_id
                )
            ).first()
        except SQLAlchemyError as e:
            print(f"Error getting user vote for comment: {str(e)}")
            return None

    def get_vote_count(self, idea_id=None, comment_id=None):
        try:
            if get_vote := bool(idea_id) ^ bool(comment_id):
                votes = self.get_by_fields(this_obj2ideas=get_vote)
                upvotes = sum(1 for vote in votes if vote.vote_type > 0)
                downvotes = sum(1 for vote in votes if vote.vote_type < 0)
                return {"upvotes": upvotes, "downvotes": downvotes, "total": upvotes-downvotes}
        except Exception as e:
            print(f"Error getting vote count for idea: {str(e)}")
            return {"upvotes": 0, "downvotes": 0, "total": 0}

    def get_user_vote(self, user_id , idea_id = None, comment_id= None):
        query = self.db_session.query(Vote).filter(Vote.this_obj2users == user_id)
        if idea_id:
            query = query.filter(Vote.this_obj2ideas == idea_id)
        if comment_id:
            query = query.filter(Vote.this_obj2comments == comment_id)
        return query.first()

    def update_vote(self,user_id, vote_type, idea_id = None, comment_id = None):
        existing_vote = self.get_user_vote(user_id, idea_id, comment_id)
        if existing_vote:
            return self.update(existing_vote.id, vote_type=vote_type)
        else:
            return self.create_vote(user_id, vote_type, idea_id, comment_id)

