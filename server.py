from flask import Flask, render_template, request, redirect, url_for, session, escape, make_response
import data_manager as dm


app = Flask(__name__)
OPTIONS = {
    "View": "view_number",
    "Vote": "vote_number",
    "Title": "title",
    "Date": "submission_time",
    "Descending": "DESC",
    "Ascending": "ASC",
}
app.secret_key = b'GULAG'


@app.route('/')
@app.route('/list', methods=['GET', 'POST'])
def route_list():
    order_direction = OPTIONS[request.form.get("order_direction", "Descending")]
    order_by = OPTIONS[request.form.get("order_by", "Date")]
    sorted_questions = dm.sort_questions(order_by, order_direction)
    return render_template('list.html', questions=sorted_questions)



@app.route('/question/<question_id>')
def route_expand_question(question_id):
    question = dm.get_question_by_id(question_id)[0]
    answers_by_question_id = dm.get_answer_by_id(question_id)
    comments_to_question = dm.get_all_comments_to_a_question(question_id)
    question["view_number"] = question["view_number"] + 1
    dm.update_view_count("question", question)
    return render_template('question.html', question=question, answers=answers_by_question_id,
                           question_id=question_id, comments=comments_to_question)


@app.route('/question/<question_id>', methods=['POST'])
def route_add_answer(question_id):
    if request.method == 'POST':
        data = request.form
        data = dict(data)
        data = dm.check_current_time(data)
        dm.add_new_answer_to_table(data)
        return redirect(url_for('route_expand_question', question_id=question_id))


@app.route('/add_question', methods=['POST', 'GET'])
def route_add_question():
    if request.method == 'POST':
        data = request.form
        data = dict(data)
        data = dm.check_current_time(data)
        dm.add_new_question_to_table(data)
        return redirect(url_for('route_list'))
    return render_template('add_question.html')


@app.route('/question/<question_id>/delete')
def route_delete_question(question_id):
    dm.delete_question(question_id)
    return redirect(url_for('route_list'))


@app.route('/question/<question_id>/new-comment', methods=['POST'])
def route_comment_question(question_id):
    print(question_id)
    data = request.form
    data = dict(data)
    data = dm.check_current_time(data)
    dm.add_comment_to_question(data)
    comment_id = data['id']
    return redirect(url_for('route_expand_question', question_id=question_id, comment_id=comment_id))


@app.route('/latest_questions', methods=['GET', 'POST'])
def route_latest_questions():
    data = dm.display_latest_questions()
    return render_template('latest_questions.html', latest_questions=data)


@app.route('/comments/<comment_id>/delete')
def route_delete_comment(comment_id):
    question_id = dm.get_question_id_by_comment_id(comment_id)
    dm.delete_comment(comment_id)
    question_id = dict(question_id[0])
    question_id = question_id['question_id']
    return redirect(url_for('route_expand_question', question_id=question_id, ))


@app.route('/answer/<answer_id>/delete')
def route_delete_answer(answer_id):
    question_id = dm.get_question_id_by_answer_id(answer_id)
    question_id = dict(question_id[0])
    question_id = question_id['question_id']
    dm.delete_answer(answer_id)
    return redirect(url_for('route_expand_question', question_id=question_id))


@app.route('/register_page')
def route_register_page():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def route_register():
    username = request.form.get("username")
    password = request.form.get("password")
    print(username, password)
    hashed_pw = dm.hash_password(password)
    dm.register_user(username, hashed_pw)
    return redirect(url_for('route_list'))


@app.route('/list_users')
def route_list_users():
    users = dm.husszonnégytonnakokain()
    return render_template('users.html', users=users)


@app.route('/login', methods=["POST"])
def route_login():
    username = request.form.get("username")
    password = request.form.get("password")
    valid_pass = dm.login_user(username)
    verification = dm.verify_password(password, valid_pass)
    if verification is True:
        redirect_to_index = redirect('/')
        response = make_response(redirect_to_index)
        response.set_cookie('username', value=username)
        return response


@app.route('/log_out', methods=["POST"])
def route_logout():
    resp = make_response(redirect(url_for('route_list')))
    resp.set_cookie('username', '', expires=0)
    return resp


if __name__ == '__main__':
    app.run(
        port=5000,
        debug=True,
    )
