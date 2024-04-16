import '../../style.css'

function ChatHistory() {
    return (
      <div className="chat-history">
        <div className="title">
            <p>Previous Chats:</p>
        </div>
        <div className="content">
            <div className="chats"></div>
        </div>
      </div>
    );
  }
  
export default ChatHistory;