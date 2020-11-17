from flask import render_template, request, session

from app.models import Waypoint, Team
from app.routes import bp


@bp.route('/found/<token>')
def found(token: str):
    waypoint = Waypoint.query.filter_by(token=token).first_or_404()
    teams = Team.query.all()
    return render_template('found.html', waypoint=waypoint, teams=teams)


@bp.route('/report', methods=['POST', 'GET'])
def report():
    print(request.form)
    return 'success'
