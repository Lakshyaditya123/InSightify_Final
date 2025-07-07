from celery import Celery, shared_task
from InSightify.CoreClasses import IdeaCRUD
from InSightify.db_server.Flask_app import dbsession
from InSightify.Common_files.response import ResponseHandler
from InSightify.CoreClasses.tags import TagCRUD
from InSightify.service_handler import AiHelper
app = Celery("InSightify_tasks", broker="redis://localhost:6379/0")

tag_crud = TagCRUD(dbsession)
idea_crud = IdeaCRUD(dbsession)
response = ResponseHandler()
ai_helper = AiHelper()

@shared_task(name="tag.handler")
def idea_worker(idea_id, tags_list):
    tag_ids_by_name = {}

    for tag in tags_list:
        id = tag.get("id")
        name = tag.get("name")
        if id and name:
            tag_ids_by_name[name.strip().title()] = id

    normalized = [tag.get('name').strip().title() for tag in tags_list if tag.get("name")]

    existing_tags = tag_crud.bulk_select_tags(normalized)
    for tag in existing_tags:
        tag_ids_by_name[tag.name] = tag.id

    missing = [
        {
            "name": tag.get("name").strip().title(),
            "tag_desc": tag.get("tag_desc", "").strip(),
            "generated_by": tag.get("generated_by", "").strip()
        }
        for tag in tags_list if tag.get("name") and tag.get("name").strip().title() not in tag_ids_by_name
    ]

    # Insert missing and get updated tag_ids_by_name
    tag_ids_by_name = tag_crud.bulk_insert_tags(missing, tag_ids_by_name)["obj"]

    id_list = [tag_ids_by_name[name] for name in normalized]

    idea_crud.update_tags(idea_id, id_list)

    if tag_crud.commit_it()["errCode"] or idea_crud.commit_it()["errCode"]:
        response.get_response(500, "Internal Server Error")
    else:
        idea=idea_crud.get_by_id(idea_id)
        idea_list=ai_helper.find_similar_ideas(idea)
        if ai_helper.merge_ideas(idea, idea_list):
            response.get_response(500, "Internal Server Error")
        else:
            response.get_response(0, "Ideas Merged Successfully!!")
    return response.send_response()







