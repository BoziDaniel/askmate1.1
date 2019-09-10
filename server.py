from flask import Flask, render_template, request, redirect, url_for
import data_manager as dm
import connection as cn
import time

app = Flask(__name__)

question_path = "sample_data/question.csv"
answer_path = "sample_data/answer.csv"


@app.route('/')
@app.route('/list', methods=['POST', 'GET'])
def route_list():
    data = dm.display_table('question')
    return render_template('list.html', sorted_questions=data)


@app.route('/question/<question_id>', methods=['POST', 'GET'])
def expand_question(question_id):
    question = dm.get_question_by_id(question_id)
    answers_by_question_id = dm.get_answer_by_id(question_id)
    return render_template('question.html', question=question, answers=answers_by_question_id)
    # if request.method == 'GET':
    #     all_questions = cn.get_all_data_from_file(question_path)
    #     all_answers = cn.get_all_data_from_file(answer_path)
    #     return render_template('question.html', question_id=question_id, answers=all_answers, questions=all_questions)
    # else:
    #     if request.method == "POST":
    #         id_ = int(dm.generate_new_id(answer_path))
    #         submission_time = int(time.time())
    #         vote_number = 0
    #         question_id = request.form.get("question_id")
    #         message = request.form.get("answer")
    #         image = request.form.get("image")
    #         new_answer = [id_, submission_time, vote_number, question_id, message, image]
    #         cn.add_new_data_to_csv(answer_path, new_answer)
    #         return redirect('/question/'+str(question_id))




@app.route('/add_question', methods=['POST', 'GET'])
def route_add_question():
    if request.method == 'POST':
        data = request.form
        data = dict(data)
        data = dm.check_current_time(data)
        dm.add_new_question_to_table(data)
        return redirect(url_for('route_list'))
    return render_template('add_question.html')


if __name__ == '__main__':
    app.run(
        port=5000,
        debug=True,
    )
