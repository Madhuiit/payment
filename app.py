from flask import Flask, render_template, request, jsonify, session
import json
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session management

DB_FILE = 'db.json'

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as file:
            return json.load(file)
    return []

def save_db(data):
    with open(DB_FILE, 'w') as file:
        json.dump(data, file, indent=2)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    name = data.get('name')
    contact = data.get('contact')
    request_type = data.get('type')

    if not name or not contact or not request_type:
        return jsonify({'message': 'All fields are required!'}), 400

    # Store the user's contact in session
    session['user_contact'] = contact  

    db = load_db()
    db.append({'name': name, 'contact': contact, 'type': request_type})
    save_db(db)

    return jsonify({'message': 'Request submitted successfully!', 'redirect': '/dashboard'})

@app.route('/dashboard')
def dashboard():
    requests = load_db()
    user_contact = session.get('user_contact', '')  # Get logged-in user contact
    return render_template('dashboard.html', requests=requests, user_contact=user_contact)

@app.route('/delete', methods=['POST'])
def delete_request():
    data = request.get_json()
    name = data.get('name')
    contact = data.get('contact')
    request_type = data.get('type')

    # Get the logged-in user's contact from session
    logged_in_contact = session.get('user_contact')

    if not logged_in_contact or logged_in_contact != contact:
        return jsonify({'success': False, 'message': 'You can only delete your own requests!'}), 403

    db = load_db()
    updated_db = [req for req in db if not (req['name'] == name and req['contact'] == contact and req['type'] == request_type)]

    if len(updated_db) == len(db):
        return jsonify({'success': False, 'message': 'Request not found'}), 404

    save_db(updated_db)
    return jsonify({'success': True, 'message': 'Request deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
