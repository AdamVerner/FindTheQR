from operator import attrgetter

from flask import render_template

from app.routes import bp
from app.models import Waypoint, Team, TeamFoundWaypoint


@bp.route('/')
@bp.route('/index')
@bp.route('/index.html')
@bp.route('/index.htm')
def index():
    teams = sorted(Team.query.all(), key=attrgetter('found_total'))

    return render_template('index.html', teams=teams, waypoints=Waypoint.query.all())


@bp.route('/map.js')
def map_gen():
    waypoints = Waypoint.query.all()
    return render_template('map_gen.js', waypoints=waypoints)


@bp.route('/robots.txt')
def robots():
    r = 'User-agent: *\n'\
        'Disallow: /\n'
    return r