from flask import render_template, request, session, flash, redirect, url_for

from app import db
from app.forms import ClaimWaypoint
from app.models import Waypoint, Team, TeamFoundWaypoint
from app.routes import bp


@bp.route('/found/<token>', methods=['GET', 'POST'])
def found(token: str):
    session['hidden_token'] = token
    return redirect('.hidden_found')


@bp.route('/found', methods=['GET', 'POST'])
def hidden_found():
    token = session['hidden_token']
    session.pop('hidden_token')

    waypoint = Waypoint.query.filter_by(token=token).first_or_404()
    teams = Team.query.all()

    form = ClaimWaypoint(teams)

    if form.validate_on_submit():
        id = next((int(s.replace('submit_', '')) for s, v in form.data.items() if v and s.startswith('submit_')))
        f = TeamFoundWaypoint(signature=form.name.data, team_id=id, waypoint_id=waypoint.id)
        db.session.add(f)
        db.session.commit()

        session['name'] = form.name.data

        flash(f'successfully claimed a point for {id}')
        return redirect(url_for('main.index'))

    return render_template('found.html', waypoint=waypoint, teams=teams, form=form)
