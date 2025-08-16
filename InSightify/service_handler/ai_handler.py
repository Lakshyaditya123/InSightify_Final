import requests
from InSightify.celery_server.Celery_tasks import app_logger
from InSightify.Common_files.config import config
from InSightify.Common_files.response import ResponseHandler
import json
from InSightify.db_server.Flask_app import dbsession
from InSightify.CoreClasses import IdeaCRUD, MergedIdeaCRUD, IdeasMergedIdeasCRUD, TagCRUD


class AiHelper:
    def __init__(self):
        self.ModeName = config.MODEL_NAME
        self.LMStudioURL = config.LM_STUDIO_URL
        self.LM_config = config.LM_CONFIG
        self.system_prompt = config.SYSTEM_PROMPT
        self.response = ResponseHandler()
        self.idea_crud = IdeaCRUD(dbsession)
        self.merge_idea_crud=MergedIdeaCRUD(dbsession)
        self.tag_crud=TagCRUD(dbsession)
        self.ideas_merged_ideas_crud=IdeasMergedIdeasCRUD(dbsession)
        self.skip_ideas=[]

    def call_lm_studio(self, user_message):
        """Send request to LM Studio API"""
        try:
            payload = {
                "model": self.ModeName,
                "messages": [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_message}
                ],
                **self.LM_config,
            } if config.LM_SYS_PROMPT_IN_REQUEST else {
                "model": self.ModeName,
                "messages": [
                    {"role": "user", "content": user_message}
                ],
                **self.LM_config,
            }
            headers = {
                "Content-Type": "application/json"
            }
            result = requests.post(self.LMStudioURL, json=payload, headers=headers)
            if result.status_code == 200:
                result_final=result.json()["choices"][0]["message"]["content"]
                if "```json" in result_final:
                    result_final = result_final.replace("```json", "")
                    result_final = result_final.replace("```", "")
                try:
                    result_flat = json.loads(result_final)
                except json.JSONDecodeError:
                    raise Exception(f"Model provided wrong output. Output not in JSON format.")

                return result_flat
            else:
                return f"Error connecting to LM Studio: {result.status_code} - {result.text}"
        except Exception as e:
            return f"Error connecting to LM Studio: {str(e)}"

    def refine_idea(self,idea):
        if idea.get("content"):
            prompt = f"Refine this idea and generate relevant tags for it: {idea.get("content")}"
            result = self.call_lm_studio(prompt)
            if "Error connecting to LM Studio:" in result:
                self.response.get_response(400, "Internal Server Error with LM Studio")
            else:
                self.response.get_response(0, "Idea Refined Successful", data_rec=result)
        else:
            self.response.get_response(400, "Idea doesn't has content required")
        return self.response.send_response()

    def merge_ideas(self, idea):
        app_logger.info("Merging ideas")
        ideas = self.idea_crud.find_similar_ideas(idea)["obj"]
        mergerd_ideas=self.merge_idea_crud.find_similar_merged_ideas(idea)["obj"]
        idea_list=[*(ideas if ideas else []) ]
        merged_idea_list=[*(mergerd_ideas if mergerd_ideas else [])]
        app_logger.info(f"Idea list: {idea_list}")
        app_logger.info(f"Merged idea list: {merged_idea_list}")
        merge_stat=None
        if idea_list or merged_idea_list:
            for idea2 in merged_idea_list:
                prompt = f'1 Merge the following ideas if and only if it is possible and provide the output in the specified format.\n "{idea.refine_content if idea.refine_content else idea.content}"\n"{idea2.content}"'
                result = self.call_lm_studio(prompt)
                if "Error connecting to LM Studio:" in result:
                    self.response.get_response(400, "Internal Server Error with LM Studio")
                elif result.get("merge_status") == "rejected":
                    app_logger.info("merged_idea merge rejected")
                    merge_stat="rejected"
                else:
                    tags_list=list(set(idea.tags_list) & set(idea2.tags_list)) + list(set(idea.tags_list) ^ set(idea2.tags_list))
                    merged_idea = result.get("merged_idea")
                    new_merged_idea = self.merge_idea_crud.update_merged_ideas(id= idea2.id, **merged_idea, tags_list=tags_list)
                    app_logger.info(f"New merged idea: {new_merged_idea}")
                    app_logger.info(f"New merged idea idea:{self.merge_idea_crud.convert_to_dict(new_merged_idea['obj'])}")
                    if self.merge_idea_crud.commit_it()["errCode"]:
                        self.response.get_response(500, "Internal Server Error")
                    else:
                        self.ideas_merged_ideas_crud.link_idea_to_merged_idea(idea_id=idea.id, merged_idea_id=new_merged_idea["obj"].id)
                        if self.ideas_merged_ideas_crud.commit_it()["errCode"]:
                            self.response.get_response(500, "Internal Server Error")
                        else:
                            skip_these_ideas=self.ideas_merged_ideas_crud.get_ideas_in_merged_idea(merged_idea_id=idea2.id)["obj"]
                            app_logger.info(f"Ideas to skip: {skip_these_ideas}")
                            self.skip_ideas+=[idea.id_ideas for idea in skip_these_ideas]
                            app_logger.info(f"Skip ideas: {self.skip_ideas}")
                            self.response.get_response(0, "Ideas merged successfully", data_rec=result)
            for idea2 in idea_list:
                if idea2.id in self.skip_ideas:
                    continue
                prompt = f'Merge the following ideas if and only if it is possible and provide the output in the specified format.\n "{idea.refine_content if idea.refine_content else idea.content}"\n"{idea2.refine_content if idea2.refine_content else idea2.content}"'
                result = self.call_lm_studio(prompt)
                if "Error connecting to LM Studio:" in result:
                    self.response.get_response(400, "Internal Server Error with LM Studio")
                elif result.get("merge_status")=="rejected":
                    app_logger.info("Idea merge rejected")
                    merge_stat="rejected"
                else:
                    tags_list=list(set(idea.tags_list) & set(idea2.tags_list)) + list(set(idea.tags_list) ^ set(idea2.tags_list))
                    merged_idea=result.get("merged_idea")
                    new_merged_idea=self.merge_idea_crud.create_merged_idea(**merged_idea, tags_list=tags_list)
                    if self.merge_idea_crud.commit_it()["errCode"]:
                        self.response.get_response(500, "Internal Server Error")
                    else:
                        self.ideas_merged_ideas_crud.link_idea_to_merged_idea(idea_id=idea.id, merged_idea_id=new_merged_idea["obj"].id)
                        self.ideas_merged_ideas_crud.link_idea_to_merged_idea(idea_id=idea2.id,merged_idea_id=new_merged_idea["obj"].id)
                        if self.ideas_merged_ideas_crud.commit_it()["errCode"]:
                            self.response.get_response(500, "Internal Server Error")
                        else:
                            self.response.get_response(0, "Ideas merged successfully", data_rec=result)
        else:
            self.response.get_response(0, "It is a unique idea !")
        if merge_stat=="rejected":
            self.response.get_response(0, "Idea merge rejected")
        return self.response.send_response()


    def merge_bulk_ideas(self,data):
        merged_idea_id=data.get("merged_idea_id")
        idea_id_list=data.get("idea_id_list",[])
        if merged_idea_id and  idea_id_list:
            ideas_list = self.idea_crud.bulk_select_ideas(idea_id_list)
            if ideas_list["errCode"]:
                self.response.get_response(500, "Internal Server Error")
            else:
                prompt = f"1 Merge the following ideas into single idea if and only if it is possible and provide the output in the specified format.\n "
                for idea in ideas_list["obj"]:
                    prompt+=f"\n{idea.refine_content if idea.refine_content else idea.content}\n"
                result = self.call_lm_studio(prompt)
                if "Error connecting to LM Studio:" in result:
                    self.response.get_response(400, "Internal Server Error with LM Studio")
                else:
                    merged_idea = result.get("merged_idea")
                    output={
                        "title": merged_idea.get("title"),
                        "subject": merged_idea.get("subject"),
                        "content": merged_idea.get("content")
                    }
                    self.response.get_response(0, "Ideas merged successfully", data_rec=output)
        else:
            self.response.get_response(1, "merged idea id or idea list is empty")
        return self.response.send_response()





