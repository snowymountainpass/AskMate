import csv
import random
import string
import time

FIELDNAMES = ["id", "submission_time", "view_number", "vote_number", "title", "message"]

HEADERS_QUESTIONS = [
    "id",
    "submission_time",
    "view_number",
    "vote_number",
    "title",
    "message",
]
HEADERS_ANSWERS = ["id", "submission_time", "vote_number", "question_id", "message"]


def generate_key():
    new_id = []
    for digit in range(5):
        random_element = random.choice(string.digits)
        new_id.append(random_element)
    return int("".join(new_id))


def get_time():
    named_tuple = time.localtime()
    current_time= time.strftime("%H:%M", named_tuple)
    return current_time


def read_all_entries(file, header):
    output = []
    with open(file, mode="r") as file:
        reader = csv.DictReader(file, fieldnames=header)
        for row in reader:
            output.append(row)
    return output[1:]


def insert_entry(title, message):
    try:
        count = len(read_all_entries("sample_data/question.csv", HEADERS_QUESTIONS))

        with open("sample_data/question.csv", mode="a", newline="\n") as file:
            writer = csv.DictWriter(file, fieldnames=HEADERS_QUESTIONS)

            writer.writerow(
                {
                    "id": count,
                    "submission_time": get_time(),
                    "view_number": 1,
                    "vote_number": 0,
                    "title": title,
                    "message": message,
                }
            )
        return count

    except:
        return 0


def insert_answer(id, message):
    try:
        count = len(read_all_entries("sample_data/answer.csv", HEADERS_ANSWERS))

        with open("sample_data/answer.csv", mode="a", newline="\n") as file:
            writer = csv.DictWriter(file, fieldnames=HEADERS_ANSWERS)

            writer.writerow(
                {
                    "id": count,
                    "submission_time": get_time(),
                    "vote_number": 0,
                    "question_id": id,
                    "message": message,
                }
            )
        return True

    except:
        return False


def read_entry(id):
    entries = read_all_entries("sample_data/question.csv", HEADERS_QUESTIONS)

    output = []
    for entry in entries:
        if int(entry["id"]) == id:
            entry["view_number"] = int(entry["view_number"]) + 1
            output = entry

    with open("sample_data/question.csv", mode="w", newline="\n") as file:
        writer = csv.DictWriter(file, fieldnames=HEADERS_QUESTIONS)
        writer.writeheader()

        for index, entry in enumerate(entries):
            writer.writerow(
                {
                    "id": index,
                    "submission_time": entry["submission_time"],
                    "view_number": entry["view_number"],
                    "vote_number": entry["vote_number"],
                    "title": entry["title"],
                    "message": entry["message"],
                }
            )
    return output


def change_entry(id, message):
    entries = read_all_entries("sample_data/question.csv", HEADERS_QUESTIONS)

    output = []
    for entry in entries:
        if int(entry["id"]) == id:
            entry["message"] = message
            output = entry

    with open("sample_data/question.csv", mode="w", newline="\n") as file:
        writer = csv.DictWriter(file, fieldnames=HEADERS_QUESTIONS)
        writer.writeheader()

        for index, entry in enumerate(entries):
            writer.writerow(
                {
                    "id": index,
                    "submission_time": entry["submission_time"],
                    "view_number": entry["view_number"],
                    "vote_number": entry["vote_number"],
                    "title": entry["title"],
                    "message": entry["message"],
                }
            )
    return output


def upvote_entry(id):
    entries = read_all_entries("sample_data/question.csv", HEADERS_QUESTIONS)

    output = []
    for entry in entries:
        if int(entry["id"]) == id:
            entry["vote_number"] = int(entry["vote_number"]) + 1
            output = entry

    with open("sample_data/question.csv", mode="w", newline="\n") as file:
        writer = csv.DictWriter(file, fieldnames=HEADERS_QUESTIONS)
        writer.writeheader()

        for index, entry in enumerate(entries):
            writer.writerow(
                {
                    "id": index,
                    "submission_time": entry["submission_time"],
                    "view_number": entry["view_number"],
                    "vote_number": entry["vote_number"],
                    "title": entry["title"],
                    "message": entry["message"],
                }
            )
    return output


def read_answers(id):
    answers = read_all_entries("sample_data/answer.csv", HEADERS_ANSWERS)
    output = []

    for answer in answers:
        if int(answer["question_id"]) == id:
            output.append(answer)

    with open("sample_data/answer.csv", mode="w", newline="\n") as file:
        writer = csv.DictWriter(file, fieldnames=HEADERS_ANSWERS)
        writer.writeheader()

        for index, answer in enumerate(answers):
            writer.writerow(
                {
                    "id": index,
                    "submission_time": answer["submission_time"],
                    "vote_number": answer["vote_number"],
                    "question_id": answer["question_id"],
                    "message": answer["message"],
                }
            )
    return output


def upvote_answer_in_db(id):
    answers = read_all_entries("sample_data/answer.csv", HEADERS_ANSWERS)
    print('IN UPVOTE_ANSWER, reading entries')

    output = None
    for answer in answers:
        if int(answer["id"]) == id:
            answer["vote_number"] = int(answer["vote_number"]) + 1
            output = answer["question_id"]

    with open("sample_data/answer.csv", mode="w", newline="\n") as file:
        writer = csv.DictWriter(file, fieldnames=HEADERS_ANSWERS)
        writer.writeheader()

        for index, answer in enumerate(answers):
            writer.writerow(
                {
                    "id": index,
                    "submission_time": answer["submission_time"],
                    "vote_number": answer["vote_number"],
                    "question_id": answer["question_id"],
                    "message": answer["message"],
                }
            )
    print('QUITING UPVOTE ANSWER')
    return output