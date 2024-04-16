import { render } from 'preact';
import ChatHistory from "./components/chat-history";
import Chat from "./components/chat";
import '../style.css';

function App() {
  return (
    <div className="container poppins-light">
        <div className="box chat-history">
         <ChatHistory />
        </div>
      <div className="box chat-main">
        <Chat />
      </div>
    </div>
  );
}

render(<App />, document.getElementById('app'));