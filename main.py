from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

import data_manager
from sample_data import (
    insert_entry,
    read_entry,
    read_answers,
    HEADERS_QUESTIONS,
    change_entry,
    insert_answer,
    upvote_entry,
    upvote_answer_in_db,
)
load_dotenv()
app = Flask(__name__)
app.secret_key = "alskua ekjegu keucyf iqek,rvgkfarg rkjegkjqaved"


@app.route("/")
def index():
    entries = data_manager.get_all_questions()
    return render_template("index.html", entries=entries)


@app.route("/entry/<int:id>", methods=["GET"])
def get_entry(id):
    data_manager.increase_question_viewcount(id)
    entry = data_manager.get_question_at_id(id)
    try:
        answers = data_manager.get_answers_for_question(id)

    except TypeError:
        print("hahahaha i crashed stuff @ accessing an entry")
        answers = None

    if not answers:

        return render_template("entry.html", entry=entry)
    else:

        return render_template("entry.html", entry=entry, answers=answers)


@app.route("/enter-edit/<int:id>", methods=["GET"])
def editting(id):
    entry = data_manager.get_question_at_id(id)
    return render_template("edit_question.html", id=id, entry=entry)


@app.route("/edit/<int:id>/", methods=["POST"])
def edit_entry(id):
    entry = data_manager.get_question_at_id(id)
    # title = entry["title"] if entry["id"] == str(id) else ""
    message = request.form.get("message")

    if data_manager.edit_question(id, message):
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
    id_row = data_manager.inject_new_question(title, message)
    for row in id_row:
        id = row['id']


    if id_row:
        flash("Entry added")
        return redirect(url_for("get_entry", id=id))

    flash("Entry not added")
    return redirect(url_for("index"))


@app.route("/entry/<int:id>/delete")
def delete_question(id):
    data_manager.delete_question(id)
    return redirect(url_for("index"))

@app.route("/post-answer/<int:id>", methods=["GET"])
def enter_answer(id):
    return render_template("post_answer.html", id=id)


@app.route("/add-answer/<int:id>", methods=["POST"])
def add_answer(id):
    message = request.form.get("message")

    if insert_answer(id, message):
        flash("Answer added")
        return redirect(url_for("get_entry", id=id))

    flash("Answer not added")
    return redirect(url_for("get_entry", id=id))


@app.route("/upvote-question/<int:id>", methods=["POST"])
def upvote_question(id):
    data_manager.upvote_question(id)

    return redirect(url_for("get_entry", id=id))


@app.route("/upvote-answer/<int:id>", methods=["GET", "POST"])
def upvote_answer(id):
    data_manager.upvote_answer(id)
    get_id = data_manager.pass_question_id(id)
    pass_id = 0
    for row in get_id:
        pass_id = row['id']

    return redirect(url_for("get_entry", id=pass_id))



if __name__ == "__main__":
    app.run(debug=True)
