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
        idea["title"] = idea["title"] if idea.get("title") else "untitled" # handle for multiple untitled
        idea["tags_list"] = idea["tags_list"] if idea.get("tags_list") else [] # handle if this is none then
        idea["refine_content"] = idea["refine_content"] if idea.get("refine_content") else None
        idea["link"] = idea["link"] if idea.get("link") else None
        idea["file_path"] = idea["file_path"] if idea.get("file_path") else None
        if idea["user_id"] and idea["subject"] and idea["content"]:
            self.idea_crud.create_idea(**idea)
            if self.user_crud.commit_it()["errCode"]:
                self.response.get_response(500, "Internal Server Error")
            else:
                self.response.get_response(0, "Idea created successfully")
        else:
            self.response.get_response(400, "user_id, subject and content are required")
            # Call Ai merged here
            # Find relevant tags here,
            # put tags and pray to god things work out...
            # have to see if the tag that has been added by the user is already there or not... and add it here
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














