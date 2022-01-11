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
# import base64
import json
# Business logic
# A service class which does all the complex logic
class UserService:
    def getUserInformation(self, email):
        return dict(user_dao.findUserInformationByEmail(email))

    def getAllEmail(self):
        return user_dao.findAllEmail()

    def uploadUserInformation(self, xlsx_file):
        # Get the excel file
        data_xls = pd.read_excel(xlsx_file)
        assert len(data_xls) > 0, "You have uploaded an empty file.."   # Error if user upload empty file, logic not proceeding

        # Use Auth0 Client secret and public key to get management_access_token
        connnection = http.client.HTTPSConnection("dev-i7062-qd.us.auth0.com")
        payload = "{\"client_id\":\"ziMcfPoiH2CFyrhKAaiOecnLsMs69lXF\",\"client_secret\":\"gsuu8u1O_qIylsmHry-8litgeu94wqLhPCbvJ56FBJ_kUgZp0qQ9ETCb17UOdm8E\",\"audience\":\"https://dev-i7062-qd.us.auth0.com/api/v2/\",\"grant_type\":\"client_credentials\"}"
        headers = { 'content-type': "application/json" }
        connnection.request("POST", "/oauth/token", payload, headers)
        res = connnection.getresponse()
        data = res.read()
        jsonData = json.loads(data)
        management_access_token = "Bearer " + jsonData["access_token"]

        b64_list = []             # A list to store base64 encoded xlsx files( up to max 2 files )
        userCredential_list = []  # User list for writting into xlsx files containing credentials
        userDetail_list = []      # list for updating user detail such as role and keys

        # Get all users in exisiting database
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
                print("Sent")
        ############################################ End of for loop 

        # Once mass creation is done, get all the email correspond with 
        # the area_id and update each record respectively
        print("Updating roles, area id and keys..")
        user_dao.updateUser(userDetail_list)
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
        eventList = event_dao.findAllEventAdmin(NOT_DELETED,NOT_EXPIRED);
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
        eventList = event_dao.findAllEventAdmin(NOT_DELETED,EXPIRED);
        event_dict_list = []
        # Convert to dict list
        for record in eventList:
            event_dict_list.append(dict(record))
        for record in event_dict_list:
            record.update(start_date_time= record['start_date_time'].strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            end_date_time=record['end_date_time'].strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
        return event_dict_list

    def putEvent(self, id, electionType, areaId, startDateTime, endDateTime, candidates):
        result_A = objectToJson(election_type_dao.findElectionTypeById(electionType, NOT_DELETED))
        result_B = objectToJson(area_dao.findAreaById(areaId, NOT_DELETED))
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
        # OK above

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
        else:
            print("Attempt Inserting")
            event = event_dao.findEventByAreaId(areaId, NOT_DELETED, NOT_EXPIRED) 
            assert event is None, "This event has already been created. Multiple events with same area are not allowed."
           
            # If result not found = no duplicate, insert data
            create_status = event_dao.putEvent(electionType, areaId, startDateTime, endDateTime, NOT_DELETED, NOT_EXPIRED)
            assert create_status == True, "Event Not Created"
         
                
        # First "remove" the old candidates
        number_of_deleted_rows = candidate_dao.updateCandidate(id, DELETED)
        print(number_of_deleted_rows)

        # Find the just inserted event id
        result_F = event_dao.findEvent(electionType, areaId, startDateTime, endDateTime, NOT_DELETED, NOT_DELETED)
        id = result_F[0]
        print(id)

        # Insert back the new candidates
        candidate_dao.insertCandidate(id, candidate_payload)
        return True;

    def getEventDetailsById(self, id):
        record = dict(event_dao.findEventDetailsById(id, NOT_DELETED, NOT_EXPIRED))
        record.update(start_date_time= record['start_date_time'].strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            end_date_time=record['end_date_time'].strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
        return record

    def deleteEventById(self, id):
        return event_dao.deleteEventById(id, DELETED)

class AreaService:
    def getAllAreaType(self):
        areaTypeList = area_dao.findAllAreaType(NOT_DELETED)
        areaType_dict_list = []
        for record in areaTypeList:
            areaType_dict_list.append(dict(record))
        return areaType_dict_list

class ElectionTypeService:
    def getAllElectionType(self):
        electionTypeList = election_type_dao.findAllElectionType(NOT_DELETED)
        election_type_dict_list = []
        for record in electionTypeList:
            election_type_dict_list.append(dict(record))
        return election_type_dict_list

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


       

        

