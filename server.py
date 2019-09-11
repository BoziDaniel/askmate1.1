from flask import Flask, render_template, request, redirect, url_for
import data_manager as dm


app = Flask(__name__)


@app.route('/')
@app.route('/list', methods=['POST', 'GET'])
def route_list():
    data = dm.display_table('question')
    return render_template('list.html', sorted_questions=data)


@app.route('/question/<question_id>', methods=['GET'])
def route_expand_question(question_id):
    question = dm.get_question_by_id(question_id)
    # question["view_number"] = int(question["view_number"]) + 1
    # dm.update_row_in_table("question", question)
    answers_by_question_id = dm.get_answer_by_id(question_id)
    return render_template('question.html', question=question, answers=answers_by_question_id, question_id=question_id)


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


@app.route('/question/<question_id>/new-comment')
def comment_question(question_id, ):
    pass

@app.route('/latest_questions', methods=['GET', 'POST'])
def route_latest_questions():
    data = dm.display_latest_questions()
    return render_template('latest_questions.html', latest_questions=data)


if __name__ == '__main__':
    app.run(
        port=5000,
        debug=True,
    )
