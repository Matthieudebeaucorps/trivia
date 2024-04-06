from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os
import random

app = Flask(__name__)
app.secret_key = 'abc124'  # Your chosen secret key

categories_dir = '/Users/matthieudebeaucorps/Desktop/Projects/OpenTriviaQA/categories_csv'
categories = ["animals", "geography", "history", "literature", "movies", "music", "science-technology", "sports", "video-games", "world"]

def load_question(category):
    df = pd.read_csv(os.path.join(categories_dir, f"{category}.csv"))
    question_row = df.sample().iloc[0]
    return question_row

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['teams'] = {
            'team1': request.form.get('team1', ''),
            'team2': request.form.get('team2', ''),
            'team3': request.form.get('team3', ''),
            'team4': request.form.get('team4', ''),
        }
        return redirect(url_for('choose_category'))
    return render_template('index.html', categories=categories)

@app.route('/choose_category')
def choose_category():
    if 'teams' not in session or all(value == '' for value in session['teams'].values()):
        # Redirect to index if teams not set
        return redirect(url_for('index'))
    return render_template('choose_category.html', categories=categories)

@app.route('/question', methods=['GET', 'POST'])
def question():
    category = request.args.get('category')
    if not category or category not in categories:
        return redirect(url_for('choose_category'))
    
    question_row = load_question(category)
    if request.method == 'POST':
        team_key = request.form.get('team')
        user_answer = request.form.get('answer')
        correct_answer = question_row['Correct']
        feedback = "Correct!" if user_answer == correct_answer else "Incorrect!"
        return render_template('answer.html', feedback=feedback, correct_answer=correct_answer, question_row=question_row)
    
    return render_template('question.html', question_row=question_row, teams=session.get('teams'))

if __name__ == '__main__':
    app.run(debug=True)