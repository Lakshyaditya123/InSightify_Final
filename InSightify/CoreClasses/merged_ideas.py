from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from InSightify.Common_files.base_crud import BaseCRUD
from InSightify.db_server.app_orm import MergedIdea, Idea


class MergedIdeaCRUD(BaseCRUD):

    def __init__(self, db_session):
        super().__init__(MergedIdea, db_session)

    def create_merged_idea(self, title, subject, content, tags_list):
        return self.create(
            title=title,
            subject=subject,
            content=content,
            tags_list=tags_list
        )
    def update_merged_ideas(self, merged_idea_id, title, subject, content, tags_list):
        return self.update(
            id=merged_idea_id,
            title=title,
            subject=subject,
            content=content,
            tags_list=tags_list
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

    def get_merged_ideas_with_users(self, get_one=False, merged_idea_id=None):
        if get_one:
            merged_ideas = [self.db_session.query(MergedIdea).options(
                joinedload(MergedIdea.ideas)).filter(MergedIdea.id == merged_idea_id).first()]
            if not merged_ideas:
                self.db_response.get_response(
                    errCode=0,
                    msg="No merged ideas found with the specified status",
                    obj=[]
                )
                return self.db_response.send_response()
        else:
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


    def find_similar_merged_ideas(self, idea: Idea):
        if not idea or not idea.tags_list:
            self.db_response.get_response(errCode=0, msg="No idea found", obj=None)
        else:
            input_tags = set(idea.tags_list)

            # Fetch all merged ideas with at least one overlapping tag
            merged_ideas = (
                self.db_session.query(MergedIdea)
                .filter(MergedIdea.tags_list.overlap(idea.tags_list))
                .all()
            )
            # Optional: Apply more than 50% overlap logic
            similar_merged_ideas = []
            for m in merged_ideas:
                if not m.tags_list or m.id==idea.id:
                    continue
                overlap = input_tags.intersection(set(m.tags_list))
                ratio = len(overlap) / len(input_tags)
                if ratio > 0.5:
                    similar_merged_ideas.append(m)
            self.db_response.get_response(errCode=0, msg="Similar merged ideas found successfully!", obj=similar_merged_ideas)
        return self.db_response.send_response()
