from flask import Flask, render_template, request, redirect, url_for
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


@app.route('/')
@app.route('/list', methods=['POST', 'GET'])
def route_list():
    try:
        order_direction = OPTIONS[request.form.get("order_direction")]
        order_by = OPTIONS[request.form.get("order_by")]
    except KeyError:
        order_direction = "DESC"
        order_by = "submission_time"
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


if __name__ == '__main__':
    app.run(
        port=5000,
        debug=True,
    )
