from InSightify.Common_files.response import ResponseHandler
from InSightify.CoreClasses import *
from InSightify.db_server.Flask_app import dbsession

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

    def add_idea(self, idea):
        idea.setdefault("title","untitled")
        idea.setdefault("tags_list", [])
        idea.setdefault("refine_content")
        idea.setdefault("link")
        idea.setdefault("file_path")
        if idea["user_id"] and idea["subject"] and idea["content"]:
            self.idea_crud.create_idea(**idea)
            if self.user_crud.commit_it()["errCode"]:
                # here i want to pass data to celery worker so that it can do the task in background

                self.response.get_response(500, "Internal Server Error")
            else:
                self.response.get_response(0, "Idea created successfully")
        else:
            self.response.get_response(400, "user_id, subject and content are required")
        return self.response.send_response()

    def idea_display(self, idea_id):
        idea=self.idea_crud.get_by_id(idea_id["idea_id"])["obj"]
        if idea:
            self.response.get_response(0,"Found Idea", data_rec = self.idea_crud.convert_to_dict(idea))
        else:
            self.response.get_response(400, "No idea found")
        return self.response.send_response()
        # pass username, pf pic and tags





# handle for idea merger, idea refinement and idea tags here by calling ai_handler here...














