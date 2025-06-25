from InSightify.Common_files.response import ResponseHandler
from InSightify.CoreClasses.ideas import IdeaCRUD
from InSightify.CoreClasses.users import UserCRUD
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
        if type(my_ideas) != str:
            if my_ideas:
                self.response.get_response(0, "Found My ideas Successfully", data=self.idea_crud.convert_to_dict_list(my_ideas))  # pass token here
            else:
                self.response.get_response(2, "No Ideas Found")
        else:
            self.response.get_response(500, "Internal Server Error")
        self.response.send_response()

    def load_wall(self, status):
        all_ideas = self.idea_crud.get_by_status(**status) # remove child ideas
        all_merged_ideas=self.merged_idea_crud.get_all(limit=-1) # list of dict pass krni hai for user and pf
        if type(all_ideas)!=str and type(all_merged_ideas)!=str:
            total_ideas = self.idea_crud.convert_to_dict_list(all_ideas)
            total_ideas +=self.merged_idea_crud.convert_to_dict_list(all_merged_ideas)
            if total_ideas:
                self.response.get_response(0, "Found My ideas Successfully", data=total_ideas)  # pass token here
            else:
                self.response.get_response(2, "No Ideas Found")
        else:
            self.response.get_response(500, "Internal Server Error")
        self.response.send_response()

    # all the response via data and that too nested when we are handling the versions else just a list of dict
    # filters and tag groupings
    # load admin
    # search wall

    # make chages for filter by status

    # user idea details vote(vote count, vote_type)
    # vote type for that user