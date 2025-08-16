from .users import *
from .roles import *
from .ideas import *
from .comments import *
from .votes import *
from .tags import *
from .merged_ideas import *
from .ideas_merged_ideas import *
from .users_roles import *
from .ideas_merged_ideas import *
from .security_ques import *

all_models={
    'user_crud' : UserCRUD,
    'role_crud' : RoleCRUD,
    'idea_crud' : IdeaCRUD,
    'comment_crud' : CommentCRUD,
    'vote_crud' : VoteCRUD,
    'tag_crud' : TagCRUD,
    'merged_idea_crud' : MergedIdeaCRUD,
    'ideas_merged_ideas' : IdeasMergedIdeasCRUD,
    'users_roles_crud' : UsersRolesCRUD,
    'security_ques_crud':SecurityQuesCRUD
}

