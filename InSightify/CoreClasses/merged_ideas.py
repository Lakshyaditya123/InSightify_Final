from sqlalchemy import or_
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
            self.db_response.get_response(errCode=0, msg="Found Records !", obj=result)
        else:
            self.db_response.get_response(errCode=0, msg="Records not found", obj=None)
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
                            "mob_number": user.mobile,
                            "bio": user.bio,
                            "profile_picture": user.profile_picture
                        })

                merged_idea_dict = {
                    "id": merged_idea.id,
                    "title": merged_idea.title,
                    "subject": merged_idea.subject,
                    "content": merged_idea.content,
                    "created_at": merged_idea.create_datetime.isoformat()
                }
                upvotes = sum(1 for vote in merged_idea.votes if vote.vote_type > 0)
                downvotes = sum(1 for vote in merged_idea.votes if vote.vote_type < 0)
                total_score = upvotes - downvotes
                vote_dict = {
                    "upvotes": upvotes,
                    "downvotes": downvotes,
                    "total_score": total_score
                }

                result.append({
                    "users": users_list,
                    "merged_idea": merged_idea_dict,
                    "vote":vote_dict
                })

                self.db_response.get_response(errCode=0, msg="Found Records !", obj=result)
        else:
            self.db_response.get_response(errCode=0, msg="Records not found", obj=None)

        return self.db_response.send_response()