import '../../style.css'
import './arrow.css'

function Chat() {
    return (
    <div className="chat">
      <div className="chat-title">
        <p>Astrogate</p>
      </div>
      <div className="chats-container">
        <div className="astrogate-chats"></div>
        <div className="user-chats"></div>
      </div>
      <div className="messages">
        <div className="message-bar">
            <input className="input-text" type="text" placeholder="Type a message... "></input>
        </div>
        <button className="submit-message">
          <div class="container2">
            <div class="arrow-and-circle">
              <div class="icono-arrow1-up arrow"></div>
              <div class="circle"></div>
            </div>
          </div>
        </button>
      </div>
    </div>
    );
  }

  export default Chat;