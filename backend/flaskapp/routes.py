from numpy import result_type
from flaskapp import app
from flaskapp.__init__ import *
from flaskapp.auth import *
from flask_cors import cross_origin
from flask import Response
from flaskapp.linkable_ring_signature import *
import json
import sys
from flaskapp.util import *
from flaskapp.services import *

#Controllers API

# This is used when user logs in for redirecting (For All Types of Users)
@app.route("/findUserInformation")
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@requires_auth
def findUserInformation():
    try:
        user = UserService().getUserInformation(session['email'])
        return jsonify(user)
    except:
        message = str(sys.exc_info()[1]) 
        print(message)
        return Response(json.dumps({"message": message}), 404, mimetype='application/json') 


# This is used to display all events. (For Admin/Electoral Board Users)
@app.route("/findAllEvent", methods=['GET'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@requires_auth
def findAllEvent():
    try:
        assert UserService().getUserRoleByEmail(session['email']) == 0, "Invalid Access Rights"
        event = EventService().getAllEventAdmin()
        print(event)
        return jsonify(event)
    except Exception:
        message = str(sys.exc_info()[1]) 
        print(message)
        return Response(json.dumps({"message": message}), 404, mimetype='application/json') 


# This is used to download all area and election type (For Admin/Electoral Board Users)
@app.route("/findAllElectionTypeAndArea")
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@requires_auth
def findAllElectionType():
    try:
        assert UserService().getUserRoleByEmail(session['email']) == 0, "Invalid Access Rights"
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


# This is used to create or update events (For Admin/Electoral Board Users)
@app.route("/updateEvent/<id>", methods=['PUT'])
@app.route("/createEvent", methods=['PUT'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@requires_auth
def putEvent(id=-1):
    assert UserService().getUserRoleByEmail(session['email']) == 0, "Invalid Access Rights"
    electionType = request.json['election_type']
    areaId = request.json['area_id']
    startDateTime = request.json['start_date_time']
    endDateTime = request.json['end_date_time']
    candidates = request.json['candidates']
    try:
        message = EventService().putEvent(id, electionType, areaId, startDateTime, endDateTime, candidates);
        status = 200
        return Response(json.dumps({"message": message}), status, mimetype='application/json') 
    except Exception:
        message = str(sys.exc_info()[1]) 
        print(message)
        return Response(json.dumps({"message": message}), 400, mimetype='application/json') 
                 

# This is used to view candidates for the election event (For Admin)
@app.route("/findEventDetailsById/<id>")
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@requires_auth
def findEventDetailsById(id):
    try:
        assert UserService().getUserRoleByEmail(session['email']) == 0, "Invalid Access Rights"
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

# This is used to delete events (For Admin/Electoral Board Users)
@app.route("/deleteEventById/<id>", methods=['DELETE'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@requires_auth
def deleteEvent(id):
    try:
        assert UserService().getUserRoleByEmail(session['email']) == 0, "Invalid Access Rights"
        CandidateService().deleteCandidateByEventId(id)
        EventService().deleteEventById(id)
        message = "Successfully deleted."
        status = 200
    except Exception:
        message = str(sys.exc_info()[1]) 
        print(message)
        return Response(json.dumps({"message": message}), 400, mimetype='application/json') 

    return Response(json.dumps({"message": message}), status, mimetype='application/json') 


# This is used to find past events (For Admin/Electoral Board Users)
@app.route("/findPastEvent", methods=['GET'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@requires_auth
def findPastEvent():
    try:
        assert UserService().getUserRoleByEmail(session['email']) == 0, "Invalid Access Rights"
        event = EventService().getAllPastEvent()
        assert len(event) > 0, "There is no event for you at the moment."
        return jsonify(event)
    except Exception:
        message = str(sys.exc_info()[1]) 
        print(message)
        return Response(json.dumps({"message": message}), 404, mimetype='application/json') 


# This is used to view results of the event (For Admin/Electoral Board Users)
@app.route("/findResultById/<id>", methods=['GET'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@requires_auth
def findResultById(id):
    try:
        assert UserService().getUserRoleByEmail(session['email']) == 0, "Invalid Access Rights"
        result = CandidateService().getResultByEventId(id)
        return jsonify(result)
    except Exception:
        message = str(sys.exc_info()[1]) 
        print(message)
        return Response(json.dumps({"message": message}), 400, mimetype='application/json')  


# This is used to upload excel files containing credentials (For Admin/Electoral Board Users)
@app.route("/upload", methods=["POST"])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@requires_auth
def uploadFile():
    try:
        assert UserService().getUserRoleByEmail(session['email']) == 0, "Invalid Access Rights"
        b64_list = UserService().uploadUserInformation(request.files['file'])
        message = "Success"
        status = 200
        return Response(json.dumps({"message": message, "excel_file": b64_list}), status, mimetype='application/json')

    except Exception:
        message = "Error, please check your file or else try again."
        print(message)
        return Response(json.dumps({"message": message}), 400, mimetype='application/json') 


# This is used to view event(s) for voter (For Voters)
@app.route("/findElectionForVoter", methods=['GET'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@requires_auth
def findElectionForVoter():
    try:
        assert UserService().getUserRoleByEmail(session['email']) == 1, "Invalid Access Rights"
        user = UserService().getAreaIdByEmail(session['email'])
        areaId = user[0]
        assert VoteHistoryService().validateVoteEligibility(session['email']), "There is no event for you at the moment."
        event = EventService().getEventForVoter(areaId)
        assert event is not None, "There is no event for you at the moment."
        return jsonify(event)
    except Exception:
        message = str(sys.exc_info()[1]) 
        print(message)
        return Response(json.dumps({"message": message}), 404, mimetype='application/json') 


# This is used to view candidates for the election event (For Voters)
@app.route("/findCandidateByEventId/<id>", methods=['GET'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@requires_auth
def findCandidateByEventId(id):
    try:
        assert UserService().getUserRoleByEmail(session['email']) == 1, "Invalid Access Rights"
        candidateList = CandidateService().getCandidateByEventId(id, session['email'])
        print(candidateList)
        return jsonify(candidateList)
    except Exception:
        message = str(sys.exc_info()[1]) 
        print(message)
        return Response(json.dumps({"message": message}), 404, mimetype='application/json') 


# This is used to vote candidates for the election event (For Voters)
@app.route("/voteCandidate", methods=['PUT'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@requires_auth
def voteCandidate():
    try:
        assert UserService().getUserRoleByEmail(session['email']) == 1, "Invalid Access Rights"
        CandidateService().voteCandidate(request.json['event_id'], request.json['private_key'], session['email'], request.json['candidate_name'])
        status = 200
        message = "Ok"
        return Response(json.dumps({"message": message}), status, mimetype='application/json') 
    except Exception:
        message = str(sys.exc_info()[1]) 
        print(message)
        return Response(json.dumps({"message": message}), 404, mimetype='application/json')    
          
# This is used to view vote status for voters (For Voters)       
@app.route("/findVoteStatus", methods=["GET"])
@cross_origin(origin='localhost',headers=['Content-Type','Authorization'])
@requires_auth
def findVoteStatus():
    try:
        assert UserService().getUserRoleByEmail(session['email']) == 1, "Invalid Access Rights"
        result = VoteHistoryService().getVoteHistory(session['email'])
        return jsonify(result)       
    except Exception:
        message = str(sys.exc_info()[1]) 
        print(message)
        return Response(json.dumps({"message": message}), 400, mimetype='application/json') 

