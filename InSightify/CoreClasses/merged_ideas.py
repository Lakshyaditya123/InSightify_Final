from sqlalchemy import or_, func
from sqlalchemy.orm import joinedload
from InSightify.Common_files.base_crud import BaseCRUD
from InSightify.db_server.Flask_app import app_logger
from InSightify.db_server.app_orm import MergedIdea, Idea, Tag, Vote, Comment


class MergedIdeaCRUD(BaseCRUD):

    def __init__(self, db_session):
        super().__init__(MergedIdea, db_session)

    def create_merged_idea(self, title, subject, content, tags_list, status=0):
        return self.create(
            title=title,
            subject=subject,
            content=content,
            tags_list=tags_list,
            status=status
        )
    def update_merged_ideas(self, merged_idea_id, title, subject, content, tags_list, status=0):
        return self.update(
            id=merged_idea_id,
            title=title,
            subject=subject,
            content=content,
            tags_list=tags_list,
            status = status
        )

    def get_vote_and_comment_count(self, merged_ideas):
        idea_ids = [idea.id for idea in merged_ideas]
        # Bulk fetch votes
        votes = self.db_session.query(
            Vote.this_obj2merged_ideas,
            Vote.vote_type
        ).filter(Vote.this_obj2merged_ideas.in_(idea_ids)).all()
        # Organize votes per idea
        vote_map = {}
        for idea_id_, vote_type in votes:
            vote_map.setdefault(idea_id_, []).append(vote_type)

        # Bulk fetch comment counts
        comment_counts = self.db_session.query(
            Comment.this_obj2merged_ideas,
            func.count(Comment.id)
        ).filter(Comment.this_obj2merged_ideas.in_(idea_ids), Comment.parent_comment==-1).group_by(Comment.this_obj2merged_ideas).all()

        comment_count_map = dict(comment_counts)

        return vote_map, comment_count_map

    def update_status(self, merged_idea_id, status):
        return self.update(merged_idea_id, status=status)

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

    def get_merged_ideas_with_users(self, user_id=None, status=1, get_one=False, merged_idea_id=None):
        try:
            query = self.db_session.query(MergedIdea).options(
                joinedload(MergedIdea.ideas).joinedload(Idea.user)
            )

            if get_one:
                query = query.filter(MergedIdea.id == merged_idea_id)
            else:
                query = query.filter(MergedIdea.status == status)

            merged_ideas = query.all()

            if not merged_ideas:
                self.db_response.get_response(
                    errCode=0,
                    msg="No merged ideas found with the specified status or ID",
                    obj=[]
                )
                return self.db_response.send_response()

            vote_map, comment_count_map = self.get_vote_and_comment_count(merged_ideas)
            result_list = []

            for merged_idea in merged_ideas:
                result = self.db_session.query(Vote).filter(
                    Vote.this_obj2merged_ideas == merged_idea.id,
                    Vote.this_obj2users == user_id
                ).first()

                idea_votes = vote_map.get(merged_idea.id, [])
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
                } if status else {}

                users_ideas_list = []
                for idea in merged_idea.ideas:
                    user = idea.user
                    users_ideas_list.append({
                        "user_details": {
                            "id": user.id,
                            "name": user.name,
                            "profile_picture": user.profile_picture
                        },
                        "idea_details": {
                            "id": idea.id,
                            "title": idea.title,
                            "subject": idea.subject
                        }
                    })

                if get_one:
                    tags = [
                        {"id": t.id, "name": t.name, "description": t.tag_desc}
                        for t in self.db_session.query(Tag).filter(Tag.id.in_(merged_idea.tags_list)).limit(7).all()
                    ]
                    result_list.append({
                        "user_idea_details": users_ideas_list,
                        "merged_idea_details": {
                            "id": merged_idea.id,
                            "title": merged_idea.title,
                            "subject": merged_idea.subject,
                            "content": merged_idea.content,
                            "status": merged_idea.status,
                            "tags_list": tags,
                            "created_at": merged_idea.create_datetime.isoformat(),
                            "comments_count": comment_count_map.get(merged_idea.id, 0)
                        },
                        "vote_details": final_result
                    })
                else:
                    result_list.append({
                        "user_idea_details": users_ideas_list,
                        "merged_idea_details": {
                            "id": merged_idea.id,
                            "title": merged_idea.title,
                            "subject": merged_idea.subject,
                            "comments_count": comment_count_map.get(merged_idea.id, 0)
                        },
                        "vote_details": final_result
                    })

            self.db_response.get_response(
                errCode=0,
                msg="Successfully retrieved ideas with complete details!",
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

    def find_similar_merged_ideas(self, idea: Idea):
        if not idea or not idea.tags_list:
            self.db_response.get_response(errCode=0, msg="No idea found", obj=None)
        else:
            input_tags = set(idea.tags_list)

            # Fetch all merged ideas with at least one overlapping tag
            merged_ideas = (
                self.db_session.query(MergedIdea)
                .filter(MergedIdea.status == 1)
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
                if ratio > 0:
                    similar_merged_ideas.append(m)
            self.db_response.get_response(errCode=0, msg="Similar merged ideas found successfully!", obj=similar_merged_ideas)
        return self.db_response.send_response()
