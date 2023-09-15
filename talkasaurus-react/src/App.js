import logo from './logo.svg';
import './App.css';
import io from "socket.io-client";
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Recorder from 'react-mp3-recorder'

let socket = io("http://localhost:8080");    // connect this to the server
socket.on("connect", () => {});

const AudioRecorder = () => {
  const [url, setUrl] = useState(null)

  const handleAudioStop = (data) => {
    console.log(' onStop: ', data)
    setUrl(URL.createObjectURL(data.blob))
  }

  const handleAudioUpload = (data) => {
    console.log(' onUpload: ', data)
    axios.post('http://localhost:5000/audio_transcription', data.blob, {
      headers: {
        'Content-Type': 'audio/mpeg',
      }
    })
  }

  const handleAudioError = (err) => {
    console.log(' onError: ', err)
  }

  return (
    <div>
      <Recorder
        onStop={handleAudioStop}
        onUpload={handleAudioUpload}
        onError={handleAudioError}
      />
 
      <audio src={url} controls />
    </div>
  )
}

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
