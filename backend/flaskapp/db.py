from flask_sqlalchemy import SQLAlchemy
from flaskapp.__init__ import *
from flaskext.mysql import MySQL

# mysql = MySQL()
# app.config['MYSQL_DATABASE_USER'] = os.getenv("MYSQL_DATABASE_USER")
# app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv("MYSQL_DATABASE_PASSWORD")
# app.config['MYSQL_DATABASE_DB'] = os.getenv("MYSQL_DATABASE_DB")
# app.config['MYSQL_DATABASE_HOST'] = os.getenv("MYSQL_DATABASE_HOST")
#app.config['MYSQL_SSL_CA'] = 'mysql+pymysql://admin:TLJB4r8NnfLu42bf@fyp.cu4xpbknfumi.ap-southeast-1.rds.amazonaws.com/production?sslmode=verify-ca&sslrootcert=ap-southeast-1-bundle.pem'
# mysql.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:TLJB4r8NnfLu42bf@fyp.cu4xpbknfumi.ap-southeast-1.rds.amazonaws.com/production?ssl_ca=C:/Users/nintu/Desktop/ap-southeast-1-bundle.pem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String, nullable=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.Integer, nullable=False)
    area_id = db.Column(db.String, nullable=True)
    public_key = db.Column(db.String, nullable=True)
    private_key = db.Column(db.String, nullable=True)
    key_image = db.Column(db.String, nullable=True)


users = Users.query.all()
print(users)