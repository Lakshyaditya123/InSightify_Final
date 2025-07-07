from InSightify.Common_files.response import ResponseHandler
from InSightify.CoreClasses import TagCRUD
from InSightify.db_server.Flask_app import dbsession

class TagHelper:
    def __init__(self):
        self.tag_crud = TagCRUD(dbsession)
        self.session = dbsession
        self.response = ResponseHandler()

    def add_tag(self, tag):
        tag.setdefault("tag_desc", "No description Available") # handle if this is none then
        if tag["name"] and tag["tag_desc"]:
            self.tag_crud.create_tag(**tag)
            if self.tag_crud.commit_it()["errCode"]:
                self.response.get_response(500, "Internal Server Error")
            else:
                self.response.get_response(0, "tag created successfully")
        else:
            self.response.get_response(400, "name and tag_desc are required")
        return self.response.send_response()

    def tag_display(self, tag_id):
        tag=self.tag_crud.get_by_id(tag_id["tag_id"])["obj"]
        if tag:
            self.response.get_response(0,"Found tag", data_rec = self.tag_crud.convert_to_dict(tag))
        else:
            self.response.get_response(400, "No tag found")
        return self.response.send_response()
    # used in admin side...
    # used for AI
    # used for dropdown