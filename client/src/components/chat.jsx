import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './Chat.css';

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isReady, setIsReady] = useState(false);
  const [isChecking, setIsChecking] = useState(true);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Check if backend is ready
    checkBackendStatus();
  }, []);

  const checkBackendStatus = async () => {
    try {
      setIsChecking(true);
      
      // Check backend status
      const statusResponse = await axios.get('http://localhost:8000/status');
      
      if (statusResponse.data.initialized) {
        setIsReady(true);
        setMessages([{
          id: 1,
          text: "Hello! I'm Astrogate, your Air Force and Space Force document assistant. I can help you find information from official military documents. What would you like to know?",
          sender: 'assistant',
          timestamp: new Date()
        }]);
      } else {
        // Backend is running but not initialized yet, wait and retry
        setTimeout(checkBackendStatus, 2000);
      }
    } catch (err) {
      console.error('Backend status check error:', err);
      // Backend not running, wait and retry
      setTimeout(checkBackendStatus, 2000);
    } finally {
      setIsChecking(false);
    }
  };

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      text: inputMessage,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await axios.post('http://localhost:8000/chat', {
        message: inputMessage
      });

      const assistantMessage = {
        id: Date.now() + 1,
        text: response.data.response,
        sender: 'assistant',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      console.error('Chat error:', err);
      
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'assistant',
        timestamp: new Date(),
        isError: true
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  if (isChecking) {
    return (
      <div className="chat-container">
        <div className="chat-header">
          <h1>Astrogate</h1>
          <p>Air Force & Space Force Document Assistant</p>
        </div>
        
        <div className="initialization-error">
          <h3>Starting Up...</h3>
          <p>Loading documents and initializing assistant...</p>
          <div className="loading-indicator">
            <div className="typing-dots">
              <div className="dot"></div>
              <div className="dot"></div>
              <div className="dot"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (!isReady) {
    return (
      <div className="chat-container">
        <div className="chat-header">
          <h1>Astrogate</h1>
          <p>Air Force & Space Force Document Assistant</p>
        </div>
        
        <div className="initialization-error">
          <h3>Connecting...</h3>
          <p>Waiting for backend to initialize. This may take a moment...</p>
          <div className="loading-indicator">
            <div className="typing-dots">
              <div className="dot"></div>
              <div className="dot"></div>
              <div className="dot"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h1>Astrogate</h1>
        <p>Air Force & Space Force Document Assistant</p>
        <div className="status-indicator">
          <span className="status-dot online"></span>
          Ready
        </div>
      </div>

      <div className="messages-container">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`message ${message.sender} ${message.isError ? 'error' : ''}`}
          >
            <div className="message-content">
              <div className="message-text">{message.text}</div>
              <div className="message-timestamp">
                {message.timestamp.toLocaleTimeString()}
              </div>
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="message assistant">
            <div className="message-content">
              <div className="loading-indicator">
                <div className="typing-dots">
                  <div className="dot"></div>
                  <div className="dot"></div>
                  <div className="dot"></div>
                </div>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      <div className="input-container">
        <div className="input-wrapper">
          <textarea
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask me about Air Force documents, uniforms, procedures..."
            disabled={isLoading}
            rows={1}
            className="message-input"
          />
          <button
            onClick={sendMessage}
            disabled={!inputMessage.trim() || isLoading}
            className="send-button"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
};

export default Chat; 