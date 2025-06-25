from InSightify.Common_files.response import ResponseHandler
from InSightify.CoreClasses import VoteCRUD
from InSightify.db_server.Flask_app import dbsession

'''user, idea, merged idea, votes, comments, tags'''

class VoteHelper:
    def __init__(self):
        self.vote_crud = VoteCRUD(dbsession)
        self.session = dbsession
        self.response = ResponseHandler()

    def update_vote(self, vote):
        if vote['user_id'] and vote['vote_type'] and (vote['idea_id'] or vote['comment_id']):
            check = self.vote_crud.update_vote(**vote)
            if type(check)!=str:
                self.response.get_response(0, "Idea created successfully")
            else:
                self.response.get_response(500, "Internal Server Error")
        else:
            self.response.get_response(400, "user_id, subject and content are required")
        return self.response.send_response()

    def vote_display(self, vote):
        vote_cnt = self.vote_crud.get_vote_count(**vote)
        # vote type for that user
        if type(vote_cnt) != str:
            if vote_cnt:
                self.response.get_response(0, "Found votes", data_rec=vote_cnt)
            else:
                self.response.get_response(400, "No votes found")
        else:
            self.response.get_response(500, "Internal Server Error")
        return self.response.send_response()


