from flask import request, Blueprint, render_template,current_app as app,  session
import seaborn as sns
import matplotlib.pyplot as plt

student_bp = Blueprint("student", __name__, url_prefix="/student")

@student_bp.context_processor
def inject_role():
    return {'role': 'student'}


@student_bp.route("/dashboard")
def dashboard():

    return render_template("dashboard.html")


@student_bp.route("/profile", methods=["GET", "POST"])
def profile():
    """ Get student profile """
    user_id = session["id"]
    if request.method == "POST":
        form_data = request.form.to_dict()
        app.students.update_profile(user_id, form_data)

    user = app.students.get_all_student_user_info(user_id)
    return render_template("profile.html", user=user)


@student_bp.route("/subjects")
def subjects():
    class_id = session["student_group"]
    return render_template("subjects.html")


@student_bp.route("/subject/learning_goals")
def subject_learning_goals():
    """ Get data of specifiek subject. """
    subject_id = 2 #
    learning_goals = app.students.get_learning_goals(subject_id)
    learning_title = app.students.get_learning_goals_title(subject_id)
    return render_template("learning_goal.html", learning_goals=learning_goals, learning_title=learning_title)


@student_bp.route("/subject/learning_goals/<int:subject_id>/result", methods=["GET"])
def subject_score(subject_id):
    """ Get exam result data in a table setting. """
    student_id = 2
    snapshot_id = subject_id
    scores = app.students.get_snapshot_by_id(snapshot_id, student_id)
    print('subject_id: ',subject_id)
    print('student_id: ',student_id)
    return render_template("score.html", scores=scores)


@student_bp.route("/learningGoals")
def learningGoals():
    return render_template("learningGoals.html")