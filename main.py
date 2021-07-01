from flask import Flask, render_template, request, redirect, url_for, flash
from sample_data import read_all_entries, insert_entry, read_entry, read_answers, HEADERS_QUESTIONS, HEADERS_ANSWERS

app = Flask(__name__)
app.secret_key = "alskua ekjegu keucyf iqek,rvgkfarg rkjegkjqaved"


@app.route("/")
def index():
    entries = read_all_entries("sample_data/question.csv", HEADERS_QUESTIONS)
    return render_template("index.html", entries=entries)


@app.route("/entry/<int:id>", methods=['GET'])
def get_entry(id):
    entry = read_entry(id)
    print(id)
    print(f'ENTRY ID TYPE{type(id)}')
    try:
        answer_all = read_answers(id)
        print(answer_all)
        print(f'TYPE ANSWER_ALL L 22 {type(answer_all)}')
        answer = []
        for element in answer_all:
            print(element)
            print(f'ELEMENT AT L 26 {type(element)}')
            if element['question_id'] == str(id):
                answer.append(element)     # de preluat doar bucati din dictionare
                print(answer)
        #answer = [question for question in answer_all if question[3] == id]
        print(answer)
    except TypeError:
        print('hahahaha i crashed stuff')
        answer = None

    if not answer:
        title = entry["title"]
        message = entry["message"]
        view_count = entry["view_number"]

        return render_template(
            "entry.html",
            title=title,
            message=message,
            view_count=view_count,
        )
    else:
        title = entry["title"]
        message = entry["message"]
        view_count = entry["view_number"]

        answer = answer["message"]

        return render_template(
            "entry.html",
            title=title,
            message=message,
            view_count=view_count,
            answer=answer
        )



@app.route("/post-question", methods=['GET'])
def enter_question():
    return render_template("post_question.html")


@app.route("/add", methods=["POST"])
def adding():
    title = request.form.get("title")
    message = request.form.get("message")

    if insert_entry(title, message):
        flash("Entry added")
        return redirect(url_for("index"))

    flash("Entry not added")
    return redirect(url_for("index"))

@app.route("/edit/<question_id>")
def edit():
    pass



if __name__ == "__main__":
    app.run(debug=True)
