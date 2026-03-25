from flask import request, Blueprint, render_template, current_app as app, session, jsonify

teacher_bp = Blueprint("teacher", __name__, url_prefix="/teacher")

@teacher_bp.context_processor
def inject_role():
    user_id = session["id"]
    if user_id:
        user = app.teachers.get_all_user_info(user_id)
        return {'role': 'teacher',
                'username': user['first_name'],
                'user_id': user['user_id']
                }
    return {}

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

    studentGroups = app.teachers.get_all_studentGroups()
    studentGroups_data = []

    for group in studentGroups:
        group_data = dict(group)
        all_students_data = app.teachers.get_all_students_studentGroup(group["id"])
        group_data["student_count"] = len(all_students_data["students"])
        studentGroups_data.append(group_data)

    return render_template("subjects.html", subject_list=subject_list, studentGroups=studentGroups_data)

@teacher_bp.route("/subjects/<int:subject_id>", methods=["GET"])
def select_subject(subject_id):
    """ Select a single subject """
    subject_name = app.teachers.get_single_subject(subject_id)
    learning_goals = app.teachers.get_all_learning_goals(subject_id)
    groups = app.teachers.get_learning_goal_by_class(class_id='1', subject_id=subject_id)

    class_id = groups[0]['class_id'] if groups else 1
    learning_goal_id = groups[0]['learning_goal_id'] if groups else 1

    goals = {}
    for g in groups:
        goal = g['learning_goal']
        print(g["learning_goal_id"], g["learning_goal"])

        if goal not in goals:
            goals[goal] = {
                "labels": [],
                "data": []
            }

        goals[goal]["labels"].append(g["student_name"])
        goals[goal]["data"].append(g["average"])


    return render_template("single_subject.html",
                           learning_goals=learning_goals,
                           subject_name=subject_name,
                           subject_id=subject_id, groups=groups, class_id=class_id, goals=goals)


@teacher_bp.route("/subjects/<int:subject_id>/data", methods=["GET"])
def data(subject_id):
    groups = app.teachers.get_learning_goal_by_class(class_id='1', subject_id=subject_id)

    student_name = [group['student_name'] for group in groups]
    # kennen = [group['kennen'] for group in groups]
    # kunnen = [group['kunnen'] for group in groups]
    avg = [group['average'] for group in groups]
    learning_goal = [group["learning_goal"] for group in groups]

    return jsonify({
        "labels": student_name,
        "avg": avg,
        "learning_goal": learning_goal,
        # "kunnen": kunnen,
    })


@teacher_bp.route("/subjects/<int:subject_id>/selected", methods=["GET"])
def go_subject(subject_id):
    """ Select a single subject """
    subject_name = app.teachers.get_single_subject(subject_id)
    learning_goals = app.teachers.get_all_learning_goals(subject_id)
    return render_template("teacher-student_learning_goal.html", learning_goals=learning_goals, subject_name=subject_name)


@teacher_bp.route("/subject/learningGoals")
def subject_learningGoals():
    return render_template("subject_learningGoals.html")

@teacher_bp.route("/learningGoals")
def learningGoals():
    return render_template("learningGoals.html")

@teacher_bp.route("/studentGroups")
def studentGroups():
    """ Get all studentGroups """

    # There's probably a way to merge it with the other studentGroup function under
    # Will get to it later (When I have the time) :D

    studentGroups = app.teachers.get_all_studentGroups()
    studentGroups_data = []

    for group in studentGroups:
        group_data = dict(group)
        all_students_data = app.teachers.get_all_students_studentGroup(group["id"])
        group_data["student_count"] = len(all_students_data["students"])
        studentGroups_data.append(group_data)

    return render_template("studentGroup.html", studentGroups=studentGroups_data)

@teacher_bp.route("/studentGroup")
def studentGroup():
    """ Get a single studentGroup """

    # There's probably a way to merge it with the other studentGroups function above
    # Will get to it later (When I have the time) :D

    teacher_id = session["teacher_id"]
    studentGroups = app.teachers.get_studentGroups(teacher_id)
    studentGroups_data = []

    for group in studentGroups:
        group_data = dict(group)
        all_students_data = app.teachers.get_all_students_studentGroup(group["id"])
        group_data["student_count"] = len(all_students_data["students"])
        studentGroups_data.append(group_data)

    return render_template("studentGroup.html", studentGroups=studentGroups_data)


@teacher_bp.route("/studentdetail/<int:id>", methods=["GET"])
def studentDetail(id):
    """ Get details about a certain person """
    # [TEST] Can be expanded on later to make it multi-functional (So it can support Teachers/Students/etc)
    studentInfo = app.students.get_all_student_user_info(id)
    role = app.users.get_user_role(id)
    subjectdata = app.teachers.get_single_student_subject(id)
    return render_template("single_student.html", personInfo=studentInfo, personrole=role, subjects=subjectdata)

@teacher_bp.route("/studentdetail/subject/<int:subject_id>/learning-goals", methods=["GET"])
def get_student_subject_learning_goals(subject_id):
    learning_goals = app.students.get_learning_goals(subject_id)
    return {"success": True, "learning_goals": [dict(row) for row in learning_goals]}, 200

@teacher_bp.route("/studentdetail/<int:id>/learning-goal/<int:learning_goal_id>/results", methods=["GET"])
def get_student_learning_goal_results(id, learning_goal_id):
    results = app.students.get_result_per_snapshot(learning_goal_id, id)
    full_results = [dict(row) for row in results]
    grouped = {}

    for item in full_results:
        key = str(item["snapshot_id"]) + "_" + item["source_id"] + "_" + item["source_type"]

        if key not in grouped:
            grouped[key] = {
                "snapshot_id": item["snapshot_id"],
                "source_type": item["source_type"],
                "source_id": item["source_id"],
                "snap_date": item["snap_date"],
                "levels": []
            }

        grouped[key]["levels"].append({
            "level": item["level"],
            "tax_id": item["tax_id"],
            "average": item["average"]

        })

    snapshots = list(grouped.values())

    return {"success": True, "results": snapshots} , 200

@teacher_bp.route("/studentGroup/<string:name>", methods=["GET"])
def select_studentGroup(name):
    """ Get a whole list of Students from a studentGroup """

    # [TEST] Calculator for now (To know if a student is doing good or is behind)
    def determine_status(avg):
        if avg is None:
            return "Geen data"
        elif avg < 0.5:
            return "Onder"
        elif avg > 0.8:
            return "Uitblinker"
        else:
            return "Op schema"

    # all_students_data = app.teachers.get_all_students_studentGroup(name)
    all_students = []
    #
    # for student in all_students_data:
    #     student = dict(student)
    #     student["status"] = determine_status(student["average"])
    #     all_students.append(student)

    return render_template("all_students.html", students=all_students, class_name=name)

@teacher_bp.route("/studentGroup/<string:name>/filter_status", methods=["GET"])
def filter_students_status(name):

    status_filter = request.args.get("status")


    group_id = app.teachers.get_group_per_name(name)
    group_results = app.students.get_studentGroup_average_all_subjects(group_id)
    group_avg_dict = {
        row[0]: row[4]
        for row in group_results
    }
    all_students_data = app.teachers.get_all_students_studentGroup(group_id)
    student_group = []
    avg_margin = 0.1

    for student in all_students_data["students"]:
        has_above = False
        has_on = False
        has_below = False

        for subject in student["subjects"]:
            subject_avg = 0
            group_avg = 0

            for learning_goal in subject["learning_goals"]:
                subject_avg += learning_goal["avg"]
                learning_goal["group_avg"] = group_avg_dict.get(learning_goal["id"])
                group_avg += learning_goal["group_avg"]

            if len(subject["learning_goals"]) > 0:
                subject["student_avg"] = subject_avg / len(subject["learning_goals"])
                subject["group_avg"] = group_avg / len(subject["learning_goals"])
            else:
                subject["student_avg"] = 0
                subject["group_avg"] = 0

            if abs(subject["student_avg"] - subject["group_avg"]) <= avg_margin:
                has_on = True
            elif subject["student_avg"] > subject["group_avg"]:
                has_above = True
            else:
                has_below = True


        if status_filter == "boven" and has_above:
            student_group.append(student)

        elif status_filter == "op" and has_on:
            student_group.append(student)

        elif status_filter == "onder" and has_below:
            student_group.append(student)

        elif status_filter is None:
            student_group.append(student)

    return jsonify( {
    "class": all_students_data["class"],
    "students": student_group
})