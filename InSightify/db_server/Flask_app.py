from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from InSightify.db_server.app_orm import dbEngine
from sqlalchemy.orm import scoped_session, sessionmaker
from InSightify.Common_files.app_logger import Logger
import os
from InSightify.Common_files.config import config

static_folder_path = os.path.join(config.BASE_DIR, "Files")

# --- Initialize the Flask App with the static folder configuration ---
app = Flask(__name__, static_folder=static_folder_path, static_url_path="/static")
app_logger = Logger().get_logger()
CORS(app)
api = Api(app)
Session = sessionmaker(bind=dbEngine)
dbsession = scoped_session(Session)

@app.route('/test')
def test_route():
    return {'message': 'Flask app is working!'}

@app.teardown_appcontext
def shutdown_session(exception=None):
    dbsession.remove()
    

