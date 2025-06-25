from InSightify.Common_files.base_crud import BaseCRUD
from InSightify.db_server.app_orm import IdeasMergedIdeas
#
# class IdeasMergedIdeasCRUD(BaseCRUD):
#
#     def __init__(self):
#         super().__init__(IdeasMergedIdeas)
#
#     def link_idea_to_merged_idea(self, db: Session, idea_id: int, merged_idea_id: int):
#         return self.create(db, id_ideas=idea_id, id_merged_ideas=merged_idea_id)
#
#     def get_ideas_in_merged_idea(self, db: Session, merged_idea_id: int):
#         return db.query(IdeasMergedIdeas).filter(
#             IdeasMergedIdeas.id_merged_ideas == merged_idea_id
#         ).all()
#
#     def get_merged_ideas_containing_idea(self, db: Session, idea_id: int):
#         return db.query(IdeasMergedIdeas).filter(
#             IdeasMergedIdeas.id_ideas == idea_id
#         ).all()
#
#     def unlink_idea_from_merged_idea(self, db: Session, idea_id: int, merged_idea_id: int):
#         link = db.query(IdeasMergedIdeas).filter(
#             IdeasMergedIdeas.id_ideas == idea_id,
#             IdeasMergedIdeas.id_merged_ideas == merged_idea_id
#         ).first()
#         if link:
#             db.delete(link)
#             db.commit()
#             return True
#         return False



class IdeasMergedIdeasCRUD(BaseCRUD):

    def __init__(self, db_session):
        super().__init__(IdeasMergedIdeas, db_session)

    def link_idea_to_merged_idea(self, idea_id, merged_idea_id):
        return self.create(id_ideas=idea_id, id_merged_ideas=merged_idea_id)

    def get_ideas_in_merged_idea(self, merged_idea_id):
        return self.get_by_fields(id_merged_ideas=merged_idea_id)

    def get_merged_ideas_for_idea(self, idea_id):
        return self.get_by_fields(id_ideas=idea_id)

    # def unlink_idea_from_merged_idea(self, idea_id, merged_idea_id):
    #     link = self.db_session.query(IdeasMergedIdeas).filter(
    #         IdeasMergedIdeas.id_ideas == idea_id,
    #         IdeasMergedIdeas.id_merged_ideas == merged_idea_id
    #     ).first()
    #     if link:
    #         self.db_session.delete(link)
    #         self.db_session.flush()
    #         return True
    #     return False