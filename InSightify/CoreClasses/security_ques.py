from InSightify.Common_files.base_crud import BaseCRUD
from InSightify.db_server.app_orm import SecurityQues

class SecurityQuesCRUD(BaseCRUD):

    def __init__(self, db_session):
        super().__init__(SecurityQues, db_session)

    def get_all_ques(self):
        return self.get_all()