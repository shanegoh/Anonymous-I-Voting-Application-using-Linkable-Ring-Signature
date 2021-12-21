from flaskapp import app
from flaskapp.__init__ import *
from flaskapp.auth import *
from flask_cors import cross_origin
from flaskapp.db import mysql
from flaskapp.roleEnum import Role
from datetime import datetime


@app.route('/', methods=['GET'])
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

@app.route("/events", methods=['GET'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
@requires_auth
@requires_id_token
def findAllEvent():
    conn = mysql.connect() 
    try:
        cursor = conn.cursor()
        query = """SELECT e.event_id, 
                   a.area_name, 
                   e.start_date_time
                   FROM event e JOIN
                   area a ON e.area_id = a.area_id
                   WHERE e.del_flag = %s 
                   AND a.del_flag = %s """
        cursor.execute(query, (0,0))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
 
    except:
        print("Error: Unable to fetch any record of events")      

    payload = []
    for record in data:
        content = { 'event_id': record[0],
                    'area_name': record[1],
                    'start_date_time': record[2]}
        payload.append(content)
        content = {}
    
    return jsonify(payload)

@app.route("/findEventById/<id>")
@cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
@requires_auth
@requires_id_token
def findEventById(id):
    conn = mysql.connect() 
    try:
        cursor = conn.cursor()
        query = """SELECT election_type, 
                   area_id, 
                   start_date_time, 
                   end_date_time, 
                   candidate 
                   FROM event 
                   WHERE event_id = %s
                   AND del_flag = %s"""
        cursor.execute(query, (id, 0))
        data = cursor.fetchone()
        print(data)
        cursor.close()
        conn.close()
 
    except:
        print("Error: Unable to fetch any record of events")  
  
    # Get all information about the particular event
    payload = []
    event_content = { 'election_type':  data[0],
                      'area_id':  data[1],
                      'start_date_time':  data[2],
                      'end_date_time':  data[3],
                      'candidate':  data[4] }
    payload.append(event_content)
    return jsonify(payload)


@app.route("/findAllElectionTypeAndArea")
@cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
@requires_auth
@requires_id_token
def findAllElectionType():
    conn = mysql.connect() 
    try:
        cursor = conn.cursor()

        query =  """SELECT * FROM election_type WHERE del_flag = %s""";
        cursor.execute(query, 0);
        result_A = cursor.fetchall()

        query =  """SELECT * FROM area WHERE del_flag = %s""";
        cursor.execute(query, 0);
        result_B = cursor.fetchall()

        cursor.close()
        conn.close()
 
    except:
        print("Error: Unable to fetch any record of events") 

    # Get all types of election
    payload = []

    electionType_payload = []
    for record in result_A:
        election_type = { 'election_id': record[0],
                          'election_name': record[1]}
        electionType_payload.append(election_type)
        election_type = {}


    payload.append(electionType_payload)

    # Get all areas
    electionArea_payload = []
    for record in result_B:
        areas = { 'area_id': record[0],
                  'area_name': record[1],
                  'election_type': record[2]}
        electionArea_payload.append(areas)
        areas = {}

    payload.append(electionArea_payload)

    return jsonify(payload)


@app.route("/updateEvent/<id>", methods=['PUT'])
@app.route("/updateEvent", methods=['PUT'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
@requires_auth
@requires_id_token
def putEvent(id=""):
    # Need to add validation here
    # ...
    electionType = request.json['election_type']
    print(electionType)
    areaId = request.json['area_id']
    print(areaId)
    startDateTime = request.json['start_date_time']
    print(startDateTime)
    endDateTime = request.json['end_date_time']
    print(endDateTime)
    candidates = request.json['candidates']
    print(candidates)

    date = datetime.strptime(startDateTime, '%Y-%m-%dT%H:%M:%S.%fZ')
    print(date)
    conn = mysql.connect() 
    try:
        cursor = conn.cursor()
        query =  """SELECT COUNT(*) FROM election_type 
                    WHERE election_id = %s
                    AND del_flag = %s""";
        cursor.execute(query, (electionType,0));  
        result_A = cursor.fetchone()  

        query =  """SELECT COUNT(*) FROM area 
                    WHERE area_id = %s
                    AND del_flag = %s""";
        cursor.execute(query, (areaId,0));  
        result_B = cursor.fetchone()  
 

    except:
        print("Error: Unable to fetch any record of events") 


    return startDateTime;


@app.route("/deleteEventById/<id>", methods=['POST'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
@requires_auth
@requires_id_token
def deleteEvent(id):
    conn = mysql.connect() 
    try:
        cursor = conn.cursor()
        query =  """UPDATE event 
                    SET del_flag = %s 
                    WHERE event_id = %s""";
        rowCount = cursor.execute(query, (1, id));
        cursor.close()
        conn.commit()
        conn.close()
    except:
        print("Error: Record Not Found") 

    if rowCount == 1:
        messageJson = { "message" :"SUCCESS"}
    else:
        messageJson = { "message" :"FAIL"}

    return messageJson;


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