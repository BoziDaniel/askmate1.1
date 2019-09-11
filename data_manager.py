import connection as cn
from datetime import datetime


@cn.connection_handler
def display_table(cursor, table):
    query = f"""SELECT * FROM {table}"""
    cursor.execute(query)
    data = cursor.fetchall()
    return data
'''
    if sort_by == "submission_time" and order == "descending":
        cursor.exexcute(""" SELECT * FROM question 
        ORDER BY %s DESC
        """)
'''



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


def get_last_id(cursor, table):
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
def add_new_question_to_table(cursor, data):
    cursor.execute("""
    INSERT INTO question (submission_time, view_number, vote_number, title, message, image) 
    VALUES (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s)""",
                   {'submission_time': data['submission_time'], 'view_number' : data['view_number'],
                   'vote_number' : data['vote_number'], 'title' : data['title'],
                   'message' : data['message'], 'image' : data['image']});


@cn.connection_handler
def add_new_answer_to_table(cursor, data):
    query = f"""INSERT INTO answer (submission_time, vote_number, question_id, message, image)
            VALUES ('{data["submission_time"]}', '{data["vote_number"]}', '{data["question_id"]}', 
                    '{data["message"]}', '{data["image"]}');"""
    cursor.execute(query)


@cn.connection_handler
def delete_data_by_id(cursor, table, id):
    query = f"""DELETE FROM {table} WHERE id = {id}"""
    cursor.execute(query)


@cn.connection_handler
def update_row_in_table(cursor, table, data):
    if table == "question":
        query = f"""UPDATE question SET submission_time='{data["submission_time"]}',view_number={data[
                    "view_number"]},vote_number={data["vote_number"]},title='{data["title"]}', message= '{data[
                    "message"].replace("'", "''")}', image='{str(data["image"]).replace("None", "")}' WHERE id={data[
                    "id"]}"""

    cursor.execute(query)


@cn.connection_handler
def delete_question(cursor, question_id):
    query1 = f""" DELETE FROM question
                WHERE id= {question_id};"""
    query2 = f""" DELETE FROM answer
                WHERE question_id= {question_id};"""
    cursor.execute(query2)
    cursor.execute(query1)


@cn.connection_handler
def display_latest_questions(cursor):
    cursor.execute("""
                    SELECT id ,submission_time , title FROM question ORDER BY submission_time DESC LIMIT 5""")
    latest_questions = cursor.fetchall()
    return latest_questions


@cn.connection_handler
def get_all_comments_to_a_question(cursor, question_id):
    query = f"""SELECT submission_time, message FROM comment
            WHERE question_id={question_id}"""
    cursor.execute(query)
    comments_to_a_question = cursor.fetchall()
    return comments_to_a_question


@cn.connection_handler
def add_comment_to_question(cursor, data):
    query = f"""INSERT INTO comment (question_id, message, submission_time)
                VALUES ('{data["question_id"]}', '{data["comment"]}', 
                        '{data["submission_time"]}')"""
    cursor.execute(query)


