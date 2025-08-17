from InSightify.Common_files.base_crud import BaseCRUD
from InSightify.db_server.app_orm import IdeasMergedIdeas



class IdeasMergedIdeasCRUD(BaseCRUD):

    def __init__(self, db_session):
        super().__init__(IdeasMergedIdeas, db_session)

    def link_idea_to_merged_idea(self, idea_id, merged_idea_id):
        # This function is fine as is
        return self.create(id_ideas=idea_id, id_merged_ideas=merged_idea_id)

    def get_ideas_in_merged_idea(self, merged_idea_id):
        return self.get_by_fields(id_merged_ideas=merged_idea_id)

    def unlink_some_ideas(self, merged_idea_id, removed_idea_ids):
        deleted_count = self.db_session.query(IdeasMergedIdeas).filter(
            IdeasMergedIdeas.id_merged_ideas == merged_idea_id,
            IdeasMergedIdeas.id_ideas.in_(removed_idea_ids)
        ).delete(synchronize_session=False)
        self.db_session.flush()
        if deleted_count == 0 or deleted_count is None:
            self.db_response.get_response(errCode=1, msg="No matching ideas found to unlink", obj=None)
        else:
            self.db_response.get_response(errCode=0, msg=f"{deleted_count} idea(s) unlinked successfully", obj=None)
        return self.db_response.send_response()

