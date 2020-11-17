import hashlib
import string
from datetime import datetime
from random import random

from sqlalchemy import distinct

from app import db


class Team(db.Model):
    id = db.Column(db.Integer, autoincrement=True, unique=True, index=True, primary_key=True)
    name = db.Column(db.String(20))
    color = db.Column(db.String(20))

    waypoint_founds = db.relationship("TeamFoundWaypoint", backref="team", lazy='dynamic')

    @property
    def found_total(self):
        return self.waypoint_founds.with_entities(distinct(TeamFoundWaypoint.id)).count()


class Waypoint(db.Model):
    id = db.Column(db.Integer, autoincrement=True, unique=True, index=True, primary_key=True)
    name = db.Column(db.String(20))
    description = db.Column(db.String(100))
    token = db.Column(db.String(16), index=True)

    coord_x = db.Column(db.Float)
    coord_y = db.Column(db.Float)

    team_founds = db.relationship("TeamFoundWaypoint", backref="waypoint", lazy=False)

    def __init__(self, name, description, coords):
        self.name = name
        self.description = description
        self.coord_x, self.coord_y = coords

        # generate pseudo random token
        self.token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))


class TeamFoundWaypoint(db.Model):
    id = db.Column(db.Integer, autoincrement=True, unique=True, index=True, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    waypoint_id = db.Column(db.Integer, db.ForeignKey('waypoint.id'))
