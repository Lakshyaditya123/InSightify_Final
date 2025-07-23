from InSightify.Common_files.response import ResponseHandler
from InSightify.CoreClasses import TagCRUD
from InSightify.db_server.Flask_app import dbsession

class TagHelper:
    def __init__(self):
        self.tag_crud = TagCRUD(dbsession)
        self.session = dbsession
        self.response = ResponseHandler()

    def add_tag(self, tag):
        tag.setdefault("tag_desc", "No description Available")
        if tag["name"] and tag["description"]:
            created_tag=self.tag_crud.create_tag(**tag)
            if self.tag_crud.commit_it()["errCode"]:
                self.response.get_response(500, "Internal Server Error")
            else:
                self.response.get_response(0, "tag created successfully", data_rec=self.tag_crud.convert_to_dict(created_tag["obj"]))
        else:
            self.response.get_response(400, "name and tag_desc are required")
        return self.response.send_response()

    def update_tag(self, tag):
        if tag["tag_id"] and tag["name"] and tag["description"]:
            self.tag_crud.update_tag(**tag)
            if self.tag_crud.commit_it()["errCode"]:
                self.response.get_response(500, "Internal Server Error")
            else:
                self.response.get_response(0, "Tag updated successfully")
        else:
            self.response.get_response(400, "tag_id, name and tag_desc are required")
        return self.response.send_response()

    def tag_display(self, tag_id):
        tag=self.tag_crud.get_by_id(tag_id["tag_id"])["obj"]
        if tag:
            self.response.get_response(0,"Found tag", data_rec = self.tag_crud.convert_to_dict(tag))
        else:
            self.response.get_response(400, "No tag found")
        return self.response.send_response()

    def tag_delete(self, tag_id):
        tag=self.tag_crud.delete_tag(tag_id.get("tag_id"))["obj"]
        if self.tag_crud.commit_it()["errCode"]:
            self.response.get_response(500, "Internal Server Error")
        else:
            self.response.get_response(0, "Tag deleted successfully", data_rec=self.tag_crud.convert_to_dict(tag))
        return self.response.send_response()
