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

def validate_government_id(government_id):
    if re.match(r"^[A-Z0-9]{6,10}$", government_id):
        return True
    return False

def validate_ssn(ssn):
    if re.match(r"^\d{3}-\d{2}-\d{4}$", ssn):
        return True
    return False

def validate_banking_info(bank_info):
    if re.match(r"^\d{9,18}$", bank_info):
        return True
    return False

def calculate_eligibility(monthly_income, total_debt, savings, savings_goal, dependents, marital_status):
    contribution = ai.projected_safe_contribution(monthly_income, savings, total_debt, savings_goal, dependents, marital_status)
    
    if contribution > 0:
        return True, {"safe_contribution": contribution}
    else:
        return False, {"safe_contribution": contribution}

# @app.route('/login', methods=['POST']) 
# def login():   
#   data = request.json  # Access the JSON data from the request   
#   username = data['username']   
#   password = data['password']   
#   user = users.find_one({'username': username})   
#   if user and bcrypt.check_password_hash(user['password'], password):     
#     session['user'] = username     
#     return jsonify({"message": "login success"}), 400   
#   else:     
#     return jsonify({"message": "you don't exist"}), 400

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.json
        full_name = data.get('full_name')
        email = data.get('email')
        phone = data.get('phone')
        address = data.get('address')
        marital_status = data.get('marital_status')
        occupation = data.get('occupation')
        
        if not occupation:
            return jsonify({"message": "You need an occupation to continue"}), 400
        
        employer = data.get('employer')
        monthly_income = float(data.get('monthly_income'))
        total_debt = float(data.get('total_debt'))
        savings = float(data.get('savings'))
        savings_goal = float(data.get('savings_goal'))
        dependents = int(data.get('dependents'))
        
        government_id = data.get('government_id')
        ssn = data.get('ssn')
        banking_info = data.get('banking_info')

        if not validate_government_id(government_id):
            return jsonify({"message": "Invalid government ID"}), 400
        if not validate_ssn(ssn):
            return jsonify({"message": "Invalid SSN"}), 400
        if not validate_banking_info(banking_info):
            return jsonify({"message": "Invalid banking info"}), 400

        is_eligible, algorithm_results = calculate_eligibility(monthly_income, total_debt, savings, savings_goal, dependents, marital_status)
        
        if not is_eligible:
            return jsonify({"message": "User not eligible due to financial concerns or legal issues"}), 400
        
        user_data = {
            'full_name': full_name,
            'email': email,
            'phone': phone,
            'address': address,
            'marital_status': marital_status,
            'occupation': occupation,
            'employer': employer,
            'monthly_income': monthly_income,
            'total_debt': total_debt,
            'savings': savings,
            'savings_goal': savings_goal,
            'dependents': dependents,
            'government_id': government_id,
            'ssn': ssn,
            'banking_info': banking_info,
            'algorithm_results': algorithm_results
        }
        
        users.insert_one(user_data)
        return jsonify({"message": "User registered successfully", "algorithm_results": algorithm_results}), 201
    
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
