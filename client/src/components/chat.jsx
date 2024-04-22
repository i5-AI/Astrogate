import '../../style.css'
import './arrow.css'
import { h, Component, Fragment } from 'preact';

export default class Chat extends Component {
  constructor(props) {
    super(props);
    this.state = {
        userInput: '',
        messages: [{
          text: "Hello, I’m Astrogate. A chatbot designed for Air Force and Space Force cadets on queries regarding the Tongue and Quill, Dress and Ceremonies, marching, and more. My information comes directly from Air Force documents, and I will provide sources for my responses. Please, ask me a question!",
          sender: 'ai'
        }]
    };
    this.userInputRef = null;
  }

  simulateAIResponse = (userInput) => {
    console.log('TESTING!!!')
    const apiUrl = 'http://localhost:3000/api/data'; // Flask API URL
    fetch(apiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
      body: JSON.stringify({ question: "testing, 1, 2, 3" }),
    })
    .then(response => {
      if (response.ok) {
        console.log("RESPONSE", response)
        return response.json(); // Parse as JSON instead of text
      } else {
        throw new Error('Network response was not ok: ' + response.statusText);
      }
    })
    .then(data => {
      // Now 'data' will be the parsed JSON object from the server
      console.log('Received data:', data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }


//   simulateAIResponse = (userInput) => {
//     const apiUrl = 'http://localhost:5000/'; // Flask API URL

//     fetch(apiUrl, {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({ question: userInput }),
//     })
//     .then(response => response.text()) // Assuming the response is plain text or HTML
//     .then(text => {
//         this.setState(prevState => ({
//             messages: [...prevState.messages, { text: text, sender: 'ai' }]
//         }));
//     })
//     .catch(error => {
//         console.error('Error:', error);
//         this.setState(prevState => ({
//             messages: [...prevState.messages, { text: "Error processing request.", sender: 'ai' }]
//         }));
//     });
// }

  // simulateAIResponse = (userInput) => {
  //   console.log('User input:', userInput);
  //   // Prepare the request URL and payload
  //   const apiUrl = 'http://localhost:5000/'; // Adjust with your actual Flask API URL
  //   const payload = {
  //     question: userInput,
  //     // Add any other data required by your API
  //   };

  //   fetch(apiUrl, {
  //     method: 'POST',
  //     headers: {
  //       'Content-Type': 'application/json',
  //       'Access-Control-Allow-Origin': '*'
  //     },
  //     body: JSON.stringify(payload),
  //   })
  //   .then(response => {
  //     if (!response.ok) {
  //       console.log("RESPONSE", response);
  //       throw new Error('Network response was not ok');
  //     }
  //     return response.json();
  //   })    
  //   .then(data => {
  //     // Handle the response from your Flask API
  //     const aiResponse = data.answer; // Adjust this according to the actual response format

  //     // Add AI response to the state
  //     this.setState(prevState => ({
  //       messages: [...prevState.messages, { text: aiResponse, sender: 'ai' }],
  //     }));
  //   })
  //   .catch(error => {
  //     // Handle any errors
  //     console.error('Error:', error);
  //     const aiResponse = "I'm sorry, there was an error processing your request.";

  //     // Add error response to the state
  //     this.setState(prevState => ({
  //       messages: [...prevState.messages, { text: aiResponse, sender: 'ai' }],
  //     }));
  //   });
  // }

  handleSubmit = () => {
    const userInputTrimmed = this.userInputRef.value.trim();
    if (userInputTrimmed) {
      this.setState(prevState => ({
        messages: [...prevState.messages, { text: userInputTrimmed, sender: 'user' }],
        userInput: ''
      }), () => {
        this.userInputRef.value = '';
        this.simulateAIResponse(userInputTrimmed);
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
            <div key={index} className={`chat-bubble ${message.sender === 'ai' ? 'ai-message' : 'user-message'}`}>
            {message.text}
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
        <button className="submit-message">
          <div class="container2">
            <div id="submit" class="arrow-and-circle" onClick={this.handleSubmit}>
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