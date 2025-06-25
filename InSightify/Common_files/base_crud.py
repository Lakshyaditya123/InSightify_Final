# from sqlalchemy.exc import SQLAlchemyError, IntegrityError
# from InSightify.db_server.Flask_app import app_logger
# from sqlalchemy import desc, asc
# from .response import ErrorResponse
# import inspect
#
# class BaseCRUD:
#
#     def __init__(self, model, db_session):
#         self.model = model
#         self.db_session = db_session
#         self.error_response = ErrorResponse()
#
#     def create(self, **kwargs):
#         try:
#             db_obj = self.model(**kwargs)
#             self.db_session.add(db_obj)
#             self.error_response.get_response(error_code=0, msg="Record created successfully.", obj=db_obj)
#         except IntegrityError as e:
#             self.db_session.rollback()
#             if hasattr(e.orig, 'pgcode'):
#                 if e.orig.pgcode == '23505':
#                     self.error_response.get_response(error_code=23505, msg="Not Unique")
#                 elif e.orig.pgcode == '23502':
#                     self.error_response.get_response(error_code=23502, msg="Null Value")
#                 elif e.orig.pgcode == '23503':
#                     self.error_response.get_response(error_code=23503, msg="Foreign Key Violation")
#             else:
#                 self.error_response.get_response(error_code=1, msg="Database Integrity Error")
#         finally:
#             return self.error_response.send_response()
#
#     def get_by_id(self, id):
#         try:
#             obj = self.db_session.query(self.model).filter(self.model.id == id).first()
#             self.error_response.get_response(error_code=0, msg="Found Record !", obj=obj)
#         except SQLAlchemyError as e:
#             app_logger.error(f"Error getting {self.model.__name__} by ID: {str(e)}")
#             self.error_response.get_response(error_code=23503, msg="Database Integrity Error")
#         finally:
#             return self.error_response.send_response()
#
#     def get_all(self, skip=0, limit=100, order_by="id", desc_order=False):
#         try:
#             query = self.db_session.query(self.model)
#             if hasattr(self.model, order_by):
#                 order_field = getattr(self.model, order_by)
#                 if desc_order:
#                     query = query.order_by(desc(order_field))
#                 else:
#                     query = query.order_by(asc(order_field))
#             if limit == -1:
#                 result = query.offset(skip).all()
#             else:
#                 result = query.offset(skip).limit(limit).all()
#             self.error_response.get_response(error_code=0, msg="Found Records !", obj=result)
#         except SQLAlchemyError as e:
#             app_logger.error(f"Error getting {self.model.__name__} by ID: {str(e)}")
#             self.error_response.get_response(error_code=1, msg="Database Integrity Error")
#         finally:
#             return self.error_response.send_response()
#
#     def update(self, id, **kwargs):
#         try:
#             db_obj = self.db_session.query(self.model).filter(self.model.id == id).first()
#             if not db_obj:
#                 self.error_response.get_response(error_code=404, msg="Record not found", obj=None)
#             else:
#                 for field, value in kwargs.items():
#                     if hasattr(db_obj, field):
#                         setattr(db_obj, field, value)
#                 self.db_session.add(db_obj)
#                 self.error_response.get_response(error_code=0, msg="Record updated successfully", obj=db_obj)
#         except SQLAlchemyError as e:
#             self.db_session.rollback()
#             app_logger.error(f"Error updating {self.model.__name__} by ID: {str(e)}")
#             self.error_response.get_response(error_code=1, msg="Database Integrity Error")
#         finally:
#             return self.error_response.send_response()
#
#     def delete(self, id):
#         try:
#             db_obj = self.db_session.query(self.model).filter(self.model.id == id).first()
#             if not db_obj:
#                 self.error_response.get_response(error_code=404, msg="Record not found", obj=None)
#             else:
#                 self.db_session.delete(db_obj)
#                 self.error_response.get_response(error_code=0, msg="Record deleted successfully", obj=None)
#         except SQLAlchemyError as e:
#             self.db_session.rollback()
#             app_logger.error(f"Error deleting {self.model.__name__}: {str(e)}")
#             self.error_response.get_response(error_code=1, msg="Database Integrity Error")
#         finally:
#             return self.error_response.send_response()
#
#     def get_by_field(self, field_name, value):
#         try:
#             if hasattr(self.model, field_name):
#                 field = getattr(self.model, field_name)
#                 obj = self.db_session.query(self.model).filter(field == value).first()
#                 self.error_response.get_response(error_code=0, msg="Record found", obj=obj)
#             else:
#                 self.error_response.get_response(error_code=404, msg="Field not found", obj=None)
#         except SQLAlchemyError as e:
#             app_logger.error(f"Error getting {self.model.__name__} by {field_name}: {str(e)}")
#             self.error_response.get_response(error_code=1, msg="Database Integrity Error")
#         finally:
#             return self.error_response.send_response()
#
#     def get_by_fields(self, **kwargs):
#         try:
#             query = self.db_session.query(self.model)
#             for field_name, value in kwargs.items():
#                 if hasattr(self.model, field_name):
#                     field = getattr(self.model, field_name)
#                     query = query.filter(field == value)
#             results = query.all()
#             self.error_response.get_response(error_code=0, msg="Records found", obj=results)
#         except SQLAlchemyError as e:
#             app_logger.error(f"Error getting {self.model.__name__} by fields: {str(e)}")
#             self.error_response.get_response(error_code=1, msg="Database Integrity Error")
#         finally:
#             return self.error_response.send_response()
#
#     def count(self):
#         try:
#             count = self.db_session.query(self.model).count()
#             self.error_response.get_response(error_code=0, msg="Count fetched", obj=count)
#         except SQLAlchemyError as e:
#             app_logger.error(f"Error counting {self.model.__name__}: {str(e)}")
#             self.error_response.get_response(error_code=1, msg="Database Integrity Error")
#         finally:
#             return self.error_response.send_response()
#
#     @staticmethod
#     def convert_to_dict_list(objects):
#         if not objects:
#             return []
#         return [{column.name: getattr(obj, column.name) for column in obj.__table__.columns} for obj in objects]
#
#     @staticmethod
#     def convert_to_dict(obj):
#         if not obj:
#             return None
#         return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}
from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from InSightify.db_server.Flask_app import app_logger
from sqlalchemy import desc, asc
from .response import DatabaseResponse

class BaseCRUD:

    def __init__(self, model, db_session):
        self.model = model
        self.db_session = db_session
        self.db_response = DatabaseResponse()

    def create(self, **kwargs):
        db_obj = self.model(**kwargs)
        self.db_session.add(db_obj)
        self.db_response.get_response(error_code=0, msg="Record created successfully.", obj=db_obj)
        return self.db_response.send_response()

    def get_by_id(self, id):
        obj = self.db_session.query(self.model).filter(self.model.id == id).first()
        if obj:
            self.db_response.get_response(error_code=0, msg="Found Record !", obj=obj)
        else:
            self.db_response.get_response(error_code=404, msg="Record not found", obj=None)
        return self.db_response.send_response()

    def get_all(self, skip=0, limit=100, order_by="id", desc_order=False):
        query = self.db_session.query(self.model)
        if hasattr(self.model, order_by):
            order_field = getattr(self.model, order_by)
            if desc_order:
                query = query.order_by(desc(order_field))
            else:
                query = query.order_by(asc(order_field))
        if limit == -1:
            result = query.offset(skip).all()
        else:
            result = query.offset(skip).limit(limit).all()
        if result:
            self.db_response.get_response(error_code=0, msg="Found Record !", obj=result)
        else:
            self.db_response.get_response(error_code=404, msg="Record not found", obj=None)
        return self.db_response.send_response()


    def update(self, id, **kwargs):
        db_obj = self.db_session.query(self.model).filter(self.model.id == id).first()
        if not db_obj:
            self.db_response.get_response(error_code=404, msg="Record not found", obj=None)
        else:
            for field, value in kwargs.items():
                if hasattr(db_obj, field):
                    setattr(db_obj, field, value)
            self.db_session.add(db_obj)
            self.db_response.get_response(error_code=0, msg="Record updated successfully", obj=db_obj)
        return self.db_response.send_response()

    def delete(self, id):
        db_obj = self.db_session.query(self.model).filter(self.model.id == id).first()
        if not db_obj:
            self.db_response.get_response(error_code=404, msg="Record not found", obj=None)
        else:
            self.db_session.delete(db_obj)
            self.db_response.get_response(error_code=0, msg="Record deleted successfully", obj=None)
        return self.db_response.send_response()

    def get_by_field(self, field_name, value):
        if hasattr(self.model, field_name):
            field = getattr(self.model, field_name)
            obj = self.db_session.query(self.model).filter(field == value).first()
            self.db_response.get_response(error_code=0, msg="Record found", obj=obj)
        else:
            self.db_response.get_response(error_code=404, msg="Field not found", obj=None)
        return self.db_response.send_response()

    def get_by_fields(self, **kwargs):
        query = self.db_session.query(self.model)
        for field_name, value in kwargs.items():
            if hasattr(self.model, field_name):
                field = getattr(self.model, field_name)
                query = query.filter(field == value)
        results = query.all()
        if results:
            self.db_response.get_response(error_code=0, msg="Found Record !", obj=results)
        else:
            self.db_response.get_response(error_code=404, msg="Record not found", obj=None)
        return self.db_response.send_response()

    def count(self):
        count = self.db_session.query(self.model).count()
        self.db_response.get_response(error_code=0, msg="Count fetched", obj=count)
        return self.db_response.send_response()

    @staticmethod
    def convert_to_dict(obj):
        if not obj:
            return None
        result = {}
        for column in obj.__table__.columns:
            value = getattr(obj, column.name)
            if isinstance(value, datetime):
                result[column.name] = value.isoformat()
            else:
                result[column.name] = value
        return result

    @staticmethod
    def convert_to_dict_list(objects):
        if not objects:
            return []
        return [BaseCRUD.convert_to_dict(obj) for obj in objects]

    def commit_it(self):
        try:
            self.db_session.commit()
            self.db_response.get_response(error_code=0, msg="Committed successfully")
        except SQLAlchemyError as e:
            self.db_session.rollback()
            if hasattr(e.orig, 'pgcode'):
                if e.orig.pgcode == '23505':
                    self.db_response.get_response(error_code=23505, msg="Not Unique")
                elif e.orig.pgcode == '23502':
                    self.db_response.get_response(error_code=23502, msg="Null Value")
                elif e.orig.pgcode == '23503':
                    self.db_response.get_response(error_code=23503, msg="Foreign Key Violation")
            app_logger.error(f"Error committing transaction for {self.model.__name__}: {str(e)}")
            self.db_response.get_response(error_code=1, msg="Database Integrity Error")

        return self.db_response.send_response()


# from sqlalchemy.exc import SQLAlchemyError, IntegrityError
# from InSightify.db_server.Flask_app import app_logger
# from sqlalchemy import desc, asc
# from .response import ErrorResponse
# import inspect
#
# class BaseCRUD:
#
#     def __init__(self, model, db_session):
#         self.model = model
#         self.db_session = db_session
#         self.error_response = ErrorResponse()
#
#     def create(self, **kwargs):
#         try:
#             db_obj = self.model(**kwargs)
#             self.db_session.add(db_obj)
#             # self.db_session.refresh(db_obj)
#             self.error_response.get_response(error_code=0, msg="Record created successfully.", obj=db_obj)
#         except IntegrityError as e:
#             self.db_session.rollback()
#             if hasattr(e.orig, 'pgcode'):
#                 if e.orig.pgcode == '23505':
#                     self.error_response.get_response(error_code=23505, msg="Not Unique")
#                 elif e.orig.pgcode == '23502':
#                     self.error_response.get_response(error_code=23502, msg="Null Value")
#                 elif e.orig.pgcode == '23503':
#                     self.error_response.get_response(error_code=23503, msg="Foreign Key Violation")
#             else:
#                 self.error_response.get_response(error_code=1, msg="Database Integrity Error")
#         finally:
#             return self.error_response.send_response()
#
#     def get_by_id(self, id):
#         try:
#             self.error_response.get_response(error_code=0, msg="Found Record !", obj= self.db_session.query(self.model).filter(self.model.id == id).first())
#         except SQLAlchemyError as e:
#             app_logger.error(f"Error getting {self.model.__name__} by ID: {str(e)}")
#             self.error_response.get_response(error_code=23503, msg="Database Integrity Error")
#         finally:
#             return self.error_response.send_response()
#
#     def get_all(self, skip=0, limit=100, order_by="id", desc_order=False):
#         try:
#             query = self.db_session.query(self.model)
#             if hasattr(self.model, order_by):
#                 order_field = getattr(self.model, order_by)
#                 if desc_order:
#                     query = query.order_by(desc(order_field))
#                 else:
#                     query = query.order_by(asc(order_field))
#             if limit == -1:
#                 self.error_response.get_response(error_code=0, msg="Found Records !", obj= query.offset(skip).all())
#             else:
#                 self.error_response.get_response(error_code=0, msg="Found Records !", obj= query.offset(skip).limit(limit).all())
#         except SQLAlchemyError as e:
#             app_logger.error(f"Error getting {self.model.__name__} by ID: {str(e)}")
#             self.error_response.get_response(error_code=1, msg="Database Integrity Error")
#         finally:
#             return self.error_response.send_response()
#
#     def update(self, id, **kwargs):
#         try:
#             db_obj = self.get_by_id(id)
#             if not db_obj:
#                 self.error_response.get_response(error_code=0, msg="Found Records !", obj=None)
#             for field, value in kwargs.items():
#                 if hasattr(db_obj, field):
#                     setattr(db_obj, field, value)
#             self.db_session.commit()
#             self.db_session.refresh(db_obj)
#             return db_obj
#         except SQLAlchemyError as e:
#             self.db_session.rollback()
#             app_logger.error(f"Error getting {self.model.__name__} by ID: {str(e)}")
#             self.error_response.get_response(error_code=1, msg="Database Integrity Error")
#
#     def delete(self, id):
#         try:
#             db_obj = self.get_by_id(id)
#             if not db_obj:
#                 return False
#
#             self.db_session.delete(db_obj)
#             self.db_session.commit()
#             return True
#         except SQLAlchemyError as e:
#             self.db_session.rollback()
#             print(f"Error deleting {self.model.__name__}: {str(e)}")
#             raise f"Database Integrity Error while calling {inspect.currentframe().f_code.co_name}"
#
#     def get_by_field(self, field_name, value):
#         try:
#             if hasattr(self.model, field_name):
#                 field = getattr(self.model, field_name)
#                 return self.db_session.query(self.model).filter(field == value).first()
#             return None
#         except SQLAlchemyError as e:
#             print(f"Error getting {self.model.__name__} by {field_name}: {str(e)}")
#             raise f"Database Integrity Error while calling {inspect.currentframe().f_code.co_name}"
#
#     def get_by_fields(self, **kwargs):
#         try:
#             query = self.db_session.query(self.model)
#
#             for field_name, value in kwargs.items():
#                 if hasattr(self.model, field_name):
#                     field = getattr(self.model, field_name)
#                     query = query.filter(field == value)
#             return query.all()
#         except SQLAlchemyError as e:
#             print(f"Error getting {self.model._name_} by fields: {str(e)}")
#             raise f"Database Integrity Error while calling {inspect.currentframe().f_code.co_name}"
#
#     def count(self):
#         try:
#             return self.db_session.query(self.model).count()
#         except SQLAlchemyError as e:
#             print(f"Error counting {self.model.__name__}: {str(e)}")
#             raise f"Database Integrity Error while calling {inspect.currentframe().f_code.co_name}"
#
#     @staticmethod
#     def convert_to_dict_list(objects):
#         if not objects:
#             return []
#         return [{column.name: getattr(obj, column.name) for column in obj.__table__.columns} for obj in objects]
#
#     @staticmethod
#     def convert_to_dict(obj):
#         if not obj:
#             return None
#         return {column.name: getattr(obj, column.name) for column in obj.__table__.columns}
#
#     def commit_it(self):
#         try:
#             self.db_session.commit()
#         except SQLAlchemyError as e:
#             self.db_session.rollback()
#             if hasattr(e.orig, 'pgcode'):
#                 if e.orig.pgcode == '23505':
#                     self.error_response.get_response(error_code=23505, msg="Not Unique")
#                 elif e.orig.pgcode == '23502':
#                     self.error_response.get_response(error_code=23502, msg="Null Value")
#                 elif e.orig.pgcode == '23503':
#                     self.error_response.get_response(error_code=23503, msg="Foreign Key Violation")
#             app_logger.error(f"Error getting {self.model.__name__} by ID: {str(e)}")
#             self.error_response.get_response(error_code=1, msg="Database Integrity Error")
