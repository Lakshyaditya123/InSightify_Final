from InSightify.Common_files.response import ResponseHandler
from InSightify.CoreClasses import CommentCRUD
from InSightify.db_server.Flask_app import dbsession

class CommentHelper:
    def __init__(self):
        self.comment_crud = CommentCRUD(dbsession)
        self.session = dbsession
        self.response = ResponseHandler()

    def add_comment(self,comment):
        comment.setdefault("parent_comment", -1)
        comment.setdefault("idea_id")
        comment.setdefault("merged_idea_id")
        if comment["user_id"] and comment["content"]:
            if not (comment["idea_id"] and comment["merged_idea_id"]) and (comment["idea_id"] or comment["merged_idea_id"]):
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
    def format_comments(comments_send):
        for comment_send in comments_send:
            comment_send["replies"] = []
        comment_map={comment_send["comment_id"]: comment_send  for comment_send in comments_send}
        for comment_send in comments_send:
            p_id = comment_send["parent_comment"]
            if p_id !=-1:
                parent = comment_map.get(p_id)
                if parent:
                    parent["replies"].append(comment_send)
        return [comment_send for comment_send in comments_send if comment_send["parent_comment"] == -1]

    def comment_display(self, data):
        if not (data.get("idea_id") or data.get("merged_idea_id")):
            self.response.get_response(400, "Either idea id or merged idea id is required")
        else:
            if get_comms:= data.get("idea_id"):
                comments = self.comment_crud.get_by_idea(idea_id=get_comms, user_id=data.get("user_id"))["obj"]
            else:
                get_comms= data.get("merged_idea_id")
                comments = self.comment_crud.get_by_idea(merged_idea_id=get_comms, user_id=data.get("user_id"))["obj"]
            if comments:
                formated_comments = self.format_comments(comments)
                self.response.get_response(0, "Found comment", data=formated_comments)
            else:
                self.response.get_response(400, "No comment found!")

        return self.response.send_response()

















