from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy import desc, asc

class BaseCRUD:

    def __init__(self, model, db_session):
        self.model = model
        self.db_session = db_session

    def create(self, **kwargs):
        try:
            db_obj = self.model(**kwargs)
            self.db_session.add(db_obj)
            self.db_session.commit()
            self.db_session.refresh(db_obj)
            return db_obj
        except IntegrityError as e:
            self.db_session.rollback()
            if hasattr(e.orig, 'pgcode'):
                if e.orig.pgcode == '23505':
                    return "Not Unique"
                elif e.orig.pgcode == '23502':
                    return "Null Value"
                elif e.orig.pgcode == '23503':
                    return "Foreign Key Violation"
            return "Database Integrity Error"

    def get_by_id(self, id):
        try:
            return self.db_session.query(self.model).filter(self.model.id == id).first()
        except SQLAlchemyError as e:
            print(f"Error getting {self.model.__name__} by ID: {str(e)}")
            return "Database Integrity Error"

    def get_all(self, skip=0, limit=100, order_by="id", desc_order=False):
        try:
            query = self.db_session.query(self.model)
            if hasattr(self.model, order_by):
                order_field = getattr(self.model, order_by)
                if desc_order:
                    query = query.order_by(desc(order_field))
                else:
                    query = query.order_by(asc(order_field))
            if limit == -1:
                return query.offset(skip).all()
            return query.offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            print(f"Error getting all {self.model._name_}: {str(e)}")
            return "Database Integrity Error"

    def update(self, id, **kwargs):
        try:
            db_obj = self.get_by_id(id)
            if not db_obj:
                return None

            for field, value in kwargs.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)

            self.db_session.commit()
            self.db_session.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"Error updating {self.model.__name__}: {str(e)}")
            return "Database Integrity Error"

    def delete(self, id):
        try:
            db_obj = self.get_by_id(id)
            if not db_obj:
                return False

            self.db_session.delete(db_obj)
            self.db_session.commit()
            return True
        except SQLAlchemyError as e:
            self.db_session.rollback()
            print(f"Error deleting {self.model.__name__}: {str(e)}")
            return "Database Integrity Error"

    def get_by_field(self, field_name, value):
        try:
            if hasattr(self.model, field_name):
                field = getattr(self.model, field_name)
                return self.db_session.query(self.model).filter(field == value).first()
            return None
        except SQLAlchemyError as e:
            print(f"Error getting {self.model.__name__} by {field_name}: {str(e)}")
            return "Database Integrity Error"

    def get_by_fields(self, **kwargs):
        try:
            query = self.db_session.query(self.model)

            for field_name, value in kwargs.items():
                if hasattr(self.model, field_name):
                    field = getattr(self.model, field_name)
                    query = query.filter(field == value)
            return query.all()
        except SQLAlchemyError as e:
            print(f"Error getting {self.model._name_} by fields: {str(e)}")
            return "Database Integrity Error"

    def count(self):
        try:
            return self.db_session.query(self.model).count()
        except SQLAlchemyError as e:
            print(f"Error counting {self.model.__name__}: {str(e)}")
            return "Database Integrity Error"

    @staticmethod
    def convert_to_dict_list(objects):
        if not objects:
            return []
        return [{column.name: getattr(obj, column.name) for column in obj.__table__.columns} for obj in objects]

    @staticmethod
    def convert_to_dict(obj):
        if not obj:
            return None
        return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}










# class BaseCRUD:
#
#     def __init__(self, model):
#         self.model = model
#
#     def create(self, db: Session, **kwargs):
#         try:
#             db_obj = self.model(**kwargs)
#             setattr(db_obj, self.model.__name__, db)
#             db.add(db_obj)
#             db.commit()
#             db.refresh(db_obj)
#             return db_obj
#         except IntegrityError as e:
#             db.rollback()
#             if e.orig.pgcode == '23505':
#                 return "Not Unique"
#             elif e.orig.pgcode == '23502':
#                 return "Null Value"
#
#
#     def get_by_id(self, db: Session, id: int):
#         return db.query(self.model).filter(self.model.id == id).first()
#
#     def get_all(self, db: Session, skip: int = 0, limit: int = 100):
#         if limit==-1:
#             return db.query(self.model).offset(skip).all()
#         return db.query(self.model).offset(skip).limit(limit).all()
#
#     def update(self, db: Session, id: int, **kwargs):
#         try:
#             db_obj = self.get_by_id(db, id)
#             if db_obj:
#                 for key, value in kwargs.items():
#                     setattr(db_obj, key, value)
#                 db.commit()
#                 db.refresh(db_obj)
#             return db_obj
#         except SQLAlchemyError as e:
#             db.rollback()
#             raise e
#
#     def delete(self, db: Session, id: int):
#         try:
#             db_obj = self.get_by_id(db, id)
#             if db_obj:
#                 db.delete(db_obj)
#                 db.commit()
#                 return True
#             return False
#         except SQLAlchemyError as e:
#             db.rollback()
#             raise e
#
#     def convert_to_dict_list(objects):
#         if not objects:
#             return []
#
#         return [
#             {column.name: getattr(obj, column.name) for column in obj.__table__.columns}
#             for obj in objects
#         ]
#
#     def convert_to_dict(obj):
#         if not obj:
#             return None
#         return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}



# Example usage functions
# def example_usage():
#     """Example of how to use the CRUD operations"""
#     from app_orm import SessionLocal
#
#     db = SessionLocal()
#
#     try:
#         # Create a user
#         new_user = user_crud.create_user(
#             db, name="John Doe", email="john@example.com",
#             mob_number="1234567890", password="hashed_password",
#             profile_picture="profile_url.jpg", bio="A sample user"
#         )
#         print(f"Created user: {new_user.name}")
#
#         # Create an idea
#         new_idea = idea_crud.create_idea(
#             db, user_id=new_user.id, title="My Great Idea",
#             subject="Innovation", content="This is a great idea!",
#             status=1
#         )
#         print(f"Created idea: {new_idea.title}")
#
#         # Create a comment
#         new_comment = comment_crud.create_comment(
#             db, user_id=new_user.id, content="Great idea!",
#             idea_id=new_idea.id
#         )
#         print(f"Created comment: {new_comment.content}")
#
#         # Create a vote
#         new_vote = vote_crud.create_vote(
#             db, user_id=new_user.id, vote_type=1,
#             idea_id=new_idea.id
#         )
#         print(f"Created vote: {new_vote.vote_type}")
#
#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         db.close()


# if __name__ == "__main__":
#     example_usage()