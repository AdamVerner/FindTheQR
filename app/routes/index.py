from flask import render_template

from app.data import teams, waypoints
from app.routes import bp


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', teams=teams, waypoints=waypoints)
