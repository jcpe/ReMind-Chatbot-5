from flask import Flask, request, jsonify, send_from_directory, redirect, url_for
import json
from answer_questions import answer_question
from create_knowledge_base import construct_base_from_directory
from answer_questions import answer_question, answer_questions
from langchain.agents import Tool
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent
from langchain import LLMMathChain

app = Flask(__name__)
llm = ChatOpenAI(temperature=0, model="gpt-4")
llm_math = LLMMathChain.from_llm(llm)

tools = [
  Tool(
    name="Readwise Reading Summarizer",
    description=
    "Useful for questions about books, concepts, ideas, definitions of terms, and more. A tool that can summarize the answers to questions from a user's Readwise book, article, and paper highlights. Please provide a full question.",
    func=lambda q: str(answer_question(q)),
    return_direct=True),
  Tool(
    name="Calculator",
    description=
    "Useful for when you need to do math or calculate expressions. Please provide an expression.",
    func=llm_math.run,
    return_direct=True)
]

memory = ConversationBufferMemory(memory_key="chat_history")
agent_chain = initialize_agent(tools,
                               llm,
                               agent="conversational-react-description",
                               memory=memory)


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
  print("Data: " + str(request.data))
  # Extract transcript and promptType from data
  transcript = data['transcript']
  last_message = transcript[-1]["text"]
  print("Message: " + str(last_message))
  answer = agent_chain.run(input=last_message)
  # answer = safely_run_agent_chain(last_message)
  print("Answer: " + str(answer))
  return str(answer)


@app.errorhandler(Exception)
def error(e):
  print("error: " + str(e))
  print(request.url)
  return "error! " + str(e)


def run():
  app.run(host='0.0.0.0')
