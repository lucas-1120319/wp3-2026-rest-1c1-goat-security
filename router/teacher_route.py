from flask import request, Blueprint, render_template, current_app as app, session, jsonify

teacher_bp = Blueprint("teacher", __name__, url_prefix="/teacher")

@teacher_bp.context_processor
def inject_role():
    return {'role': 'teacher'}

@teacher_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@teacher_bp.route("/profile", methods=["GET", "POST"])
def profile():
    user_id = session["id"]

    if request.method == "POST":
        form_data = request.form.to_dict()
        app.teachers.update_profile(user_id, form_data)

    user = app.teachers.get_all_teacher_user_info(user_id)
    return render_template("profile.html", user=user)

@teacher_bp.route("/subjects")
def subjects():
    """ Show list of subjects"""
    subject_list = app.teachers.get_all_subjects()
    return render_template("subjects.html", subject_list=subject_list)

@teacher_bp.route("/subjects/<int:subject_id>", methods=["GET"])
def select_subject(subject_id):
    """ Select a single subject """
    subject_name = app.teachers.get_single_subject(subject_id)
    learning_goals = app.teachers.get_all_learning_goals(subject_id)
    return render_template("single_subject.html", learning_goals=learning_goals, subject_name=subject_name)


@teacher_bp.route("/subject/learningGoals")
def subject_learningGoals():
    return render_template("subject_learningGoals.html")

@teacher_bp.route("/learningGoals")
def learningGoals():
    return render_template("learningGoals.html")

@teacher_bp.route("/studentGroups")
def studentGroups():
    """ Get all studentGroups """
    studentGroups = app.teachers.get_all_studentGroups()
    return render_template("studentGroup.html", studentGroups=studentGroups)

@teacher_bp.route("/studentGroup")
def studentGroup():
    """ Get a single studentGroup """
    teacher_id = session["teacher_id"]
    studentGroups = app.teachers.get_studentGroups(teacher_id)
    return render_template("studentGroup.html", studentGroups=studentGroups)


@teacher_bp.route("/studentGroup/<string:name>", methods=["GET"])
def select_studentGroup(name):
    """ Get a whole list of Students from a studentGroup """

    # [TEST] Calculator for now (To know if a student is doing good or is behind)
    def determine_status(avg):
        if avg is None:
            return "Geen data"
        elif avg < 0.5:
            return "Achterloopt"
        elif avg > 0.8:
            return "Uitblinker"
        else:
            return "Op schema"

    all_students_data = app.teachers.get_all_students_studentGroup(name)
    all_students = []

    for student in all_students_data:
        student = dict(student)
        student["status"] = determine_status(student["average"])
        all_students.append(student)

    return render_template("all_students.html", students=all_students, class_name=name)

@teacher_bp.route("/studentGroup/<string:name>/filter_status", methods=["GET"])
def filter_students_status(name):

    status_filter = request.args.get("status")

    def determine_status(avg):
        if avg is None:
            return "Geen data"
        elif avg < 0.5:
            return "Achterloopt"
        elif avg > 0.8:
            return "Uitblinker"
        else:
            return "Op schema"

    all_students_data = app.teachers.get_all_students_studentGroup(name)

    students = []

    for student in all_students_data:
        student = dict(student)
        avg = student["average"] or 0
        student_status = determine_status(avg)
        student["status"] = student_status

        if status_filter is None or student_status == status_filter:
            students.append(student)

    return jsonify(students)