from flask import Flask, render_template, request, jsonify, session
import json
import os
import hashlib

app = Flask(__name__)
app.secret_key = "your_secret_key"

DB_FILE = 'db.json'

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
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
    if not data:
        return jsonify({'message': 'Invalid request! No data received'}), 400

    name = data.get('name')
    password = data.get('password')
    contact = data.get('contact')
    location = data.get('location')
    amount = data.get('amount')
    request_type = data.get('type')

    if not all([name, password, contact, location, amount, request_type]):
        return jsonify({'message': 'All fields are required!'}), 400

    try:
        amount = int(float(amount))  
    except ValueError:
        return jsonify({'message': 'Amount must be a valid number'}), 400

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    session['user_password'] = hashed_password  

    db = load_db()
    db.append({
        'name': name,
        'password': hashed_password,
        'contact': contact,
        'location': location,
        'amount': amount,
        'type': request_type
    })
    save_db(db)

    return jsonify({'message': 'Request submitted successfully!', 'redirect': '/dashboard'})

@app.route('/dashboard')
def dashboard():
    requests = load_db()
    user_password = session.get('user_password', '')
    return render_template('dashboard.html', requests=requests, user_password=user_password)

@app.route('/delete', methods=['POST'])
def delete_request():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')

    if not name or not password:
        return jsonify({'success': False, 'message': 'Invalid request'}), 400

    logged_in_password = session.get('user_password')
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    if logged_in_password != hashed_password:
        return jsonify({'success': False, 'message': 'Incorrect password! You can only delete your own requests.'}), 403

    db = load_db()
    updated_db = [req for req in db if not (req['name'] == name and req['password'] == hashed_password)]
    save_db(updated_db)

    return jsonify({'success': True, 'message': 'Request deleted successfully'})
