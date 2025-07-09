from sqlalchemy import Column, Integer, SmallInteger, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.sql import func
from InSightify.db_server.app_database import InsightifyDB

dbApp = InsightifyDB()
dbEngine = dbApp.get_engine()
metadata_curr = dbApp.get_metadata()

Base = declarative_base(metadata=metadata_curr)


class TimestampMixin:
    create_datetime = Column(DateTime, nullable=False, default=func.now())
    lastchange_datetime = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())


class SecurityQues(Base):
    __tablename__ = 'security_ques'
    __table_args__ = {'schema': 'in_use'}

    id = Column(SmallInteger, primary_key=True)
    content = Column(String, nullable=False)

    # Relationships
    users = relationship("User", back_populates="security_question")


class Role(Base, TimestampMixin):
    __tablename__ = 'roles'
    __table_args__ = {'schema': 'in_use'}

    id = Column(SmallInteger, primary_key=True)
    roles = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)

    # Relationships
    users = relationship("User", secondary="in_use.users_roles", back_populates="roles")


class User(Base, TimestampMixin):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'in_use'}

    id = Column(SmallInteger, primary_key=True)
    this_obj2security_ques = Column(SmallInteger, ForeignKey('in_use.security_ques.id'), nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    mobile = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    security_ques_answer = Column(String, nullable=False)
    # profile_picture = Column(String, nullable=False, unique=True)
    profile_picture = Column(String, nullable=False)
    bio = Column(String)

    # Relationships
    security_question = relationship("SecurityQues", back_populates="users")
    roles = relationship("Role", secondary="in_use.users_roles", back_populates="users")
    ideas = relationship("Idea", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    votes = relationship("Vote", back_populates="user")


class Vote(Base, TimestampMixin):
    __tablename__ = 'votes'
    __table_args__ = {'schema': 'in_use'}

    id = Column(SmallInteger, primary_key=True)
    this_obj2users = Column(SmallInteger, ForeignKey('in_use.users.id'), nullable=False)
    this_obj2ideas = Column(SmallInteger, ForeignKey('in_use.ideas.id'))
    this_obj2merged_ideas = Column(SmallInteger, ForeignKey('in_use.merged_ideas.id'))
    this_obj2comments = Column(SmallInteger, ForeignKey('in_use.comments.id'))
    vote_type = Column(SmallInteger, nullable=False)

    # Relationships
    user = relationship("User", back_populates="votes")
    idea = relationship("Idea", back_populates="votes")
    comment = relationship("Comment", back_populates="votes")
    merged_idea = relationship("MergedIdea", back_populates="votes")


class Idea(Base, TimestampMixin):
    __tablename__ = 'ideas'
    __table_args__ = {'schema': 'in_use'}

    id = Column(SmallInteger, primary_key=True)
    this_obj2users = Column(SmallInteger, ForeignKey('in_use.users.id'), nullable=False)
    title = Column(String, nullable=False)  # Changed to NOT NULL to match SQL
    subject = Column(String, nullable=False)
    content = Column(String, nullable=False)
    refine_content = Column(String)
    tags_list = Column(ARRAY(SmallInteger), nullable=False)  # Make it nullable afterwards pleaseeee for the database alsoooo
    link = Column(String)  # Added new field
    file_path = Column(String)  # Added new field
    status = Column(SmallInteger, nullable=False) # Make it change with admin... for now it is default pass all
    parent_idea = Column(SmallInteger)  # Added new field

    # Relationships
    user = relationship("User", back_populates="ideas")
    comments = relationship("Comment", back_populates="idea")
    votes = relationship("Vote", back_populates="idea")
    merged_ideas = relationship("MergedIdea", secondary="in_use.ideas_merged_ideas", back_populates="ideas")


class Comment(Base, TimestampMixin):
    __tablename__ = 'comments'
    __table_args__ = {'schema': 'in_use'}

    id = Column(SmallInteger, primary_key=True)
    this_obj2users = Column(SmallInteger, ForeignKey('in_use.users.id'),
                            nullable=False)  # Fixed typo from this__obj2users
    this_obj2ideas = Column(SmallInteger, ForeignKey('in_use.ideas.id'))
    this_obj2merged_ideas = Column(SmallInteger, ForeignKey('in_use.merged_ideas.id'))
    parent_comment = Column(SmallInteger, default=-1)  # Changed from parent_id to parent_comment
    content = Column(String, nullable=False)

    # Relationships
    user = relationship("User", back_populates="comments")
    idea = relationship("Idea", back_populates="comments")
    merged_idea = relationship("MergedIdea", back_populates="comments")
    votes = relationship("Vote", back_populates="comment")


class Tag(Base, TimestampMixin):
    __tablename__ = 'tags'
    __table_args__ = {'schema': 'in_use'}

    id = Column(SmallInteger, primary_key=True)
    name = Column(String, nullable=False)
    tag_desc = Column(String, nullable=False)
    status = Column(SmallInteger, nullable=False)
    generated_by = Column(String, nullable=False)


class MergedIdea(Base, TimestampMixin):
    __tablename__ = 'merged_ideas'
    __table_args__ = {'schema': 'in_use'}

    id = Column(SmallInteger, primary_key=True)
    title = Column(String)
    subject = Column(String, nullable=False)
    content = Column(String, nullable=False)
    tags_list = Column(ARRAY(SmallInteger))

    # Relationships
    ideas = relationship("Idea", secondary="in_use.ideas_merged_ideas", back_populates="merged_ideas")
    comments = relationship("Comment", back_populates="merged_idea")
    votes = relationship("Vote", back_populates="merged_idea")

class IdeasMergedIdeas(Base):
    __tablename__ = 'ideas_merged_ideas'
    __table_args__ = {'schema': 'in_use'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_merged_ideas = Column(SmallInteger, ForeignKey('in_use.merged_ideas.id'), nullable=False)
    id_ideas = Column(SmallInteger, ForeignKey('in_use.ideas.id'), nullable=False)


class UsersRoles(Base):
    __tablename__ = 'users_roles'
    __table_args__ = {'schema': 'in_use'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_roles = Column(SmallInteger, ForeignKey('in_use.roles.id'), nullable=False)
    id_users = Column(SmallInteger, ForeignKey('in_use.users.id'), nullable=False)
