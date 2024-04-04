from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
import random

app = Flask(__name__)

categories_dir = '/Users/matthieudebeaucorps/Desktop/Projects/OpenTriviaQA/categories csv'
categories = ["animals", "geography", "history", "literature", "movies", "music", "science-technology", "sports", "video-games", "world"]

def load_question(category):
    df = pd.read_csv(os.path.join(categories_dir, f"{category}.csv"))
    question_row = df.sample().iloc[0]
    return question_row

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', categories=categories)

@app.route('/question', methods=['GET', 'POST'])
def question():
    category = request.args.get('category')
    if not category or category not in categories:
        return redirect(url_for('index'))
    
    question_row = load_question(category)
    if request.method == 'POST':
        user_answer = request.form.get('answer')
        correct_answer = question_row['Correct']
        feedback = "Correct!" if user_answer == correct_answer else "Incorrect!"
        return render_template('answer.html', feedback=feedback, correct_answer=correct_answer, question_row=question_row)
    
    return render_template('question.html', question_row=question_row)

if __name__ == '__main__':
    app.run(debug=True)



