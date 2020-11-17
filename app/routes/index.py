from flask import render_template, flash

from app.data import teams, waypoints
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
