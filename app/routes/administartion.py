from urllib.parse import urlunparse, urlparse, urlsplit, urljoin, urlunsplit

from flask import flash, render_template, redirect, url_for

from app import auth, db
from app.forms import AddWaypoint, AddTeam
from app.models import Waypoint, Team, TeamFoundWaypoint
from app.routes import admin_bp as bp


@bp.route('/')
@bp.route('/index')
@bp.route('/index.html')
@auth.required
def index():

    teams = Team.query.all()[::-1]
    waypoints = Waypoint.query.all()[::-1]
    finds = TeamFoundWaypoint.query.all()[::-1]

    split = urlsplit(url_for('.fake_logout', _external=True))
    print(split)
    logout = urlunsplit(split[:1] + ('foo:bar@' + split[1],) + split[2:])
    print(logout)
    return render_template('admin/index.html', teams=teams, waypoints=waypoints, finds=finds, logout=logout)


@bp.route('/logout')
@auth.required
def fake_logout():
    return redirect(url_for('main.index'))


@bp.route('/waypoints/add', methods=['GET', 'POST'])
@auth.required
def add_waypoint():
    form = AddWaypoint()

    if form.validate_on_submit():
        wp = Waypoint(form.name.data, form.desciprion.data, (form.coord_x.data, form.coord_y.data))
        db.session.add(wp)
        db.session.commit()
        flash(f'"{form.name.data}" successfully added')

    return render_template('add_waypoint.html', form=form)


@bp.route('/teams/add', methods=['GET', 'POST'])
@auth.required
def add_team():
    form = AddTeam()

    if form.validate_on_submit():
        t = Team(name=form.name.data, color=form.color.data)
        db.session.add(t)
        db.session.commit()
        flash(f'"{form.name.data}" successfully added')
        return redirect(url_for('.index'))

    return render_template('add_team.html', form=form)


@bp.route('/team/<int:id>/remove', methods=['GET', 'POST'])
@auth.required
def remove_team(id):
    t = Team.query.filter_by(id=id).first_or_404()
    t.waypoint_founds.delete()
    Team.query.filter_by(id=id).delete()
    db.session.commit()
    flash(f'"{t.name}" removed')
    return redirect(url_for('.index'))


@bp.route('/waypoint/<int:id>/remove', methods=['GET', 'POST'])
@auth.required
def remove_waypoint(id):
    w = Waypoint.query.filter_by(id=id).first_or_404()
    Waypoint.query.filter_by(id=id).delete()
    w.team_founds.delete()
    db.session.commit()
    flash(f'"{w.name}" removed')
    return redirect(url_for('.index'))


@bp.route('/find/<int:id>/remove', methods=['GET', 'POST'])
@auth.required
def remove_find(id):
    tw = TeamFoundWaypoint.query.filter_by(id=id).first_or_404()
    flash(f'"{tw.waypoint.name} - {tw.signature}" removed')
    TeamFoundWaypoint.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('.index'))
