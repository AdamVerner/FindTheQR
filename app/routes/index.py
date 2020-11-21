from flask import render_template

from app.routes import bp
from app.models import Waypoint, Team, TeamFoundWaypoint


@bp.route('/')
@bp.route('/index')
@bp.route('/index.html')
@bp.route('/index.htm')
def index():
    # flash('hello')
    print(Team.query.all())
    print(Waypoint.query.all())
    return render_template('index.html', teams=Team.query.all(), waypoints=Waypoint.query.all())


@bp.route('/map.js')
def map_gen():
    waypoints = Waypoint.query.all()
    print(waypoints)
    return render_template('map_gen.js', waypoints=waypoints)
