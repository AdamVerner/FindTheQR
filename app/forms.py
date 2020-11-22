from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired, ValidationError, Length

from app.models import Waypoint, Team


def ClaimWaypoint(teams):
    class ClaimWaypointClass(FlaskForm):
        # TODO prefill
        name = StringField(
            'Name',
            validators=[DataRequired(), Length(max=20)],
            render_kw={"placeholder": "Jméno"},
            default=session.get('name'),
        )

    # Dynamically create submit field for all teams
    for team in teams:
        field = SubmitField(
            team.name,
            render_kw={'style': f'background-color: {team.color}', 'class': 'btn btn-lg btn-primary btn-block mt-2'},
        )
        setattr(ClaimWaypointClass, f'submit_{team.id}', field)

    return ClaimWaypointClass()


class AddWaypoint(FlaskForm):
    coord_x = FloatField("X", validators=[DataRequired()], render_kw={"placeholder": "X"})
    coord_y = FloatField("X", validators=[DataRequired()], render_kw={"placeholder": "Y"})

    name = StringField('Name', validators=[DataRequired(), Length(max=20)], render_kw={"placeholder": "Name"})
    desciprion = StringField('Description', validators=[DataRequired()], render_kw={"placeholder": "Description"})

    Add = SubmitField("Add waypoint", render_kw={'class': 'btn btn-lg btn-primary btn-block mt-2'})

    def validate_name(self, name):
        if Waypoint.query.filter_by(name=name.data).first():
            raise ValidationError('Waypoint with this name already exists')


class AddTeam(FlaskForm):
    _colors = {
        'Blue': '#007bff',
        'Gray': '#6c757d',
        'Green': '#28a745',
        'Red': '#dc3545',
        'Yellow': '#ffc107',
        'Cyan': '#17a2b8',
    }

    name = StringField('Name', validators=[DataRequired(), Length(max=20)], render_kw={"placeholder": "Name"})
    color = SelectField('Color', choices=[(v, k) for k, v in _colors.items()])

    Add = SubmitField("Add team", render_kw={'class': 'btn btn-lg btn-primary btn-block mt-2'})

    def validate_name(self, name):
        if Team.query.filter_by(name=name.data).first():
            raise ValidationError('Waypoint with this name already exists')
