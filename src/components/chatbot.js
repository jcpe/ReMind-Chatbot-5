import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

const Chatbot = () => {
  // Array of different prompts
  const prompts = [
    'Welcome! Can you share with me the particular issue or question you need assistance with today?',
    'Hi there! What specific challenge can I help you tackle right now?',
    'Greetings! I\'m here to help. What\'s the exact problem you\'re facing that you\'d like some assistance with?',
    'Hello! To better assist you, could you describe the particular problem or topic you need help with?',
    'Good day! What specific issue or question brings you here today that I can help with?',
    'Hi! I\'m ready to assist. Can you tell me about the specific challenge or query you have in mind?',
    'Welcome aboard! What particular problem or question do you need help solving today?',
    'Hello! I\'m your assistant for today. Could you specify the problem or area where you\'re seeking assistance?',
    'Hi! Let\'s get started. What specific issue or challenge can I assist you with today?',
    'Greetings! To offer the best assistance, could you please tell me about the specific problem or question you have? This stuff'
  ];

  // Function to get a random prompt
  const getRandomPrompt = () => {
    const randomIndex = Math.floor(Math.random() * prompts.length);
    console.log(prompts[randomIndex]);
    return prompts[randomIndex];
  };

  const [messages, setMessages] = useState([{ sender: 'bot', text: getRandomPrompt() }]);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages]);

  const sendMessage = async () => {
    if (input.trim() === '') return;

    const newMessages = [...messages, { sender: 'user', text: input }];
    setMessages(newMessages);
    setInput('');

    try {
      const response = await axios.post('/ask', { transcript: newMessages }, { withCredentials: true });
      const botMessage = response.data;
      setMessages((prevMessages) => [...prevMessages, { sender: 'bot', text: botMessage }]);
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <>
      <div className="chatbot-header">Re:Mind</div>
      <div className="chatbot">
        <div className="messages">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.sender}`}>
              {message.text}
            </div>
          ))}
          <div ref={messagesEndRef}></div>
        </div>
        <div className="input-area">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          />
          <button onClick={sendMessage}>Send</button>
        </div>
      </div>
    </>
  );
  };

export default Chatbot;
