from flaskapp import app
from flaskapp.__init__ import *
from flaskapp.auth import *
from flask_cors import cross_origin
from flaskapp.db import mysql
from flaskapp.roleEnum import Role
from datetime import datetime , timezone
import json
import pytz
from flask import Response

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
def putEvent(id=-1):

    electionType = request.json['election_type']
    areaId = request.json['area_id']
    startDateTime = request.json['start_date_time']
    endDateTime = request.json['end_date_time']
    candidates = request.json['candidates']

    conn = mysql.connect()
    try:
        cursor = conn.cursor()

        query =  """SELECT * FROM election_type WHERE election_id = %s AND del_flag = %s""";
        result_A = cursor.execute(query, (electionType,0));  
        print(result_A)
        query =  """SELECT * FROM area WHERE area_id = %s AND del_flag = %s""";
        result_B = cursor.execute(query, (areaId,0));  
        print(result_B)
        time_difference = datetime.strptime(endDateTime, '%Y-%m-%dT%H:%M:%S.%fZ') - datetime.strptime(startDateTime, '%Y-%m-%dT%H:%M:%S.%fZ')
        result = time_difference.total_seconds() * 1000     #Multiply by 1000 for milliseconds
        result_C = (True if result >= 14400000 else False)
        print(result_C)
        # to do: valid the start time make sure it does not fall in the past
        date_time_now_UTC = datetime.now(timezone.utc)
        parsedTime = datetime.strptime(startDateTime, '%Y-%m-%dT%H:%M:%S.%fZ')
        startDateTime_formatted_UTC = datetime.strftime(parsedTime, '%Y-%m-%d %H:%M:%S')
        currentDateTime_formatted_UTC = datetime.strftime(date_time_now_UTC, '%Y-%m-%d %H:%M:%S')
        result_D = (True if currentDateTime_formatted_UTC < startDateTime_formatted_UTC else False)
        print(result_D)
        # Rebuild the json data, if violated, error will be thrown
        payload = []
        for object in candidates:
            candidate = {"name" : object['name'], "image" : object['image']}
            payload.append(candidate)
            candidate = {}
        
        candidate_payload = json.dumps({"candidates": payload})

        # election_type, area, time diff must be correct in order to proceed
        if (result_A & result_B & result_C & result_D):
            # If id is present
            print("YES")
            if id != -1:
                print("Yes got ID")
                query =  """SELECT * FROM event 
                            WHERE event_id = %s
                            AND del_flag = %s""";
                result_E = cursor.execute(query,(id,0));
            else:
                result_E = False;

            # Got record, we need to update
            if (result_E):
                print("Updating")
                query =  """UPDATE event SET
                            election_type = %s,
                            area_id = %s,
                            start_date_time = %s,
                            end_date_time = %s,
                            candidate = %s
                            WHERE event_id = %s
                            AND del_flag = %s""";
                result_F = cursor.execute(query, 
                                            (electionType, 
                                                areaId, 
                                                datetime.strptime(startDateTime, '%Y-%m-%dT%H:%M:%S.%fZ'), 
                                                datetime.strptime(endDateTime, '%Y-%m-%dT%H:%M:%S.%fZ'),
                                                candidate_payload,
                                                id,0))
                message = ("Event Successfully Updated" if result_F else "Record Already Updated")
                status = 200
            else:
                print("Attempt Inserting")
                query =  """SELECT * FROM event WHERE area_id = %s AND del_flag = %s"""
                result_G = cursor.execute(query, (areaId, 0))
                message = "This event has already been created. Multiple events with same area are not allowed."
                status = 406

                # If result not found = no duplicate, insert data
                if (not result_G):
                    query =  """INSERT INTO event 
                    (election_type, 
                    area_id, 
                    start_date_time, 
                    end_date_time, 
                    candidate, 
                    del_flag) VALUES 
                                ( %s, %s, %s, %s, %s, %s)""";
                            
                    result_H = cursor.execute(query, 
                                                (electionType,
                                                    areaId, 
                                                    datetime.strptime(startDateTime, '%Y-%m-%dT%H:%M:%S.%fZ'), 
                                                    datetime.strptime(endDateTime, '%Y-%m-%dT%H:%M:%S.%fZ'),
                                                    candidate_payload,0))    
                    message = ("Event Successfully Created" if result_H else "Event Not Created")    
                    status = (201 if result_H else 406)   

            cursor.close()
            conn.commit()
            conn.close()  
        else:
            message = 'Event information is invalid. Please verify.'
            print(message)
            status = 406
 
    except:
        message = 'Unable create event. Please try again.'
        print(message)
        status = 406
                 
    return Response(json.dumps({"message": message}), status, mimetype='application/json') 


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
        result_A = cursor.execute(query, (1, id));
        cursor.close()
        conn.commit()
        conn.close()
    except:
        print("Error: Record Not Found") 

    if result_A:
        status = { "status" : "SUCCESS",
                    "message" : "Successfully deleted."}
    else:
        status = { "status" : "FAIL",
                   "message" : "Error! Failed delete event. Please try again."}

    return status


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