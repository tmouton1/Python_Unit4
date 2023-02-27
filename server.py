from flask import Flask, render_template, url_for, redirect
from model import db, connect_to_db, User, Team, Project
from forms import TeamForm, ProjectForm, DelForm
import jinja2

app = Flask(__name__)
app.secret_key = "mysecretkey"

app.jinja_env.undefined = jinja2.StrictUndefined  

user_id = 1 


@app.route("/")
def home():
    team_form = TeamForm()
    project_form = ProjectForm()
    project_form.update_teams(User.query.get(user_id).teams)
    return render_template("home.html", team_form = team_form, project_form = project_form)


@app.route("/add-team", methods=["POST"])
def add_team():
    team_form = TeamForm()

    if team_form.validate_on_submit():
        teamname = team_form.teamname.data
        new_team = Team(teamname=teamname,user_id=user_id,id=id)

        with app.app_context():
            db.session.add(new_team)
            db.session.commit()
        print(team_form.teamname.data)

        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

# =========================================================

@app.route('/teams')
def list_team():


    teams=Team.query.all()
    # with app.app_context():
    #     db.session.query()
    #     db.session.commit()
    print(teams)

    return render_template('teams.html', teams=teams)


    # teams = Team.query.all()

    # with app.app_context():
    #         db.create_all(teams)
    #         db.session.commit()
    #     print(team_form.teamname.data)


# ======================================================

@app.route("/add-project", methods=["POST"])
def add_project():
    project_form = ProjectForm()
    project_form.update_teams(User.query.get(user_id).teams)

    if project_form.validate_on_submit():
        project_name = project_form.project_name.data
        description = project_form.description.data
        completed = project_form.completed.data
        team_id = project_form.team_selection.data

        new_project = Project(project_name, completed, team_id, description)
        with app.app_context():
            db.session.add(new_project)
            db.session.commit()

        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))

# ==================================

@app.route('/teams')
def list_teams():

    teams = Team.query.all()
    with app.app_context():
        db.session.query(teams)
        db.commit()
        
    return render_template('teams.html',teams=teams)
# =================================

@app.route('/projects')
def list_projects():

    projects = Project.query.all()
    print(projects)

    return render_template('projects.html',projects=projects)

# =======================================

@app.route('/delete', methods=['GET', 'POST'])
def del_project():
    form = DelForm()

    if form.validate_on_submit():

        id = form.id.data
        project = Project.query.get(id)
        with app.app_context():
            db.session.delete(project)
            db.session.commit()

            return redirect(url_for('projects'))
        return render_template('delete-project.html',form=form)

# ===================================

if __name__ == "__main__":
    connect_to_db(app)
    app.env = "development"
    app.run(debug = True, port = 8000, host = "localhost")