from datetime import datetime
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from data.database import Database
from router.student_route import student_bp
from router.teacher_route import teacher_bp
from models.students import Student
from models.teachers import Teacher
from models.user import User
from models.seed import Seed

from models.data_converter import data_converter

app = Flask(__name__)
app.secret_key = "super_duper_secret_key"

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "data", "app.db")
app.register_blueprint(student_bp)
app.register_blueprint(teacher_bp)

_db = Database(DB_PATH)
app.students = Student(DB_PATH)
app.teachers = Teacher(DB_PATH)
app.seeder = Seed(DB_PATH)
app.users = User(DB_PATH)

@app.route("/")
def index():
    # counts = {
    #     "experts": users.count_all()[0],
    #     "organizations": organizations.count_all()[0],
    #     "studies": studies.count_all()[0],
    #     "enrollments": enrollments.count_all()[0],
    # }
    return render_template("login.html")

@app.route("/login")
def login():
    """Shows the login page"""
    return render_template("login.html")

@app.route("/register")
def register():
    """Shows the register page"""
    return render_template("register.html")

@app.route("/signin", methods=["POST"])
def signin():
    """Gets the form's data and logs in the user with the correct validation (NEEDS REVAMP)"""
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        print("Form data:", email, password)
        main_user = app.users.authenticate(email, password)

        if not main_user:
            return render_template(
                "login.html", error="Verkeerde email en of wachtwoord"
            )

        user_role = app.users.get_user_role(main_user["id"])

        session["id"] = main_user["id"]
        session["role"] = user_role["name"]

        print(user_role["name"], session["id"])

        print("SUCCESSFULLY LOGGED IN")

        # -- Can be used later to redirect certain roles to different pages [TEST] --
        if session["role"] == "teacher":
            session["teacher_id"] = app.teachers.get_teacher_id(session["id"])['id']

            return redirect(url_for("teacher.profile"))
        elif session["role"] == "student":
            session["student_group"] = app.students.get_student_class(session["id"])["name"]
            return redirect(url_for("student.profile"))
        # --

        return redirect(url_for("index"))


@app.route("/signup", methods=["POST"])
def signup():
    """Gets the form's data and registers the user with correct validation (NEEDS REVAMP)"""
    if g.current_user:
        return redirect(url_for("index"))

    if request.method == "POST":
        role = "student"  # request.form["role"] # HARD coded for nu
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirmpassword"]
        print("Form data:", email, password, confirm_password)
        existing_user = False #users.authenticate_register(email)

        print(existing_user)

        if existing_user:
            return render_template("register.html", error="Gebruiker bestaat al")

        if password != confirm_password:
            return render_template(
                "register.html", error="Wachtwoorden zijn niet gelijk aan elkaar"
            )

        new_user = False #users.create_new_user(email, password, role)
        print("New User created:", new_user)

        return redirect(url_for("index")) #Can later lead to creating your profile


@app.route("/signout")
def signout():
    """logs the current user out and clears the session"""
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True, port=5001)
