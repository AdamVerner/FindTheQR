from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


def ClaimWaypoint(teams):
    class ClaimWaypointClass(FlaskForm):
        # TODO prefill
        name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Jméno"})

    # Dynamically create submit field for all teams
    for team in teams:
        print(team)
        field = SubmitField(
            team.name,
            render_kw={'style': f'background-color: {team.color}', 'class': 'btn btn-lg ' 'btn-primary btn-block mt-2'},
        )
        setattr(ClaimWaypointClass, f'submit_{team.name}', field)

    return ClaimWaypointClass()
