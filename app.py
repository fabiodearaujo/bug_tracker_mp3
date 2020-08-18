import os
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

        register = {
            "user_name": request.form.get("user_name").lower(),
            "user_pass": generate_password_hash(request.form.get("user_pass")),
            "project_name": "",
            "user_category": "regular"
        }
        mongo.db.user.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("user_name").lower()
        flash("Registration Successful")
        return redirect(url_for("dashboard", user_name=session["user"]))
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
                    session["user"] = request.form.get("user_name").lower()
                    flash("Welcome, {}".format(request.form.get("user_name")))
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
    user_name = mongo.db.user.find_one(
        {"user_name": session["user"]})["user_name"]
    return render_template("dashboard.html", user_name=user_name)


@app.route("/get_users", methods=["GET", "POST"])
def get_users():
    users = mongo.db.user.find()
    return render_template("users.html", user_result=users)


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