from datetime import datetime
import os
from flask import Flask
from data.database import Database

from models.students import Student
from models.teachers import Teacher
from models.user import User
from models.seed import Seed

from models.data_converter import data_converter

app = Flask(__name__)
app.secret_key = "super_duper_secret_key"

BASE_DIR = os.path.dirname(__file__)
DB_PATH = os.path.join(BASE_DIR, "data", "app.db")

_db = Database(DB_PATH)
app.students = Student(DB_PATH)
app.teachers = Teacher(DB_PATH)
app.seeder = Seed(DB_PATH)
users = User(DB_PATH)
json_data = os.path.join(BASE_DIR, "data", "data-sample.json")
data_converter = data_converter(DB_PATH, json_data)

# Seeding 2 users assigned to teacher
app.seeder.create_row_teacher()
app.seeder.create_student_group()
app.seeder.add_students_in_group()
app.seeder.assign_teacher_group()
app.seeder.assign_class_subjects()

if __name__ == "__main__":
    app.run(debug=True, port=5001)
