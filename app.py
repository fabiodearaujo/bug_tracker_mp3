import os
import json
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

# Solution from stack overflow to resolve error
# TypeError: Object of type ObjectId is not JSON serializable
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.user.find_one(
            {"user_name": request.form.get("user_name").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        # Automatically register as a regular user, only a Manager can change.
        register = {
            "user_name": request.form.get("user_name").lower(),
            "user_pass": generate_password_hash(request.form.get("user_pass")),
            "user_category": "regular"
        }
        mongo.db.user.insert_one(register)

        flash("Registration Successful, please login!")
        return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.user.find_one(
            {"user_name": request.form.get("user_name").lower()})

        if existing_user:
            #ensure hashed password matches user input
            if check_password_hash(
                existing_user["user_pass"], request.form.get("user_pass")):
                    session["user"] = existing_user["user_name"]
                    session["category"] = existing_user["user_category"]
                    flash("Welcome, {}!".format(existing_user["user_name"]))
                    return redirect(url_for(
                        "dashboard", user_name=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username does not exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")



@app.route("/dashboard/<user_name>", methods=["GET", "POST"])
def dashboard(user_name):
    #user_name = mongo.db.user.find_one({"user_name": session["user"]})
    projects = list(mongo.db.project.find(
        {"user_name": session["user"]}).sort("project_name", 1))
    proj_count = []
    tickets = []
    for proj in projects:
        proj_count.append(proj["project_name"])
        proj_receipt = proj["project_name"]
        if proj_receipt:
            ticket = list(mongo.db.ticket.find({"project_name": proj_receipt}))
            tickets.extend(ticket)    
    if not projects:
        flash("No Projects assigned yet, please contact your manager")
        return redirect(url_for("home"))

    return render_template("dashboard.html", 
        user_name=user_name, projects=projects, tickets=tickets)


@app.route("/search", methods=["GET", "POST"])
def search_user():
    query = request.form.get("query")
    user_reg = mongo.db.user.find_one({"$text": {"$search": query}})
    return render_template("manage_user.html", user_reg=user_reg)


@app.route("/manage_user/<user_name>", methods=["GET", "POST"])
def manage_user(user_name):
    user_reg = mongo.db.user.find_one(
            {"user_name": session["user"]})
    return render_template("manage_user.html", user_reg=user_reg)


@app.route("/edit_user/<user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    user = mongo.db.user.find_one({"_id": ObjectId(user_id)})
    if request.method == "POST":
        # modify user name and category with the information from the form
        # but leave password untouched.
        modify = {
            "user_name": request.form.get("user_name").lower(),
            "user_pass": user["user_pass"],
            "user_category": request.form.get("user_category")
        }
        mongo.db.user.replace_one({"_id": ObjectId(user_id)}, modify)

        flash("User information updated Successfully")
        return redirect(url_for("home"))

    return render_template("edit_user.html", user=user)


@app.route("/change_pass/<user_id>", methods=["GET", "POST"])
def change_pass(user_id):
    user = mongo.db.user.find_one({"_id": ObjectId(user_id)})
    if request.method == "POST":
        # Automatically register as a regular user, only a Manager can change.
        modify = {
            "user_name": user["user_name"],
            "user_pass": generate_password_hash(request.form.get("user_pass")),
            "user_category": user["user_category"]
        }
        mongo.db.user.replace_one({"_id": ObjectId(user_id)}, modify)

        flash("User password changed Successfully")
        if session["user"] == modify["user_name"]:
            return redirect(url_for("logout"))
        else:
            return redirect(url_for("home"))

    return render_template("change_pass.html", user=user)


@app.route("/create_project", methods=["GET", "POST"])
def create_project():
    if request.method == "POST":
        # returns the list from selection and store in userlist
        userlist = request.form.getlist("user_name")
        # loop throug the list and create 1 entry for each user
        for user in userlist:
            project = {
                "project_name": request.form.get("project_name"),
                "project_description": request.form.get("project_description"),
                "project_target_date": request.form.get("project_target_date"),
                "user_name": user,
                "project_archive": "off"
            }
            mongo.db.project.insert_one(project)

        flash("Project created successfuly")
        return redirect(url_for("create_project"))

    users = mongo.db.user.find().sort("user_name", 1)
    return render_template("create_project.html", users=users)


@app.route("/create_ticket", methods=["GET","POST"])
def create_ticket():
    if request.method == "POST":
        ticket = {
            "ticket_title": request.form.get("ticket_title"),
            "ticket_description": request.form.get("ticket_description"),
            "ticket_status": "open",
            "category_name": request.form.get("category_name"),
            "project_name": request.form.get("project_name"),
            "created_by": session["user"]
        }
        mongo.db.ticket.insert_one(ticket)
        flash("New ticket created Successfuly")
        return redirect(url_for("create_ticket"))

    categories = mongo.db.category.find().sort("category_name", 1)
    projects = mongo.db.project.find().sort("project_name", 1)
    proj_test = list(mongo.db.project.find({ "user_name": session["user"]}))
    if proj_test:
        return render_template("create_ticket.html", 
        categories=categories, projects=projects)
    else:
        flash("No Projects assigned to you yet, please contact your manager")
        return redirect("home")

    return render_template("create_ticket.html", 
        categories=categories, projects=projects)


@app.route("/project_delete_conf/<project_name>", methods=["GET","POST"])
def project_delete_conf(project_name):
    project_name = mongo.db.project.find_one({"project_name": project_name})["project_name"]
    return render_template("project_delete_conf.html", project_name=project_name)


@app.route("/delete_project/<project_name>")
def delete_project(project_name):
    ticketlist = list(mongo.db.ticket.find({"project_name": project_name}))
    ticket_convert = JSONEncoder().encode(ticketlist)
    tickets = json.loads(ticket_convert)
    for ticket in tickets:
        ticket_id = ticket['_id']
        mongo.db.ticket.remove({"_id": ObjectId(ticket_id)})

    projectlist = list(mongo.db.project.find({"project_name": project_name}))
    project_convert = JSONEncoder().encode(projectlist)
    projects = json.loads(project_convert)
    for project in projects:
        project_id = project['_id']
        mongo.db.project.remove({"_id": ObjectId(project_id)})

    flash("The Project and its Tickets were deleted successfuly")
    return redirect(url_for("home"))


@app.route("/project_archive_conf/<project_name>", methods=["GET","POST"])
def project_archive_conf(project_name):
    project_name = mongo.db.project.find_one({"project_name": project_name})["project_name"]
    return render_template("project_archive_conf.html", project_name=project_name)


@app.route("/archive_project/<project_name>")
def archive_project(project_name):
    projectlist = list(mongo.db.project.find({"project_name": project_name}))
    project_convert = JSONEncoder().encode(projectlist)
    projects = json.loads(project_convert)
    for project in projects:
        project_update = {
            "project_name": project["project_name"],
            "project_description": project["project_description"],
            "project_target_date": project["project_target_date"],
            "user_name": project["user_name"],
            "project_archive": "on"
        }
        mongo.db.project.replace_one({"_id": ObjectId(project["_id"])}, project_update)

    flash("The Project is archived successfuly")
    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    # remove user from session cookies and return to home
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)