from flask import Flask, render_template, request, redirect, url_for
import json
import os
from crypto_utils import encrypt_password, decrypt_password

app = Flask(__name__)

DATA_FILE = 'database.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump({'voters': {}, 'votes': {}}, f)
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = load_data()
    if request.method == 'POST':
        voter_id = request.form['voter_id']
        password = request.form['password']
        if voter_id not in data['voters']:
            data['voters'][voter_id] = encrypt_password(password)
            save_data(data)
            msg = "Registration successful!"
        else:
            msg = "Voter ID already registered."
        return render_template('index.html', message=msg)
    return render_template('index.html')

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    data = load_data()
    if request.method == 'POST':
        voter_id = request.form['voter_id']
        password = request.form['password']
        choice = request.form['candidate']
        if voter_id in data['voters'] and decrypt_password(data['voters'][voter_id]) == password:
            if voter_id not in data['votes']:
                data['votes'][voter_id] = choice
                save_data(data)
                return "Vote submitted!"
            else:
                return "You have already voted!"
        else:
            return "Invalid voter credentials."
    return '''
        <form method="post">
            Voter ID: <input name="voter_id"><br>
            Password: <input name="password" type="password"><br>
            Vote for:
            <select name="candidate">
                <option value="Alice">Alice</option>
                <option value="Bob">Bob</option>
            </select><br>
            <input type="submit" value="Vote">
        </form>
    '''

@app.route('/results')
def results():
    data = load_data()
    vote_counts = {}
    for vote in data['votes'].values():
        vote_counts[vote] = vote_counts.get(vote, 0) + 1
    return f"<h2>Results</h2><pre>{json.dumps(vote_counts, indent=2)}</pre>"

if __name__ == '__main__':
    app.run(debug=True)