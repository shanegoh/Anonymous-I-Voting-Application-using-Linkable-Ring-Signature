from flaskapp.util import DELETED, NOT_DELETED, NOT_EXPIRED
from flaskapp.models import Users, Event, ElectionType, Candidate, Area, KeyImage, VoteHistory
from flaskapp.db import db
from datetime import datetime, timezone
from sqlalchemy.orm.exc import NoResultFound

# Database access object
class UserDAO:
    def __init__(self, model):
        self.model = model    

    def findUserInformationByEmail(self, email):
        return ( Users.query
                .with_entities(Users.role, Users.area_id)  
                .filter(Users.email == email)
                .one())    

    def findAreaNameByEmail(self, email, deleteFlag):
        return Users.query.join(Area, Area.area_id == Users.area_id) \
            .with_entities(Area.area_name) \
            .filter(Area.del_flag == deleteFlag) \
            .filter(Users.email == email) \
            .first()
        
    def findNumberOfParticipantByEventId(self, eventId):
        return Users.query \
            .filter(Users.area_id.in_(Event.query.with_entities(Event.area_id) \
            .filter(Event.event_id == eventId))) \
            .count()
    
    def findAllPrivateAndPublicKeyByEvent(self, eventId, deleteFlag, expireFlag):
        return Users.query \
            .with_entities(Users.private_key, Users.public_key) \
            .filter(Users.area_id.in_(Event.query.with_entities(Event.area_id) \
            .filter(Event.event_id == eventId) \
            .filter(Event.del_flag == deleteFlag) \
            .filter(Event.expire_flag == expireFlag))) \
            .all();

    def findEmailByPrivateKey(self, privateKey):
        return Users.query.with_entities(Users.email) \
            .filter(Users.private_key == privateKey) \
            .first()

    def findPrivateKeyByEmail(self, email):
        return Users.query.with_entities(Users.private_key) \
            .filter(Users.email == email) \
            .first()

    def findAllEmail(self):
        return Users.query.with_entities(Users.email) \
            .all()

    def updateUser(self, user_list):
        db.session.bulk_update_mappings(Users, user_list)
        db.session.commit()
    
    def findAreaIdByEmail(self, email):
        return Users.query.with_entities(Users.area_id) \
            .filter(Users.email == email) \
            .one()


class EventDAO:
    def __init__(self, model):
        self.model = model    
    
    def findAllEvent(self, deleteFlag, expireFlag):
        return Event.query.join(Area, Event.area_id == Area.area_id) \
            .with_entities(Event.event_id,Area.area_name,Event.start_date_time, Event.end_date_time) \
            .filter(Event.del_flag == deleteFlag) \
            .filter(Area.del_flag == deleteFlag) \
            .filter(Event.expire_flag == expireFlag) \
            .all()

    def findEventForVoter(self, areaId, deleteFlag, expireFlag):
        return Event.query.join(Area, Event.area_id == Area.area_id) \
            .with_entities(Event.event_id,Area.area_name,Event.start_date_time, Event.end_date_time) \
            .filter(Event.del_flag == deleteFlag) \
            .filter(Area.del_flag == deleteFlag) \
            .filter(Event.expire_flag == expireFlag) \
            .filter(Event.area_id == areaId) \
            .first()

    def findEventById(self, eventId, deleteFlag, expireFlag):
        return Event.query.filter(Event.event_id == eventId) \
            .filter(Event.del_flag == deleteFlag) \
            .filter(Event.expire_flag == expireFlag) \
            .one()

    def findEventDetailsById(self, id, deleteFlag, expireFlag):
        return Event.query.with_entities(Event.election_type, Event.area_id, Event.start_date_time, Event.end_date_time) \
            .filter(Event.start_date_time > datetime.now(timezone.utc)) \
            .filter(Event.event_id == id) \
            .filter(Event.del_flag == deleteFlag) \
            .filter(Event.expire_flag == expireFlag) \
            .one()

    def findEventStartDateTime(self, eventId, deleteFlag, expireFlag):
        return Event.query.with_entities(Event.start_date_time) \
            .filter(Event.event_id == eventId) \
            .filter(Event.del_flag == deleteFlag) \
            .filter(Event.expire_flag == expireFlag) \
            .one();


    def updateEvent(self, id, electionType, areaId, startDateTime, endDateTime, deleteFlag, expireFlag):
        event = Event.query.filter(Event.event_id == id) \
            .filter(Event.del_flag == deleteFlag) \
            .filter(Event.expire_flag == expireFlag) \
            .first()
        event.election_type = electionType
        event.area_id = areaId
        event.start_date_time = datetime.strptime(startDateTime, '%Y-%m-%dT%H:%M:%S.%fZ')
        event.end_date_time = datetime.strptime(endDateTime, '%Y-%m-%dT%H:%M:%S.%fZ')
        db.session.commit()
        return True

    def findEventByAreaId(self, areaId, deleteFlag, expireFlag):
        return Event.query.filter(Event.area_id == areaId) \
            .filter(Event.del_flag == deleteFlag) \
            .filter(Event.expire_flag == expireFlag) \
            .first()

    def putEvent(self, electionType, areaId, startDateTime, endDateTime, deleteFlag, expireFlag):
        event = Event(election_type = electionType, \
                        area_id = areaId, \
                        start_date_time = datetime.strptime(startDateTime, '%Y-%m-%dT%H:%M:%S.%fZ'), \
                        end_date_time = datetime.strptime(endDateTime, '%Y-%m-%dT%H:%M:%S.%fZ'), \
                        del_flag = NOT_DELETED, \
                        expire_flag = NOT_EXPIRED)
        db.session.add(event)
        db.session.commit();
        return True;
              
    def findEvent(self, electionType, areaId, startDateTime, endDateTime, deleteFlag, expireFlag):
        return Event.query.with_entities(Event.event_id) \
            .filter(Event.election_type == electionType) \
            .filter(Event.area_id == areaId) \
            .filter(Event.start_date_time == datetime.strptime(startDateTime, '%Y-%m-%dT%H:%M:%S.%fZ')) \
            .filter(Event.end_date_time == datetime.strptime(endDateTime, '%Y-%m-%dT%H:%M:%S.%fZ')) \
            .filter(Event.del_flag == deleteFlag) \
            .filter(Event.expire_flag == expireFlag) \
            .one()       

    def deleteEventById(self, id, deleteFlag):
        number_of_row = Event.query.filter(Event.event_id == id) \
            .update(dict(del_flag=deleteFlag)) 
        db.session.commit();
        return number_of_row  
 

class ElectionTypeDAO:
    def __init__(self, model):
        self.model = model    
    def findAllElectionType(self, deleteFlag):
        return ElectionType.query \
            .with_entities(ElectionType.election_id, ElectionType.election_name) \
            .filter(ElectionType.del_flag == deleteFlag) \
            .all()

    def findElectionTypeById(self, electionId, deleteFlag):
        return ElectionType.query \
            .filter(ElectionType.election_id == electionId) \
            .filter(ElectionType.del_flag == deleteFlag) \
            .one()


class AreaDAO:
    def __init__(self, model):
        self.model = model
    def findAllAreaType(self, deleteFlag):
        return Area.query \
            .with_entities(Area.area_id, Area.area_name, Area.election_type) \
            .filter(Area.del_flag == deleteFlag) \
            .all()

    def findAreaById(self, areaId, deleteFlag):
        return Area.query \
            .filter(Area.area_id == areaId) \
            .filter(Area.del_flag == deleteFlag) \
            .one()


class CandidateDAO:
    def __init__(self, model):
        self.model = model

    def updateCandidate(self, eventId, deleteFlag):
        number_of_row = Candidate.query \
            .filter(Candidate.event_id == eventId) \
            .update(dict(del_flag=deleteFlag))
        db.session.commit();
        return number_of_row

    def insertCandidate(self, id, candidate_payload):
        for record in candidate_payload:
            candidate = Candidate(event_id = id, candidate_name = record['candidate_name'], candidate_image = record['candidate_image'])
            db.session.add(candidate)
        db.session.commit();
        return True;

    def findAllCandidatesByEventId(self, id, deleteFlag):
        return Candidate.query.with_entities(Candidate.candidate_name, Candidate.candidate_image)\
            .filter(Candidate.event_id == id) \
            .filter(Candidate.del_flag == deleteFlag) \
            .all()

    def deleteCandidateByEventId(self, id, deleteFlag):
        number_of_row = Candidate.query \
            .filter(Candidate.event_id == id) \
            .update(dict(del_flag=deleteFlag)) 
        db.session.commit();
        return number_of_row 

    def findCandidateByEventId(self, id, email, deleteFlag, expireFlag):
        return Candidate.query.join(Event, Event.event_id == Candidate.event_id) \
            .join(Area, Area.area_id == Event.area_id) \
            .join(Users, Users.area_id == Area.area_id) \
            .with_entities(Area.area_name, Candidate.candidate_name, Candidate.candidate_image) \
            .filter(Users.email == email) \
            .filter(Users.key_image.is_(None)) \
            .filter(Candidate.event_id == id) \
            .filter(Event.del_flag == deleteFlag) \
            .filter(Event.expire_flag == expireFlag) \
            .filter(Candidate.del_flag == deleteFlag) \
            .filter(Area.del_flag == deleteFlag) \
            .all()
    def incrementVoteCount(self, eventId, candidateName, deleteFlag):
        number_of_row = Candidate.query.filter(Candidate.event_id == eventId) \
            .filter(Candidate.candidate_name == candidateName) \
            .filter(Candidate.del_flag == deleteFlag) \
            .update(dict(vote_count = Candidate.vote_count + 1))
        db.session.commit();
        return number_of_row
       
    def findResultByEventId(self, eventId, deleteFlag, expireFlag):
        return Candidate.query \
            .join(Event, Event.event_id == Candidate.event_id) \
            .with_entities(Candidate.candidate_name, Candidate.vote_count, Area.query.with_entities(Area.area_name) \
            .filter(Area.area_id == Event.area_id).label("area_name")) \
            .filter(Candidate.event_id == eventId) \
            .filter(Event.expire_flag == expireFlag) \
            .filter(Candidate.del_flag == deleteFlag) \
            .filter(Event.del_flag == deleteFlag) \
            .all()
   

class KeyImageDao:
    def __init__(self, model):
        self.model = model

    def findAllKeyImageByEventId(self, eventId):
        return KeyImage.query \
            .with_entities(KeyImage.key_image) \
            .filter(KeyImage.event_id == eventId) \
            .all()
    def insertKeyImageByEventId(self, eventId, keyImage):
        keyImage = KeyImage(event_id = eventId, key_image = keyImage)
        db.session.add(keyImage)
        db.session.commit();
        return True;


class VoteHistoryDAO:
    def __init__(self, model):
        self.model = model

    def insertVoteHistory(self, email):
        voteHistory = VoteHistory(email = email)
        db.session.add(voteHistory)
        db.session.commit();
        return True;

    def findVoteStatus(self, email):
        try:
            VoteHistory.query.filter(VoteHistory.email == email).one()
            return 1
        except NoResultFound:
            return 0



user_dao = UserDAO(Users)
event_dao = EventDAO(Event)  
election_type_dao = ElectionTypeDAO(ElectionType)
area_dao = AreaDAO(Area)
candidate_dao = CandidateDAO(Candidate)
keyImage_dao = KeyImageDao(KeyImage)
voteHistory_dao = VoteHistoryDAO(VoteHistory)