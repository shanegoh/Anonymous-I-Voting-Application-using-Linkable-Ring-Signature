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
        assert len(event) > 0, "There is no event for you at the moment."
        return jsonify(event)
    except Exception:
        message = str(sys.exc_info()[1]) 
        print(message)
        return Response(json.dumps({"message": message}), 404, mimetype='application/json') 
            

@app.route("/findEventDetailsById/<id>")
@cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
@requires_auth
@requires_id_token
def findEventDetailsById(id):
    try:
        event = EventService().getEventDetailsById(id)
        candidate = CandidateService().getAllEventCandidates(id)    
        # Get all information about the particular event + candidate
        event['candidates'] = candidate
        print(event)

    except Exception:
        message = str(sys.exc_info()[1]) 
        print(message)
        return Response(json.dumps({"message": message}), 404, mimetype='application/json') 

    return jsonify(event)


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
    try:
        EventService().putEvent(id, electionType, areaId, startDateTime, endDateTime, candidates);
        message = "Event updated."
        status = 200
    except Exception:
        message = str(sys.exc_info()[1]) 
        print(message)
        return Response(json.dumps({"message": message}), 400, mimetype='application/json') 
                 
    return Response(json.dumps({"message": message}), status, mimetype='application/json') 



@app.route("/deleteEventById/<id>", methods=['DELETE'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
@requires_auth
@requires_id_token
def deleteEvent(id):
    try:
        CandidateService().deleteCandidateByEventId(id)
        EventService().deleteEventById(id)
        message = "Successfully deleted."
        status = 200
    except Exception:
        message = str(sys.exc_info()[1]) 
        print(message)
        return Response(json.dumps({"message": message}), 400, mimetype='application/json') 

    return Response(json.dumps({"message": message}), status, mimetype='application/json') 


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
  

# This needs authorization
@app.route("/upload", methods=["POST"])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
@requires_auth
@requires_id_token
def uploadFile():

    try:
        b64_list = UserService().uploadUserInformation(request.files['file'])
        message = "Success"
        status = 200
        return Response(json.dumps({"message": message, "excel_file": b64_list}), status, mimetype='application/json')

    except Exception:
        message = str(sys.exc_info()[1]) 
        print(message)
        return Response(json.dumps({"message": message}), 400, mimetype='application/json') 
     
       
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
