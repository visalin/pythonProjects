"""
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        name = request.form['name']
        return render_template('greeting.html', name=name)
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
"""
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages
feedback_data = {}
@app.route('/', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form['name']
        feedback = request.form['feedback']
        if name and feedback:
            feedback_data['name'] = name
            feedback_data['feedback'] = feedback
            return redirect(url_for('greet'))
        else:
            flash('Please fill out both fields.', 'error')
            return redirect(url_for('feedback'))
    return render_template('feedback_form.html')

@app.route('/greet')
def greet():
    name = feedback_data.get('name')
    feedback = feedback_data.get('feedback')
    return render_template('greeting.html', name=name, feedback=feedback)

if __name__ == '__main__':
    app.run(debug=True)

#https://github.com/visalin/pythonProjects

""" Http error Codes :
                200 --Succuess -- Request was successful
                400 --Bad request --Request has invalid syntax
                401 --Unauthorized access --Client need to authorize the request
                403 --Forbidden --Client dosent have the access to access the request
                404 --Page not found -- Page not found
                408 -- Request timed out ---Session timed out waiting for the request
                500 --Internal server Error --Server is in unexpected condition to  process the request
                502,504 -- Bad Gateway ---Got a invalid response from the upstream server
                503 -- Service unavailable --- Server is not in responding to fulfill the request

"""
