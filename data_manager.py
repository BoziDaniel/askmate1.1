import connection as cn
from datetime import datetime

@cn.connection_handler
def display_questions(cursor, table):
    query = f"""SELECT * FROM {table}"""
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
def add_new_data_to_table(cursor, table):
    pass