from InSightify.Common_files.response import ResponseHandler
from InSightify.CoreClasses import CommentCRUD
from InSightify.db_server.Flask_app import dbsession

class CommentHelper:
    def __init__(self):
        self.comment_crud = CommentCRUD(dbsession)
        self.session = dbsession
        self.response = ResponseHandler()

    def add_comment(self,comment):
        comment["parent_comment"] = comment["parent_comment"] if comment.get("parent_comment") else -1
        comment["idea_id"] = comment["idea_id"] if comment.get("idea_id") else None
        comment["merged_idea_id"] = comment["merged_idea_id"] if comment.get("merged_idea_id") else None
        if comment["user_id"] and comment["content"]:
            if not (comment["idea_id"] and comment["merged_idea_id"]) and (comment["idea_id"] or comment["merged_idea_id"]):
                # There should be only one idea_id or merged_id
                self.comment_crud.create_comment(**comment)
                if self.comment_crud.commit_it()["errCode"]:
                    self.response.get_response(500, "Internal Server Error")
                else:
                    self.response.get_response(0, "Comment created successfully")
            else:
                self.response.get_response(400, "Either idea id or merged idea id is required")
        else:
            self.response.get_response(400, "user_id and content are required")
        return self.response.send_response()

    @staticmethod
    def format_comments(comments):
        for comment in comments:  # Adds another field Children
            comment["Children"] = []
        comment_map={comment["id"]: comment  for comment in comments}
        for comment in comments:
            p_id = comment["parent_comment"]
            if p_id !=-1:
                parent = comment_map.get(p_id)
                if parent:
                    parent["Children"].append(comment)
        return comments

    def comment_display(self, idea_ids):
        if not (idea_ids.get("idea_id") or idea_ids.get("merged_idea_id")):
            self.response.get_response(400, "Either idea id or merged idea id is required")
        else:
            if get_comms:= idea_ids.get("idea_id"):
                comments = self.comment_crud.get_by_idea(get_comms)["obj"]
            else:
                get_comms= idea_ids.get("merged_idea_id")
                comments = self.comment_crud.get_by_merged_idea(get_comms)["obj"]

            if comments:
                formated_comments = self.format_comments(self.comment_crud.convert_to_dict_list(comments))
                self.response.get_response(0, "Found Idea", data_rec=formated_comments)
            else:
                self.response.get_response(400, "No idea found")

        return self.response.send_response()

















