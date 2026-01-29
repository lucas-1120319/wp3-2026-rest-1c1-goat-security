from datetime import datetime
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from data.database import Database

from models.students import Student
from models.teachers import Teacher

app = Flask(__name__)
app.secret_key = "super_duper_secret_key"

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "data", "app.db")

_db = Database(DB_PATH)
students = Student(DB_PATH)
teachers = Teacher(DB_PATH)

@app.route("/")
def index():
    # counts = {
    #     "experts": users.count_all()[0],
    #     "organizations": organizations.count_all()[0],
    #     "studies": studies.count_all()[0],
    #     "enrollments": enrollments.count_all()[0],
    # }
    return render_template("index.html")

@app.route("/student-dashboard")
def student_dashboard():
    return render_template("student-dashboard.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
