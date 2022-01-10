from flaskapp.daos import *
from flaskapp.util import *
from datetime import datetime, timezone
# import base64
# import json
# Business logic
# A service class which does all the complex logic
class UserService:
    def getUserInformation(self, email):
        return dict(user_dao.findUserInformationByEmail(email))

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

    # def putEvent(self, id, electionType, areaId, startDateTime, endDateTime, candidates):
        # result_A = election_type_dao.findElectionTypeById(electionType, NOT_DELETED)
        # result_B = area_dao.findAreaById(areaId, NOT_DELETED)

        # time_difference = datetime.strptime(endDateTime, '%Y-%m-%dT%H:%M:%S.%fZ') - datetime.strptime(startDateTime, '%Y-%m-%dT%H:%M:%S.%fZ')
        # result = time_difference.total_seconds() * 1000     #Multiply by 1000 for milliseconds
        # result_C = (True if result >= 14400000 else False)
        # print(result_C)
        # # to do: valid the start time make sure it does not fall in the past
        # date_time_now_UTC = datetime.now(timezone.utc)
        # parsedTime = datetime.strptime(startDateTime, '%Y-%m-%dT%H:%M:%S.%fZ')
        # startDateTime_formatted_UTC = datetime.strftime(parsedTime, '%Y-%m-%d %H:%M:%S')
        # currentDateTime_formatted_UTC = datetime.strftime(date_time_now_UTC, '%Y-%m-%d %H:%M:%S')
        # result_D = (True if currentDateTime_formatted_UTC < startDateTime_formatted_UTC else False)
        # print(result_D)

        # # Rebuild the json data, if violated, error will be thrown
        # # Also store only the image path for candidate image
        # candidate_payload = []
        # for object in candidates:
        #     image_b64 = object['candidate_image']
        #     base64result = image_b64.split(',')[1];
        #     as_bytes = bytes(base64result, 'utf-8')
        #     image_path = "img/" + object['candidate_name'] + ".png"
        #     with open(image_path, "wb") as fh:
        #       fh.write(base64.decodebytes(as_bytes))

        #     candidate = {"candidate_name" : object['candidate_name'], 
        #                   "candidate_image" : image_path}
        #     candidate_payload.append(candidate)
        #     candidate = {}
        
        # print(candidate_payload)

        # # election_type, area, time diff must be correct in order to proceed
        # if (result_A & result_B & result_C & result_D):
        #     # If id is present
        #     print("YES")
        #     if id != -1:
        #         result_E = event_dao.findEventById(id, NOT_DELETED, NOT_EXPIRED)
        #     else:
        #         result_E = False;

        #     # Got record, we need to update
        #     if (result_E):
        #         # Check if the event is on going
        #         result_start_date_time = event_dao.findEventStartDateTime(id, NOT_DELETED, NOT_EXPIRED)
        #         start = result_start_date_time[0] 
        #         date_time_now_UTC = datetime.now(timezone.utc)
        #         startDateTime_formatted_UTC = datetime.strftime(start, '%Y-%m-%d %H:%M:%S')
        #         currentDateTime_formatted_UTC = datetime.strftime(date_time_now_UTC, '%Y-%m-%d %H:%M:%S')
        #         assert (currentDateTime_formatted_UTC < startDateTime_formatted_UTC), "Unable to modify ongoing event."

        #         print("Updating")

        #         assert event_dao.updateEvent(id, electionType, areaId, startDateTime, endDateTime, NOT_DELETED, NOT_EXPIRED) == 1, "Event Failed to update"
        #     else:
        #         print("Attempt Inserting")
        #         assert event_dao.findEventByAreaId(areaId, NOT_DELETED, NOT_EXPIRED) == 0, "This event has already been created. Multiple events with same area are not allowed."

                
        #         # If result not found = no duplicate, insert data
        #         assert event_dao.putEvent(electionType, areaId, startDateTime, endDateTime, NOT_DELETED, NOT_EXPIRED) == 1, "Event Not Created"
                    
        #     # First "remove" the old candidates
        #     candidate_dao.updateCandidate(id, DELETED)

        #     # Find the just inserted event id
        #     result_F = event_dao.findEvent(electionType, areaId, startDateTime, endDateTime, NOT_DELETED, NOT_DELETED)
        #     id = result_F[0]

        #     # Insert back the new candidates
        #     candidate_dao.insertCandidate(id, candidate_payload)
        # else:
        #     message = 'Event information is invalid. Please verify.'
        #     print(message)
        #     status = 406

        # return True;


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


       

        

