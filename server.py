from flask import Flask, render_template, request, redirect, url_for
import data_manager as dm
import connection as cn
import time

app = Flask(__name__)


@app.route('/')
@app.route('/list', methods=['POST', 'GET'])
def route_list():
    data = dm.display_table('question')
    return render_template('list.html', sorted_questions=data)


@app.route('/question/<question_id>', methods=['GET'])
def expand_question(question_id):
    question = dm.get_question_by_id(question_id)
    answers_by_question_id = dm.get_answer_by_id(question_id)
    return render_template('question.html', question=question, answers=answers_by_question_id, question_id=question_id)


@app.route('/question/<question_id>', methods=['POST'])
def add_answer(question_id):
    if request.method == 'POST':
        data = request.form
        data = dict(data)
        data = dm.check_current_time(data)
        dm.add_new_answer_to_table(data)
        return redirect(url_for('expand_question', question_id=question_id))


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
def delete_question(question_id):
    print(question_id)
    dm.delete_question(question_id)
    return redirect(url_for('route_list'))

@app.route('/question/<question_id>/new-comment')
def comment_question(question_id, ):
    pass


if __name__ == '__main__':
    app.run(
        port=5000,
        debug=True,
    )
