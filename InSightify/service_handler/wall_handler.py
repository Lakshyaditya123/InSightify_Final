from InSightify.Common_files.response import ResponseHandler
from InSightify.CoreClasses.ideas import IdeaCRUD
from InSightify.CoreClasses.merged_ideas import MergedIdeaCRUD
from InSightify.db_server.Flask_app import dbsession


class WallHelper:
    def __init__(self):
        self.idea_crud = IdeaCRUD(dbsession)
        self.merged_idea_crud = MergedIdeaCRUD(dbsession)
        self.response=ResponseHandler()
        self.session=dbsession

    def load_wall(self,data=None, user="user"):
        if user=="user":
            all_ideas = self.idea_crud.get_all_ideas_with_details(user_id=data.get("user_id"))["obj"]
            all_merged_ideas = self.merged_idea_crud.get_merged_ideas_with_users(data.get("user_id"))["obj"]
            my_ideas = self.idea_crud.get_by_user(data.get("user_id"))["obj"]
        else:
            all_ideas = self.idea_crud.get_all_ideas_with_details(status=0)["obj"]
            all_merged_ideas = self.merged_idea_crud.get_merged_ideas_with_users(status=0)["obj"]
            my_ideas=None
        if all_ideas or all_merged_ideas or my_ideas:
            result={"all_ideas": all_ideas if all_ideas else [], "all_merged_ideas": all_merged_ideas if all_merged_ideas else [], "all_my_ideas": my_ideas if my_ideas and user=="user" else []}
            self.response.get_response(0, "Found all ideas Successfully", data_rec=result)
        else:
            self.response.get_response(2, "No Ideas Found")
        return self.response.send_response()
