from flask import Flask, render_template, request, session, redirect, url_for
import random as r
import requests
import json
import time

app = Flask(__name__)
app.secret_key = 'something'

#https://opentdb.com/api.php?amount=10&category=9&difficulty=easy&type=multiple

# {'response_code': 0, 'results': [{'type': 'multiple', 'difficulty': 'easy', 'category': 'General Knowledge', 'question': 'What geometric shape is generally used for stop signs?', 'correct_answer': 'Octagon', 'incorrect_answers': ['Hexagon', 'Circle', 'Triangle']}, 
# {'type': 'multiple', 'difficulty': 'easy', 'category': 'General Knowledge', 'question': 'Which one of the following rhythm games was made by Harmonix?', 'correct_answer': 'Rock Band', 'incorrect_answers': ['Meat Beat Mania', 'Guitar Hero Live', 'Dance Dance Revolution']}

#for question
# questions['results'[current_question]['question']]    
#for answer
#student_answer = questions['results'][current_question]['correct_answer']





@app.route('/', methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        no_ques = request.form.get('no_ques')
        category_api = requests.get(f'https://opentdb.com/api_category.php')
        category_list = category_api.json()
        category = request.form.get('category')
        diff = request.form.get('diff')
        type = request.form.get('type')

        question = requests.get(f'https://opentdb.com/api.php?amount={no_ques}&category={category}&difficulty={diff}&type={type}')
        session['questions'] = question.json()

        session['score'] = 0
        session['current_question'] = 0

        return redirect(url_for('quiz'))
    return render_template('index.html')


# @app.route('/quiz', methods = ['GET','POST'])
# def quiz():    

#     question_no = len( session['questions']['results'] )

#     if session['current_question'] < question_no:

#         current = session['questions']['results'][session['current_question']]

#         questions = current['question']

#         correct_answer = current['correct_answer']

#         options = current['incorrect_answers'].copy()
#         options.append(correct_answer)
#         r.shuffle(options)
#     #     incorrect_answers = session['questions']['results'][session['current_question']]['incorrect_answers']
#     #     correct_answer = session['questions']['results'][session['current_question']]['correct_answer']
#     #     if correct_answer not in incorrect_answers:
#     #         incorrect_answers.append(correct_answer)
#     #     r.shuffle(incorrect_answers)
#     #     options = incorrect_answers

#     #     #SHOWING QUESTIONS
#     #     questions = session['questions']['results'][session['current_question']]['question']

    
#     else :
#         return redirect(url_for('result'))
    
#     # ACCEPTING ANSWERS AND CHECKING 
#     if request.method == 'POST':
#         answer = request.form.get('answer')
#         if answer ==  correct_answer:
#             session['score'] += 1

#         session['current_question'] += 1

#         if session['current_question'] >= question_no:
#             questions = session['questions']['results'][session['current_question']]['question']
#             return redirect(url_for('result'))

#     # if request.method == "POST":
#     #     print("POST BLOCK EXECUTED")

#     #     answer = request.form.get("answer")

#     #     if answer == correct_answer:
#     #         session["score"] += 1

#     #     session["current_question"] += 1

#     #     print("After Increment:", session["current_question"])

#     # print("----------------------")
#     # print("Method:", request.method)
#     # print("Current:", session["current_question"])
#     # print("Total:", question_no)


#     return render_template('quiz.html', question = questions, options = options)


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():

    question_no = len(session['questions']['results'])

    # ---------- User submitted an answer ----------
    if request.method == "POST":

        current = session['questions']['results'][session['current_question']]

        answer = request.form.get("answer")

        if answer == current["correct_answer"]:
            session["score"] += 1

        session["current_question"] += 1

        if session["current_question"] >= question_no:
            return redirect(url_for("result"))

        return redirect(url_for("quiz"))

    # ---------- Show current question ----------

    current = session['questions']['results'][session['current_question']]

    question = current["question"]

    options = current["incorrect_answers"].copy()
    options.append(current["correct_answer"])
    r.shuffle(options)

    progress = ((session['current_question']) / question_no) * 100

    return render_template(
        "quiz.html",
        question=question,
        options=options,
        progress=progress,
        current=session['current_question'] + 1,
        total=question_no
    )


@app.route('/result')
def result():

    score = session['score']
    per = ( score / len( session['questions']['results'])) * 100
    if 90 <= per <= 100:
        grade = 'A'
        comment = 'Well Done Hero !!'
    elif 80 <= per < 90:
        grade = 'B'
        comment = 'Keep Going !!'
    elif 70 <= per < 80:
        grade = 'C'
        comment = 'Can Do Better !!'
    elif 60 <= per < 70:
        grade = 'D'
        comment = 'Not Bad !!'
    elif 50 <= per < 60:
        grade = 'E'
        comment = 'Need To Work Hard !!'
    else :
        grade = 'F'
        comment = 'Not Quite Good, But you Can Do Better !!'

    return render_template('result.html', score = score, per = per, grade = grade, comment = comment)


if __name__ == "__main__":
    app.run(debug=True)