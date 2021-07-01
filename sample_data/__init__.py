import csv
import random
import string

FIELDNAMES = ["id","submission_time","view_number","vote_number", "title", "message"]

HEADERS_QUESTIONS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message']
HEADERS_ANSWERS = ['id', 'submission_time', 'vote_number', 'question_id', 'message']


def generate_key():
    new_id = []
    for digit in range(5):
        random_element = random.choice(string.digits)
        new_id.append(random_element)
    return int(''.join(new_id))


def get_questions(file):
    input_file = csv.DictReader(open(file))
    return input_file


def save_question(some_dictionary, file):
    with open(file, 'a', newline='\n') as csvfile:
        fieldnames = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(some_dictionary)
        csvfile.close()
        return csvfile



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
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)


            writer.writerow(
                {
                    "id": count,
                    "submission_time": generate_key(),
                    "view_number": 1,
                    "vote_number": 0,
                    "title": title,
                    "message": message
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
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()

        for index, entry in enumerate(entries):
            writer.writerow(
                {
                    "id": index,
                    "submission_time": entry["submission_time"],
                    "view_number": entry["view_number"],
                    "vote_number": entry["vote_number"],
                    "title": entry["title"],
                    "message": entry["message"]

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
                    "message": answer["message"]

                }
            )
    return output



