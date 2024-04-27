// @ts-nocheck
import '../../style.css'
import './arrow.css'
import { Component, createRef } from 'preact';
import axios from 'axios';

export default class Chat extends Component {
  constructor(props) {
    super(props);
    this.state = {
        userInput: '',
        messages: [{
          text: "Hello, I’m Astrogate. A chatbot designed for Air Force and Space Force cadets on queries regarding the Tongue and Quill, Dress and Ceremonies, marching, and more. My information comes directly from Air Force documents, and I will provide sources for my responses. Please, ask me a question!",
          sender: 'ai',
          globalDocumentText: '' // temporary storage for the document text
        }],
        isThinking: false

    };
    this.userInputRef = createRef();
  }

  //function to respond to enter key or clicking arrow
  handleSubmit = () => {
    const userInputTrimmed = this.userInputRef.current.value.trim();
    if (userInputTrimmed) {
      this.setState(prevState => ({
        messages: [...prevState.messages, { text: userInputTrimmed, sender: 'user' }],
        userInput: ''
      }), () => {
        this.userInputRef.current.value = '';
        this.submitQuery(userInputTrimmed);
      });
    } else {
      console.log('No query to send.');
    }
  };

  //function to create embedding from the question
  submitQuery = (userQuery) => {
    this.setState({ isThinking: true });
    /* axios.post('https://chat.i5space.com:3000/create-embedding', {
      query: userQuery
    })
    .then(response => {
      const answer = response.data.answer;
      this.setState(prevState => ({
        messages: [...prevState.messages, { text: answer, sender: 'ai' }]
      }));
      this.setState({ isThinking: false });
    })
    .catch(error => {
      this.setState({ isThinking: false });
      console.error("Error:", error);
    }); */
    this.setState({ isThinking: true });
    
    setTimeout(() => {
      this.setState({ isThinking: false });
      const fullMessage = "Thank you for your interest in the Astrogate chatbot. Currently the chatbot is still in beta testing, full functionality will be available in the coming weeks.";
      this.typeMessage(fullMessage.split(" "), 0);
    }, 2000); 
  };

  typeMessage = (words, index) => {
    if (index < words.length) {
      let nextMessage = [...this.state.messages];
      if (nextMessage.length === 0 || nextMessage[nextMessage.length - 1].sender !== 'ai') {
        nextMessage.push({ text: '', sender: 'ai', globalDocumentText: '' });
      }
  
      const lastAiMessageIndex = nextMessage.length - 1;
      nextMessage[lastAiMessageIndex].text += (index === 0 ? '' : ' ') + words[index];
  
      this.setState({
        messages: nextMessage,
      });
      setTimeout(() => this.typeMessage(words, index + 1), 150);
    }
  };
  

  handleInputChange = (e) => {
    if (e.key === 'Enter') {
      this.handleSubmit();
    } else {
      this.setState({ userInput: e.target.value });
    }
  };

  scrollToBottom = () => {
    const chatContainer = document.querySelector('.user-chats');
    // Get the offsetHeight of the thinking dots, if they exist.
    const thinkingDots = document.querySelector('.thinking-dots');
    const thinkingDotsHeight = thinkingDots ? thinkingDots.offsetHeight : 0;
  
    // Use chatContainer.scrollHeight to include the height of the content and the dots.
    chatContainer.scrollTop = chatContainer.scrollHeight + thinkingDotsHeight;
  };
  
  componentDidUpdate(prevProps, prevState) {
    if (prevState.messages.length < this.state.messages.length || this.state.isThinking) {
      this.scrollToBottom();
    }
  }
  

  render() {
    return (
      <div className="chat">
        <div className="chat-title">
          <p>Astrogate</p>
        </div>
        <div className="chats-container">
          <div className="astrogate-chats"></div>
          <div className="user-chats">
            {this.state.messages.map((message, index) => (
              <div key={index} className={`chat-bubble ${message.sender === 'ai' ? 'ai-message' : 'user-message'}`}>
                {message.text}
              </div>
            ))}
            {this.state.isThinking && <div className="thinking-dots">
              <div className="dot"></div>
              <div className="dot"></div>
              <div className="dot"></div>
            </div>}
          </div>
        </div>
        <div className="messages">
          <div className="bar">
            <div className="message-bar">
              <input
                ref={this.userInputRef}
                className="input-text"
                type="text"
                placeholder="Type a message..."
                value={this.state.userInput} 
                onChange={this.handleInputChange} 
                onKeyPress={this.handleInputChange}
              />
            </div>
            <button className="submit-message" onClick={this.handleSubmit}>
              <div className="container2">
                <div id="submit" className="arrow-and-circle">
                  <div className="icono-arrow1-up arrow"></div>
                  <div className="circle"></div>
                </div>
              </div>
            </button>
          </div>
        </div>
      </div>
    );
  }
};  