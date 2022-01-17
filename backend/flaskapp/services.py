from flaskapp.daos import *
from flaskapp.util import *
from datetime import datetime, timezone
from flaskapp.linkable_ring_signature import *
from flaskapp.roleEnum import Role
import base64
import http.client
import pandas as pd
import string
import sys
import ast
# import base64
import json
# Business logic
# A service class which does all the complex logic
class UserService:
    def getUserInformation(self, email):
        return dict(user_dao.findUserInformationByEmail(email))

    def updateUser(self, user_list):
        print("updating user")
        return user_dao.updateUser(user_list)

    def getNumberOfParticipantByEventId(self, eventId):
        return user_dao.findNumberOfParticipantByEventId(eventId)

    def getAllEmail(self):
        return user_dao.findAllEmail()

    def getAreaNameByEmail(self, email):
        return user_dao.findAreaNameByEmail(email, NOT_DELETED)

    def getAreaIdByEmail(self, email):
        return user_dao.findAreaIdByEmail(email)

    def getNumberOfParticipantByEventId(self, eventId):
        return user_dao.findNumberOfParticipantByEventId(eventId)

    def getAllPrivateAndPublicKeyByEvent(self, eventId, deleteFlag, expireFlag):
        return user_dao.findAllPrivateAndPublicKeyByEvent(eventId, deleteFlag, expireFlag)

    def getEmailByPrivateKey(self, privateKey):
        return user_dao.findEmailByPrivateKey(privateKey)

    def uploadUserInformation(self, xlsx_file):
        # Get the excel file
        data_xls = pd.read_excel(xlsx_file)
        assert len(data_xls) > 0, "You have uploaded an empty file.."   # Error if user upload empty file, logic not proceeding
        print("first")
        # Use Auth0 Client secret and public key to get management_access_token
        connnection = http.client.HTTPSConnection("dev-a6828r5z.us.auth0.com")
        payload = "{\"client_id\":\"vMOfBnYOJszlqdGdDek62rMyhsUY9srE\",\"client_secret\":\"27JENkP6Q22nXmTlbUcR44ABceE1DLV3n23QTBUVWL9U6fwIMFgTp0KTmBpacTDk\",\"audience\":\"https://dev-a6828r5z.us.auth0.com/api/v2/\",\"grant_type\":\"client_credentials\"}"
        headers = { 'content-type': "application/json" }
        connnection.request("POST", "/oauth/token", payload, headers)
        res = connnection.getresponse()
        data = res.read()
        print(data)
        jsonData = json.loads(data)
        management_access_token = "Bearer " + jsonData["access_token"]
        print("Continue")

        b64_list = []             # A list to store base64 encoded xlsx files( up to max 2 files )
        userCredential_list = []  # User list for writting into xlsx files containing credentials
        userDetail_list = []      # list for updating user detail such as role and keys

        # Get all email in exisiting database
        userList = UserService().getAllEmail()
        userRecord_db = [record[0] for record in userList]       # Convert all records into a list

        existing_user_list = []     # list to store exisiting users
        skip_index = []             # Index to be skipped
        for i in data_xls.index:
            if (data_xls['email'][i] in userRecord_db):
                existing_user_list.append({ "Account already created": data_xls['email'][i] })
                skip_index.append(i)

        number_of_participants = len(data_xls) - len(existing_user_list)    # Get the actual no. of account generating
        print(number_of_participants)
        # Generate keys based on number of participants on the same area
        privateKey, publicKey = generate_keys(number_of_participants)
        private_key_list = export_private_keys_in_list(privateKey)
        public_key_list = export_private_keys_in_list(publicKey)

        j = 0;
        # Loop all provided users and check if they exist
        for i in data_xls.index:
            if i not in skip_index:
                # Password generator
                # characters to generate password from
                characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")   
                # picking random characters from the list
                pass_phrase = []
                length = 20
                for k in range(length):
                    pass_phrase.append(characters[int.from_bytes(os.urandom(1), byteorder="big") % len(characters)])   
                password = "".join(pass_phrase)
                print("Generated Password")

                # Store the details for later xlsx file output
                userCredential = { "email": data_xls['email'][i], 
                            "area_id": data_xls['area_id'][i], 
                            "password": password,
                            "private_key": private_key_list[j]}
                userCredential_list.append(userCredential)

                # Store details for updating user profile
                userUpdate = { "email": data_xls['email'][i], 
                                "role": Role.Voter.value,
                                "area_id": data_xls['area_id'][i], 
                                "private_key": private_key_list[j],
                                "public_key": public_key_list[j]}
                userDetail_list.append(userUpdate)
                j+=1
                
                print("Sending payload to auth0")
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
                print(data)
                print("Sent")
        ############################################ End of for loop 

        # Once mass creation is done, get all the email correspond with 
        # the area_id and update each record respectively
        print("Updating roles, area id and keys..")
        UserService().updateUser(userDetail_list)
        print("Updated")

        # Set user list into a excel format and encode the data
        if len(userCredential_list) > 0:
            print("Creating xlsx file containing user credentials...")
            b64_list.append(generateExcelFile(userCredential_list))

        # Set exisiting user list into a excel format and encode the data 
        if len(existing_user_list) > 0:
            print("Creating xlsx file containing existing users...")
            b64_list.append(generateExcelFile(existing_user_list))
        return b64_list



class EventService:
    # Get all events in database that is not deleted nor expire
    def getAllEventAdmin(self):
        eventList = event_dao.findAllEvent(NOT_DELETED,NOT_EXPIRED);
        event_dict_list = []
        # Convert to dict list
        for record in eventList:
            event_dict_list.append(dict(record))
        for record in event_dict_list:
            record.update(start_date_time= record['start_date_time'].strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            end_date_time=record['end_date_time'].strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
        return event_dict_list

    # Get all events that are not deleted and is expired!
    def getAllPastEvent(self):
        eventList = event_dao.findAllEvent(NOT_DELETED,EXPIRED);
        event_dict_list = []
        # Convert to dict list
        for record in eventList:
            event_dict_list.append(dict(record))
        for record in event_dict_list:
            record.update(start_date_time= record['start_date_time'].strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            end_date_time=record['end_date_time'].strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
        return event_dict_list

    def getEventDetailsById(self, id):
        record = dict(event_dao.findEventDetailsById(id, NOT_DELETED, NOT_EXPIRED))
        record.update(start_date_time= record['start_date_time'].strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            end_date_time=record['end_date_time'].strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
        return record

    def deleteEventById(self, id):
        return event_dao.deleteEventById(id, DELETED)

    def getEventForVoter(self, areaId):
        record =  event_dao.findEventForVoter(areaId, NOT_DELETED, NOT_EXPIRED)
        if record is None:
            return record;
        else:
            record = dict(record)
            record.update(start_date_time= record['start_date_time'].strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            end_date_time=record['end_date_time'].strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
            return record

    def putEvent(self, id, electionType, areaId, startDateTime, endDateTime, candidates):
        message= ""
        result_A = objectToJson(ElectionTypeService().getElectionTypeById(electionType, NOT_DELETED))
        result_B = objectToJson(AreaService().getAreaById(areaId, NOT_DELETED))
        time_difference = datetime.strptime(endDateTime, '%Y-%m-%dT%H:%M:%S.%fZ') - datetime.strptime(startDateTime, '%Y-%m-%dT%H:%M:%S.%fZ')
        result = time_difference.total_seconds() * 1000     #Multiply by 1000 for milliseconds
        result_C = (True if result >= 14400000 else False)
        assert result_C == True, "Start and End time must be at least 4 hours."

        # to do: valid the start time make sure it does not fall in the past
        date_time_now_UTC = datetime.now(timezone.utc)
        parsedTime = datetime.strptime(startDateTime, '%Y-%m-%dT%H:%M:%S.%fZ')
        startDateTime_formatted_UTC = datetime.strftime(parsedTime, '%Y-%m-%d %H:%M:%S')
        currentDateTime_formatted_UTC = datetime.strftime(date_time_now_UTC, '%Y-%m-%d %H:%M:%S')
        result_D = (True if currentDateTime_formatted_UTC < startDateTime_formatted_UTC else False)
        assert result_D == True, "Invalid start time."

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

        # If id is present
        print("YES")
        if id != -1:
            result_E = True if isinstance(event_dao.findEventById(id, NOT_DELETED, NOT_EXPIRED), Event) else False
            print(result_E)
        else:
            result_E = False;

        # Got record, we need to update
        if (result_E):
            # Check if the event is on going
            result_start_date_time = event_dao.findEventStartDateTime(id, NOT_DELETED, NOT_EXPIRED)
            start = result_start_date_time[0] 
            date_time_now_UTC = datetime.now(timezone.utc)
            startDateTime_formatted_UTC = datetime.strftime(start, '%Y-%m-%d %H:%M:%S')
            currentDateTime_formatted_UTC = datetime.strftime(date_time_now_UTC, '%Y-%m-%d %H:%M:%S')
            assert (currentDateTime_formatted_UTC < startDateTime_formatted_UTC), "Unable to modify ongoing event."
            print("Updating")
            assert event_dao.updateEvent(id, electionType, areaId, startDateTime, endDateTime, NOT_DELETED, NOT_EXPIRED) == True, "Event Failed to update"
            message = "Event updated."
        else:
            print("Attempt Inserting")
            event = event_dao.findEventByAreaId(areaId, NOT_DELETED, NOT_EXPIRED) 
            assert event is None, "This event has already been created. Multiple events with same area are not allowed."
           
            # If result not found = no duplicate, insert data
            create_status = event_dao.putEvent(electionType, areaId, startDateTime, endDateTime, NOT_DELETED, NOT_EXPIRED)
            assert create_status == True, "Event Not Created"
            message = "Event Created."
         
        # First "remove" the old candidates
        number_of_deleted_rows = candidate_dao.updateCandidate(id, DELETED)
        print(number_of_deleted_rows)

        # Find the just inserted event id
        result_F = event_dao.findEvent(electionType, areaId, startDateTime, endDateTime, NOT_DELETED, NOT_DELETED)
        id = result_F[0]
        print(id)

        # Insert back the new candidates
        candidate_dao.insertCandidate(id, candidate_payload)
        return message;


class AreaService:
    def getAllAreaType(self):
        areaTypeList = area_dao.findAllAreaType(NOT_DELETED)
        areaType_dict_list = []
        for record in areaTypeList:
            areaType_dict_list.append(dict(record))
        return areaType_dict_list

    def getAreaById(self, areaId, deleteFlag):
        return area_dao.findAreaById(areaId, deleteFlag);

class ElectionTypeService:
    def getAllElectionType(self):
        electionTypeList = election_type_dao.findAllElectionType(NOT_DELETED)
        election_type_dict_list = []
        for record in electionTypeList:
            election_type_dict_list.append(dict(record))
        return election_type_dict_list
    
    def getElectionTypeById(self, electionType, deleteFlag):
        return election_type_dao.findElectionTypeById(electionType, deleteFlag)

    def getElectionTypeById(self, electionType, deleteFlag):
        return election_type_dao.findElectionTypeById(electionType, deleteFlag)
        
class CandidateService:
    def getAllEventCandidates(self, id):
        candidateList = candidate_dao.findAllCandidatesByEventId(id, NOT_DELETED)
        candidate_list_dict = []
        for record in candidateList:
            record = dict(record)
            record.update(candidate_image = pathToFile(record['candidate_image']))
            candidate_list_dict.append(record)
        return candidate_list_dict
    
    def deleteCandidateByEventId(self, id):
        return candidate_dao.deleteCandidateByEventId(id, DELETED)

    def getCandidateByEventId(self, id, email):
        candidateList = candidate_dao.findCandidateByEventId(id, email, NOT_DELETED, NOT_EXPIRED)
        candidate_dict_list = []
        for record in candidateList:
            record = dict(record)
            record.update(candidate_image = encodePng(record['candidate_image']))
            candidate_dict_list.append(record)
        return candidate_dict_list
        
    def voteCandidate(self, eventId, privateKey, email, candidateName):
        number_of_participants = UserService().getNumberOfParticipantByEventId(eventId)
        print(number_of_participants)
        private_public_list = UserService().getAllPrivateAndPublicKeyByEvent(eventId, NOT_DELETED, NOT_EXPIRED)
        print(private_public_list)

        privateKeyOwner = UserService().getEmailByPrivateKey(privateKey)
        print(privateKeyOwner)
        assert privateKeyOwner is not None, "Invalid private key."
        assert (email == privateKeyOwner[0]) == True, "Private key does not belong to you!"

        # Adding all private and public keys into each list
        x = []  # list of all secret keys
        y = []  # list of all public keys
        for record in private_public_list:
            x.append(int(record[0]))
            assert record[1][0] == "(" and record[1][-1] == ")"
            e1 = int(record[1][1:-1].split(",")[0])
            e2 = int(record[1][1:-1].split(",")[1])
            y.append(ecdsa.ellipticcurve.Point(curve_secp256k1, e1, e2)) # convert to Point object

        print(x)
        print(y)
        # Getting the index_idx for signature
        i = 0
        for k in range(0,number_of_participants):
            if int(privateKey) == x[k]:
                i = k   
                break

        # Create and verify signature
        signature = ring_signature(int(privateKey), i, candidateName, y)
        assert verify_ring_signature(candidateName, y, *signature) == True, "Invalid Signature"    
       
        # fetch a list of key image tagged to this event
        key_image_list = KeyImageService().getAllKeyImageByEventId(eventId)
        print(key_image_list)

        # Verify key image
        for keyImage in key_image_list:
           keyImage = ast.literal_eval(keyImage['key_image']) # convert string list to list
           print(keyImage)
           assert check_keyImage(signature, keyImage) != True, "You have already voted."
        
        #Insert new key image into database.
        assert KeyImageService().insertKeyImageByEventId(eventId, get_image_from_signature(signature)) == True, "Failed to insert key image"
        #Increment vote count
        candidate_dao.incrementVoteCount(eventId, candidateName, NOT_DELETED)
        VoteHistoryService().insertVoteHistory(email)
  

    def getResultByEventId(self, eventId):
        candidateResult = candidate_dao.findResultByEventId(eventId, NOT_DELETED, EXPIRED)
        candidateResult_dict_list = []
        for record in candidateResult:
            candidateResult_dict_list.append(dict(record))
        return candidateResult_dict_list

class KeyImageService:
    def getAllKeyImageByEventId(self, eventId):
        keyImageList = keyImage_dao.findAllKeyImageByEventId(eventId)
        keyImage_dict_list = []
        for record in keyImageList:
            keyImage_dict_list.append(dict(record))
        return keyImage_dict_list     

    def insertKeyImageByEventId(self, eventId, keyImage):
        return keyImage_dao.insertKeyImageByEventId(eventId, keyImage)

class VoteHistoryService:
    def insertVoteHistory(self, email):
        return voteHistory_dao.insertVoteHistory(email)

    def getVoteHistory(self, email):
        status = "Submitted" if voteHistory_dao.findVoteStatus(email) != 0 else "Not Submitted"
        areaName = UserService().getAreaNameByEmail(email)[0]
        payload = {"area": areaName, "status": status }
        return payload
    
    def validateVoteEligibility(self, email):
        return True if voteHistory_dao.findVoteStatus(email) == 0 else False

        