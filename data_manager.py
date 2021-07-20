import database_common


@database_common.connection_handler
def get_all_questions(cursor):
    query = """
    SELECT * 
    FROM question
    ORDER BY id
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
    INNER JOIN question 
        ON answer.question_id = question.id
    WHERE question_id = %(id)s
    """
    cursor.execute(query, {'id':id})
    return cursor.fetchall()


@database_common.connection_handler
def upvote_question(cursor, id):
    query = """
    UPDATE question
    SET vote_number = vote_number + 1
    WHERE id = %(id)s
    """
    cursor.execute(query, {'id':id})


@database_common.connection_handler
def upvote_answer(cursor, id):
    query = """
    UPDATE answer
    SET vote_number = vote_number + 1
    WHERE id = %(id)s
    """
    cursor.execute(query, {'id':id})


@database_common.connection_handler
def pass_question_id(cursor, id):
    query = """
    SELECT question.id 
    FROM question
    INNER JOIN answer
    ON question.id = answer.question_id
    WHERE answer.question_id = %(id)s
    """
    cursor.execute(query, {'id':id})
    return cursor.fetchall()


@database_common.connection_handler
def edit_question(cursor, id, message):
    query = """
    UPDATE question
    SET message = %(message)s
    WHERE id = %(id)s
    """
    cursor.execute(query, {'message':message, 'id':id})
    return True