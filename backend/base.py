from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_cors import CORS
from pymongo import MongoClient
from flask_bcrypt import Bcrypt

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # * allows all origins (for development purposes)
app.secret_key = 'your_secret_key_here'  

client = MongoClient("mongodb+srv://saminsarker05:MrutdMWZtMlwi5JU@cluster0.oyvge.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client.flask_db
todos = db.todos
users = db.users

bcrypt = Bcrypt(app)


@app.route('/register', methods=['POST'])
def register():
  print('hello world')
  response_body = {
    "name": "Nagato",
    "about" :"Hello! I'm a full stack developer that loves python and javascript"
  }
  
  data = request.json  # Access the JSON data from the request
  username = data['username']
  password = data['password']
  print(password)

  hash_password = bcrypt.generate_password_hash(password).decode('utf-8')

  if users.find_one({"username": username}):
    return jsonify({"message": "Username already exists"}), 400
  
  users.insert_one({
    'username': username,
    'password': hash_password
  })
  return jsonify({"message": "User registered successfully"}), 201


@app.route('/login', methods=['POST'])
def login():

  data = request.json  # Access the JSON data from the request
  username = data['username']
  password = data['password']

  user = users.find_one({'username': username})
  if user and bcrypt.check_password_hash(user['password'], password):
    session['user'] = username 
    return jsonify({"message": "login success"}), 400
  else:
    return jsonify({"message": "you don't exist"}), 400





@app.route('/test', methods=['GET'])
def home():
  response_body = {
    "name": "Nagato",
    "about" :"Hello! I'm a full stack developer that loves python and javascript"
  }
  return jsonify(response_body), 200