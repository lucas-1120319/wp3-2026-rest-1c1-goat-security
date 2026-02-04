from flask import Blueprint, render_template, session
student_bp = Blueprint("student", __name__, url_prefix="/student")

@student_bp.route("/profile")
def dashboard():

    return render_template("profile.html")

