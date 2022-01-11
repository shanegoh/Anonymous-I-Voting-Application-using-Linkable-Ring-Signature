from flask_sqlalchemy import SQLAlchemy
from flaskapp.__init__ import *

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/{}?ssl_ca=./flaskapp/ap-southeast-1-bundle.pem'.format(os.getenv("MYSQL_DATABASE_USER"), os.getenv("MYSQL_DATABASE_PASSWORD"), os.getenv("MYSQL_DATABASE_HOST"), os.getenv("MYSQL_DATABASE_DB"))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

