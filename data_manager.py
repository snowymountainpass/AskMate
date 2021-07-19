import database_common


@database_common.connection_handler
def get_all_questions(cursor):
    query = """
    SELECT * 
    FROM question
    """
    cursor.execute(query)
    return cursor.fetchall()
