import os
import requests
import json
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import (
    generate_password_hash, check_password_hash)
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

# Enviroment configuration variables
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
admpass = os.environ.get("ADMPASS")
api_key = os.environ.get("APPID")

mongo = PyMongo(app)

# Solution from stack overflow to resolve error
# TypeError: Object of type ObjectId is not JSON serializable
# https://stackoverflow.com/questions/16586180/typeerror-objectid
# -is-not-json-serializable
# It was not possible to read the result returned form the DB
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


@app.route("/")
@app.route("/home", methods=["GET", "POST"])
def home():
    # Setting up the API URL to request the JSON file
    api_url = ("http://api.openweathermap.org/data/2.5/"
               "weather?&APPID={}&q={},{}&units=metric")

    if "user_city" in session:
        # Request Data from API including api_key and city
        w_request = requests.get(api_url.format(
            api_key, session["user_city"], session["user_country"]))
    else:
        # Request Data from API including api_key and city
        w_request = requests.get(api_url.format(
            api_key, "Dublin", "IE"))

    # Convert data to Jason Dictionary
    weather = w_request.json()
    w_icon = "http://openweathermap.org/img/wn/{}@2x.png".format(
        weather["weather"][0]["icon"])
    w_cond = weather["weather"][0]["main"]
    w_desc = weather["weather"][0]["description"]
    w_temp = int(weather["main"]["temp"])
    w_hum = int(weather["main"]["humidity"])
    w_city = weather["name"]
    if "user_city" in session:
        w_ctry = session["user_country"].upper()
        w_dictionary = {
            "city": w_city,
            "country": w_ctry,
            "condition": w_cond,
            "description": w_desc,
            "temperature": w_temp,
            "humidity": w_hum,
            "icon": w_icon
        }
    else:
        w_dictionary = {
            "city": "Dublin",
            "country": "IE",
            "condition": w_cond,
            "description": w_desc,
            "temperature": w_temp,
            "humidity": w_hum,
            "icon": w_icon
        }

    return render_template("home.html", w_dictionary=w_dictionary)


# App route for User Registration - based on Tim's videos
# The Code Institute
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.user.find_one(
            {"user_name": request.form.get("user_name").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        # Automatically register as a regular user, only a Manager
        # can change.
        register = {
            "user_name": request.form.get("user_name").lower(),
            "user_pass": generate_password_hash(request.form.get(
                "user_pass")),
            "user_category": "regular",
            "user_city": request.form.get("user_city").lower(),
            "user_country": request.form.get("user_country")
        }

        project = {
            "project_name": request.form.get("user_name")+"_baseproj",
            "project_description": request.form.get(
                                        "Base Project"),
            "project_target_date": request.form.get(
                                        "30 December, 2030"),
            "user_name": request.form.get("user_name"),
            "project_archive": "off"
        }
            
        
        # Setting up the API URL to request the JSON file
        api_url = ("http://api.openweathermap.org/data/2.5/"
                   "weather?&APPID={}&q={},{}&units=metric")
        # Request Data from API including api_key and city
        w_request = requests.get(api_url.format(
            api_key, register["user_city"], register["user_country"]))
        weather = w_request.json()
        # check if city and country informed are valid
        if weather["cod"] == 200:
            mongo.db.user.insert_one(register)
            mongo.db.project.insert_one(project)
            flash("Registration Successful, please login!")
            return redirect(url_for("login"))
        else:
            flash("Combination City/Country not found,"
                  " please try again")

    return render_template("register.html")


# App route to login page - based on Tim's videos - The Code Institute
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.user.find_one(
            {"user_name": request.form.get("user_name").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user["user_pass"], request.form.get(
                    "user_pass")):
                session["user"] = existing_user["user_name"]
                session["user_city"] = existing_user["user_city"]
                session["user_country"] = existing_user["user_country"]
                session["category"] = existing_user["user_category"]
                flash("Welcome, {}!".format(existing_user[
                                                    "user_name"]))
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


# App route to login as Admin for test purposes
@app.route("/admin_login")
def admin_login():
    existing_user = mongo.db.user.find_one(
            {"user_name": "admintest"})
    if check_password_hash(
            existing_user["user_pass"], admpass):
        session["user"] = existing_user["user_name"]
        session["user_city"] = existing_user["user_city"]
        session["user_country"] = existing_user["user_country"]
        session["category"] = existing_user["user_category"]
        flash("Welcome, {}!".format(existing_user["user_name"]))
        return redirect(url_for(
            "dashboard", user_name=session["user"]))
    else:
        flash("Please contact the developer")
        return redirect(url_for("login"))

    return render_template("login.html")


# App route for the User Dashboard where it will be
# displayed the projects and tickets
@app.route("/dashboard/<user_name>", methods=["GET", "POST"])
def dashboard(user_name):
    # return the project list of the user
    projects = list(mongo.db.project.find(
        {"user_name": session["user"]}).sort("project_name", 1))
    # lists to receive projects and tickets
    proj_count = []
    tickets = []
    # Check if there are projects to the user, if no projecs assigned
    # user is not allowed to access the dashboard
    if not projects:
        flash("No Projects assigned yet, please contact your manager")
        return redirect(url_for("home"))
    else:
        # iterate through the projects to get the tickets for each one
        for proj in projects:
            proj_count.append(proj["project_name"])
            proj_receipt = proj["project_name"]
            if proj_receipt:
                ticket = list(mongo.db.ticket.find(
                                {"project_name": proj_receipt}))
                tickets.extend(ticket)

    # Setting up the API URL to request the JSON file
    api_url = ("http://api.openweathermap.org/data/2.5/"
               "weather?&APPID={}&q={},{}&units=metric")
    # Request Data from API including api_key and city
    w_request = requests.get(api_url.format(
        api_key, session["user_city"], session["user_country"]))
    # Convert data to Jason Dictionary
    weather = w_request.json()
    w_icon = "http://openweathermap.org/img/wn/{}@2x.png".format(
        weather["weather"][0]["icon"])
    w_cond = weather["weather"][0]["main"]
    w_desc = weather["weather"][0]["description"]
    w_temp = int(weather["main"]["temp"])
    w_hum = int(weather["main"]["humidity"])
    w_city = weather["name"]
    w_ctry = session["user_country"].upper()
    w_dictionary = {
        "city": w_city,
        "country": w_ctry,
        "condition": w_cond,
        "description": w_desc,
        "temperature": w_temp,
        "humidity": w_hum,
        "icon": w_icon
    }
    return render_template("dashboard.html",
                           user_name=user_name, projects=projects,
                           tickets=tickets, w_dictionary=w_dictionary)


# App route for search user function - based on Tim's video
# The code Institute
@app.route("/search", methods=["GET", "POST"])
def search_user():
    query = request.form.get("query")
    user_reg = mongo.db.user.find_one({"$text": {"$search": query}})
    return render_template("manage_user.html", user_reg=user_reg)


# App route to Manage Users
@app.route("/manage_user/<user_name>", methods=["GET", "POST"])
def manage_user(user_name):
    user_reg = mongo.db.user.find_one(
            {"user_name": session["user"]})
    return render_template("manage_user.html", user_reg=user_reg)


# App route for editing the user
@app.route("/edit_user/<user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    user = mongo.db.user.find_one({"_id": ObjectId(user_id)})
    if request.method == "POST":
        # modify user name and category with the information from
        # the form but leave password untouched.
        if session["category"] == "manager":
            modify = {
                "user_name": user["user_name"],
                "user_pass": user["user_pass"],
                "user_category": request.form.get("user_category"),
                "user_city": request.form.get("user_city"),
                "user_country": request.form.get("user_country")
            }
        else:
            modify = {
                "user_name": user["user_name"],
                "user_pass": user["user_pass"],
                "user_category": user["user_category"],
                "user_city": request.form.get("user_city"),
                "user_country": request.form.get("user_country")
            }

        # Setting up the API URL to request the JSON file
        api_url = ("http://api.openweathermap.org/data/2.5/"
                   "weather?&APPID={}&q={},{}&units=metric")
        # Request Data from API including api_key and city
        w_request = requests.get(api_url.format(
            api_key, modify["user_city"], modify["user_country"]))
        weather = w_request.json()
        # check if city and country informed are valid
        if weather["cod"] == 200:
            mongo.db.user.replace_one(
                {"_id": ObjectId(user_id)}, modify)
            flash("User updated Successfully, changes"
                  " will be reflected after next Log In")
            return redirect(url_for(
                        "dashboard", user_name=session["user"]))
        else:
            flash("Combination City/Country not found,"
                  " please try again")

    return render_template("edit_user.html", user=user)


# App route to Change Password
@app.route("/change_pass/<user_id>", methods=["GET", "POST"])
def change_pass(user_id):
    user = mongo.db.user.find_one({"_id": ObjectId(user_id)})
    if request.method == "POST":
        # Only password is affected with this change
        modify = {
            "user_name": user["user_name"],
            "user_pass": generate_password_hash(
                            request.form.get("user_pass")),
            "user_category": user["user_category"],
            "user_city": user["user_city"],
            "user_country": user["user_country"]
        }
        mongo.db.user.replace_one({"_id": ObjectId(user_id)}, modify)

        flash("User password changed Successfully")
        # if the user is changing its own password the system
        # will force logout, but if a manager changing for another
        # user, the system will keep it loged in.
        if session["user"] == modify["user_name"]:
            return redirect(url_for("logout"))
        else:
            return redirect(url_for(
                        "dashboard", user_name=session["user"]))

    return render_template("change_pass.html", user=user)


# App Route to Create Project
@app.route("/create_project", methods=["GET", "POST"])
def create_project():
    if request.method == "POST":
        # returns the list from selection and store in userlist
        userlist = request.form.getlist("user_name")
        # loop throug the list and create 1 entry for each user
        # projects will have Archive status Off by defaut
        for user in userlist:
            project = {
                "project_name": request.form.get("project_name"),
                "project_description": request.form.get(
                                            "project_description"),
                "project_target_date": request.form.get(
                                            "project_target_date"),
                "user_name": user,
                "project_archive": "off"
            }
            mongo.db.project.insert_one(project)

        flash("Project created successfuly")
        return redirect(url_for(
            "dashboard", user_name=session["user"]))

    users = mongo.db.user.find().sort("user_name", 1)
    return render_template("create_project.html", users=users)


# App route to Create Tickets
@app.route("/create_ticket", methods=["GET", "POST"])
def create_ticket():
    if request.method == "POST":
        # create 1 ticket with status set automaticaly to open
        ticket = {
            "ticket_title": request.form.get("ticket_title"),
            "ticket_description": request.form.get(
                                    "ticket_description"),
            "ticket_status": "open",
            "category_name": request.form.get("category_name"),
            "project_name": request.form.get("project_name"),
            "created_by": session["user"],
            "assigned_to": session["user"]
        }
        mongo.db.ticket.insert_one(ticket)
        flash("New ticket created Successfuly")
        return redirect(url_for("create_ticket"))

    # Get categories from DB to selection on the render template
    categories = mongo.db.category.find().sort("category_name", 1)
    # Get project to link to the ticket
    projects = mongo.db.project.find().sort("project_name", 1)
    proj_test = list(mongo.db.project.find(
                        {"user_name": session["user"]}))
    if proj_test:
        return render_template("create_ticket.html",
                               categories=categories,
                               projects=projects)
    else:
        # if user has no projects assigned,
        # he is not able to create tickets
        flash("No Projects assigned to you yet,"
              " please contact your manager")
        return redirect("home")

    return render_template("create_ticket.html",
                           categories=categories, projects=projects)


# App Route for confirmation step before deleting a project
@app.route(
    "/project_delete_conf/<project_name>", methods=["GET", "POST"])
def project_delete_conf(project_name):
    project_name = mongo.db.project.find_one(
                    {"project_name": project_name})["project_name"]
    return render_template(
            "project_delete_conf.html", project_name=project_name)


# App Route for the Delete Project + Tickets function.
@app.route("/delete_project/<project_name>")
def delete_project(project_name):
    # Getting tickets related to the project
    ticketlist = list(mongo.db.ticket.find(
                        {"project_name": project_name}))
    # For some reason the list was not in the correct
    # format and I had to encode it
    ticket_convert = JSONEncoder().encode(ticketlist)
    # Again another transformation to be able to work with the data
    tickets = json.loads(ticket_convert)
    # loop through the tickets and delete all related to the project
    for ticket in tickets:
        ticket_id = ticket['_id']
        mongo.db.ticket.remove({"_id": ObjectId(ticket_id)})

    # Getting the Projects (It has 1 entry for each user assigned to it)
    projectlist = list(mongo.db.project.find(
                        {"project_name": project_name}))
    # Again I was not able to work with the data and had to encode
    project_convert = JSONEncoder().encode(projectlist)
    # then transform it on a json dictionary to be able to work.
    projects = json.loads(project_convert)
    # loop through the Project itens deleting all occurences
    for project in projects:
        project_id = project['_id']
        mongo.db.project.remove({"_id": ObjectId(project_id)})

    flash("The Project and its Tickets were deleted successfuly")
    return redirect(url_for("dashboard", user_name=session["user"]))


# App route to Project Archiving confirmation
@app.route(
    "/project_archive_conf/<project_name>", methods=["GET", "POST"])
def project_archive_conf(project_name):
    project_name = mongo.db.project.find_one(
                    {"project_name": project_name})["project_name"]
    return render_template(
            "project_archive_conf.html", project_name=project_name)


# App Route to Archiving project function
@app.route("/archive_project/<project_name>")
def archive_project(project_name):
    # Getting tickets related to the project
    ticketlist = list(mongo.db.ticket.find(
                        {"project_name": project_name}))
    # For some reason the list was not in the correct
    # format and I had to encode it
    ticket_convert = JSONEncoder().encode(ticketlist)
    # Again another transformation to be able to work with the data
    tickets = json.loads(ticket_convert)
    # loop through the tickets and close all
    # tickets related to the project
    for ticket in tickets:
        ticket_id = ticket['_id']
        ticket_edit = {
            "ticket_title": ticket["ticket_title"],
            "ticket_description": ticket["ticket_description"],
            "ticket_status": "closed",
            "category_name": ticket["category_name"],
            "project_name": ticket["project_name"],
            "created_by": session["user"],
            "assigned_to": ticket["assigned_to"]
        }
        mongo.db.ticket.replace_one(
                    {"_id": ObjectId(ticket_id)}, ticket_edit)

    # Get the list of projects
    projectlist = list(mongo.db.project.find(
                            {"project_name": project_name}))
    # encode it
    project_convert = JSONEncoder().encode(projectlist)
    # load json dictionary
    projects = json.loads(project_convert)
    # loop through the project to each user
    # and change Archiving status to "ON"
    for project in projects:
        project_update = {
            "project_name": project["project_name"],
            "project_description": project["project_description"],
            "project_target_date": project["project_target_date"],
            "user_name": project["user_name"],
            "project_archive": "on"
        }
        mongo.db.project.replace_one(
                    {"_id": ObjectId(project["_id"])}, project_update)

    flash("The Project is archived successfuly")
    return redirect(url_for("dashboard", user_name=session["user"]))


# App route to close the ticket
@app.route("/close_ticket/<ticket_id>")
def close_ticket(ticket_id):
    ticket = mongo.db.ticket.find_one({"_id": ObjectId(ticket_id)})
    ticket_update = {
        "ticket_title": ticket["ticket_title"],
        "ticket_description": ticket["ticket_description"],
        "ticket_status": "closed",
        "category_name": ticket["category_name"],
        "project_name": ticket["project_name"],
        "created_by": ticket["created_by"],
        "assigned_to": ticket["assigned_to"]
    }
    mongo.db.ticket.replace_one(
                        {"_id": ObjectId(ticket_id)}, ticket_update)
    flash("Your Ticket was closed sussesfuly")
    return redirect(url_for("dashboard", user_name=session["user"]))


# App route to reopen the ticket
@app.route("/reopen_ticket/<ticket_id>")
def reopen_ticket(ticket_id):
    ticket = mongo.db.ticket.find_one({"_id": ObjectId(ticket_id)})
    ticket_update = {
        "ticket_title": ticket["ticket_title"],
        "ticket_description": ticket["ticket_description"],
        "ticket_status": "open",
        "category_name": ticket["category_name"],
        "project_name": ticket["project_name"],
        "created_by": ticket["created_by"],
        "assigned_to": ticket["assigned_to"]
    }
    mongo.db.ticket.replace_one(
                        {"_id": ObjectId(ticket_id)}, ticket_update)
    flash("Your Ticket was reopened sussesfuly")
    return redirect(url_for("dashboard", user_name=session["user"]))


# App Route to edit the ticket
@app.route("/edit_ticket/<ticket_id>", methods=["GET", "POST"])
def edit_ticket(ticket_id):
    if request.method == "POST":
        # ticket can be updated anytime to include more comments
        # or completely change it
        ticket_edit = {
            "ticket_title": request.form.get("ticket_title"),
            "ticket_description": request.form.get(
                                        "ticket_description"),
            "ticket_status": "open",
            "category_name": request.form.get("category_name"),
            "project_name": request.form.get("project_name"),
            "created_by": session["user"],
            "assigned_to": request.form.get("assigned_to")
        }
        mongo.db.ticket.replace_one(
                            {"_id": ObjectId(ticket_id)}, ticket_edit)

        flash("Ticket updated Successfully")
        return redirect(url_for(
                            "dashboard", user_name=session["user"]))

    ticket = mongo.db.ticket.find_one({"_id": ObjectId(ticket_id)})
    ticketid = ticket["_id"]
    # Get categories from DB to selection on the render template
    categories = list(mongo.db.category.find().sort(
                                                "category_name", 1))
    # Get project to link to the ticket
    projects = list(mongo.db.project.find(
        {"user_name": session["user"]}).sort("project_name", 1))
    proj_users = list(mongo.db.project.find(
        {"project_name": ticket["project_name"]}).sort("user_name")
    )

    return render_template(
        "edit_ticket.html", ticket_id=ticketid,
        categories=categories, projects=projects, ticket=ticket,
        proj_users=proj_users)


@app.route("/documentation")
def documentation():
    return render_template("documentation.html")


# App route to Logout
@app.route("/logout")
def logout():
    # remove user from session cookies and return to home
    flash("You have been logged out")
    session.pop("user")
    session.pop("category")
    session.pop("user_city")
    session.pop("user_country")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
