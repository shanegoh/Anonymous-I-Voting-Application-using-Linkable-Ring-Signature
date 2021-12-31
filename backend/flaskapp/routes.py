from numpy import result_type
from flaskapp import app
from flaskapp.__init__ import *
from flaskapp.auth import *
from flask_cors import cross_origin
from flask import Response
from flaskapp.db import mysql
from flaskapp.roleEnum import Role
from datetime import datetime , timezone
from flaskapp.linkable_ring_signature import *
import json
import pandas as pd
import http.client
import string
import base64
import numpy as np
import traceback
import ast

#Controllers API
#This needs authentication
@app.route("/findUserInformation")
@cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
@requires_auth
@requires_id_token
def findUserInformation():
    x, y = generate_keys(1)
    private_key = export_private_keys_in_list(x)
    public_key = export_private_keys_in_list(y)
    print("Private Key: %s"%private_key[0])
    print("Public Key: %s"%public_key[0])
    conn = mysql.connect()
    try:
        cursor = conn.cursor()
        query = """SELECT role, area_id from users WHERE email = %s"""
        cursor.execute(query, session['email'])
        data = cursor.fetchone()
        role_id = data[0]
        area_id = data[1]
        cursor.close()
        conn.close()
        message = "Successfully retrieve record."
        status = 200
    except:
        print("Could not get user information")
        return Response(json.dumps({"message": "Could not get user information. Please refresh and try again. "\
            "If the problem persist, please contact the administrator"}), 400, mimetype='application/json') 

    # Validate user role 
    if role_id == Role.Admin.value:             # 0 = Admin
        response = {"role_id": role_id}
    else:                                       # 1 = Voter
        response ={"role_id": role_id, "area_id": area_id}
    
    return Response(json.dumps({"message": message, "record": response}), status, mimetype='application/json') 


@app.route("/findElectionForVoter", methods=['GET'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
@requires_auth
@requires_id_token
def findElectionForVoter():
    conn = mysql.connect()
    try:
        cursor = conn.cursor()
        query = """SELECT area_id FROM users WHERE email = %s"""
        cursor.execute(query, session['email'])
        result_A = cursor.fetchone()
        area_id = result_A[0]
        print(area_id)
        query = """SELECT e.event_id, 
                   a.area_name, 
                   e.start_date_time,
                   e.end_date_time
                   FROM event e JOIN
                   area a ON e.area_id = a.area_id
                   WHERE e.del_flag = %s 
                   AND a.del_flag = %s 
                   AND e.expire_flag = %s
                   AND e.area_id = %s"""
        cursor.execute(query,(0,0,0,area_id))
        result_B = cursor.fetchone()
        payload = { 'event_id': result_B[0],
                    'area_name': result_B[1],
                    'start_date_time': result_B[2],
                    'end_date_time': result_B[3]}
        cursor.close()
        conn.close()
    except:
        print("Could not get any elections.")
        return Response(json.dumps({"message": "There is no event for you."}), 404, mimetype='application/json') 
    
    return jsonify(payload)

@app.route("/findCandidateByEventId/<id>", methods=['GET'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
@requires_auth
@requires_id_token
def findCandidateByEventId(id):
    conn = mysql.connect()
    try:
        cursor = conn.cursor()
        query = """SELECT (SELECT area_name FROM area WHERE area_id IN (SELECT area_id 
                    FROM event WHERE event_id = 18)) as area_name, candidate_name, 
                    candidate_image 
                    FROM candidate 
                    WHERE event_id = %s 
                    AND del_flag = %s"""
        cursor.execute(query, (id,0))
        result_A = cursor.fetchall()
        payload = []
        for record in result_A:
            # Encode png as base64
            with open(record[2], "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            content = { 'area_name': record[0],
                        'candidate_name': record[1],
                        'candidate_image': encoded_string.decode('UTF-8')}
            payload.append(content)
        cursor.close()
        conn.close()
    except:
        print("Could not get any candidates")
        return Response(json.dumps({"message": "Could not get any candidates"}), 400, mimetype='application/json') 
    
    return jsonify(payload)


@app.route("/voteCandidate", methods=['PUT'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
@requires_auth
@requires_id_token
def voteCandidate():
    conn = mysql.connect()
    try:
        cursor = conn.cursor()
        # query to count total participants
        query = """SELECT COUNT(*) as number_of_participants 
                    FROM users WHERE area_id 
                    IN (SELECT area_id FROM event where event_id = %s)"""
        cursor.execute(query, request.json['event_id'])
        result_A = cursor.fetchone()
        number_of_participants = result_A[0]

        # query to find all private and public key to respective event
        query = """SELECT private_key, public_key FROM users WHERE area_id 
                    IN (SELECT area_id FROM event 
                    WHERE event_id = %s AND del_flag = %s AND expire_flag = %s)"""
        cursor.execute(query, (request.json['event_id'],0,0))
        result_B = cursor.fetchall()

        x = []  # list of all secret keys
        y = []  # list of all public keys
        for record in result_B:
            x.append(int(record[0]))
            assert record[1][0] == "(" and record[1][-1] == ")"
            e1 = int(record[1][1:-1].split(",")[0])
            e2 = int(record[1][1:-1].split(",")[1])
            y.append(ecdsa.ellipticcurve.Point(curve_secp256k1, e1, e2)) # convert to Point object

        private_key = int(request.json['private_key'])
        i = 0
        j = 0
        for k in range(0,number_of_participants):
            if private_key == x[k]:
                i = k   
                break
            j += 1
        assert (j == number_of_participants) == False, "Please check that you have entered a valid key."

        signature = ring_signature(private_key, i, request.json['candidate_name'], y)
        assert verify_ring_signature(request.json['candidate_name'], y, *signature) == True, "Invalid Signature"
        
        # fetch signature from database record
        query = """SELECT signature FROM users WHERE private_key = %s"""
        cursor.execute(query, request.json['private_key'])
        result_C = cursor.fetchone()

        # If voter's record doesnt have the signature
        if(str(result_C[0]) == "None"):
            # add signature
            query = """UPDATE users SET signature = %s WHERE private_key = %s"""
            assert cursor.execute(query, (get_image_from_signature(signature), request.json['private_key'])) == 1, "Failed to update signature"
            query = """UPDATE candidate SET vote_count = (vote_count + 1) 
                        WHERE event_id = %s 
                        AND candidate_name = %s
                        AND del_flag = %s"""
            assert cursor.execute(query,(request.json['event_id'],request.json["candidate_name"],0))
            cursor.close()
            conn.commit()
            conn.close()
            message = "Success!"
            status = 200
        else:
            keyImage = ast.literal_eval(result_C[0]) # convert string list to list
            assert check_keyImage(signature, keyImage) == True, "There might be some error."
            print("hre")
            message = "You are only allowed to vote once."
            status = 400
    except Exception:
        traceback.print_exc()
        message = traceback.format_exc() #continue here!
        print("Hello")
        return Response(json.dumps({"message": message}), 400, mimetype='application/json') 
   
    return Response(json.dumps({"message": message}), status, mimetype='application/json') 


@app.route("/findAllEvent", methods=['GET'])
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
                   AND a.del_flag = %s 
                   AND e.expire_flag = %s"""
        cursor.execute(query, (0,0,0))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        payload = []
        for record in data:
            content = { 'event_id': record[0],
                        'area_name': record[1],
                        'start_date_time': record[2]}
            payload.append(content)
            content = {}
    except:
        print("Error: Unable to fetch any record of events")
        message = "Error: Unable to fetch any record of events"      
        return Response(json.dumps({"message": message}), 400, mimetype='application/json') 
        
    return jsonify(payload)


@app.route("/findPastEvent", methods=['GET'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
@requires_auth
@requires_id_token
def findPastEvent():
    conn = mysql.connect() 
    try:
        cursor = conn.cursor()
        query = """SELECT e.event_id, 
                   a.area_name, 
                   e.start_date_time
                   FROM event e JOIN
                   area a ON e.area_id = a.area_id
                   WHERE e.del_flag = %s 
                   AND a.del_flag = %s 
                   AND e.expire_flag = %s"""
        cursor.execute(query, (0,0,1))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
 
        payload = []
        for record in data:
            print(record[2])
            content = { 'event_id': record[0],
                        'area_name': record[1],
                        'start_date_time': record[2]}
            payload.append(content)
            content = {}
        message = "Successfully retrieve all records."  
        status = 200 
    except:
        print("Error: Unable to fetch any record of events")
        message = "Unable to fetch any record of events. Please refresh."      
        return Response(json.dumps({"message": message}), 400, mimetype='application/json') 
        
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
                   end_date_time
                   FROM event 
                   WHERE event_id = %s
                   AND del_flag = %s
                   AND expire_flag = %s"""
        cursor.execute(query, (id,0,0))
        result_A = cursor.fetchone()
        print(result_A)

        query = """SELECT candidate_name, candidate_image
                   FROM candidate 
                   WHERE event_id = %s
                   AND del_flag = %s"""
        cursor.execute(query, (id,0))
        result_B = cursor.fetchall()
        print(result_B)
        cursor.close()
        conn.close()

        candidate_payload = []
        for record in result_B:
            candidate_content = { 'candidate_name':  record[0],
                                'candidate_image':  record[1] }
            candidate_payload.append(candidate_content) 

        # Get all information about the particular event + candidate
        payload = []
        event_content = { 'election_type':  result_A[0],
                        'area_id':  result_A[1],
                        'start_date_time':  result_A[2],
                        'end_date_time':  result_A[3], 
                        'candidates': candidate_payload}    
        payload.append(event_content)
    except:
        print("Error: Unable to fetch any record of events")  
        message = "Unable to fetch any record of events. Please refresh."
        return Response(json.dumps({"message": message}), 400, mimetype='application/json') 
        
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
@app.route("/createEvent", methods=['PUT'])
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

        message = ""
        # Rebuild the json data, if violated, error will be thrown
        # Also store only the image path for candidate image
        candidate_payload = []
        for object in candidates:
            image_b64 = object['candidate_image']
            base64result = image_b64.split(',')[1];
            as_bytes = bytes(base64result, 'utf-8')
            image_path = "img/" + object['candidate_name'] + ".png"
            with open(image_path, "wb") as fh:
              fh.write(base64.decodebytes(as_bytes))

            candidate = {"candidate_name" : object['candidate_name'], 
                          "candidate_image" : image_path}
            candidate_payload.append(candidate)
            candidate = {}
        
        print(candidate_payload)


        # election_type, area, time diff must be correct in order to proceed
        if (result_A & result_B & result_C & result_D):
            # If id is present
            print("YES")
            if id != -1:
                print("Yes got ID")
                query =  """SELECT * FROM event 
                            WHERE event_id = %s
                            AND del_flag = %s
                            AND expire_flag = %s""";
                result_E = cursor.execute(query,(id,0,0));
            else:
                result_E = False;

            # Got record, we need to update
            if (result_E):
                print("Updating")
                query =  """UPDATE event SET
                            election_type = %s,
                            area_id = %s,
                            start_date_time = %s,
                            end_date_time = %s
                            WHERE event_id = %s
                            AND del_flag = %s
                            AND expire_flag = %s""";
                cursor.execute(query, 
                                (electionType, 
                                    areaId, 
                                    datetime.strptime(startDateTime, '%Y-%m-%dT%H:%M:%S.%fZ'), 
                                    datetime.strptime(endDateTime, '%Y-%m-%dT%H:%M:%S.%fZ'),
                                    id,0,0))

                message = "Event Successfully Updated"
                print(message)
                status = 200
            else:
                print("Attempt Inserting")
                query =  """SELECT * FROM event WHERE area_id = %s AND del_flag = %s AND expire_flag = %s"""
                result_G = cursor.execute(query, (areaId, 0,0))
                message = "This event has already been created. Multiple events with same area are not allowed."
                status = 406

                # If result not found = no duplicate, insert data
                if (not result_G):
                    query =  """INSERT INTO event 
                    (election_type, 
                    area_id, 
                    start_date_time, 
                    end_date_time, 
                    del_flag,
                    expire_flag) VALUES 
                                ( %s, %s, %s, %s, %s, %s)""";
                            
                    result_H = cursor.execute(query, 
                                                (electionType,
                                                    areaId, 
                                                    datetime.strptime(startDateTime, '%Y-%m-%dT%H:%M:%S.%fZ'), 
                                                    datetime.strptime(endDateTime, '%Y-%m-%dT%H:%M:%S.%fZ'),
                                                    0,0))    
                    message = ("Event Successfully Created" if result_H else "Event Not Created")    
                    status = (201 if result_H else 406)   
                 
            conn.commit()
          
            # First "remove" the old candidates
            query = """UPDATE candidate SET del_flag = %s WHERE event_id = %s""";
            cursor.execute(query,(1,id))
          
            query = """SELECT event_id FROM event WHERE 
                        election_type = %s AND
                        area_id = %s AND
                        start_date_time = %s AND
                        end_date_time = %s AND
                        del_flag = %s AND
                        expire_flag = %s"""
            cursor.execute(query,(electionType,
                                    areaId,
                                        datetime.strptime(startDateTime, '%Y-%m-%dT%H:%M:%S.%fZ'),
                                        datetime.strptime(endDateTime, '%Y-%m-%dT%H:%M:%S.%fZ'),0,0))
            result_F = cursor.fetchone()
            id = result_F[0]
         
            # Insert back the new candidates
            query = """INSERT INTO candidate 
            (event_id, candidate_name, candidate_image)  
            VALUES""";
            for record in candidate_payload:
                    query += """ (%s, "%s", "%s"),""" %(id,record['candidate_name'], record['candidate_image'])
            print(query)
            cursor.execute(query[:-1]);
            print("Reach here")
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
        return Response(json.dumps({"message": message}), 400, mimetype='application/json') 
                 
    return Response(json.dumps({"message": message}), status, mimetype='application/json') 



@app.route("/deleteEventById/<id>", methods=['DELETE'])
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
        query = """UPDATE candidate SET del_flag = %s WHERE event_id =%s"""
        result_B = cursor.execute(query, (1, id));
        message = ("Successfully deleted." if result_A & result_B else "Error! Failed delete event. Please try again.")
        status = (200 if result_A & result_B else 404)
        cursor.close()
        conn.commit()
        conn.close()

    except:
        print("Error: Record Not Found") 
        message = 'Failed to delete record. Please try again'
        return Response(json.dumps({"message": message}), 400, mimetype='application/json') 

    return Response(json.dumps({"message": message}), status, mimetype='application/json') 


@app.route("/findResultById/<id>", methods=['GET'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
@requires_auth
@requires_id_token
def findResultById(id):
    conn = mysql.connect() 
    try:
        cursor = conn.cursor()
        query =  """SELECT e.area_id, 
                    (SELECT area_name FROM area WHERE area_id = e.area_id) AS area_name, 
                    c.candidate_name, 
                    c.candidate_image, 
                    c.vote_count 
                    FROM candidate c
                    JOIN event e
                    ON c.event_id = e.event_id
                    WHERE c.event_id = %s""";

        cursor.execute(query, id);
        result_A = cursor.fetchall()
        cursor.close()
        conn.close()

        candidate_payload = []
        for record in result_A:
            candidate_content = { "area_id": record[0], 
                                    "area_name": record[1],
                                    "candidate_name": record[2], 
                                    "candidate_image": record[3], 
                                    "vote_count": record[4]}
            candidate_payload.append(candidate_content)

        message = "Successfully retrieve record."    
        status = 200
    except:
        print("Error: Record Not Found") 
        message = 'No record found. Please refresh.'
        return Response(json.dumps({"message": message}), 404, mimetype='application/json') 

    return Response(json.dumps({"message": message, "candidates": candidate_payload}), status, mimetype='application/json') 
  

# This needs authorization
@app.route("/upload", methods=["POST"])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
@requires_auth
@requires_id_token
def uploadFile():
    conn = mysql.connect() 
    try: 
        cursor = conn.cursor()
        # Use Auth0 Client secret and public key to get management_access_token
        connnection = http.client.HTTPSConnection("dev-i7062-qd.us.auth0.com")
        payload = "{\"client_id\":\"ziMcfPoiH2CFyrhKAaiOecnLsMs69lXF\",\"client_secret\":\"gsuu8u1O_qIylsmHry-8litgeu94wqLhPCbvJ56FBJ_kUgZp0qQ9ETCb17UOdm8E\",\"audience\":\"https://dev-i7062-qd.us.auth0.com/api/v2/\",\"grant_type\":\"client_credentials\"}"
        headers = { 'content-type': "application/json" }
        connnection.request("POST", "/oauth/token", payload, headers)
        res = connnection.getresponse()
        data = res.read()
        jsonData = json.loads(data)
        management_access_token = "Bearer " + jsonData["access_token"]

        # Get the excel file
        xlsx_file = request.files['file']
        data_xls = pd.read_excel(xlsx_file)
        number_of_participants = len(data_xls); # Check number of participants within the list.

        # Generate keys based on number of participants on the same area
        privateKey, publicKey = generate_keys(number_of_participants)
        private_key_list = export_private_keys_in_list(privateKey)
        public_key_list = export_private_keys_in_list(publicKey)
        print(private_key_list)
        print(public_key_list)
        user_list = []
        for i in data_xls.index:
            # Password generator
            ## characters to generate password from
            characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")   
            ## picking random characters from the list
            pass_phrase = []
            length = 20
            for k in range(length):
                pass_phrase.append(characters[int.from_bytes(os.urandom(1), byteorder="big") % len(characters)])   
            password = "".join(pass_phrase)
            # Generate key set

            # Store the details for later xlsx file output
            user = { "email": data_xls['email'][i], 
                        "role": data_xls['role'][i], 
                        "area_id":data_xls['area_id'][i], 
                        "password": password,
                        "private_key": private_key_list[i],
                        "public_key": public_key_list[i]}
            user_list.append(user)

            # add user to auth0
            payload = '{"email": "%s", '\
                        '"nickname": "%s", '\
                        '"connection": "Username-Password-Authentication", '\
                        '"password": "%s" }'%(data_xls['email'][i], "empty", password)
            # Use management_access_token to create user with auth0
            headers = {
                'content-type': "application/json",
                'authorization': management_access_token
                }
            connnection.request("POST", "/api/v2/users", payload, headers)
            res = connnection.getresponse()
            data = res.read()
        ############################################ End of for loop 

        print("Running Here before update")
        print(user_list)
        # Once mass creation is done, get all the email correspond with 
        # the area_id and update each record respectively
        for i, user in enumerate(user_list):
            print(public_key_list[i])
            query = """UPDATE users SET area_id = %s, role = %s, public_key = %s, private_key = %s WHERE email = %s """
            result = cursor.execute(query, (user['area_id'], user['role'], public_key_list[i], private_key_list[i], user['email']));
            print(result)
        cursor.close()
        conn.commit()
        conn.close()

        # Set user list into a excel format and encode the data
        df = pd.DataFrame(user_list)
        df.to_excel('Generated_Credentials.xlsx')
        data = open('Generated_Credentials.xlsx', 'rb').read()
        os.remove("Generated_Credentials.xlsx") # remove file after read
        base64_encoded = base64.b64encode(data).decode('UTF-8') # encode for sending back to front end
        message = "Success!"
        status = 200
    except:
        print("error")
        return Response(json.dumps({"message": "Fail"}), 400, mimetype='application/json') 

    return Response(json.dumps({"message": message, "excel_file": base64_encoded}), status, mimetype='application/json')
   
       

@app.route("/findVoteStatus", methods=["GET"])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
@requires_auth
@requires_id_token
def findVoteStatus():
    conn = mysql.connect() 
    try: 
        cursor = conn.cursor()
        query =  """SELECT a.area_name, IF(ISNULL(u.signature), "Not Submitted","Submitted")
                    FROM users u join area a ON a.area_id = u.area_id 
                    WHERE u.email = %s AND a.del_flag = %s""";
        cursor.execute(query, (session['email'], 0));
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        payload = {"area": result[0], "status": result[1]}
        status = 200
    except:
        message = "Failed to retrieve vote status"
        print(message)
        return Response(json.dumps({"message": message}), 400, mimetype='application/json') 

    return Response(json.dumps(payload), status, mimetype='application/json')
