from sqlalchemy import or_, func, select
from sqlalchemy.orm import joinedload
from InSightify.Common_files.base_crud import BaseCRUD
from InSightify.db_server.Flask_app import app_logger
from InSightify.db_server.app_orm import Idea, Vote, Comment, Tag, MergedIdea
from InSightify.Common_files.config import config


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
        ideas=self.get_by_fields(this_obj2users=user_id)["obj"]
        final_ideas=[]
        if ideas:
            vote_map, comment_count_map = self.get_vote_and_comment_count(ideas)
            for idea in ideas:
                idea_votes = vote_map.get(idea.id, [])
                upvotes = sum(1 for v in idea_votes if v > 0)
                downvotes = sum(1 for v in idea_votes if v < 0)
                final_ideas.append({
                    "idea_id":idea.id,
                    "title":idea.title,
                    "subject":idea.subject,
                    "status":idea.status,
                    "comments_count": comment_count_map.get(idea.id, 0),
                    "total_votes": upvotes - downvotes
                })
            status_order = {1: 0, 0: 1, -1: 2}
            sorted_ideas = sorted(final_ideas, key=lambda x: status_order.get(x['status'], 3))
            self.db_response.get_response(errCode=0, msg="Found Record !", obj=sorted_ideas)
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

    def get_vote_and_comment_count(self,ideas):
        idea_ids = [idea.id for idea in ideas]
        votes = self.db_session.query(
            Vote.this_obj2ideas,
            Vote.vote_type
        ).filter(Vote.this_obj2ideas.in_(idea_ids)).all()
        vote_map = {}
        for idea_id_, vote_type in votes:
            vote_map.setdefault(idea_id_, []).append(vote_type)

        comment_counts = self.db_session.query(
            Comment.this_obj2ideas,
            func.count(Comment.id)
        ).filter(Comment.this_obj2ideas.in_(idea_ids), Comment.parent_comment==-1).group_by(Comment.this_obj2ideas).all()

        comment_count_map = dict(comment_counts)

        return vote_map,comment_count_map


    def get_all_ideas_with_details(self, user_id=None, status=1, get_one=False, idea_id=None):
        try:
            query = self.db_session.query(Idea).options(joinedload(Idea.user))
            if get_one:
                query = query.filter(Idea.id == idea_id)
                merged_ideas = []
            else:
                query = query.filter(Idea.status == status, ~Idea.merged_ideas.any())
                if status == 1:
                    merged_ideas = self.db_session.query(MergedIdea).options(
                        joinedload(MergedIdea.ideas)
                    ).filter(MergedIdea.status == 0).all()
                elif status == 0:
                    merged_ideas = self.db_session.query(MergedIdea).options(
                        joinedload(MergedIdea.ideas)
                    ).filter(MergedIdea.status == 0).all()
                else:
                    merged_ideas = []

            ideas = query.all()
            if merged_ideas:
                for merged_idea in merged_ideas:
                    ideas.extend(merged_idea.ideas)

            ideas = list(set(ideas))
            if not ideas:
                self.db_response.get_response(
                    errCode=0,
                    msg="No ideas found with the specified filters",
                    obj=[]
                )
                return self.db_response.send_response()
            vote_map, comment_count_map = self.get_vote_and_comment_count(ideas)
            result_list = []
            for idea in ideas:
                if idea.status==0 and status==1 and merged_ideas:
                    continue
                if idea.status==1 and status==0 and merged_ideas:
                    continue
                result = self.db_session.query(Vote).filter(Vote.this_obj2ideas == idea.id, Vote.this_obj2users==user_id).first()
                idea_votes = vote_map.get(idea.id, [])
                upvotes = sum(1 for v in idea_votes if v > 0)
                downvotes = sum(1 for v in idea_votes if v < 0)
                final_result = {
                    "user_vote_details": {
                        "vote_id": result.id if result else None,
                        "vote_type": result.vote_type if result else None,
                    },
                    "vote_details": {
                    "upvotes": upvotes,
                    "downvotes": downvotes,
                    "total": upvotes - downvotes
                }
                }if status else {}
                # fetch user_vote_details
                if get_one:
                    tags = [
                        {"id": t.id, "name":t.name, "description": t.tag_desc}
                        for t in self.db_session.query(Tag).filter(Tag.id.in_(idea.tags_list)).limit(7).all()
                    ]
                    result_list.append({
                        "user_details": {
                            "id": idea.user.id,
                            "name": idea.user.name,
                            "email": idea.user.email,
                            "profile_picture": idea.user.profile_picture,
                        } if idea.user else [],

                        "idea_details": {
                            "id": idea.id,
                            "title": idea.title,
                            "subject": idea.subject,
                            "content": idea.content,
                            "refine_content": idea.refine_content,
                            "status": idea.status,
                            "tags_list": tags,
                            "link": idea.link,
                            "file_path": idea.file_path,
                            "created_at": idea.create_datetime.isoformat(),
                            "comments_count": comment_count_map.get(idea.id, 0)
                        },
                        "vote_details":final_result
                    })
                else:
                    result_list.append({
                        "user_details": {
                            "id": idea.user.id,
                            "name": idea.user.name,
                            "profile_picture": idea.user.profile_picture,
                        } if idea.user else [],
                        "idea_details": {
                            "id": idea.id,
                            "title": idea.title,
                            "subject": idea.subject,
                            "status": idea.status,
                            "created_at": idea.create_datetime.isoformat(),
                            "comments_count": comment_count_map.get(idea.id, 0)
                        },
                        "vote_details":final_result
                    }
                    )

            self.db_response.get_response(
                errCode=0,
                msg=f"Successfully retrieved ideas with complete details!",
                obj=result_list
            )

        except Exception as e:
            app_logger.error(f"Error in get_all_ideas_with_details: {str(e)}")
            self.db_response.get_response(
                errCode=2,
                msg=f"Error retrieving ideas with details: {str(e)}",
                obj=None
            )

        return self.db_response.send_response()

    def find_similar_ideas(self, idea: Idea):
        if not idea or not idea.tags_list:
            self.db_response.get_response(errCode=0, msg="No idea found", obj=None)
        else:
            input_tags = set(idea.tags_list)
            other_ideas = (
                self.db_session.query(Idea)
                .filter(Idea.id != idea.id,Idea.status==1)
                # .filter(Idea.id != idea.id, Idea.status == 1)
                .filter(Idea.tags_list.overlap(idea.tags_list))
                .all()
            )
            similar_ideas = []
            for other in other_ideas:
                if not other.tags_list or other.id==idea.id:
                    continue
                overlap = input_tags.intersection(set(other.tags_list))
                ratio = len(overlap) / len(input_tags)
                if ratio >= config.SIMILARITY_RATIO:
                    similar_ideas.append(other)
            if similar_ideas:
                self.db_response.get_response(
                    errCode=0,
                    msg="Similar ideas found successfully!",
                    obj=similar_ideas)
            else:
                self.db_response.get_response(
                    errCode=0,
                    msg="No similar ideas found!",
                    obj=None)

        return self.db_response.send_response()


    def bulk_select_ideas(self, idea_list):
        self.db_session.execute(select(Idea).where(Idea.id.in_(idea_list))).scalars().all()
        self.db_response.get_response(errCode=0, msg="Found tags", obj=self.db_session.query(self.model))
        return self.db_response.send_response()
