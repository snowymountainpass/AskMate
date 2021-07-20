import database_common


@database_common.connection_handler
def get_all_questions(cursor):
    query = """
    SELECT * 
    FROM question
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
    cursor.execute(query, {'id':id})
    return cursor.fetchall()


@database_common.connection_handler
def get_answers_for_question(cursor, id):
    query = """
    SELECT answer.message, answer.submission_time, answer.vote_number, answer.id
    FROM answer
    LEFT JOIN question 
        ON answer.question_id = question.id
    WHERE question_id = %(id)s
    """
    cursor.execute(query, {'id':id})
    return cursor.fetchall()


# @database_common.connection_handler
# def get_column(cursor, database, column):
#     query