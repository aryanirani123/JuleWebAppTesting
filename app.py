from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)
FEEDBACK_FILE = 'feedback.json'

def load_feedback():
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, 'r') as f:
            return json.load(f)
    return []

def save_feedback(name, message):
    feedback = load_feedback()
    feedback.append({'name': name, 'message': message})
    with open(FEEDBACK_FILE, 'w') as f:
        json.dump(feedback, f, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    message = request.form['message']
    save_feedback(name, message)
    return redirect('/feedback')

@app.route('/feedback')
def feedback():
    feedback = load_feedback()
    return render_template('feedback.html', feedback=feedback)

if __name__ == '__main__':
    app.run(debug=True)
