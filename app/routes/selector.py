from functools import wraps
from datetime import datetime

import pytz
from flask import render_template, request, session, flash, redirect, url_for, current_app

from app import db
from app.forms import ClaimWaypoint
from app.models import Waypoint, Team, TeamFoundWaypoint
from app.routes import bp


def check_end_of_game(f):

    @wraps(f)
    def inner(*args, **kwargs):

        now = pytz.timezone('Europe/Prague').localize(datetime.now())
        end = datetime.fromisoformat(current_app.config.get('END_DATE'))

        if now > end:
            return render_template('over.html')

        return f(*args, **kwargs)

    return inner



@bp.route('/found/<token>', methods=['GET', 'POST'])
@check_end_of_game
def found(token: str):
    session['hidden_token'] = token
    return redirect(url_for('.hidden_found'))


@bp.route('/found', methods=['GET', 'POST'])
@check_end_of_game
def hidden_found():

    waypoint = Waypoint.query.filter_by(token=session['hidden_token']).first_or_404()
    teams = Team.query.all()

    form = ClaimWaypoint(teams)

    if form.validate_on_submit():
        id = next((int(s.replace('submit_', '')) for s, v in form.data.items() if v and s.startswith('submit_')))
        f = TeamFoundWaypoint(signature=form.name.data, team_id=id, waypoint_id=waypoint.id)
        db.session.add(f)
        db.session.commit()

        session['name'] = form.name.data

        flash(f'{waypoint.name} úspěšně nalezen.')
        session.pop('hidden_token')
        return redirect(url_for('main.index'))

    return render_template('found.html', waypoint=waypoint, teams=teams, form=form)
