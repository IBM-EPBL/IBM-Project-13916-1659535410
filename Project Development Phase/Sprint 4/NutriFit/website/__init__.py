from flask import Flask
import ibm_db
from os import path
from flask_login import LoginManager
import json
from .models import User

dsn_hostname = ""
dsn_uid = ""
dsn_pwd = ""
dsn_driver =  "{IBM DB2 ODBC DRIVER}"
dsn_database = "BLUDB"
dsn_port = 0
dsn_protocol = "TCPIP"

dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};"
    "SECURITY=SSL"
).format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd)



def connect_db():
    conn = ibm_db.connect(dsn,"","")
    return conn

conn = connect_db()

def create_app():
    print("create_app")
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'password'
    


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        sql = "SELECT * FROM USERS WHERE ID = '" + str(id) + "'"
        stmt = ibm_db.exec_immediate(conn, sql)
        result = ibm_db.fetch_assoc(stmt)
        user = User(result['ID'], result['EMAIL'], result['FIRSTNAME'], result['LASTNAME'], result['PASSWORDHASH'], result['DOB'], result['GENDER'], result['HEIGHT'], result['WEIGHT'], result['WEIGHTGOAL'])
        return user

    return app