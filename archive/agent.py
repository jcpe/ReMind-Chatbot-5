import logging
import sys
from llama_index import GPTSimpleVectorIndex

from langchain.agents import Tool
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent


def query(q):
  index = GPTSimpleVectorIndex.load_from_disk("readwise.json")
  print("Got question: " + str(q))
  return str(index.query(q))


def start_agent():
  logging.basicConfig(stream=sys.stdout, level=logging.INFO)
  logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

  tools = [
    Tool(
      name="Reading Summarizer",
      description=
      "useful for when you need to answer questions from a user's book, article, and paper highlights. please input the user's entire question",
      func=query,
      return_direct=True)
  ]

  memory = ConversationBufferMemory(memory_key="chat_history")
  llm = ChatOpenAI(temperature=0)
  agent_chain = initialize_agent(tools,
                                 llm,
                                 agent="conversational-react-description",
                                 memory=memory,
                                 verbose=True)
  print(agent_chain.run(input="Hey there! My name is Dan"))
  print(agent_chain.run(input="What do my reading highlights say about love?"))
  print(agent_chain.run(input="What do my reading highlights say about suffering?"))
  print(agent_chain.run(input="What's my name?"))
