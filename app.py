from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

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

    db = load_db()
    db.append({'name': name, 'contact': contact, 'type': request_type})
    save_db(db)

    return jsonify({'message': 'Request submitted successfully!', 'redirect': '/dashboard'})

@app.route('/dashboard')
def dashboard():
    requests = load_db()
    return render_template('dashboard.html', requests=requests)

@app.route('/delete', methods=['POST'])
def delete_request():
    data = request.get_json()
    name = data.get('name')
    contact = data.get('contact')
    request_type = data.get('type')

    db = load_db()
    updated_db = [req for req in db if not (req['name'] == name and req['contact'] == contact and req['type'] == request_type)]

    if len(updated_db) == len(db):
        return jsonify({'success': False, 'message': 'Request not found'}), 404

    save_db(updated_db)
    return jsonify({'success': True, 'message': 'Request deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
