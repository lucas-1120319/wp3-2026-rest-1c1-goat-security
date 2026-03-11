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
    learning_goals = app.students.get_learning_goals(subject_id)
    learning_title = app.students.get_learning_goals_title(subject_id)

    learning_goals = [dict(row) for row in learning_goals]
    student_id = session["id"]

    for learning_goal in learning_goals:
        learning_goal["result"] = app.students.get_learning_goals_number_of_results(learning_goal["id"], student_id)
        learning_goal["keywords"] = app.students.learning_goal_keywords(learning_goal["id"])

    return render_template("learning_goal.html", learning_goals=learning_goals, learning_title=learning_title, subject_id=subject_id)

@student_bp.route("/subject/learning_goals/filter_average")
def filter_average():
    student_id = session["id"]
    try:
        average = float(request.args.get("average", 0))
    except ValueError:
        average = 0
    filter_keywords = request.args.get("filter_keywords")

    subject_id = int(request.args.get("subject_id"))
    learning_goals = app.students.get_learning_goals_filter_keywords(subject_id, filter_keywords)
    learning_goals = [dict(row) for row in learning_goals]

    for goal in learning_goals:
        goal["result"] = app.students.get_learning_goals_number_of_results(goal["id"], student_id)
        keywords = app.students.learning_goal_keywords(goal["id"])
        keywords_list = [{"name": k[0]} for k in keywords]

        goal["keywords"] = keywords_list
    return jsonify(learning_goals)


@student_bp.route("/subject/learning_goals/<int:snapshot_id>/result", methods=["GET"])
def results(snapshot_id):
    """ Get exam results per snapshot_id. """
    student_id = session["id"]
    scores = app.students.get_snapshot(snapshot_id, student_id)
    score_title = app.students.get_snapshot_title(snapshot_id, student_id)
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
        "labels": ["Onthouden", "Begrijpen", "Toepassen", "Analyseren"],
        "kunnen": kunnen,
        "kennen": kennen,
        "toepassen": confidence,
        # "analyseren": [kunnen[3], kennen[3], confidence[3]],
    })

@student_bp.route("/subject/learning_goals/<int:learning_goal_id>/examlist", methods=["GET"])
def exam_list(learning_goal_id):
    """ Get exam result data in a table setting. """
    student_id = session["id"]
    learning_goal = app.students.get_learning_goal(learning_goal_id)
    learning_goal_title  = learning_goal["title"]
    subject_name  = learning_goal["subject_name"]

    scores = app.students.get_exam_list(learning_goal_id, student_id)

    keywords = app.students.learning_goal_keywords(learning_goal_id)

    return render_template("examlist.html", scores=scores, learning_goal_id=learning_goal_id, keywords=keywords, learning_goal_title=learning_goal_title, subject_name=subject_name)

@student_bp.route("/all_snapshot_average/<int:learning_goal_id>", methods=["GET"])
def all_snapshot_average(learning_goal_id):
    student_id = session["id"]
    scores = app.students.get_result_per_snapshot(learning_goal_id, student_id)
    # Extract data into separate lists
    onthouden = []
    begrijpen = []
    toepassen = []
    analyseren = []

    for score in scores:
        if score["level"] == "Onthouden":
            onthouden.append(score["average"])
        elif score["level"] == "Begrijpen":
            begrijpen.append(score["average"])
        elif score["level"] == "Toepassen":
            toepassen.append(score["average"])
        elif score["level"] == "Analyseren":
            analyseren.append(score["average"])


    def avg(values):
        return round(sum(values) / len(values), 2) if values else 0


    return jsonify({
        "onthouden": avg(onthouden),
        "begrijpen": avg(begrijpen),
        "toepassen": avg(toepassen),
        "analyseren": avg(analyseren),
    })

@student_bp.route("/learningGoals_data/<int:learning_goal_id>", methods=["GET"])
def learningGoals_data(learning_goal_id):
    student_id = session["id"]
    scores = app.students.get_result_per_snapshot(learning_goal_id, student_id)
    # Extract data into separate lists
    labels = sorted(set(score["snap_date"] for score in scores))
    average = [score["average"] for score in scores]
    onthouden_average = []
    begrijpen_average = []
    toepassen_average = []
    analyseren_average = []
    for score in scores:
        if score["level"] == "Onthouden":
            onthouden_average.append(score["average"])
        if score["level"] == "Begrijpen":
            begrijpen_average.append(score["average"])
        if score["level"] == "Toepassen":
            toepassen_average.append(score["average"])
        if score["level"] == "Analyseren":
            analyseren_average.append(score["average"])

    return jsonify({
        "labels": labels,
        "onthouden": onthouden_average,
        "begrijpen": begrijpen_average,
        "toepassen": toepassen_average,
        "analyseren": analyseren_average,

    })
@student_bp.route("/learningGoals")
def learningGoals():
    return render_template("learningGoals.html")

