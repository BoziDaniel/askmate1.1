import connection as cn
from datetime import datetime

@cn.connection_handler
def display_table(cursor, table):
    query = f"""SELECT * FROM {table}"""
    cursor.execute(query)
    data = cursor.fetchall()
    return data


@cn.connection_handler
def get_question_by_id(cursor, id):
    query = f"""SELECT * FROM question WHERE id = {id}"""
    cursor.execute(query)
    data = cursor.fetchall()
    return data


@cn.connection_handler
def get_answer_by_id(cursor, question_id):
    query = f"""SELECT * FROM answer WHERE question_id = {question_id}"""
    cursor.execute(query)
    data = cursor.fetchall()
    return data


def get_next_id(cursor, table):
    query = f"""SELECT id FROM {table} ORDER BY id DESC LIMIT 1"""
    cursor.execute(query)
    last_id = cursor.fetchone()
    next_id = last_id["id"] + 1
    return next_id


def replace_commas(data):
    data = dict(data)
    for column in data:
        data[column] = data[column].replace("'", "''")
    return data


def check_current_time(data):
    data["submission_time"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return data


@cn.connection_handler
def add_new_row_to_table(cursor, table):
    pass