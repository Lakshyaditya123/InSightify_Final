from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from InSightify.Common_files.base_crud import BaseCRUD
from InSightify.db_server.Flask_app import app_logger
from InSightify.db_server.app_orm import Idea, Vote, Comment


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

    def get_by_status_without_ver_without_child(self, status=1):
        return self.get_by_fields(status=status, parent_idea=-1)

    def get_by_tags(self, tag_ids):
        result = self.db_session.query(self.model).filter(
            self.model.tags_list.op('&&')(tag_ids)
        ).all()
        if result:
            self.db_response.get_response(errCode=0, msg="Found Record !", obj=result)
        else:
            self.db_response.get_response(errCode=0, msg="Record not found", obj=None)
        return self.db_response.send_response()

    def update_status(self, idea_id, status):
        return self.update(idea_id, status=status)

    def update_tags(self, idea_id, tags_list):
        return self.update(idea_id, tags_list=tags_list)

    def search_ideas(self, search_term):
        result = self.db_session.query(self.model).filter(
            or_(
                self.model.title.ilike(f"%{search_term}%"),
                self.model.subject.ilike(f"%{search_term}%"),
                self.model.content.ilike(f"%{search_term}%"))).all()
        if result:
            self.db_response.get_response(errCode=0, msg="Found Record !", obj=result)
        else:
            self.db_response.get_response(errCode=0, msg="Record not found", obj=None)
        return self.db_response.send_response()

    def get_all_ideas_with_details(self, status=1):
        try:
            ideas = self.db_session.query(Idea).options(
                joinedload(Idea.user)
            ).filter(Idea.status == status).all()
            if not ideas:
                self.db_response.get_response(
                    errCode=0,
                    msg="No ideas found with the specified status",
                    obj=[]
                )
                return self.db_response.send_response()

            result_list = []

            for idea in ideas:
                # Get all votes for this idea
                idea_votes = self.db_session.query(Vote).filter(
                    Vote.this_obj2ideas == idea.id
                ).all()

                # Get comments count for this idea
                comments_count = self.db_session.query(Comment).filter(
                    Comment.this_obj2ideas == idea.id
                ).count()

                # Calculate vote statistics
                upvotes = sum(1 for vote in idea_votes if vote.vote_type > 0)
                downvotes = sum(1 for vote in idea_votes if vote.vote_type < 0)
                total_score = upvotes - downvotes

                # Build the simplified dictionary for this idea
                idea_dict = {
                    "user_details": [{
                        "id": idea.user.id,
                        "name": idea.user.name,
                        "email": idea.user.email,
                        "profile_picture": idea.user.profile_picture,
                        "bio": idea.user.bio
                    } if idea.user else {}],

                    "idea_details": {
                        "id": idea.id,
                        "title": idea.title,
                        "subject": idea.subject,
                        "content": idea.content,
                        "refine_content": idea.refine_content,
                        "tags_list": idea.tags_list,
                        "link": idea.link,
                        "file_path": idea.file_path,
                        "parent_idea": idea.parent_idea,
                        "created_at": idea.create_datetime.isoformat(),
                        "comments_count": comments_count
                    },

                    "vote_details": {
                        "upvotes": upvotes,
                        "downvotes": downvotes,
                        "total_score": total_score,
                        "total_voters": len(idea_votes)
                    }
                }

                result_list.append(idea_dict)

            self.db_response.get_response(
                errCode=0,
                msg=f"Successfully retrieved {len(result_list)} ideas with complete details!",
                obj=result_list
            )

        except Exception as e:
            app_logger.error(f"Error in get_all_ideas_with_details_simplified: {str(e)}")
            self.db_response.get_response(
                errCode=2,
                msg=f"Error retrieving ideas with details: {str(e)}",
                obj=None
            )
        return self.db_response.send_response()