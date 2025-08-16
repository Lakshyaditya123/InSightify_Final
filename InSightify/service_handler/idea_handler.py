from InSightify.Common_files.response import ResponseHandler
from InSightify.CoreClasses import *
from InSightify.db_server.Flask_app import dbsession, app_logger
from InSightify.celery_server.celery_app import app as celery_app

'''user, idea, merged idea, votes, comments, tags'''

class IdeaHelper:
    def __init__(self):
        self.user_crud = UserCRUD(dbsession)
        self.idea_crud = IdeaCRUD(dbsession)
        self.merge_idea_crud = MergedIdeaCRUD(dbsession)
        self.vote_crud = VoteCRUD(dbsession)
        self.comment_crud = CommentCRUD(dbsession)
        self.tag_crud = TagCRUD(dbsession)
        self.ideas_merged_ideas_crud = IdeasMergedIdeasCRUD(dbsession)
        self.session = dbsession
        self.response = ResponseHandler()
        self.logger = app_logger

    def add_idea(self, data):
        idea=data.get("idea")
        tags_list=data.get("tags_list")
        refine_content=data.get("refine_content")
        idea.setdefault("title","untitled")
        idea.setdefault("tags_list",[])
        idea.get("status", 0)
        idea.get("parent_idea")
        idea.get("refine_content")
        idea.get("link")
        idea.get("file_path")
        if idea.get("user_id") and idea.get("subject") and idea.get("content"):
            if refine_content:
                idea["refine_content"]=refine_content
            idea=self.idea_crud.create_idea(**idea)
            if self.user_crud.commit_it()["errCode"]:
                self.response.get_response(500, "Internal Server Error")
            else:
                celery_app.send_task('tags_worker', args=[idea["obj"].id, tags_list])
                self.response.get_response(0, "Idea created successfully")
        else:
            self.response.get_response(400, "user_id, subject and content are required")
        return self.response.send_response()

    def idea_display(self, data):
        if data.get("idea_id"):
            idea_with_details=self.idea_crud.get_all_ideas_with_details(get_one=True,user_id= data.get("user_id"), idea_id=data.get("idea_id"))
        else:
            idea_with_details=self.merge_idea_crud.get_merged_ideas_with_users(get_one=True, user_id= data.get("user_id"), merged_idea_id=data.get("merged_idea_id"))
        idea_obj=idea_with_details["obj"][0]
        if idea_with_details["errCode"]:
            self.response.get_response(500, f"Internal Server Error: {idea_with_details['msg']}")
        elif idea_obj:
            self.response.get_response(0,"Found Idea", data_rec = idea_obj)
        else:
            self.response.get_response(400, "No idea found")
        return self.response.send_response()

    def update_idea_status(self, data):
        if (data.get("idea_id") or data.get("merged_idea_id")) and data.get("status"):
            if data.get("idea_id"):
                if data.get("update_idea_tags") and data.get("tags_list",[]):
                    self.idea_crud.update_tags(data.get("idea_id"), data.get("tags_list"))
                idea=self.idea_crud.update_status(data.get("idea_id"),  data.get("status"))
                if self.idea_crud.commit_it()["errCode"]:
                    self.response.get_response(500, "Internal Server Error")
                else:
                    self.response.get_response(0, "Idea status updated successfully",data_rec=self.idea_crud.convert_to_dict(idea["obj"]))
            else:
                if data.get("merged_idea_details"):
                    merged_idea_data=data.get("merged_idea_details")
                    merged_idea_data.pop("status")
                    merged_idea_data.pop("comments_count")
                    merged_idea_data.pop("created_at")
                    tags_list=merged_idea_data.pop("tags_list")
                    tags_list_ids=[tag["id"] for tag in tags_list]
                    removed_idea_ids=data.get("removed_idea_ids",[])
                    print(merged_idea_data)
                    print(removed_idea_ids)
                    self.logger.info(f"merged_idea_data: {merged_idea_data}")
                    self.logger.info(f"removed_idea_ids: {removed_idea_ids}")
                    if removed_idea_ids:
                        self.ideas_merged_ideas_crud.unlink_some_ideas(merged_idea_data.get("id"), removed_idea_ids)
                        if self.ideas_merged_ideas_crud.commit_it()["errCode"]:
                            self.response.get_response(500, "Internal Server Error")
                            self.logger.info("error in unlinking some ideas from merged idea")

                        else:
                            self.logger.info("Successfully unlinked some ideas from merged idea")
                            new_merged_idea = self.merge_idea_crud.update_merged_ideas(**merged_idea_data, status=1, tags_list=tags_list_ids)["obj"]
                    else:
                        new_merged_idea = self.merge_idea_crud.update_merged_ideas(**merged_idea_data, status=1, tags_list=tags_list_ids)["obj"]
                else:
                    new_merged_idea = self.merge_idea_crud.update_status(merged_idea_id=data.get("merged_idea_id"), status=data.get("status"))["obj"]
                if self.merge_idea_crud.commit_it()["errCode"]:
                    self.response.get_response(500, "Internal Server Error")
                else:
                    child_ideas = self.ideas_merged_ideas_crud.get_ideas_in_merged_idea(merged_idea_id=new_merged_idea.id)["obj"]
                    child_idea_list=[idea.id_ideas for idea in child_ideas]
                    for idea_id in child_idea_list:
                        self.idea_crud.update_status(idea_id, 1)
                    if self.merge_idea_crud.commit_it()["errCode"] and  self.idea_crud.commit_it()["errCode"]:
                        self.response.get_response(500, "Internal Server Error")
                    else:
                        self.response.get_response(0, "Idea status updated successfully", data_rec=self.merge_idea_crud.convert_to_dict(new_merged_idea))
        else:
            self.response.get_response(400, "idea_id or merged_idea_id and status are required")
        return self.response.send_response()















