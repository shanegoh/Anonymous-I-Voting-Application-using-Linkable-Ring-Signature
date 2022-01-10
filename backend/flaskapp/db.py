from flask_sqlalchemy import SQLAlchemy
from flaskapp.__init__ import *

#from flaskext.mysql import MySQL

# mysql = MySQL()
# app.config['MYSQL_DATABASE_USER'] = os.getenv("MYSQL_DATABASE_USER")
# app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv("MYSQL_DATABASE_PASSWORD")
# app.config['MYSQL_DATABASE_DB'] = os.getenv("MYSQL_DATABASE_DB")
# app.config['MYSQL_DATABASE_HOST'] = os.getenv("MYSQL_DATABASE_HOST")
#app.config['MYSQL_SSL_CA'] = 'mysql+pymysql://admin:TLJB4r8NnfLu42bf@fyp.cu4xpbknfumi.ap-southeast-1.rds.amazonaws.com/production?sslmode=verify-ca&sslrootcert=ap-southeast-1-bundle.pem'
# mysql.init_app(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:TLJB4r8NnfLu42bf@fyp.cu4xpbknfumi.ap-southeast-1.rds.amazonaws.com/production?ssl_ca=C:/Users/nintu/Desktop/ap-southeast-1-bundle.pem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}?ssl_ca=./flaskapp/ap-southeast-1-bundle.pem'.format(os.getenv("MYSQL_DATABASE_USER"), os.getenv("MYSQL_DATABASE_PASSWORD"), os.getenv("MYSQL_DATABASE_HOST"), os.getenv("MYSQL_DATABASE_DB"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# class Users(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     nickname = db.Column(db.String, nullable=True)
#     email = db.Column(db.String, unique=True, nullable=False)
#     password = db.Column(db.String, nullable=False)
#     role = db.Column(db.Integer, nullable=False, default=1)
#     area_id = db.Column(db.String, nullable=True)
#     public_key = db.Column(db.String, nullable=True)
#     private_key = db.Column(db.String, nullable=True)
#     key_image = db.Column(db.String, nullable=True)

# class Event(db.Model):
#     event_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
#     election_type = db.Column(db.Integer, nullable=False)
#     area_id = db.Column(db.String, unique=True, nullable=False)
#     start_date_time = db.Column(db.DateTime, nullable=False)
#     end_date_time = db.Column(db.DateTime, nullable=False)
#     del_flag = db.Column(db.Integer, nullable=False, default=0)
#     expire_flag = db.Column(db.Integer, nullable=False, default=0)

# class ElectionType(db.Model):
#     election_id = db.Column(db.Integer, primary_key=True, nullable=False)
#     election_name = db.Column(db.String, nullable=False)
#     del_flag = db.Column(db.Integer, nullable=False, default=0)

# class Candidate(db.Model):
#     id = db.Column(db.Integer, primary_key=True, nullable=False)
#     event_id = db.Column(db.Integer, nullable=False)
#     candidate_name = db.Column(db.String, nullable=False)
#     candidate_image = db.Column(db.String, nullable=False)
#     vote_count = db.Column(db.Integer, nullable=False, default=0)
#     del_flag = db.Column(db.Integer, nullable=False, default=0)

# class Area(db.Model):
#     area_id = db.Column(db.String, primary_key=True, nullable=False, unique=True)
#     area_name = db.Column(db.String, nullable=False)
#     election_type = db.Column(db.String, nullable=False)
#     del_flag = db.Column(db.Integer, nullable=False, default=0)

# #Check if the protocol is ecrypted
# result = db.engine.execute("SHOW STATUS LIKE 'Ssl_cipher'")
# names = [row[1] for row in result]
# print (names)

# print(Users.query.limit(1).all())