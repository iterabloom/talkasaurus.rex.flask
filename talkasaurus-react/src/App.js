/*
TODO: add more error messages, especially around failed expectations of a conversational bot in a response

allows users to record their voice, and it reflects the conversation in real-time. 
It also fetches the conversation history database where the user can access their chat history at any point, 
and export those conversations in CSV format

This react app is divided into three main components:
  1. AudioRecorder: A react-based audio recorder to capture mic input from the user
  2. sendAudioFile: An async function to send the recorded audio to the backend
  3. base64toUint8Array: This function converts base64 data into Uint8Array which is the required format for the Audio() object.
*/

import React, { useEffect, useState } from 'react';
import { SocketProvider, useSocket } from './SocketContextPanel';
import axios from 'axios';
import './App.css';
import AudioRecorder from 'react-audio-recorder';

/*
The App function has been assigned as a constant with 3 core functions:
1: sendAudioFile sends the audio file data to the backend using FormData and axios.
2: base64ToUint8Array is essentially converting base64 data into Uint8Array which is the required format for the Audio() object of the context.
• It has main a listener setup for socket.on("response"). On receiving a response, it performs base64 conversion using the base64ToUnit8Array function that we created above and then creates an Object URL for the blob using the URL.createObjectURL function native to JavaScript.
• The socket's response also gets converted into an audio url which React can work with and is played directly in the browser.
*/
const App = () => {
  // Define state variables
  const [url, setUrl] = useState(null);
  const [conversation, setConversation] = useState([]);  
  const socket = useSocket();

  // Function to send audio file to backend
  const sendAudioFile = async (data) => {
    const formData = new FormData();
    formData.append('file', data.blob, 'audio.wav');
    try {
      await axios.post(`${process.env.REACT_APP_SERVER_URL}/audio_transcription`, formData);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  }

  // TODO: error handling for these fetch calls should be enhanced. When the APIs return non-OK responses 
  //       (4xx, 5xx status codes), these scenarios should be handled and appropriate error message should be displayed to the user
 
  // Fetch conversations from backend
  const fetchConversations = () => {
    axios.get("/api/conversations").then(res => {
      setConversation(res.data);
    });
  };

  // Export conversations as CSV
  const exportConversationsCSV = () => {
    let filename = 'conversations.csv';
    let contentType = 'text/csv';
    axios({
      url: '/api/conversations/csv',
      method: 'GET',
      responseType: 'blob',
    }).then((response) => {
      let blob = new Blob([response.data], {type: 'text/csv'});
      let link = document.createElement('a');
      link.href = window.URL.createObjectURL(blob);
      link.download = filename;
      link.click();
    });
  };

  // Convert base64 data to Uint8Array as required by Audio()
  const base64ToUint8Array = (base64) => {
    const binary_string = atob(base64);
    const len = binary_string.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
        bytes[i] = binary_string.charCodeAt(i);
    }
    return bytes;
  }

  // React useEffect hook to setup socket response listener and fetch conversation history
  useEffect(() => {
    socket.on("response", (res) => {
      // Convert response to ObjectURL and play the audio
      const audioBlob = new Blob([base64ToUint8Array(res.audio_data)], { type: 'audio/mpeg' });
      const url = URL.createObjectURL(audioBlob);

      const audio = new Audio(url);
      audio.play();
      fetchConversations(); // Re-fetch conversations on every response
    });
  }, [socket]);

  return (
    <SocketProvider>
      // Printable UI for the application
      <AudioRecorder sendFile={sendAudioFile} />
      <h1>Conversations</h1>
      <button className="btn btn-primary" onClick={fetchConversations}>Refresh</button>
      <button className="btn btn-info" onClick={exportConversationsCSV}>Export CSV</button>
      {conversation.map((item, index) => (
        <div className="conversation-item">
          <p>{item.User}: {item.Response}</p>
        </div>
      ))}
    </SocketProvider>
  );
}

export default App;


//The React app only works in development mode for now. The complete and deploy-ready application requires more work. For instance, Docker related scripts need to be edited to reflect this change. 


//TODO: one test checks if the Refresh button fetches the conversation data and another checks if the audio plays upon recording and receiving responses
