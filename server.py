from flask import Flask, render_template, url_for, redirect, session, flash, request
# from flask_wtf import FlaskForm
from model import db, connect_to_db, User, Team, Project
from forms import TeamForm, ProjectForm, LoginForm
import jinja2

app = Flask(__name__)
app.secret_key = "keep this secret"

app.jinja_env.undefined = jinja2.StrictUndefined  


user_id = 1

@app.route("/")
def home():
    team_form = TeamForm()
    project_form = ProjectForm()
    project_form.update_teams(User.quer.get(user_id).teams)
    return render_template("home.html", team_form = team_form, project_form = project_form)

@app.route("/add-team", methods=["POST"])
def add_team():
    team_form = TeamForm()

    if team_form.validate_on_submit():
        team_name = team_form.team_name.data
        new_team = Team(team_name, user_id)
        with app.app_context():
            db.session.add(new_team)
            db.session.commit()
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))


@app.route("/add-project", methods=["POST"])
def add_project():
    project_form = ProjectForm()
    project_form.update_teams(User.query.get(user_id).teams)

    if project_form.validate_on_submit():
        project_name = project_form.project_name.data
        description = project_form.description.data
        completed = project_form.completed.data
        team_id = project_form.team_selection.data

        new_project = Project(project_name, completed, team_id, description = description)
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))



@app.route("/login", methods=["GET", "POST"])
def login():
   """Log user into site."""
   form = LoginForm(request.form)

   if form.validate_on_submit():
      username = form.username.data
      password = form.password.data

      user = user.get_by_username(username)

      if not user or user['password'] != password:
            flash("Invalid username or password")
            return redirect('/login')

      session["username"] = user['username']
      flash("Logged in.")
      return redirect("/")

   return render_template("login.html", form=form)


@app.route("/logout")
def logout():

   del session["username"]
   flash("Logged out.")
   return redirect("/login")

if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug = True)