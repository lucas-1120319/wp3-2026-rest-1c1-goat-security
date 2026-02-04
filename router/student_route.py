from flask import Blueprint, render_template, session
student_bp = Blueprint("student", __name__, url_prefix="/student")

@student_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@student_bp.route("/profile")
def profile():
    return render_template("profile.html")

@student_bp.route("/subjects")
def subjects():
    return render_template("subjects.html")

@student_bp.route("/subject/learningGoals")
def subject_learningGoals():
    return render_template("subject_learningGoals.html")

@student_bp.route("/learningGoals")
def learningGoals():
    return render_template("learningGoals.html")