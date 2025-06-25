from DCE.dbserver.flask_app import dbsession
from DCE.Leggero.Leggero_psycopg2 import LeggeroPsycopg2
from DCE import DBFUNCTION
import os
from DCE.Leggero.Leggero_Model_Reflection import LeggeroApplicationDB
from sqlalchemy.engine.reflection import Inspector


class ViewRefresh:
    def __init__(self):
        self.session = dbsession
        self.psycopg2 = LeggeroPsycopg2()
        self.connection = self.psycopg2.get_connection()
        self.cursor = self.connection.cursor()
        self.cursor.execute("SET SCHEMA 'in_use'")
        self.normal_views = []
        self.files = []

    def delete_view(self):
        for v_rec in self.normal_views:
            del_query = 'DROP view IF EXISTS {} CASCADE;'.format(v_rec)
            try:
                self.cursor.execute(del_query)
            except Exception as e:
                print({'rec': v_rec, 'msg': e})
        self.connection.commit()

    def get_view_files(self):
        dirname = os.path.dirname(os.path.abspath(DBFUNCTION.__file__))
        for dirpath, dirnames, filenames in os.walk(os.path.join(dirname, 'view_definitions')):
            self.files = [os.path.join(dirpath, fname) for fname in filenames]

    def get_file_data(self, filename):
        view_def = open(filename, 'r').read()
        return view_def

    def create_view(self):
        """
        This function is used to create or replace view using psycopg2 connection:
        Summary:There are some specific views which were not being executed by SqlAlchemy due to wrong interpretation by
        sqlalchmy, Like,.case_timeslots.sql,my_cases_created_today_timeslots_repvw.sql,in these query
        Therefore, we need to use
        psycopg2 connection which executes same query without raising any error
        """
        all_files = self.files
        total_views = len(all_files)
        view_run_count_map = {}
        views_not_refreshed = []
        while all_files:
            current = all_files.pop(0)
            content = self.get_file_data(current)
            try:
                self.cursor.execute(content)
            except Exception as e:
                if view_run_count_map.get(current, 0) > 100:
                    views_not_refreshed.append(current)
                else:
                    all_files.append(current)
                self.connection.rollback()
            else:
                self.connection.commit()
            view_run_count_map[current] = view_run_count_map.get(current, 0) + 1

        print("Refreshed:")
        print("Views Refreshed: ", total_views-len(views_not_refreshed))
        print("Views Unrefreshed: ", len(views_not_refreshed))
        print("Unrefreshed Views: ", views_not_refreshed)

    def del_cursor(self):
        self.connection.close()

    def get_view_names(self):
        _ladb = LeggeroApplicationDB('DCEAPP')
        engine = _ladb.get_dbengine()
        insp = Inspector.from_engine(engine)
        views = insp.get_view_names('in_use')

        material_views = []
        self.normal_views = [i for i in views if i not in material_views]

    def create_material_views(self):
        """
        Summary:This function is used to refresh some exceptional matriral views those were used to delete while
        refreshing normal views, therefore we need to create them.
        """
        mat_views = []
        m_views = ['cases_all_logged_mat_view.sql']
        dirname = os.path.dirname(os.path.abspath(DBFUNCTION.__file__))
        for dirpath, dirnames, filenames in os.walk(os.path.join(dirname, 'material_view_definitions')):
            mat_views = [os.path.join(dirpath, fname) for fname in filenames if fname in m_views]

        self.files = mat_views
        self.create_view()


if __name__ == '__main__':
    obj = ViewRefresh()
    obj.get_view_names()
    obj.delete_view()
    obj.get_view_files()
    obj.create_view()
    obj.create_material_views()
    obj.del_cursor()

