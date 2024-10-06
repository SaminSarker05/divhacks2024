from flask import Flask, render_template, request, redirect, url_for, flash
from flask_cors import CORS
from pymongo import MongoClient


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # Allow requests from your React frontend

client = MongoClient("mongodb+srv://saminsarker05:MrutdMWZtMlwi5JU@cluster0.oyvge.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client.flask_db
todos = db.todos

# ...
@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method=='POST':
        content = request.form['content']
        degree = request.form['degree']
        todos.insert_one({'content': content, 'degree': degree})
        return redirect(url_for('index'))

    all_todos = todos.find()
    return render_template('index.html', todos=all_todos)

@app.route('/home', methods=['GET'])
def home():
  response_body = {
    "name": "Nagato",
    "about" :"Hello! I'm a full stack developer that loves python and javascript"
  }
  return response_body, 200