from datetime import datetime
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from data.database import Database
from models.students import Student
from models.teachers_seed import Teacher
from models.data_converter import data_converter

app = Flask(__name__)
app.secret_key = "super_duper_secret_key"

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "data", "app.db")

_db = Database(DB_PATH)
students = Student(DB_PATH)
teachers = Teacher(DB_PATH)
json_data = os.path.join(BASE_DIR, "data", "data-sample.json")
# data_converter = data_converter(DB_PATH, json_data)


# Seeding 2 users assigned to teacher
teachers.create_row_teacher()

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
