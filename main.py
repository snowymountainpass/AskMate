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


@app.route("/")
def index():
    criterion = request.args.get("criterion", "id")
    direction = request.args.get("direction", "asc")
    entries = data_manager.get_all_questions(criterion, direction)
    username = session.get("username")

    return render_template("index.html", entries=entries, username=username)


@app.route("/entry/<int:id>", methods=["GET", "POST"])
def get_entry(id):
    data_manager.increase_question_viewcount(id)
    user_id = session.get("user_id")
    username = session.get("username")
    entry = data_manager.get_question_at_id(id, username, user_id)

    try:
        answers = data_manager.get_answers_for_question(id, username, user_id)
        question_comments = data_manager.get_comments_for_question(id, username, user_id)
        answer_comments = data_manager.get_comments_for_answer(id, username, user_id)
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
    )


@app.route("/enter-edit/<int:id>", methods=["GET"])
def editting(id):
    entry = data_manager.get_question_at_id(id)
    return render_template("edit_question.html", id=id, entry=entry)


@app.route("/edit/<int:id>/", methods=["POST"])
def edit_entry(id):
    entry = data_manager.get_question_at_id(id)
    # title = entry["title"] if entry["id"] == str(id) else ""
    message = request.form.get("message")
    image = request.form.get("image")

    if data_manager.edit_question(id, message, image):
        flash("Question successfully edited")
        return redirect(url_for("get_entry", id=id))

    flash("Edit was not saved")
    return redirect(url_for("get_entry", id=id))


@app.route("/post-question", methods=["GET"])
def enter_question():
    return render_template("post_question.html")


@app.route("/add", methods=["POST"])
def add_new_question():
    title = request.form.get("title")
    message = request.form.get("message")
    savepath = os.path.join(app.config.get("UPLOAD_FOLDER"), "no-image-available.png")
    user_id = session.get("user_id")

    if "image" in request.files:
        image = request.files.get("image")
        savepath = os.path.join(app.config.get("UPLOAD_FOLDER"), image.filename)
        image.save(savepath)

    id_row = data_manager.inject_new_question(title, message, savepath,user_id)
    for row in id_row:
        id = row["id"]

    if id_row:
        flash("Success !")
        return redirect(url_for("get_entry", id=id))

    flash("Entry not added")
    return redirect(url_for("index"))


@app.route("/entry/<int:id>/delete")
def delete_question(id):
    data_manager.delete_question(id)
    return redirect(url_for("index"))


@app.route("/add-answer/question-<int:id_question>", methods=["GET", "POST"])
def add_answer(id_question):
    if request.method == "GET":
        return render_template("post_answer.html", id=id_question)
    elif request.method == "POST":
        message = request.form.get("message")
        data_manager.add_answer_to_question(id_question, message)
        return redirect(url_for("get_entry", id=id_question))


@app.route("/delete-answer/<int:id_question>/<int:id_answer>", methods=["GET", "POST"])
def delete_answer(id_answer, id_question):
    data_manager.delete_answer_to_question(id_answer)
    return redirect(url_for("get_entry", id=id_question))


@app.route("/edit-answer/question-<int:id_question>/answer-<int:id_answer>",
           methods=["GET", "POST"], )
def edit_answer(id_answer, id_question):
    old_message = data_manager.get_message_from_answer(id_answer)
    old_message = old_message[0].get("message")

    if request.method == "GET":
        return render_template("post_answer.html", id=id_question, message=old_message)
    elif request.method == "POST":
        new_message = request.form.get("message")
        data_manager.edit_answer_to_question(id_answer, old_message, new_message)
        return redirect(url_for("get_entry", id=id_question))


@app.route("/add-a-comment/<int:id_question>/<int:id_answer>", methods=["GET", "POST"])
def add_comment(id_answer, id_question):
    if request.method == "GET":
        return render_template("post_comment.html", id=id_answer)
    elif request.method == "POST":
        comment_message = request.form.get("message")
        data_manager.add_comment_to_answer(id_answer, id_question, comment_message)
        return redirect(url_for("get_entry", id=id_question))


@app.route("/upvote-question/<int:id>", methods=["POST"])
def upvote_question(id):
    data_manager.upvote_question(id)

    return redirect(url_for("get_entry", id=id))


@app.route("/downvote-question/<int:id>", methods=["GET", "POST"])
def downvote_question(id):
    data_manager.downvote_question(id)

    return redirect(url_for("get_entry", id=id))


@app.route("/upvote-answer/<int:id>-<int:q_id>", methods=["GET", "POST"])
def upvote_answer(id, q_id):
    data_manager.upvote_answer(id)

    return redirect(url_for("get_entry", id=q_id))


@app.route("/downvote-answer/<int:id>-<int:q_id>", methods=["GET", "POST"])
def downvote_answer(id, q_id):
    data_manager.downvote_answer(id)

    return redirect(url_for("get_entry", id=q_id))


@app.route("/entry/<int:id>/comment", methods=["GET", "POST"])
def add_comment_question(id):
    if request.method == "POST":
        comment_message = request.form.get("message")
        data_manager.inject_question_comment(id, comment_message)

        return redirect(url_for("get_entry", id=id))

    return render_template("post_comment.html", id=id)


@app.route("/edit-comment/<int:id>-<int:q_id>", methods=["GET", "POST"])
def edit_comment_question(id, q_id):
    this_comment = data_manager.get_comment(id)
    print(this_comment)

    if request.method == "POST":
        print(id)
        comment_message = request.form.get("message")
        print(id)
        print(comment_message)
        data_manager.edit_comment(id, comment_message)

        return redirect(url_for("get_entry", id=q_id))
    return render_template("edit_comment.html", id=id, comments=this_comment)


@app.route("/entry/<int:id>-<int:q_id>/delete", methods=["GET", "POST"])
def delete_comment_question(id, q_id):
    data_manager.delete_comment(id)
    return redirect(url_for("get_entry", id=q_id))


@app.route("/users", methods=["GET"])
def show_users():
    entries = data_manager.show_users()
    return render_template("users.html", entries=entries)


@app.route("/register_user", methods=["GET", "POST"])
def register_user():
    if request.method == "POST":
        username = request.form.get("user")
        password = request.form.get("pass")
        data_manager.register_new_user(username, password)
        return redirect(url_for('index'))

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


@app.route("/user/user_name")
def show_user_details():
    user_id = session.get("user_id")
    user_name = session.get("username")
    user_details = data_manager.get_user_details(user_id)
    return render_template("user_details.html", username=user_name, user_details=user_details)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
