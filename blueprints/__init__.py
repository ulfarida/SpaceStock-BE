import json, os
from datetime import timedelta
from functools import wraps

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_cors import CORS

app = Flask(__name__)

app.config['APP_DEBUG']=True


# =========================================
# ================DATABASE=================
# =========================================

try :
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:alta123@0.0.0.0:3306/building_test'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:alta123@0.0.0.0:3306/building'
except Exception as e :
    raise e

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# ======================================
# =========IMPORT BLUEPRINT=============
# ======================================

from blueprints.building.resources import bp_building
app.register_blueprint(bp_building, url_prefix = '/building')

db.create_all()


@app.after_request
def after_request(response):
    try:
        requestData = request.get_json()
    except Exception as e:
        requestData = request.args.to_dict()

    log = {
        'status_code':response.status_code,
        'method':request.method,
        'code':response.status,
        'uri':request.full_path,
        'request': requestData, 
        'response': json.loads(response.data.decode('utf-8'))
    }

    if response.status_code == 200:
        app.logger.info("REQUEST_LOG\t%s", json.dumps(log))
    elif response.status_code >= 400:
        app.logger.warning("REQUEST_LOG\t%s", json.dumps(log))
    
    return response