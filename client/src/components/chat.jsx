import '../../style.css'
import './arrow.css'
import { Component } from 'preact'; 

export default class Chat extends Component {
  constructor(props) {
      super(props);
      this.state = {
          userInput: '',
          messages: []
      };
      this.userInputRef = null;
  }

  handleSubmit = () => {
    const userInputTrimmed = this.userInputRef.value.trim();
    if (userInputTrimmed) {
      this.setState(prevState => ({
        messages: [...prevState.messages, userInputTrimmed],
        userInput: ''
      }), () => {
        this.userInputRef.value = '';
      });
    } else {
      console.log('No query to send.');
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
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }

  componentDidUpdate(prevProps, prevState) {
    if (prevState.messages.length < this.state.messages.length) {
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
          <div key={index} className="chat-bubble">
            {message}
          </div>
            ))}
        </div>
      </div>
      <div className="messages">
        <div className="message-bar">
        <input
          ref={el => this.userInputRef = el}
          className="input-text"
          type="text"
          placeholder="Type a message..."
          value={this.state.userInput} 
          onChange={this.handleInputChange} 
          onKeyPress={this.handleInputChange}
        />
        </div>
        <button className="submit-message" onClick={this.handleSubmit}>
          <div class="container2">
            <div id="submit" class="arrow-and-circle">
              <div class="icono-arrow1-up arrow"></div>
              <div class="circle"></div>
            </div>
          </div>
        </button>
      </div>
    </div>
        );
      }
  }