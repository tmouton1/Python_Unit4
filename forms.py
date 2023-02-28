from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length

class TeamForm(FlaskForm):
    teamname = StringField('team name', validators=[DataRequired(), Length(min=4, max=255)])
    submit = SubmitField("submit")

class ProjectForm(FlaskForm):
    projectname = StringField('project name', validators=[DataRequired(), Length(min=4, max=255)])
    description = TextAreaField('description')
    completed = BooleanField("completed?")
    team_selection = SelectField("team")
    submit = SubmitField("submit")

    def update_teams(self, teams):
        self.team_selection.choices = [ (team.id, team.teamname) for team in teams]

class DelForm(FlaskForm):

    id = IntegerField("Id Number of Project to Remove: ")
    submit = SubmitField("Remove Project")



