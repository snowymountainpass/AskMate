from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

import data_manager
from sample_data import (
    read_all_entries,
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
    entries = read_all_entries()
    return render_template("index.html", entries=entries)


@app.route("/entry/<int:id>", methods=["GET"])
def get_entry(id):
    entry = data_manager.get_question_at_id(id)
    print(entry)
    print(type(entry))
    try:
        answers = data_manager.get_answers_for_question(id)
        print(answers)

    except TypeError:
        print("hahahaha i crashed stuff @ accessing an entry")
        answers = None

    if not answers:

        return render_template("entry.html", entry=entry)
    else:

        return render_template("entry.html", entry=entry, answers=answers)


@app.route("/enter-edit/<int:id>", methods=["GET"])
def editting(id):
    entry = read_entry(id)
    return render_template("edit_question.html", id=id, entry=entry)


@app.route("/edit/<int:id>/", methods=["POST"])
def edit_entry(id):
    entry = read_entry(id)
    # title = entry["title"] if entry["id"] == str(id) else ""
    message = request.form.get("message")

    if change_entry(id, message):
        flash("Question successfully edited")
        return redirect(url_for("get_entry", id=id))

    flash("Edit was not saved")
    return redirect(url_for("get_entry", id=id))


@app.route("/post-question", methods=["GET"])
def enter_question():
    return render_template("post_question.html")


@app.route("/add", methods=["POST"])
def adding():
    title = request.form.get("title")
    message = request.form.get("message")
    id = insert_entry(title, message)

    if bool(id):
        flash("Entry added")
        return redirect(url_for("get_entry", id=id))

    flash("Entry not added")
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
    upvote_entry(id)
    return redirect(url_for("get_entry", id=id))


@app.route("/upvote-answer/<int:id>", methods=["GET", "POST"])
def upvote_answer(id):
    question_id = upvote_answer_in_db(id)
    return redirect(url_for("get_entry", id=question_id))


if __name__ == "__main__":
    app.run(debug=True)
