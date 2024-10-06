from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_cors import CORS
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
import re

import ai_algorithms as ai  

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.secret_key = 'your_secret_key_here'  

client = MongoClient("mongodb+srv://saminsarker05:MrutdMWZtMlwi5JU@cluster0.oyvge.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.flask_db
users = db.users
bcrypt = Bcrypt(app)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = users.find_one({'username': username})  # Query MongoDB for the user

        if user and bcrypt.check_password_hash(user['password'], password):
            session['user'] = username  # Save username in the session
            return redirect(url_for('dashboard'))  # Redirect to dashboard after login
        else:
            return jsonify({"message": "Invalid credentials"}), 400

    return render_template('login.html')  # Render login page


@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html', username=session['user'])
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
