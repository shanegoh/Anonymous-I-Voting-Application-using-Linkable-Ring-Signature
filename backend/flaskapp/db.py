from flaskext.mysql import MySQL
from flaskapp.__init__ import *


mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = os.getenv("MYSQL_DATABASE_USER")
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv("MYSQL_DATABASE_PASSWORD")
app.config['MYSQL_DATABASE_DB'] = os.getenv("MYSQL_DATABASE_DB")
app.config['MYSQL_DATABASE_HOST'] = os.getenv("MYSQL_DATABASE_HOST")
#app.config['MYSQL_SSL_CA'] = 'mysql+pymysql://admin:TLJB4r8NnfLu42bf@fyp.cu4xpbknfumi.ap-southeast-1.rds.amazonaws.com/production?sslmode=verify-ca&sslrootcert=ap-southeast-1-bundle.pem'
mysql.init_app(app)