from InSightify.CoreClasses import IdeaCRUD
from InSightify.db_server.Flask_app import dbsession
from InSightify.Common_files.response import ResponseHandler
from InSightify.db_server.Flask_app import app_logger
from InSightify.CoreClasses.tags import TagCRUD
from InSightify.celery_server.celery_app import app
tag_crud = TagCRUD(dbsession)
idea_crud = IdeaCRUD(dbsession)
response = ResponseHandler()

@app.task(name="tags_worker")
def tags_worker(idea_id, tags_list):
    app_logger.info("------------Idea worker started-----------")
    tag_ids_by_name = {}
    for tag in tags_list:
        id = tag.get("id")
        name = tag.get("name")
        if id and name:
            tag_ids_by_name[name.strip().title()] = id
    normalized = [tag.get('name').strip().title() for tag in tags_list if tag.get("name")]
    existing_tags = tag_crud.bulk_select_tags(normalized)["obj"]
    for tag in existing_tags:
        tag_ids_by_name[tag.name] = tag.id
    id_list = tag_ids_by_name.values()
    if id_list:
        tag_crud.update_tag_status(id_list)
        if tag_crud.commit_it()["errCode"]:
            response.get_response(500, "Internal Server Error")
            app_logger.error("Internal Server Error")
        else:
            response.get_response(0, "Tags updated successfully!!")
    else:
        response.get_response(0, "No tags found")
        return response.send_response()

    missing = [
        {
            "name": tag.get("name").strip().title(),
            "description": tag.get("description", "").strip(),
            "generated_by": tag.get("generated_by")
        }
        for tag in tags_list if tag.get("name") and tag.get("name").strip().title() not in tag_ids_by_name
    ]
    tag_ids_by_name = tag_crud.bulk_insert_tags(missing, tag_ids_by_name)["obj"]

    id_list = [tag_ids_by_name[name] for name in normalized]
    idea_crud.update_tags(idea_id, id_list)
    if tag_crud.commit_it()["errCode"] or idea_crud.commit_it()["errCode"]:
        response.get_response(500, "Internal Server Error")
        app_logger.error("Internal Server Error")
    else:
        idea=idea_crud.get_by_id(idea_id)["obj"]
        response.get_response(0, "Tags updated successfully!!", data_rec=idea_crud.convert_to_dict(idea))
    return response.send_response()

@app.task(name="merge_idea_worker")
def merge_idea_worker(idea_id):
    from InSightify.service_handler import AiHelper
    ai_helper = AiHelper()
    idea=idea_crud.get_by_id(idea_id)["obj"]
    if ai_helper.merge_ideas(idea)["errCode"]:
        response.get_response(500, "Internal Server Error")
        app_logger.error("Internal Server Error")
    else:
        response.get_response(0, "Ideas Merged Successfully!!")
        app_logger.info("Idea merged successfully")