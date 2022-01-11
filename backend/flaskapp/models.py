from flaskapp.db import *
from dataclasses import dataclass
from datetime import datetime
# Database models

@dataclass
class Users(db.Model):
    id = db.Column(db.Integer, nullable=False) ##
    nickname = db.Column(db.String, nullable=True)
    email = db.Column(db.String, unique=True, nullable=False, primary_key=True)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.Integer, nullable=False, default=1)
    area_id = db.Column(db.String, nullable=True)
    public_key = db.Column(db.String, nullable=True)
    private_key = db.Column(db.String, nullable=True)
    key_image = db.Column(db.String, nullable=True)

@dataclass
class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    election_type = db.Column(db.Integer, nullable=False)
    area_id = db.Column(db.String, unique=True, nullable=False)
    start_date_time = db.Column(db.DateTime, nullable=False)
    end_date_time = db.Column(db.DateTime, nullable=False)
    del_flag = db.Column(db.Integer, nullable=False, default=0)
    expire_flag = db.Column(db.Integer, nullable=False, default=0)

@dataclass
class ElectionType(db.Model):
    election_id = db.Column(db.Integer, primary_key=True, nullable=False)
    election_name = db.Column(db.String, nullable=False)
    del_flag = db.Column(db.Integer, nullable=False, default=0)

@dataclass
class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    event_id = db.Column(db.Integer, nullable=False)
    candidate_name = db.Column(db.String, nullable=False)
    candidate_image = db.Column(db.String, nullable=False)
    vote_count = db.Column(db.Integer, nullable=False, default=0)
    del_flag = db.Column(db.Integer, nullable=False, default=0)

@dataclass
class Area(db.Model):
    area_id = db.Column(db.String, primary_key=True, nullable=False, unique=True)
    area_name = db.Column(db.String, nullable=False)
    election_type = db.Column(db.String, nullable=False)
    del_flag = db.Column(db.Integer, nullable=False, default=0)

result = db.engine.execute("SHOW STATUS LIKE 'Ssl_cipher'")
names = [row[1] for row in result]
print (names)