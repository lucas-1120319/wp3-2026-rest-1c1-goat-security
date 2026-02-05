from flask import Blueprint, render_template, session
teacher_bp = Blueprint("teacher", __name__, url_prefix="/teacher")

def inject_role():
    return {'role': 'teacher'}

@teacher_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@teacher_bp.route("/profile")
def profile():
    return render_template("profile.html")

@teacher_bp.route("/subjects")
def subjects():
    return render_template("subjects.html")

@teacher_bp.route("/subject/learningGoals")
def subject_learningGoals():
    return render_template("subject_learningGoals.html")

@teacher_bp.route("/learningGoals")
def learningGoals():
    return render_template("learningGoals.html")

@teacher_bp.route("/studentGroups")
def studentGroups ():
    return render_template("studentGroups.html")