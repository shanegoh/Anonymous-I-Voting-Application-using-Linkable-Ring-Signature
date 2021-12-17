from flaskapp import app
from flaskapp.__init__ import *
from flaskapp.auth import *
from flask_cors import cross_origin
from flaskapp.db import mysql
from flaskapp.roleEnum import Role

@app.route('/wtf', methods=['GET'])
def hello():
    return 'Hello, GET!'

@app.route('/wtf', methods=['POST'])
def zxc():
    name = request.json['name']
    return name;

    #Controllers API

#This needs authentication
@app.route("/api/private")
@cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
@requires_auth
@requires_id_token
def private():
    conn = mysql.connect()
    try:
        cursor = conn.cursor()
        query = """SELECT role from users WHERE email = %s"""
        email = session['email']
        cursor.execute(query, email)
        data = cursor.fetchone()
        role_id = data[0]
        cursor.close()
        conn.close()
 
    except:
        print("Error: Unable to fetch any record")

    # Validate user role 
    if role_id == Role.Admin.value:             # 0 = Admin
        response = jsonify({"role_id": role_id,
                            "sample": 123})
    else:                                       # 1 = Voter
        response = jsonify({"role_id": role_id,
                            "sample": 456})
    
    return response


# This needs authorization
@app.route("/api/private-scoped")
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def private_scoped():
    if requires_scope("read:messages"):
        response = "Hello from a private endpoint! You need to be authenticated and have a scope of read:messages to see this."
        return jsonify(message=response)
    raise AuthError({
        "code": "Unauthorized",
        "description": "You don't have access to this resource"
    }, 403)