import '../../style.css'

function ChatHistory() {
    return (
      <div className="chat-history">
        <div className="title">
            <p className="previous-chats">Previous Chats:</p>
        </div>
        <div className="content">
            <div className="chats"></div>
        </div>
      </div>
    );
  }
  
export default ChatHistory;