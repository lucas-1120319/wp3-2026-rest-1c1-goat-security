from flask import Blueprint, render_template, session
teacher_bp = Blueprint("teacher", __name__, url_prefix="/teacher")

def inject_role():
    return {'role': 'teacher'}

@teacher_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@teacher_bp.route("/profile", methods=["GET", "POST"])
def profile():
    user_id = 6
    if request.method == "POST":
        form_data = request.form.to_dict()
        app.teacher.update_profile(user_id, form_data)

    user = app.students.get_all_teacher_user_info(user_id)
    return render_template("profile.html", user=user)

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