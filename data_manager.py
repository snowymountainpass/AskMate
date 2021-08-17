import datetime

from psycopg2 import sql

import database_common


def get_time():
    return datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S")


@database_common.connection_handler
def get_all_questions(cursor, criterion, direction):
    criteria = ["id", "title", "submission_time", "message", "view_number", "vote_number"]
    directions = ["asc", "desc"]

    if criterion in criteria and direction in directions:
        query = f"""
        SELECT * 
        FROM question
        ORDER BY {criterion} {direction}
        """
    cursor.execute(query)
    return cursor.fetchall()


# @database_common.connection_handler
# def get_all_questions_t_a(cursor):
#     query = """
#     SELECT * 
#     FROM question
#     ORDER BY title
#     """
#     cursor.execute(query)
#     return cursor.fetchall()


# @database_common.connection_handler
# def get_all_questions_st_a(cursor):
#     query = """
#     SELECT * 
#     FROM question
#     ORDER BY submission_time
#     """
#     cursor.execute(query)
#     return cursor.fetchall()


# @database_common.connection_handler
# def get_all_questions_mess_a(cursor):
#     query = """
#     SELECT * 
#     FROM question
#     ORDER BY message
#     """
#     cursor.execute(query)
#     return cursor.fetchall()


# @database_common.connection_handler
# def get_all_questions_views_a(cursor):
#     query = """
#     SELECT * 
#     FROM question
#     ORDER BY view_number
#     """
#     cursor.execute(query)
#     return cursor.fetchall()


# @database_common.connection_handler
# def get_all_questions_votes_a(cursor):
#     query = """
#     SELECT * 
#     FROM question
#     ORDER BY vote_number
#     """
#     cursor.execute(query)
#     return cursor.fetchall()


@database_common.connection_handler
def get_question_at_id(cursor, id):
    query = """
    SELECT *
    FROM question
    WHERE id = %(id)s
    """
    cursor.execute(query, {"id": id})
    return cursor.fetchall()


@database_common.connection_handler
def get_answers_for_question(cursor, id):
    query = """
    SELECT answer.id, answer.submission_time, answer.vote_number, answer.question_id, answer.message, answer.image
    FROM answer
    INNER JOIN question 
        ON answer.question_id = question.id
    WHERE question_id = %(id)s
    ORDER BY answer.id
    """
    cursor.execute(query, {"id": id})
    return cursor.fetchall()


@database_common.connection_handler
def get_message_from_answer(cursor, id_answer):
    query = """
    SELECT answer.message
    FROM answer
    INNER JOIN question 
    ON answer.question_id = question.id
    WHERE answer.id=%(id_answer)s
    """
    cursor.execute(query, {"id_answer": id_answer})
    return cursor.fetchall()


@database_common.connection_handler
def get_comments_for_question(cursor, id):
    query = """
    SELECT comment.id, comment.message, comment.submission_time, edited_count
    FROM comment
    INNER JOIN question 
        ON comment.question_id = question.id
    WHERE question_id = %(id)s AND answer_id IS NULL
    ORDER BY comment.id
    """
    cursor.execute(query, {"id": id})
    return cursor.fetchall()


@database_common.connection_handler
def get_comments_for_answer(cursor, id):
    query = """
    SELECT comment.id, comment.question_id, comment.answer_id, comment.message, comment.submission_time, edited_count
    FROM comment
    INNER JOIN question 
        ON comment.question_id = question.id
    WHERE question_id = %(id)s AND answer_id IS NOT NULL
    ORDER BY comment.id
    """
    cursor.execute(query, {"id": id})
    return cursor.fetchall()


# @data_commons.connection_handler
# def get_comments_by_answer(cursor, id_answer, id_question):
#     query = """
#     SELECT comment.message,comment.question_id,comment.answer_id,comment.submission_time
#     FROM comment
#     INNER JOIN answer ON comment.answer_id = answer.id
#     WHERE comment.answer_id=%(id_answer)s AND comment.question_id = %(id_question)s
#     """
#     cursor.execute(query, {"id_answer": id_answer, "id_question": id_question})
#     return cursor.fetchall()


@database_common.connection_handler
def increase_question_viewcount(cursor, id):
    query = """
    UPDATE question
    SET view_number = view_number + 1
    WHERE id = %(id)s
    """
    cursor.execute(query, {"id": id})


@database_common.connection_handler
def delete_question(cursor, id):
    question_comments_query = """
    DELETE FROM comment
    WHERE question_id = %(id)s
    """
    cursor.execute(question_comments_query, {"id": id})

    answers_query = """
    DELETE FROM answer
    WHERE question_id = %(id)s
    """
    cursor.execute(answers_query, {"id": id})

    query = """
    DELETE FROM question
    WHERE id = %(id)s
    """
    cursor.execute(query, {"id": id})


@database_common.connection_handler
def delete_answer(cursor, id, question_id):
    query = """
    DELETE FROM answer
    WHERE question_id = %(question_id)s AND
    id = %(id)s
    """
    cursor.execute(query, {"question_id": question_id, "id": id})


@database_common.connection_handler
def upvote_question(cursor, id):
    query = """
    UPDATE question
    SET vote_number = vote_number + 1
    WHERE id = %(id)s
    """
    cursor.execute(query, {"id": id})


@database_common.connection_handler
def downvote_question(cursor, id):
    query = """
    UPDATE question
    SET vote_number = vote_number - 1
    WHERE id = %(id)s
    """
    cursor.execute(query, {"id": id})


@database_common.connection_handler
def upvote_answer(cursor, id):
    query = """
    UPDATE answer
    SET vote_number = vote_number + 1
    WHERE id = %(id)s
    """
    cursor.execute(query, {"id": id})


@database_common.connection_handler
def downvote_answer(cursor, id):
    query = """
    UPDATE answer
    SET vote_number = vote_number - 1
    WHERE id = %(id)s
    """
    cursor.execute(query, {"id": id})


@database_common.connection_handler
def edit_question(cursor, id, message, image):
    query = """
    UPDATE question
    SET message = %(message)s,
    image = %(image)s
    WHERE id = %(id)s
    """
    cursor.execute(query, {"message": message, "image": image, "id": id})
    return True


@database_common.connection_handler
def inject_new_question(cursor, title, message, image):
    get_time_of_posting = get_time()
    query = """
    INSERT INTO question
    (submission_time, view_number, vote_number, title, message, image)
    VALUES (%(time)s, 0, 0, %(title)s, %(message)s, %(image)s)
    """
    cursor.execute(
        query,
        {
            "time": get_time_of_posting,
            "title": title,
            "message": message,
            "image": image,
        },
    )
    get_id_query = """
    SELECT id
    FROM question
    WHERE submission_time = %(time)s AND title = %(title)s AND message = %(message)s
    """
    cursor.execute(
        get_id_query, {"time": get_time_of_posting, "title": title, "message": message}
    )
    return cursor.fetchall()


@database_common.connection_handler
def add_answer_to_question(cursor, id_question, message):
    query = """
    INSERT INTO answer (submission_time, vote_number, question_id, message)
    VALUES (%(submission_time)s,%(vote_number)s,%(question_id)s,%(message)s)
    """
    cursor.execute(
        query,
        {
            "submission_time": get_time(),
            "vote_number": 0,
            "question_id": id_question,
            "message": message,
            # 'image': applicant_details.get("image"),
        },
    )


@database_common.connection_handler
def inject_question_comment(cursor, id, message):
    get_time_of_posting = get_time()
    query = """
    INSERT INTO comment
    (question_id, answer_id, message, submission_time, edited_count)
    VALUES (%(question_id)s, Null, %(message)s, %(time)s, 0)
    
    """
    cursor.execute(
        query,
        {
            "question_id": id,
            "message": message,
            "time": get_time_of_posting,
        },
    )


@database_common.connection_handler
def add_comment_to_answer(cursor, id_answer, id_question, comment_message):
    query = """
    INSERT INTO comment (question_id,answer_id,message,submission_time,edited_count)
    VALUES (%(question_id)s,%(answer_id)s,%(message)s,%(submission_time)s,%(edited_count)s)    
    """
    cursor.execute(
        query,
        {
            "question_id": id_question,
            "answer_id": id_answer,
            "message": comment_message,
            "submission_time": get_time(),
            "edited_count": 0,
        },
    )


@database_common.connection_handler
def get_comment(cursor, id):
    query = """
    SELECT *
    FROM comment
    WHERE id = %(id)s
    """
    cursor.execute(query, {"id": id})
    return cursor.fetchall()


@database_common.connection_handler
def edit_comment(cursor, id, message):
    current_time = get_time()
    query = """
    UPDATE comment
    SET message = %(message)s, submission_time = %(submission_time)s, edited_count = edited_count + 1
    WHERE id = %(id)s
    """
    cursor.execute(
        query,
        {
            "message": message,
            "id": id,
            "submission_time": current_time,
        },
    )


@database_common.connection_handler
def delete_comment_question(cursor, comment_id, question_id):
    query = """
        DELETE FROM comment
        WHERE id = %(comment_id)s AND 
        question_id = %(question_id)s
        """
    cursor.execute(query, {"comment_id": comment_id, "question_id":question_id})


@database_common.connection_handler
def delete_comment_answer(cursor, comment_id, answer_id, question_id):
    query = """
        DELETE FROM comment
        WHERE id = %(comment_id)s AND 
        answer_id = %(answer_id)s
        """
    cursor.execute(query, {"comment_id": comment_id, "answer_id": answer_id})


@database_common.connection_handler
def delete_answer_to_question(cursor, id_answer):
    comment_query = """
    DELETE FROM comment
    WHERE answer_id = %(id_answer)s
    """
    cursor.execute(comment_query, {"id_answer": id_answer})
    query = """
    DELETE FROM answer
    WHERE id=%(id_answer)s
    """
    cursor.execute(query, {"id_answer": id_answer})


@database_common.connection_handler
def edit_answer_to_question(cursor, id_answer, old_message, new_message):
    query = """
    UPDATE answer
    SET message = %(new_message)s, submission_time = %(submission_time)s
    WHERE id=%(id_answer)s AND message = %(old_message)s
    """
    cursor.execute(
        query,
        {
            "new_message": new_message,
            "submission_time": get_time(),
            "id_answer": id_answer,
            "old_message": old_message,
        },
    )


@database_common.connection_handler
def sort_answers(
    cursor, id_question, sort_by_criteria, display_order
):  # https://pysql.tecladocode.com/section08/lectures/08_sql_string_composition/
    query = """
        SELECT *
        FROM answer
        INNER JOIN question 
        ON answer.question_id = question.id
        WHERE question.id = %(id_question)s
        ORDER BY %(sort_by_criteria)s %(display_order)s
        """

    # %(sort_by_criteria)s %(display_order)s
    cursor.execute(
        query,
        {
            "id_question": id_question,
            "sort_by_criteria": sort_by_criteria,
        },
    )  # 'display_order': display_order


@database_common.connection_handler
def sort_answers_wip(
    cursor, id_question, sort_by_criteria, display_order
):  # https://kb.objectrocket.com/postgresql/python-parameterized-sql-for-postgres-915
    query = ""
    query += "SELECT *"
    query += "FROM answer"
    query += "INNER JOIN question"
    query += "ON answer.question_id = question.id"
    query += "WHERE question.id = %id_question"
    query += "ORDER BY %(sort_by_criteria)s %(display_order)s"
    cursor.execute(
        query,
        (
            id_question,
            sort_by_criteria,
            display_order,
        ),
    )
