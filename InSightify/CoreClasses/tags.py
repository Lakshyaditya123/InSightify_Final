from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError

from InSightify.Common_files.base_crud import BaseCRUD
from InSightify.db_server.app_orm import Tag

class TagCRUD(BaseCRUD):

    def __init__(self, db_session):
        super().__init__(Tag, db_session)

    def create_tag(self, name, tag_desc, status=1, generated_by="user"):
        return self.create(
            name=name,
            tag_desc=tag_desc,
            status=status,
            generated_by=generated_by)

    def get_by_name(self, name):
        return self.get_by_field("name", name)

    def get_by_generated_by(self, generated_by):
        return self.get_by_field("generated_by", generated_by)

    def get_active_tags(self):
        return self.get_by_fields(status=1)

    def search_tags(self, search_term):
        result=self.db_session.query(self.model).filter(
            or_(
                self.model.name.ilike(f"%{search_term}%"),
                self.model.tag_desc.ilike(f"%{search_term}%")
            )
        ).all()
        if result:
            self.db_response.get_response(errCode=0, msg="Found Records !", obj=result)
        else:
            self.db_response.get_response(errCode=0, msg="Records not found", obj=None)
        return self.db_response.send_response()

    def bulk_select_tags(self,tag_list):
        self.db_session.execute(select(Tag).where(Tag.name.in_(tag_list))).scalars().all()
        self.db_response.get_response(errCode=0,msg="Found tags", obj=self.db_session.query(self.model))
        return self.db_response.send_response()

    def bulk_insert_tags(self, missing_tags: list[dict], tag_ids_by_name: dict) -> dict:
        new_tags = []
        for tag_data in missing_tags:
            name = tag_data.get("name").strip().title()
            tag_desc = tag_data.get("tag_desc", "").strip()
            tag_status = 0
            generated_by = tag_data.get("generated_by", "AI").strip()
            new_tags.append(Tag(name=name, tag_desc=tag_desc,status=tag_status, generated_by=generated_by))

        if new_tags:
            self.db_session.add_all(new_tags)
            self.db_session.flush()  # assigns IDs without committing

            for tag in new_tags:
                tag_ids_by_name[tag.name] = tag.id

        self.db_response.get_response(errCode=0, msg="Inserted tags", obj=tag_ids_by_name)
        return self.db_response.send_response()





