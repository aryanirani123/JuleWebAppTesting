from flask import Flask, render_template, request, redirect
# Removed: import json
# Removed: import os
from firestore_service import add_feedback, get_feedback # Added

app = Flask(__name__)
# Removed: FEEDBACK_FILE = 'feedback.json'

# Removed: load_feedback() function
# Removed: save_feedback() function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    message = request.form['message']
    try:
        add_feedback(name, message) # Changed
    except ValueError as e:
        # Handle potential errors from add_feedback, e.g., empty name/message
        # You might want to flash a message to the user or render an error page
        print(f"Error submitting feedback: {e}") # Or use proper logging
        # For now, just redirecting, but in a real app, provide user feedback
        return redirect('/') # Or to a page indicating an error
    return redirect('/feedback')

@app.route('/feedback')
def feedback():
    try:
        feedback_items = get_feedback() # Changed
    except Exception as e:
        # Handle potential errors from get_feedback
        print(f"Error fetching feedback: {e}") # Or use proper logging
        feedback_items = [] # Present an empty list on error
    return render_template('feedback.html', feedback=feedback_items) # Changed variable name

if __name__ == '__main__':
    app.run(debug=True)
