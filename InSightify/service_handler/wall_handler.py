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

    def load_my_space(self, user_id):
        my_ideas = self.idea_crud.get_by_user(**user_id)
        if my_ideas["errCode"] == 0:
            if my_ideas["obj"]:
                self.response.get_response(0, "Found My ideas Successfully", data=self.idea_crud.convert_to_dict_list(my_ideas["obj"]))  # pass token here
            else:
                self.response.get_response(2, "No Ideas Found")
        else:
            self.response.get_response(500, "Internal Server Error")
        return self.response.send_response()

    def load_wall_with_child(self, status):
        all_ideas = self.idea_crud.get_all_ideas_with_details(**status)# remove child ideas
        all_merged_ideas = self.merged_idea_crud.get_merged_ideas_with_users()
        if all_ideas or all_merged_ideas:
            result={"all_ideas": all_ideas["obj"]if all_ideas else [], "all_merged_ideas": all_merged_ideas["obj"] if all_merged_ideas else []}
            self.response.get_response(0, "Found all ideas Successfully", data_rec=result)  # pass token here
        else:
            self.response.get_response(2, "No Ideas Found")
        return self.response.send_response()