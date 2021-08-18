from flask import Flask, render_template, request, redirect, url_for, flash, session
from dotenv import load_dotenv
import os

import data_manager




load_dotenv()
app = Flask(__name__)
app.secret_key = "alskua ekjegu keucyf iqek,rvgkfarg rkjegkjqaved"
app.config["UPLOAD_FOLDER"] = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    "static",
    "images",
)


users = {"alex": "1234", "laura": "2468", "cipi": "1357"}

@app.route("/")
def index():
    criterion = request.args.get("criterion", "id")
    direction = request.args.get("direction", "asc")
    entries = data_manager.get_all_questions(criterion, direction)
    username = session.get("username")
    user_id = session.get("user_id")
    print(username)
    return render_template("index.html", entries=entries, username=username)

# @app.route("/register", methods=["GET", "POST"])
# def register():
#     global users
#
#     if request.method == "POST":
#         users[request.form.get("user")] = request.form.get("pass")
#         session["user"] = request.form.get("user")
#
#         return redirect(url_for("index"))
#
#     return render_template("register.html")


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     global users
#
#     if request.method == "POST":
#         u = request.form.get("user")
#         p = request.form.get("pass")
#
#         if u in users.keys() and users[u] == p:
#             session["user"] = u
#
#         return redirect(url_for("index"))
#
#     return render_template("login.html")





@app.route("/entry/<int:question_id>", methods=["GET", "POST"])
def get_entry(question_id):
    data_manager.increase_question_viewcount(question_id)
    entry = data_manager.get_question_at_id(question_id)
    username = session.get("username")
    user_id = session.get("user_id")
    print(username)
    print(user_id)

    try:
        answers = data_manager.get_answers_for_question(question_id)
        question_comments = data_manager.get_comments_for_question(question_id)
        answer_comments = data_manager.get_comments_for_answer(question_id)
        print(answer_comments)
        print(question_comments)

    except TypeError:
        print("hahahaha i crashed stuff @ accessing an entry")
        answers = None
        question_comments = None
        answer_comments = None

    return render_template(
        "entry.html",
        entry=entry,
        answers=answers,
        question_comments=question_comments,
        answer_comments=answer_comments,
        username=username,
        user_id=user_id,
    )


# @app.route('/entry/question-<int:id_question>/answer-<int:id_answer>/comments', methods=["GET", "POST"])
# def get_comments(id_question, id_answer):
#     headers = ["Answer", "Posted at", "Number of votes", "Answer ID"]
#     entry = data_manager.get_question_by_id(id_question)
#     entry_answers = data_manager.get_answers_by_question(id_question)
#
#     if request.method == "GET":
#         if entry_answers is None:
#             return render_template('entry.html', entry=entry, headers=headers)
#         else:
#             return render_template('entry.html', entry=entry, answers=entry_answers, headers=headers)
#     elif request.method == "POST":
#         comments = data_manager.get_comments_by_answer(id_answer, id_question)
#         print(comments)
#         return render_template('entry.html', entry=entry, answers=entry_answers, headers=headers, comments=comments)


@app.route("/enter-edit/<int:question_id>", methods=["GET"])
def editting(question_id):
    entry = data_manager.get_question_at_id(question_id)
    return render_template("edit_question.html", question_id=question_id, entry=entry)


@app.route("/edit/<int:question_id>/", methods=["POST"])
def edit_entry(question_id):
    entry = data_manager.get_question_at_id(question_id)
    # title = entry["title"] if entry["id"] == str(id) else ""
    message = request.form.get("message")
    image = request.form.get("image")

    if data_manager.edit_question(question_id, message, image):
        flash("Question successfully edited")
        return redirect(url_for("get_entry", question_id=question_id))

    flash("Edit was not saved")
    return redirect(url_for("get_entry", question_id=id))


@app.route("/post-question", methods=["GET"])
def enter_question():
    return render_template("post_question.html")


@app.route("/add", methods=["POST"])
def add_new_question():
    title = request.form.get("title")
    message = request.form.get("message")
    username = session.get("username")
    user_id = session.get("user_id")
    savepath = os.path.join(app.config.get("UPLOAD_FOLDER"), "no-image-available.png")

    if "image" in request.files:
        image = request.files.get("image")
        savepath = os.path.join(app.config.get("UPLOAD_FOLDER"), image.filename)
        image.save(savepath)
    else:
        image = "No image"

    id_row = data_manager.inject_new_question(title, message, savepath, username, user_id)
    for row in id_row:
        question_id = row["id"]

    if id_row:
        flash("Success !")
        return redirect(url_for("get_entry", question_id=question_id))

    flash("Entry not added")
    return redirect(url_for("index"))


@app.route("/entry/<int:question_id>/delete")
def delete_question(question_id):
    data_manager.delete_question(question_id)
    return redirect(url_for("index"))


@app.route("/add-answer/question-<int:question_id>", methods=["GET", "POST"])
def add_answer(question_id):

    if request.method == "GET":
        return render_template("post_answer.html", question_id=question_id)
    elif request.method == "POST":
        message = request.form.get("message")
        username = session.get("username")
        user_id = session.get("user_id")
        data_manager.add_answer_to_question(question_id, message, username, user_id)
        return redirect(url_for("get_entry", question_id=question_id))


@app.route("/delete-answer/<int:answer_id>/<int:question_id>", methods=["GET", "POST"])
def delete_answer(answer_id, question_id):
    data_manager.delete_answer_to_question(answer_id)
    return redirect(url_for("get_entry", question_id=question_id))


@app.route(
    "/edit-answer/question-<int:question_id>/answer-<int:answer_id>",
    methods=["GET", "POST"],
)
def edit_answer(answer_id, question_id):
    old_message = data_manager.get_message_from_answer(answer_id)
    old_message = old_message[0].get("message")

    if request.method == "GET":
        return render_template("post_answer.html", question_id=question_id, message=old_message)
    elif request.method == "POST":
        new_message = request.form.get("message")
        data_manager.edit_answer_to_question(answer_id, old_message, new_message)
        return redirect(url_for("get_entry", question_id=question_id))


@app.route("/add-a-comment/<int:question_id>/<int:answer_id>", methods=["GET", "POST"])
def add_comment(answer_id, question_id):
    if request.method == "GET":
        return render_template("post_comment.html", answer_id=answer_id)
    elif request.method == "POST":
        comment_message = request.form.get("message")
        username = session.get("username")
        user_id = session.get("user_id")

        data_manager.add_comment_to_answer(answer_id, question_id, comment_message, username, user_id)
        return redirect(url_for("get_entry", question_id=question_id))


@app.route("/upvote-question/<int:question_id>", methods=["POST"])
def upvote_question(question_id):
    data_manager.upvote_question(question_id)

    return redirect(url_for("get_entry", question_id=question_id))


@app.route("/downvote-question/<int:question_id>", methods=["GET", "POST"])
def downvote_question(question_id):
    data_manager.downvote_question(question_id)

    return redirect(url_for("get_entry", question_id=question_id))


@app.route("/upvote-answer/<int:answer_id>-<int:question_id>", methods=["GET", "POST"])
def upvote_answer(answer_id, question_id):
    data_manager.upvote_answer(answer_id)

    return redirect(url_for("get_entry", question_id=question_id))


@app.route("/downvote-answer/<int:answer_id>-<int:question_id>", methods=["GET", "POST"])
def downvote_answer(answer_id, question_id):
    data_manager.downvote_answer(answer_id)

    return redirect(url_for("get_entry", question_id=question_id))


@app.route("/entry/<int:question_id>/comment", methods=["GET", "POST"])
def add_comment_question(question_id):
    if request.method == "POST":
        comment_message = request.form.get("message")
        username = session.get("username")
        user_id = session.get("user_id")

        data_manager.inject_question_comment(question_id, comment_message, username, user_id)

        return redirect(url_for("get_entry", question_id=question_id))

    return render_template("post_comment.html", question_id=question_id)


@app.route("/edit-comment/<int:comment_id>-<int:question_id>", methods=["GET", "POST"])
def edit_comment(comment_id, question_id):
    this_comment = data_manager.get_comment(comment_id)

    if request.method == "POST":
        comment_message = request.form.get("message")
        data_manager.edit_comment(comment_id, comment_message)

        return redirect(url_for("get_entry", question_id=question_id))
    return render_template("edit_comment.html", comment_id=comment_id, comments=this_comment)


@app.route("/entry/<int:comment_id>-<int:question_id>/delete", methods=["GET", "POST"])
def delete_comment_question(comment_id, question_id):
    data_manager.delete_comment_question(comment_id, question_id)
    return redirect(url_for("get_entry", question_id=question_id))


@app.route("/entry/<int:comment_id>-<int:answer_id>-<int:question_id>/delete", methods=["GET", "POST"])
def delete_comment_answer(comment_id, answer_id, question_id):
    data_manager.delete_comment_answer(comment_id, answer_id, question_id)
    return redirect(url_for("get_entry", question_id=question_id))


@app.route("/users", methods=["GET"])
def show_users():
    entries = data_manager.show_users()
    return render_template("users.html", entries=entries)


@app.route("/register_user", methods=["GET", "POST"])
def register_user():
    if request.method == "POST":
        username = request.form.get("user")
        password = request.form.get("pass")
        if not data_manager.check_existing_username(username):
            data_manager.register_new_user(username, password)
            return redirect(url_for('index'))
        else:
            flash("Username is already taken !")
            return redirect(url_for("register_user"))



    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login_user():
    if request.method == "POST":
        username = request.form.get("user")
        password = request.form.get("pass")
        for element in data_manager.login(username):
            db_password = element["password"]

        if password == db_password:
            # session["user_id"] = data_manager.user_id_return(username, password)
            for userid in data_manager.user_id_return(username, password):
                db_user_id = userid["user_id"]
            session["user_id"] = db_user_id
            session["username"] = username
            return redirect(url_for('index'))
        else:
            flash("Invalid credentials !")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
