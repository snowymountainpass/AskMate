import datetime

from psycopg2 import sql

import database_common


def get_time():
    return datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')
    # return time.strftime("%H:%M", time.localtime())


@database_common.connection_handler
def get_all_questions(cursor):
    query = """
    SELECT * 
    FROM question
    ORDER BY id
    """
    cursor.execute(query)
    return cursor.fetchall()


# @database_common.connection_handler
# def TEST_SORTING(cursor, table, column, order):
#     query = sql.SQL("""
#     SELECT * FROM {table}
#     ORDER BY {column} {order}
#     """)
#     cursor.execute(query, {'table':table, 'column':column, 'order':order})
#     return cursor.fetchall()


@database_common.connection_handler
def get_all_questions_t_a(cursor):
    query = """
    SELECT * 
    FROM question
    ORDER BY title
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_all_questions_st_a(cursor):
    query = """
    SELECT * 
    FROM question
    ORDER BY submission_time
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_all_questions_mess_a(cursor):
    query = """
    SELECT * 
    FROM question
    ORDER BY message
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_all_questions_views_a(cursor):
    query = """
    SELECT * 
    FROM question
    ORDER BY view_number
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_all_questions_votes_a(cursor):
    query = """
    SELECT * 
    FROM question
    ORDER BY vote_number
    """
    cursor.execute(query)
    return cursor.fetchall()


@database_common.connection_handler
def get_question_at_id(cursor, id):
    query = """
    SELECT *
    FROM question
    WHERE id = %(id)s
    """
    cursor.execute(query, {'id': id})
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
    cursor.execute(query, {'id': id})
    return cursor.fetchall()


@database_common.connection_handler
def get_comments_for_question(cursor, id):
    query = """
    SELECT comment.id, comment.message, comment.submission_time, edited_count
    FROM comment
    INNER JOIN question 
        ON comment.question_id = question.id
    WHERE question_id = %(id)s
    ORDER BY comment.id
    """
    cursor.execute(query, {'id': id})
    return cursor.fetchall()


@database_common.connection_handler
def increase_question_viewcount(cursor, id):
    query = """
    UPDATE question
    SET view_number = view_number + 1
    WHERE id = %(id)s
    """
    cursor.execute(query, {'id': id})


@database_common.connection_handler
def delete_question(cursor, id):
    answers_query = """
    DELETE FROM answer
    WHERE question_id = %(id)s
    """
    cursor.execute(answers_query, {'id': id})
    query = """
    DELETE FROM question
    WHERE id = %(id)s
    """
    cursor.execute(query, {'id': id})


@database_common.connection_handler
def delete_answer(cursor, id, question_id):
    query = """
    DELETE FROM answer
    WHERE question_id = %(question_id)s AND
    id = %(id)s
    """
    cursor.execute(query, {'question_id': question_id, 'id': id})


@database_common.connection_handler
def upvote_question(cursor, id):
    query = """
    UPDATE question
    SET vote_number = vote_number + 1
    WHERE id = %(id)s
    """
    cursor.execute(query, {'id': id})


@database_common.connection_handler
def downvote_question(cursor, id):
    query = """
    UPDATE question
    SET vote_number = vote_number - 1
    WHERE id = %(id)s
    """
    cursor.execute(query, {'id': id})


@database_common.connection_handler
def upvote_answer(cursor, id):
    query = """
    UPDATE answer
    SET vote_number = vote_number + 1
    WHERE id = %(id)s
    """
    cursor.execute(query, {'id': id})


@database_common.connection_handler
def downvote_answer(cursor, id):
    query = """
    UPDATE answer
    SET vote_number = vote_number - 1
    WHERE id = %(id)s
    """
    cursor.execute(query, {'id': id})


@database_common.connection_handler
def edit_question(cursor, id, message, image):
    query = """
    UPDATE question
    SET message = %(message)s,
    image = %(image)s
    WHERE id = %(id)s
    """
    cursor.execute(query, {'message': message, 'image': image, 'id': id})
    return True


@database_common.connection_handler
def inject_new_question(cursor, title, message, image):
    get_time_of_posting = get_time()
    query = """
    INSERT INTO question
    (submission_time, view_number, vote_number, title, message, image)
    VALUES (%(time)s, 0, 0, %(title)s, %(message)s, %(image)s)
    """
    cursor.execute(query, {'time': get_time_of_posting, 'title': title, 'message': message, 'image': image})
    get_id_query = """
    SELECT id
    FROM question
    WHERE submission_time = %(time)s AND title = %(title)s AND message = %(message)s
    """
    cursor.execute(get_id_query, {'time': get_time_of_posting, 'title': title, 'message': message})
    return cursor.fetchall()


@database_common.connection_handler
def inject_question_comment(cursor, id, message):
    get_time_of_posting = get_time()
    query = """
    INSERT INTO comment
    (question_id, answer_id, message, submission_time, edited_count)
    VALUES (%(question_id)s, Null, %(message)s, %(time)s, 0)
    
    """
    cursor.execute(query, {'question_id': id, 'message': message, 'time': get_time_of_posting, })


@database_common.connection_handler
def get_comment(cursor, id):
    query = """
    SELECT *
    FROM comment
    WHERE id = %(id)s
    """
    cursor.execute(query, {'id': id})
    return cursor.fetchall()


@database_common.connection_handler
def edit_comment(cursor, id, message):
    current_time = get_time()
    query = """
    UPDATE comment
    SET message = %(message)s, submission_time = %(submission_time)s, edited_count = edited_count + 1
    WHERE id = %(id)s
    """
    cursor.execute(query, {'message': message, 'id': id, 'submission_time': current_time, })


@database_common.connection_handler
def delete_comment(cursor, id):
    query = """
        DELETE FROM comment
        WHERE id = %(id)s
        """
    cursor.execute(query, {'id':id})