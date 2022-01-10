from numpy import result_type
from flaskapp import app
from flaskapp.__init__ import *
from flaskapp.auth import *
from flask_cors import cross_origin
from flask import Response
from flaskapp.roleEnum import Role
from datetime import datetime , timezone
from flaskapp.linkable_ring_signature import *
import json
import pandas as pd
import http.client
import string
import base64
import numpy as np
import ast
import sys
from flaskapp.util import *
from flaskapp.services import *

@app.route("/")
@cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
def zxc():
    #return jsonify(user_dao.get_all())
    user = UserService().getUserInformation('production_admin@gmail.com')
    return jsonify(user)


#     return Response(json.dumps({"message": "ok"}), 200, mimetype='application/json') 

#Controllers API
#This needs authentication
@app.route("/findUserInformation")
@cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
@requires_auth
@requires_id_token
def findUserInformation():
    try:
        user = UserService().getUserInformation(session['email'])
        return jsonify(user)
    except:
        message = str(sys.exc_info()[1]) 
        print(message)
        return Response(json.dumps({"message": message}), 404, mimetype='application/json') 


# @app.route("/findElectionForVoter", methods=['GET'])
# @cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
# @requires_auth
# @requires_id_token
# def findElectionForVoter():
#     conn = mysql.connect()
#     try:
#         cursor = conn.cursor()
#         # Query to find area_id 
#         query = """SELECT area_id, key_image FROM users WHERE email = %s"""
#         cursor.execute(query, session['email'])
#         result_A = cursor.fetchone()
#         area_id = result_A[0]
#         print(area_id)
#         print( result_A[1] is None)
#         assert result_A[1] is None, "There is no event for you at the moment."
#         print("reach here")

#         query = """SELECT e.event_id, 
#                    a.area_name, 
#                    e.start_date_time,
#                    e.end_date_time
#                    FROM event e JOIN
#                    area a ON e.area_id = a.area_id
#                    WHERE e.del_flag = %s 
#                    AND a.del_flag = %s 
#                    AND e.expire_flag = %s
#                    AND e.area_id = %s"""
#         x = cursor.execute(query,(0,0,0,area_id))
#         result_B = cursor.fetchone()
#         assert result_B is not None, "There is no event for you at the moment."
#         payload = { 'event_id': result_B[0],
#                     'area_name': result_B[1],
#                     'start_date_time': result_B[2],
#                     'end_date_time': result_B[3]}
#         cursor.close()
#         conn.close()
#     except Exception:
#         message = str(sys.exc_info()[1]) 
#         print(message)
#         return Response(json.dumps({"message": message}), 404, mimetype='application/json') 
    
#     return jsonify(payload)

# @app.route("/findCandidateByEventId/<id>", methods=['GET'])
# @cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
# @requires_auth
# @requires_id_token
# def findCandidateByEventId(id):
#     conn = mysql.connect()
#     # need to add a validation : search base on email
#     try:
#         cursor = conn.cursor()
#         query = """SELECT a.area_name, c.candidate_name, c.candidate_image 
#                             FROM candidate c JOIN event e 
#                             ON c.event_id = e.event_id JOIN area a 
#                             ON e.area_id = a.area_id JOIN users u 
#                             ON a.area_id = u.area_id 
#                             WHERE u.email = %s
#                             AND isnull(key_image)
#                             AND c.event_id = %s
#                             AND e.del_flag = %s
#                             AND e.expire_flag = %s
#                             AND c.del_flag = %s
#                             AND a.del_flag = %s"""
#         assert (cursor.execute(query, (session['email'],id,0,0,0,0)) > 0), "No such event, redirecting..." 
#         result_A = cursor.fetchall()
#         payload = []
#         for record in result_A:
#             # Encode png as base64
#             with open(record[2], "rb") as image_file:
#                 encoded_string = base64.b64encode(image_file.read())
#             content = { 'area_name': record[0],
#                         'candidate_name': record[1],
#                         'candidate_image': encoded_string.decode('UTF-8')}
#             payload.append(content)
#         cursor.close()
#         conn.close()
#     except Exception:
#         message = str(sys.exc_info()[1]) 
#         print(message)
#         return Response(json.dumps({"message": message}), 400, mimetype='application/json') 
    
#     return jsonify(payload)


# @app.route("/voteCandidate", methods=['PUT'])
# @cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
# @requires_auth
# @requires_id_token
# def voteCandidate():
#     conn = mysql.connect()
#     try:
#         cursor = conn.cursor()
#         # query to count total participants
#         query = """SELECT COUNT(*) as number_of_participants 
#                     FROM users WHERE area_id 
#                     IN (SELECT area_id FROM event where event_id = %s)"""
#         cursor.execute(query, request.json['event_id'])
#         result_A = cursor.fetchone()
#         number_of_participants = result_A[0]

#         # query to find all private and public key to respective event
#         query = """SELECT private_key, public_key FROM users WHERE area_id 
#                     IN (SELECT area_id FROM event 
#                     WHERE event_id = %s AND del_flag = %s AND expire_flag = %s)"""
#         cursor.execute(query, (request.json['event_id'],0,0))
#         result_B = cursor.fetchall()

#         # query to find if the private key given is theirs
#         query = """SELECT email FROM users WHERE private_key = %s"""
#         cursor.execute(query, request.json['private_key'])
#         result_C = cursor.fetchone()
#         assert result_C is not None, "Invalid private key."
#         assert (session['email'] == result_C[0]) == True, "Private key does not belong to you!"

#         # Adding all private and public keys into each list
#         x = []  # list of all secret keys
#         y = []  # list of all public keys
#         for record in result_B:
#             x.append(int(record[0]))
#             assert record[1][0] == "(" and record[1][-1] == ")"
#             e1 = int(record[1][1:-1].split(",")[0])
#             e2 = int(record[1][1:-1].split(",")[1])
#             y.append(ecdsa.ellipticcurve.Point(curve_secp256k1, e1, e2)) # convert to Point object

#         # Getting the index_idx for signature
#         i = 0
#         for k in range(0,number_of_participants):
#             if int(request.json['private_key']) == x[k]:
#                 i = k   
#                 break

#         # Create and verify signature
#         signature = ring_signature(int(request.json['private_key']), i, request.json['candidate_name'], y)
#         assert verify_ring_signature(request.json['candidate_name'], y, *signature) == True, "Invalid Signature"
        
#         # fetch key_image from database record
#         query = """SELECT key_image FROM users WHERE private_key = %s"""
#         cursor.execute(query, request.json['private_key'])
#         result_D = cursor.fetchone()

#         # If voter's record doesnt have key_image
#         if(str(result_D[0]) == "None"):
#             # add key_image
#             query = """UPDATE users SET key_image = %s WHERE private_key = %s"""
#             assert cursor.execute(query, (get_image_from_signature(signature), request.json['private_key'])) == 1, "Failed to update key image"
#             query = """UPDATE candidate SET vote_count = (vote_count + 1) 
#                         WHERE event_id = %s 
#                         AND candidate_name = %s
#                         AND del_flag = %s"""
#             assert cursor.execute(query,(request.json['event_id'],request.json["candidate_name"],0))
#             cursor.close()
#             conn.commit()
#             conn.close()
#             message = "Success!"
#             status = 200
#         else:   # Else, if have, means voted already
#             keyImage = ast.literal_eval(result_D[0]) # convert string list to list
#             assert check_keyImage(signature, keyImage) == True, "There might be some error."
#             print("hre")
#             message = "You are only allowed to vote once."
#             status = 400
#     except Exception:
#         message = str(sys.exc_info()[1]) 
#         print(message)
#         return Response(json.dumps({"message": message}), 400, mimetype='application/json') 
   
#     return Response(json.dumps({"message": message}), status, mimetype='application/json') 


@app.route("/findAllEvent", methods=['GET'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
@requires_auth
@requires_id_token
def findAllEvent():
    try:
        event = EventService().getAllEventAdmin()
        print(event)
        return jsonify(event)
    except Exception:
        message = str(sys.exc_info()[1]) 
        print(message)
        return Response(json.dumps({"message": message}), 404, mimetype='application/json') 


@app.route("/findPastEvent", methods=['GET'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
@requires_auth
@requires_id_token
def findPastEvent():
    try:
        event = EventService().getAllPastEvent()
        return jsonify(event)
    except Exception:
        message = str(sys.exc_info()[1]) 
        print(message)
        return Response(json.dumps({"message": message}), 404, mimetype='application/json') 
            

# @app.route("/findEventById/<id>")
# @cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
# @requires_auth
# @requires_id_token
# def findEventById(id):
#     conn = mysql.connect() 
#     try:
#         cursor = conn.cursor()
#         query = """SELECT election_type, 
#                    area_id, 
#                    start_date_time, 
#                    end_date_time
#                    FROM event 
#                    WHERE CURRENT_TIMESTAMP < start_date_time
#                    AND event_id = %s
#                    AND del_flag = %s
#                    AND expire_flag = %s"""
#         assert (cursor.execute(query, (id,0,0)) != 0), "No event found. Please try again."
#         result_A = cursor.fetchone()

#         # Query for all candidate name and iamge
#         query = """SELECT candidate_name, candidate_image
#                    FROM candidate 
#                    WHERE event_id = %s
#                    AND del_flag = %s"""
#         cursor.execute(query, (id,0))
#         result_B = cursor.fetchall()
#         print(result_B)
#         cursor.close()
#         conn.close()

#         candidate_payload = []
#         for record in result_B:
#             with open(record[1], "rb") as image_file:
#                 encoded_string = base64.b64encode(image_file.read())
#                 pngFile = encoded_string.decode('UTF-8')
#             candidate_content = { 'candidate_name':  record[0],
#                                 'candidate_image':  pngFile }
#             candidate_payload.append(candidate_content) 

#         # Get all information about the particular event + candidate
#         payload = []
#         event_content = { 'election_type':  result_A[0],
#                         'area_id':  result_A[1],
#                         'start_date_time':  result_A[2],
#                         'end_date_time':  result_A[3], 
#                         'candidates': candidate_payload}    
#         payload.append(event_content)
#     except Exception:
#         message = str(sys.exc_info()[1]) 
#         print(message)
#         return Response(json.dumps({"message": message}), 404, mimetype='application/json') 
        
#     return jsonify(payload)


@app.route("/findAllElectionTypeAndArea")
@cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
@requires_auth
@requires_id_token
def findAllElectionType():
    try:
        electionTypeList = ElectionTypeService().getAllElectionType();
        areaList = AreaService().getAllAreaType();
        payload = []
        payload.append(electionTypeList)
        payload.append(areaList)
        return jsonify(payload)
    except Exception:
        message = str(sys.exc_info()[1]) 
        print(message)
        return Response(json.dumps({"message": message}), 404, mimetype='application/json')   



# @app.route("/updateEvent/<id>", methods=['PUT'])
# @app.route("/createEvent", methods=['PUT'])
# @cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
# @requires_auth
# @requires_id_token
# def putEvent(id=-1):

#     electionType = request.json['election_type']
#     areaId = request.json['area_id']
#     startDateTime = request.json['start_date_time']
#     endDateTime = request.json['end_date_time']
#     candidates = request.json['candidates']
#     # try:
#     #     logic = EventService().putEvent(id, electionType, areaId, startDateTime, endDateTime, candidates);
#     # except Exception:
#     #     message = str(sys.exc_info()[1]) 
#     #     print(message)
#     #     return Response(json.dumps({"message": message}), 400, mimetype='application/json') 
                 
#     return "ok"
    # conn = mysql.connect()
    # try:
    #     cursor = conn.cursor()

    #     query =  """SELECT * FROM election_type WHERE election_id = %s AND del_flag = %s""";
    #     result_A = cursor.execute(query, (electionType,0));  
    #     print(result_A)
    #     query =  """SELECT * FROM area WHERE area_id = %s AND del_flag = %s""";
    #     result_B = cursor.execute(query, (areaId,0));  
    #     print(result_B)

    #     time_difference = datetime.strptime(endDateTime, '%Y-%m-%dT%H:%M:%S.%fZ') - datetime.strptime(startDateTime, '%Y-%m-%dT%H:%M:%S.%fZ')
    #     result = time_difference.total_seconds() * 1000     #Multiply by 1000 for milliseconds
    #     result_C = (True if result >= 14400000 else False)
    #     print(result_C)
    #     # to do: valid the start time make sure it does not fall in the past
    #     date_time_now_UTC = datetime.now(timezone.utc)
    #     parsedTime = datetime.strptime(startDateTime, '%Y-%m-%dT%H:%M:%S.%fZ')
    #     startDateTime_formatted_UTC = datetime.strftime(parsedTime, '%Y-%m-%d %H:%M:%S')
    #     currentDateTime_formatted_UTC = datetime.strftime(date_time_now_UTC, '%Y-%m-%d %H:%M:%S')
    #     result_D = (True if currentDateTime_formatted_UTC < startDateTime_formatted_UTC else False)
    #     print(result_D)
        
    #     message = ""
    #     # Rebuild the json data, if violated, error will be thrown
    #     # Also store only the image path for candidate image
    #     candidate_payload = []
    #     for object in candidates:
    #         image_b64 = object['candidate_image']
    #         base64result = image_b64.split(',')[1];
    #         as_bytes = bytes(base64result, 'utf-8')
    #         image_path = "img/" + object['candidate_name'] + ".png"
    #         with open(image_path, "wb") as fh:
    #           fh.write(base64.decodebytes(as_bytes))

    #         candidate = {"candidate_name" : object['candidate_name'], 
    #                       "candidate_image" : image_path}
    #         candidate_payload.append(candidate)
    #         candidate = {}
        
    #     print(candidate_payload)


    #     # election_type, area, time diff must be correct in order to proceed
    #     if (result_A & result_B & result_C & result_D):
    #         # If id is present
    #         print("YES")
    #         if id != -1:
    #             print("Yes got ID")
    #             query =  """SELECT * FROM event 
    #                         WHERE event_id = %s
    #                         AND del_flag = %s
    #                         AND expire_flag = %s""";
    #             result_E = cursor.execute(query,(id,0,0));
    #         else:
    #             result_E = False;

    #         # Got record, we need to update
    #         if (result_E):
    #             # Check if the event is on going
    #             query = "SELECT start_date_time FROM event WHERE event_id = %s"
    #             cursor.execute(query,id)
    #             start = cursor.fetchone()[0] 
    #             date_time_now_UTC = datetime.now(timezone.utc)
    #             startDateTime_formatted_UTC = datetime.strftime(start, '%Y-%m-%d %H:%M:%S')
    #             currentDateTime_formatted_UTC = datetime.strftime(date_time_now_UTC, '%Y-%m-%d %H:%M:%S')
    #             assert (currentDateTime_formatted_UTC < startDateTime_formatted_UTC), "Unable to modify ongoing event."

    #             print("Updating")
    #             query =  """UPDATE event SET
    #                         election_type = %s,
    #                         area_id = %s,
    #                         start_date_time = %s,
    #                         end_date_time = %s
    #                         WHERE event_id = %s
    #                         AND del_flag = %s
    #                         AND expire_flag = %s""";
    #             cursor.execute(query, 
    #                             (electionType, 
    #                                 areaId, 
    #                                 datetime.strptime(startDateTime, '%Y-%m-%dT%H:%M:%S.%fZ'), 
    #                                 datetime.strptime(endDateTime, '%Y-%m-%dT%H:%M:%S.%fZ'),
    #                                 id,0,0)) == 1, "Event Failed to update"

    #             message = "Event Successfully Updated"
    #             print(message)
    #             status = 200
    #         else:
    #             print("Attempt Inserting")
    #             query =  """SELECT * FROM event WHERE area_id = %s AND del_flag = %s AND expire_flag = %s"""
    #             assert cursor.execute(query, (areaId, 0,0)) == 0, "This event has already been created. Multiple events with same area are not allowed."

    #             # If result not found = no duplicate, insert data
    #             query =  """INSERT INTO event 
    #             (election_type, 
    #             area_id, 
    #             start_date_time, 
    #             end_date_time, 
    #             del_flag,
    #             expire_flag) VALUES 
    #                         ( %s, %s, %s, %s, %s, %s)""";
                        
    #             assert cursor.execute(query, 
    #                                         (electionType,
    #                                             areaId, 
    #                                             datetime.strptime(startDateTime, '%Y-%m-%dT%H:%M:%S.%fZ'), 
    #                                             datetime.strptime(endDateTime, '%Y-%m-%dT%H:%M:%S.%fZ'),
    #                                             0,0)) == 1, "Event Not Created"
    #             message = "Event Created"
    #             print(message)
    #             status = 200                   
    #         conn.commit()
          
    #         # First "remove" the old candidates
    #         query = """UPDATE candidate SET del_flag = %s WHERE event_id = %s""";
    #         cursor.execute(query,(1,id))
          
    #         # Find the just inserted event id
    #         query = """SELECT event_id FROM event WHERE 
    #                     election_type = %s AND
    #                     area_id = %s AND
    #                     start_date_time = %s AND
    #                     end_date_time = %s AND
    #                     del_flag = %s AND
    #                     expire_flag = %s"""
    #         assert cursor.execute(query,(electionType,
    #                                 areaId,
    #                                     datetime.strptime(startDateTime, '%Y-%m-%dT%H:%M:%S.%fZ'),
    #                                     datetime.strptime(endDateTime, '%Y-%m-%dT%H:%M:%S.%fZ'),0,0)) == 1, "Fail to retrieve inserted event."
    #         result_F = cursor.fetchone()
    #         id = result_F[0]
         
    #         # Insert back the new candidates
    #         query = """INSERT INTO candidate 
    #         (event_id, candidate_name, candidate_image)  
    #         VALUES""";
    #         for record in candidate_payload:
    #                 query += """ (%s, "%s", "%s"),""" %(id,record['candidate_name'], record['candidate_image'])
    #         assert cursor.execute(query[:-1]) == 2, "Failed to update candidate."
    #         cursor.close()
    #         conn.commit()
    #         conn.close()  
    #     else:
    #         message = 'Event information is invalid. Please verify.'
    #         print(message)
    #         status = 406
 




# @app.route("/deleteEventById/<id>", methods=['DELETE'])
# @cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
# @requires_auth
# @requires_id_token
# def deleteEvent(id):
#     conn = mysql.connect() 
#     try:
#         cursor = conn.cursor()
#         query =  """UPDATE event 
#                     SET del_flag = %s 
#                     WHERE event_id = %s""";
#         result_A = cursor.execute(query, (1, id));
#         query = """UPDATE candidate SET del_flag = %s WHERE event_id =%s"""
#         result_B = cursor.execute(query, (1, id));
#         message = "Event Successfully Deleted"
#         status = 200
#         cursor.close()
#         conn.commit()
#         conn.close()

#     except:
#         print("Error: Record Not Found") 
#         message = 'Failed to delete record. Please try again'
#         return Response(json.dumps({"message": message}), 400, mimetype='application/json') 

#     return Response(json.dumps({"message": message}), status, mimetype='application/json') 


# @app.route("/findResultById/<id>", methods=['GET'])
# @cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
# @requires_auth
# @requires_id_token
# def findResultById(id):
#     conn = mysql.connect() 
#     try:
#         cursor = conn.cursor()
#         query =  """SELECT (SELECT area_name FROM area WHERE area_id = e.area_id) AS area_name, 
#                     c.candidate_name, 
#                     c.vote_count 
#                     FROM candidate c
#                     JOIN event e
#                     ON c.event_id = e.event_id
#                     WHERE c.event_id = %s
#                     AND e.expire_flag = %s
#                     AND c.del_flag = %s
#                     AND e.del_flag = %s""";

#         cursor.execute(query, (id,1,0,0));
#         result_A = cursor.fetchall()
#         cursor.close()
#         conn.close()

#         candidate_payload = []
#         for record in result_A:
#             candidate_content = {  "area_name": record[0],
#                                     "candidate_name": record[1], 
#                                     "vote_count": record[2]}
#             candidate_payload.append(candidate_content)

#         message = "Successfully retrieve record."    
#         status = 200
#     except:
#         print("Error: Record Not Found") 
#         message = 'No record found. Please refresh.'
#         return Response(json.dumps({"message": message}), 404, mimetype='application/json') 

#     return Response(json.dumps({"message": message, "candidates": candidate_payload}), status, mimetype='application/json') 
  

# # This needs authorization
# @app.route("/upload", methods=["POST"])
# @cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
# @requires_auth
# @requires_id_token
# def uploadFile():
#     conn = mysql.connect() 
#     try: 
#         cursor = conn.cursor()
#         # Use Auth0 Client secret and public key to get management_access_token
#         connnection = http.client.HTTPSConnection("dev-i7062-qd.us.auth0.com")
#         payload = "{\"client_id\":\"ziMcfPoiH2CFyrhKAaiOecnLsMs69lXF\",\"client_secret\":\"gsuu8u1O_qIylsmHry-8litgeu94wqLhPCbvJ56FBJ_kUgZp0qQ9ETCb17UOdm8E\",\"audience\":\"https://dev-i7062-qd.us.auth0.com/api/v2/\",\"grant_type\":\"client_credentials\"}"
#         headers = { 'content-type': "application/json" }
#         connnection.request("POST", "/oauth/token", payload, headers)
#         res = connnection.getresponse()
#         data = res.read()
#         jsonData = json.loads(data)
#         management_access_token = "Bearer " + jsonData["access_token"]

#         # Get the excel file
#         xlsx_file = request.files['file']
#         data_xls = pd.read_excel(xlsx_file)
#         assert len(data_xls) > 0, "You have uploaded an empty file.."   # Error if user upload empty file, logic not proceeding
    
#         # Get all users in exisiting database
#         query = """SELECT email FROM users"""
#         cursor.execute(query)
#         user_record_list = [record[0] for record in cursor.fetchall()]       # Convert all records into a list

#         # list to store exisiting users
#         existing_user_list = []
#         skip_index = []
#         for i in data_xls.index:
#             if (data_xls['email'][i] in user_record_list):
#                 existing_user_list.append({ "Account already created": data_xls['email'][i] })
#                 skip_index.append(i)

#         number_of_participants = len(data_xls) - len(existing_user_list)    # Get the actual no. of account generating
#         print("OK here")
#         print(number_of_participants)
#         # A list to store base64 encoded xlsx files( up to max 2 files )
#         b64_list = []
#         # Generate keys based on number of participants on the same area
#         privateKey, publicKey = generate_keys(number_of_participants)
#         private_key_list = export_private_keys_in_list(privateKey)
#         public_key_list = export_private_keys_in_list(publicKey)
#         user_list = []  # User list for writting into xlsx files
#         j = 0;
#         # Loop all provided users and check if they exist
#         for i in data_xls.index:
#             if i not in skip_index:
#                 # Filter them if user exist
#                 # Password generator
#                 # characters to generate password from
#                 characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")   
#                 # picking random characters from the list
#                 pass_phrase = []
#                 length = 20
#                 for k in range(length):
#                     pass_phrase.append(characters[int.from_bytes(os.urandom(1), byteorder="big") % len(characters)])   
#                 password = "".join(pass_phrase)
#                 print("Generated Password")
#                 # Store the details for later xlsx file output
#                 user = { "email": data_xls['email'][i], 
#                             "area_id": data_xls['area_id'][i], 
#                             "password": password,
#                             "private_key": private_key_list[j]}
#                 user_list.append(user)
#                 ++j
#                 print("Sending payload to auth0")
#                 # add user to auth0
#                 payload = '{"email": "%s", '\
#                             '"nickname": "%s", '\
#                             '"connection": "Username-Password-Authentication", '\
#                             '"password": "%s" }'%(data_xls['email'][i], "empty", password)
#                 # Use management_access_token to create user with auth0
#                 headers = {
#                     'content-type': "application/json",
#                     'authorization': management_access_token
#                     }
#                 connnection.request("POST", "/api/v2/users", payload, headers)
#                 res = connnection.getresponse()
#                 data = res.read()
#                 print("Sent")
#         ############################################ End of for loop 
#         # Once mass creation is done, get all the email correspond with 
#         # the area_id and update each record respectively
#         print("Updating roles, area id and keys..")
#         for i, user in enumerate(user_list):
#             query = """UPDATE users SET area_id = %s, role = %s, public_key = %s, private_key = %s WHERE email = %s """
#             cursor.execute(query, (user['area_id'], Role.Voter.value, public_key_list[i], private_key_list[i], user['email']));
#         print("Updated")
#         cursor.close()
#         conn.commit()
#         conn.close()

#         # Set user list into a excel format and encode the data
#         if len(user_list) > 0:
#             print("Creating xlsx file containing user credentials...")
#             df = pd.DataFrame(user_list)
#             df.to_excel('Generated_Credentials.xlsx')
#             data = open('Generated_Credentials.xlsx', 'rb').read()
#             os.remove("Generated_Credentials.xlsx") # remove file after read
#             base64_encoded_credentials = base64.b64encode(data).decode('UTF-8') # encode for sending back to front end
#             b64_list.append(base64_encoded_credentials)

#         # Set exisiting user list into a excel format and encode the data 
#         if len(existing_user_list) > 0:
#             print("Creating xlsx file containing existing users...")
#             df2 = pd.DataFrame(existing_user_list)
#             df2.to_excel('Existing_Users.xlsx')
#             data = open('Existing_Users.xlsx', 'rb').read()
#             os.remove("Existing_Users.xlsx") # remove file after read
#             base64_encoded_existing_user = base64.b64encode(data).decode('UTF-8') # encode for sending back to front end
#             b64_list.append(base64_encoded_existing_user)
            
#         message = "Please read the file for more information."
#         status = 200
#     except Exception:
#         message = str(sys.exc_info()[1]) 
#         print(message)
#         return Response(json.dumps({"message": message}), 400, mimetype='application/json') 

#     return Response(json.dumps({"message": message, "excel_file": b64_list}), status, mimetype='application/json')
   
       

# @app.route("/findVoteStatus", methods=["GET"])
# @cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
# @requires_auth
# @requires_id_token
# def findVoteStatus():
#     conn = mysql.connect() 
#     try: 
#         cursor = conn.cursor()
#         query =  """SELECT a.area_name, IF(ISNULL(u.key_image), "Not Submitted","Submitted")
#                     FROM users u join area a ON a.area_id = u.area_id 
#                     WHERE u.email = %s AND a.del_flag = %s""";
#         cursor.execute(query, (session['email'], 0));
#         result = cursor.fetchone()
#         cursor.close()
#         conn.close()
#         payload = {"area": result[0], "status": result[1]}
#         status = 200
#     except:
#         message = "Failed to retrieve vote status"
#         print(message)
#         return Response(json.dumps({"message": message}), 400, mimetype='application/json') 

#     return Response(json.dumps(payload), status, mimetype='application/json')
