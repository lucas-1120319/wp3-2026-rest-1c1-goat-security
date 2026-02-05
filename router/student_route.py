from flask import request, Blueprint, render_template,current_app as app,  session
student_bp = Blueprint("student", __name__, url_prefix="/student")

@student_bp.context_processor
def inject_role():
    return {'role': 'student'}


@student_bp.route("/dashboard")
def dashboard():

    return render_template("dashboard.html")


@student_bp.route("/profile", methods=["GET", "POST"])
def profile():
    user_id = 6
    if request.method == "POST":
        form_data = request.form.to_dict()
        app.students.update_profile(user_id, form_data)

    user = app.students.get_all_student_user_info(user_id)
    return render_template("profile.html", user=user)

@student_bp.route("/subjects")
def subjects():
    return render_template("subjects.html")

@student_bp.route("/subject/learningGoals")
def subject_learningGoals():
    return render_template("subject_learningGoals.html")

@student_bp.route("/learningGoals")
def learningGoals():
    return render_template("learningGoals.html")