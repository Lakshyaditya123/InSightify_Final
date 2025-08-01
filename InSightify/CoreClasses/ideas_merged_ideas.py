from InSightify.Common_files.base_crud import BaseCRUD
from InSightify.db_server.app_orm import IdeasMergedIdeas
from InSightify.db_server.Flask_app import app_logger  # Import app_logger


class IdeasMergedIdeasCRUD(BaseCRUD):

    def __init__(self, db_session):
        super().__init__(IdeasMergedIdeas, db_session)

    def link_idea_to_merged_idea(self, idea_id, merged_idea_id):
        # This function is fine as is
        return self.create(id_ideas=idea_id, id_merged_ideas=merged_idea_id)

    def get_ideas_in_merged_idea(self, merged_idea_id):
        return self.get_by_fields(id_merged_ideas=merged_idea_id)
