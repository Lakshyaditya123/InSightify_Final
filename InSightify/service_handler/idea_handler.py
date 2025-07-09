from InSightify.Common_files.response import ResponseHandler
from InSightify.CoreClasses import *
from InSightify.db_server.Flask_app import dbsession, app_logger
from InSightify.celery_server.celery_app import app as celery_app

'''user, idea, merged idea, votes, comments, tags'''

class IdeaHelper:
    def __init__(self):
        self.user_crud = UserCRUD(dbsession)
        self.idea_crud = IdeaCRUD(dbsession)
        self.merge_ideas_crud = MergedIdeaCRUD(dbsession)
        self.vote_crud = VoteCRUD(dbsession)
        self.comment_crud = CommentCRUD(dbsession)
        self.tag_crud = TagCRUD(dbsession)
        self.session = dbsession
        self.response = ResponseHandler()

    def add_idea(self, data):
        idea=data.get("idea")
        tags_list=data.get("tags_list")
        refine_content=data.get("refine_idea")
        idea.setdefault("title","untitled")
        idea.setdefault("tags_list",[])
        idea.get("parent_idea")
        idea.get("refine_content")
        idea.get("link")
        idea.get("file_path")
        if idea.get("user_id") and idea.get("subject") and idea.get("content"):
            if refine_content:
                idea["refine_content"]=refine_content["refine_content"]
            response=self.idea_crud.create_idea(**idea)
            if self.user_crud.commit_it()["errCode"]:
                self.response.get_response(500, "Internal Server Error")
            else:
                self.response.get_response(0, "Idea created successfully")
                celery_app.send_task('idea_worker', args=[response["obj"].id, tags_list])
        else:
            self.response.get_response(400, "user_id, subject and content are required")
        return self.response.send_response()

    # def idea_display(self, idea_id):
    #     idea=self.idea_crud.get_by_id(idea_id.get("idea_id"))["obj"]
    #     user=self.user_crud.get_by_id(idea.user_id)["obj"]
    #
    #     if idea:
    #         self.response.get_response(0,"Found Idea", data_rec = self.idea_crud.convert_to_dict(idea))
    #     else:
    #         self.response.get_response(400, "No idea found")
    #     return self.response.send_response()
    #     # pass username, pf pic and tag

    def idea_display(self, idea):
        if idea.get("idea_type")=="idea":
            idea_with_details=self.idea_crud.get_all_ideas_with_details(status=1, get_one=True, idea_id=idea.get("idea_id"))
        else:
            idea_with_details=self.merge_ideas_crud.get_merged_ideas_with_users(get_one=True, merged_idea_id=idea.get("merged_idea_id"))
        if idea_with_details["errCode"]:
            self.response.get_response(500, f"Internal Server Error: {idea_with_details['msg']}")
        elif idea_with_details["obj"]:
            self.response.get_response(0,"Found Idea", data_rec = idea_with_details["obj"][0])
        else:
            self.response.get_response(400, "No idea found")
        return self.response.send_response()
















