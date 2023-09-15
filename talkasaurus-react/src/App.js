import logo from './logo.svg';
import './App.css';
import io from "socket.io-client";

let socket = io("http://localhost:8080");    // connect this to the server
socket.on("connect", () => {});

function handleAudioFile(file) {
    let audio = new Audio(file);
    audio.play();
}
function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
