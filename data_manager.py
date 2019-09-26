import connection as cn
import bcrypt
from datetime import datetime
from psycopg2 import sql


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password['password'].encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)



@cn.connection_handler
def display_table(cursor, table):
    query = f"""SELECT * FROM {table}"""
    cursor.execute(query)
    data = cursor.fetchall()
    return data


@cn.connection_handler
def get_question_by_id(cursor, id_):
    cursor.execute("""SELECT question.*, users.name FROM question
                        JOIN users ON users.id = question.user_id
                        WHERE question.id = %(id)s""", {'id': id_})
    data = cursor.fetchall()
    return data


@cn.connection_handler
def get_answer_by_id(cursor, question_id):
    query = f"""SELECT answer.*, users.name FROM answer 
    JOIN users ON users.id = answer.user_id
     WHERE question_id = {question_id}"""
    cursor.execute(query)
    data = cursor.fetchall()
    return data


def check_current_time(data):
    data["submission_time"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return data


@cn.connection_handler
def add_new_question_to_table(cursor, data, username):
    user_id = get_user_id_by_username(username)
    cursor.execute("""
    INSERT INTO question (submission_time, view_number, vote_number, title, message, image, user_id) 
    VALUES (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s,
           %(image)s, %(user_id)s)""",
                   {'submission_time': data['submission_time'], 'view_number': data['view_number'],
                    'vote_number': data['vote_number'], 'title': data['title'],
                    'message': data['message'], 'image': data['image'], 'user_id': user_id['id']});


@cn.connection_handler
def add_new_answer_to_table(cursor, data, username):
    user_id = get_user_id_by_username(username)
    query = f"""INSERT INTO answer (submission_time, vote_number, question_id, message, image, user_id)
            VALUES ('{data["submission_time"]}', '{data["vote_number"]}', '{data["question_id"]}', 
                    '{data["message"]}', '{data["image"]}', '{user_id["id"]}');"""
    cursor.execute(query)


@cn.connection_handler
def delete_data_by_id(cursor, table, id):
    query = f"""DELETE FROM {table} WHERE id = {id}"""
    cursor.execute(query)


@cn.connection_handler
def update_view_count(cursor, table, data):
    if table == "question":
        view = data["view_number"]
        id_ = data["id"]
        query = f"""UPDATE question SET view_number = {view} WHERE id = {id_}"""
        cursor.execute(query)


@cn.connection_handler
def display_latest_questions(cursor):
    cursor.execute("""
                    SELECT id ,submission_time , title FROM question ORDER BY submission_time DESC LIMIT 5""")
    latest_questions = cursor.fetchall()
    return latest_questions


@cn.connection_handler
def get_all_comments_to_a_question(cursor, question_id):
    query = f"""SELECT submission_time, message, comment.id, users.name FROM comment
            JOIN users ON users.id = comment.user_id
            WHERE question_id={question_id}"""
    cursor.execute(query)
    comments_to_a_question = cursor.fetchall()
    return comments_to_a_question


@cn.connection_handler
def add_comment_to_question(cursor, data, username):
    user_id = get_user_id_by_username(username)
    query = f"""INSERT INTO comment (question_id, message, submission_time, user_id)
                VALUES ('{data["question_id"]}', '{data["comment"]}', 
                        '{data["submission_time"]}', '{user_id["id"]}')"""

    cursor.execute(query)


@cn.connection_handler
def generate_comment_id(cursor):
    cursor.execute("""SELECT id FROM comment 
                    ORDER BY id DESC LIMIT 1;""")
    last_id = cursor.fetchone()
    next_id = last_id['id'] + 1
    print(next_id)
    return next_id
#Jenci erre írt egy jobbat táblás paraméterrel de az most nincs meg meg nem működött, írtam egy
# baltábbat de lehet erre sincs szükség
# cs gondoltam szebb ha nem az adatbázis generálja az id-t.


@cn.connection_handler
def delete_comment(cursor, id_):
    cursor.execute("""DELETE FROM comment 
                    WHERE id= %(id)s""", {'id': id_})


@cn.connection_handler
def delete_answer(cursor, id_):
    cursor.execute("""DELETE FROM comment
                    WHERE answer_id= %(id_)s""", {'id_': id_});

    cursor.execute("""DELETE FROM answer
                    WHERE id= %(id_)s""", {'id_': id_});


@cn.connection_handler
def delete_question(cursor, question_id):
    query1 = f""" DELETE FROM question
                  WHERE id= {question_id};"""
    query2 = f""" DELETE FROM answer
                  WHERE question_id= {question_id};"""
    query3 = f"""DELETE FROM comment
                  WHERE question_id={question_id};"""
    cursor.execute(query3)
    cursor.execute(query2)
    cursor.execute(query1)


@cn.connection_handler
def get_question_id_by_comment_id(cursor, comment_id):
    cursor.execute("""SELECT question_id FROM comment
                    WHERE id= %(comment_id)s""", {'comment_id': comment_id})
    question_id = cursor.fetchall()
    return question_id


@cn.connection_handler
def sort_questions(cursor, order_by, order_direction):
    query = f"""SELECT question.*, users.name FROM question
            JOIN users ON users.id = question.user_id 
            ORDER BY {order_by} {order_direction}"""
    cursor.execute(query)
    data = cursor.fetchall()
    return data


@cn.connection_handler
def get_question_id_by_answer_id(cursor, answer_id):
    cursor.execute("""SELECT question_id FROM answer
                    WHERE id=%(answer_id)s""", {'answer_id': answer_id})
    question_id = cursor.fetchall()
    return question_id


@cn.connection_handler
def register_user(cursor, name_, password_):
    date_ = datetime.now()
    cursor.execute(
       """INSERT INTO users (name, password, date)
                    VALUES (%(name_)s, %(password_)s, %(date_)s)"""
        ,{'name_': name_, 'password_': password_, 'date_': date_ })


@cn.connection_handler
def husszonnégytonnakokain(cursor):
    """get all users"""
    query = "SELECT name, date FROM users"
    cursor.execute(query)
    users = cursor.fetchall()
    return users


@cn.connection_handler
def login_user(cursor, username):
    cursor.execute("""SELECT password FROM users 
    WHERE name = %(username)s""", {'username': username})
    hashed_pass = cursor.fetchone()
    return hashed_pass


@cn.connection_handler
def search_from_questions(cursor, search_phrase):
    query = f"""SELECT * FROM question
    WHERE title LIKE '%{search_phrase}%' OR message LIKE '%{search_phrase}%'"""
    cursor.execute(query)
    search_result = cursor.fetchall()
    return search_result


@cn.connection_handler
def get_user_id_by_username(cursor, username):
    cursor.execute("""SELECT id FROM users
                    WHERE name = %(username)s""", {'username': username})
    user_name =cursor.fetchone()
    return user_name


