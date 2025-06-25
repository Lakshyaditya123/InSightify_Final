from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from InSightify.db_server.app_orm import dbEngine
from sqlalchemy.orm import scoped_session, sessionmaker
from InSightify.Common_files.app_logger import Logger

app = Flask(__name__)
app_logger = Logger().get_logger()
CORS(app)
api = Api(app)
Session = sessionmaker(bind=dbEngine)
dbsession = scoped_session(Session)

# Add a simple test route to verify Flask is working
@app.route('/test')
def test_route():
    return {'message': 'Flask app is working!'}

