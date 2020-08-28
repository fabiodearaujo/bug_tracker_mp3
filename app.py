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
                    flash("Welcome, {}".format(existing_user["user_name"]))
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
    return render_template("edit_user.html", user=user)


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