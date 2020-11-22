import hashlib
import string
from datetime import datetime
from random import choices

from sqlalchemy import distinct

from app import db


class Team(db.Model):
    id = db.Column(db.Integer, autoincrement=True, unique=True, index=True, primary_key=True)
    name = db.Column(db.String(20))
    color = db.Column(db.String(20))

    waypoint_founds = db.relationship("TeamFoundWaypoint", backref="team", lazy='dynamic')

    @property
    def found_total(self):

        mapping = {}
        for f in TeamFoundWaypoint.query.order_by(TeamFoundWaypoint.timestamp.asc()).all():
            mapping[f.waypoint_id] = f.team_id

        total = len([k for k, v in mapping.items() if v == self.id])

        return total


class Waypoint(db.Model):
    id = db.Column(db.Integer, autoincrement=True, unique=True, index=True, primary_key=True)
    name = db.Column(db.String(20))
    description = db.Column(db.String(100))
    token = db.Column(db.String(16), index=True)

    coord_x = db.Column(db.Float)
    coord_y = db.Column(db.Float)

    team_founds = db.relationship("TeamFoundWaypoint", backref="waypoint", lazy='dynamic')

    def __init__(self, name, description, coords):
        self.name = name
        self.description = description
        self.coord_x, self.coord_y = coords

        # generate pseudo random token
        self.token = ''.join(choices(string.ascii_uppercase + string.digits, k=16))

    @property
    def owners(self):
        """King of the hill style finding"""
        query = TeamFoundWaypoint.query.filter_by(waypoint_id=self.id)
        query = query.order_by(TeamFoundWaypoint.timestamp.desc()).limit(1)

        return (tfw.team for tfw in query.all())


class TeamFoundWaypoint(db.Model):
    id = db.Column(db.Integer, autoincrement=True, unique=True, index=True, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    signature = db.Column(db.String(20))

    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    waypoint_id = db.Column(db.Integer, db.ForeignKey('waypoint.id'))
