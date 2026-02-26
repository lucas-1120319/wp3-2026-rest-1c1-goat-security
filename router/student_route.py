from flask import request, Blueprint, render_template, current_app as app, session, jsonify

student_bp = Blueprint("student", __name__, url_prefix="/student")

@student_bp.context_processor
def inject_role():
    user_id = session["id"]
    if user_id:
        user = app.students.get_all_student_user_info(user_id)
        return {'role': 'student',
                'username': user['first_name'],
                'user_id': user['user_id']
                }
    return {}


@student_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@student_bp.route("/profile", methods=["GET", "POST"])
def profile():
    """ Get student profile. """
    user_id = session["id"]
    if request.method == "POST":
        form_data = request.form.to_dict()
        app.students.update_profile(user_id, form_data)

    user = app.students.get_all_student_user_info(user_id)
    return render_template("profile.html", user=user)


@student_bp.route("/subjects")
def subjects():
    class_id = session["student_group"]
    subjects = app.students.get_all_subjects_students(class_id)
    print(subjects) #["id"] and ["name"] of the subjects
    return render_template("subjects.html", subjects=subjects)


@student_bp.route("/subject/learning_goals/<int:subject_id>", methods=["GET"])
def subject_learning_goals(subject_id):
    """ Get data of specifiek subject. """
    # subject_id = 1 #
    learning_goals = app.students.get_learning_goals(subject_id)
    learning_title = app.students.get_learning_goals_title(subject_id)
    return render_template("learning_goal.html", learning_goals=learning_goals, learning_title=learning_title)


# @student_bp.route("/subject/learning_goals/<int:learning_goal_id>/result", methods=["GET"])
# def subject_score(learning_goal_id):
#     """ Get exam result data in a table setting. """
#     student_id = session["id"]
#     scores = app.students.get_snapshot_by_learning_goal_id(learning_goal_id, student_id)
#     print('student_id: ',student_id)
#     return render_template("score.html", scores=scores)

@student_bp.route("/subject/learning_goals/<int:snapshot_id>/result", methods=["GET"])
def results(snapshot_id):
    """ Get exam results per snapshot_id. """
    student_id = session["id"]
    scores = app.students.get_snapshot(snapshot_id, student_id)
    score_title = app.students.get_snapshot_title(snapshot_id, student_id)
    print('student_id: ',student_id)
    return render_template("score.html", scores=scores, score_title=score_title)


@student_bp.route("/data/<int:snapshot_id>", methods=["GET"])
def data(snapshot_id):
    student_id = session["id"]
    scores = app.students.get_snapshot(snapshot_id, student_id)
    kunnen = [score['tax_kunnen'] for score in scores]
    kennen = [score['tax_kennen'] for score in scores]
    confidence = [score['tax_confidence'] for score in scores]
    date = [score['snap_at'] for score in scores]

    return jsonify({
        "labels": ['Onthouden', 'begrijpen', 'toepassen', 'analyseren'],
        "onthouden": kunnen,
        "begrijpen": kennen,
        "toepassen": confidence,
        # "analyseren": [kunnen[3], kennen[3], confidence[3]],
    })

@student_bp.route("/subject/learning_goals/<int:learning_goal_id>/examlist", methods=["GET"])
def exam_list(learning_goal_id):
    """ Get exam result data in a table setting. """
    student_id = session["id"]
    scores = app.students.get_exam_list(learning_goal_id, student_id)
    return render_template("examlist.html", scores=scores)

@student_bp.route("/learningGoals")
def learningGoals():
    return render_template("learningGoals.html")

