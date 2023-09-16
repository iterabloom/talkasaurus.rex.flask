import logo from './logo.svg';
import './App.css';
import io from "socket.io-client";
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import Recorder from 'react-mp3-recorder'

// Utility function
function base64ToUint8Array(base64) {
  const binary_string = atob(base64);
  const len = binary_string.length;
  const bytes = new Uint8Array(len);
  for (let i = 0; i < len; i++) {
      bytes[i] = binary_string.charCodeAt(i);
  }
  return bytes;
}


let socket = io("http://localhost:8080");    // connect this to the server
socket.on("connect", () => {});

socket.on('response', (data) => {
  const audioBlob = new Blob([base64ToUint8Array(data.audio_data)], { type: 'audio/mpeg' });
  const url = URL.createObjectURL(audioBlob);
  audioRef.current.src = url;  // audioRef is a ref to an <audio> element
});

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
    //TODO: may need more handling logic here
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
  const handleAudioUpload = async (data) => {
    try {
      const formData = new FormData();
      formData.append('file', data.blob);
      const res = await axios.post('http://localhost:5000/audio_transcription', formData);
    } catch (error) {
      console.log('Error uploading file:', error);
    }
  }
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