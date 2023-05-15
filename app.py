from flask import Flask, request, jsonify, send_from_directory, redirect, url_for
import json

app = Flask(__name__)


@app.route('/<path:path>')
def serve_static(path):
  # Serve file from public directory
  return send_from_directory('public', path)


@app.route('/')
def index():
  return send_from_directory('public', 'index.html')


@app.route('/ask', methods=['POST'])
def ask():
  # Get message from request body
  data = json.loads(request.data)

  # # Extract transcript and promptType from data
  # transcript = data['transcript']
  # promptType = data['promptType']
  # messages = data['messages']
  # style = data['style']
  # persona = data['persona']
  # last_message = messages[-1]["message"]

  # # Generate response
  # response = answer_question(last_message)

  return "yooooo"


def run():
  app.run(host='0.0.0.0')
