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
    # entries = read_all_entries("sample_data/question.csv", HEADERS_QUESTIONS)
    # return render_template("index.html", entries=entries)
    entries = data_manager.get_all_questions()
    return render_template("index.html", entries=entries)


@app.route("/entry/<int:id>", methods=["GET"])
def get_entry(id):
    entry = read_entry(id)
    try:
        answer_all = read_answers(id)
        answer = []
        for element in answer_all:
            answer_headings = ["message", "submission_time", "vote_number", "answer_id"]
            current_information = []
            if element["question_id"] == str(id):
                message_val = element["message"]
                current_information.append(message_val)
                sub_time = element["submission_time"]
                current_information.append(sub_time)
                vote_nr = element["vote_number"]
                current_information.append(vote_nr)
                answer_id = element["id"]
                current_information.append(answer_id)

                compile_answer = {
                    answer_headings[i]: current_information[i]
                    for i in range(len(answer_headings))
                }
                answer.append(compile_answer)
    except TypeError:
        print("hahahaha i crashed stuff @ accessing an entry")
        answer = None

    if not answer:
        title = entry["title"]
        message = entry["message"]
        view_count = entry["view_number"]
        submission_time = entry["submission_time"]
        question_votes = entry["vote_number"]

        return render_template(
            "entry.html",
            title=title,
            message=message,
            view_count=view_count,
            submission_time=submission_time,
            question_votes=question_votes,
            id=id,
        )
    else:
        title = entry["title"]
        message = entry["message"]
        view_count = entry["view_number"]
        submission_time = entry["submission_time"]
        question_votes = entry["vote_number"]

        answer = answer

        return render_template(
            "entry.html",
            title=title,
            message=message,
            view_count=view_count,
            submission_time=submission_time,
            question_votes=question_votes,
            answer=answer,
            id=id,
        )


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
