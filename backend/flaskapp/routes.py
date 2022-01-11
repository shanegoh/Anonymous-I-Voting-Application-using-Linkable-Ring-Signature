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
import numpy as np
import sys
from flaskapp.util import *
from flaskapp.services import *

# @app.route("/")
# @cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
# def zxc():
#     #return jsonify(user_dao.get_all())
#     user = UserService().getUserInformation('production_admin@gmail.com')
#     return jsonify(user)


# #     return Response(json.dumps({"message": "ok"}), 200, mimetype='application/json') 

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


@app.route("/findElectionForVoter", methods=['GET'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
@requires_auth
@requires_id_token
def findElectionForVoter():

    try:
        user = UserService().getAreaIdKeyImageByEmail(session['email'])
        areaId = user[0]
        assert user[1] is None, "There is no event for you at the moment."
        event = EventService().getEventForVoter(areaId)
        assert event is not None, "There is no event for you at the moment."
        print(event)
        return jsonify(event)
    except Exception:
        message = str(sys.exc_info()[1]) 
        print(message)
        return Response(json.dumps({"message": message}), 404, mimetype='application/json') 

@app.route("/findCandidateByEventId/<id>", methods=['GET'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
@requires_auth
@requires_id_token
def findCandidateByEventId(id):
    try:
        candidateList = CandidateService().getCandidateByEventId(id, session['email'])
        print(candidateList)
        return jsonify(candidateList)
    except Exception:
        message = str(sys.exc_info()[1]) 
        print(message)
        return Response(json.dumps({"message": message}), 404, mimetype='application/json') 


@app.route("/voteCandidate", methods=['PUT'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
@requires_auth
@requires_id_token
def voteCandidate():
    try:
        CandidateService().voteCandidate(request.json['event_id'], request.json['private_key'], session['email'], request.json['candidate_name'])
   
        return Response(json.dumps({"message": "not ok"}), 404, mimetype='application/json') 
    except Exception:
        message = str(sys.exc_info()[1]) 
        print(message)
        return Response(json.dumps({"message": message}), 404, mimetype='application/json')    


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


@app.route("/findResultById/<id>", methods=['GET'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
@requires_auth
@requires_id_token
def findResultById(id):
    try:
        result = CandidateService().getResultByEventId(id)
        return jsonify(result)
    except Exception:
        message = str(sys.exc_info()[1]) 
        print(message)
        return Response(json.dumps({"message": message}), 400, mimetype='application/json')   

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
     
       
@app.route("/findVoteStatus", methods=["GET"])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization', 'id_token'])
@requires_auth
@requires_id_token
def findVoteStatus():
    try:
        result = VoteHistoryService().getVoteHistory(session['email'])
        return jsonify(result)       
    except Exception:
        message = str(sys.exc_info()[1]) 
        print(message)
        return Response(json.dumps({"message": message}), 400, mimetype='application/json') 

