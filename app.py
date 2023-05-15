from flask import Flask, request, jsonify, send_from_directory, redirect, url_for
import json
from answer_questions import answer_question

app = Flask(__name__)


@app.route('/<path:path>')
def serve_static(path):
  # Serve file from public directory
  return send_from_directory('public', path)


@app.route('/')
def index():
  return send_from_directory('public', 'index.html')


@app.route('/new', methods=['POST', 'GET'])
def new():
  "hey there!"


@app.route('/ask', methods=['POST'])
def ask():
  # Get message from request body
  data = json.loads(request.data)
  print("Data: " + str(request.data))
  # Extract transcript and promptType from data
  transcript = data['transcript']
  last_message = transcript[-1]["text"]
  print("Message: " + str(last_message))
  answer = answer_question(last_message)
  print("Answer: " + str(answer))
  return str(answer)


@app.errorhandler(Exception)
def error(e):
  print("error: " + str(e))
  print(request.url)
  return "error! " + str(e)


def run():
  app.run(host='0.0.0.0')
