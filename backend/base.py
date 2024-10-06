from flask import Flask 
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})  # Allow requests from your React frontend

@app.route('/home', methods=['GET'])
def home():
  response_body = {
    "name": "Nagato",
    "about" :"Hello! I'm a full stack developer that loves python and javascript"
  }
  return response_body, 200