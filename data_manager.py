import connection as cn


@cn.connection_handler
def display_questions(cursor):
    query = """SELECT * FROM question"""
    cursor.execute(query)
    data = cursor.fetchall()
    return data