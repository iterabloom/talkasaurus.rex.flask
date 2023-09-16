import logo from './logo.svg';
import './App.css';
import io from "socket.io-client";
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import AudioRecorder from 'react-audio-recorder';
import { SocketProvider } from './SocketContextPanel'; // import the SocketProvider

const socket = io(process.env.REACT_APP_SERVER_URL);
socket.on("connect", () => {});
socket.on('voice', (data) => {
  const audioBlob = new Blob([base64ToUint8Array(data.audio_data)], { type: 'audio/mpeg' });
  const url = URL.createObjectURL(audioBlob);
  
  const audio = new Audio(url);
  audio.play();
});

function base64ToUint8Array(base64) {
    const binary_string = atob(base64);
    const len = binary_string.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
        bytes[i] = binary_string.charCodeAt(i);
    }
    return bytes;
}

const App = () => {
  const [url, setUrl] = useState(null)
  const sendAudioFile = async (data) => {
    const formData = new FormData();
    formData.append('file', data.blob, 'audio.wav');
    try {
      await axios.post(`${process.env.REACT_APP_SERVER_URL}/audio_transcription`, formData);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  }

  // Wrap the AudioRecorder component with the SocketProvider
  return (
    <SocketProvider>
      <AudioRecorder sendFile={sendAudioFile} />
    </SocketProvider>
  );
}

export default App;