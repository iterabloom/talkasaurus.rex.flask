/*
  This react app is divided into three main components:
  1. AudioRecorder: A react-based audio recorder to capture mic input from the user
  2. sendAudioFile: An async function to send the recorded audio to the backend
  3. base64toUint8Array: This function converts base64 data into Uint8Array which is the required format for the Audio() object.
*/

// Importing all the necessary modules
import logo from './logo.svg';
import './App.css';
import axios from 'axios';
import AudioRecorder from 'react-audio-recorder';
import { SocketProvider, useSocket } from './SocketContextPanel'; // import the SocketProvider and useSocket hook

/*
The App function has been assigned as a constant with 3 core functions:
1: sendAudioFile sends the audio file data to the backend using FormData and axios.
2: base64ToUint8Array is essentially converting base64 data into Uint8Array which is the required format for the Audio() object of the context.
• It has main a listener setup for socket.on("response"). On receiving a response, it performs base64 conversion using the base64ToUnit8Array function that we created above and then creates an Object URL for the blob using the URL.createObjectURL function native to JavaScript.
• The socket's response also gets converted into an audio url which React can work with and is played directly in the browser.
*/
const App = () => {
  const [url, setUrl] = useState(null)

  const sendAudioFile = async (data) => {
    const formData = new FormData();
    formData.append('file', data.blob, 'audio.wav');
    // Post request at local backend server using axios
    try {
      await axios.post(`${process.env.REACT_APP_SERVER_URL}/audio_transcription`, formData);
    } catch (error) {
      console.error('Error uploading file:', error);
    }
  }

  // Establishing a connection with the socket
  const socket = useSocket();

  // Function to convert base64 data to Uint8Array as required by Audio()
  const base64ToUint8Array = (base64) => {
    const binary_string = atob(base64);
    const len = binary_string.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
        bytes[i] = binary_string.charCodeAt(i);
    }
    return bytes;
  }

  // Setup a socket response listener on render
  useEffect(() => {
    socket.on("response", (res) => {
      // Convert response to ObjectURL and play the audio
      const audioBlob = new Blob([base64ToUint8Array(res.audio_data)], { type: 'audio/mpeg' });
      const url = URL.createObjectURL(audioBlob);

      const audio = new Audio(url);
      audio.play();
    	})
  	}, [socket]);  

  return (
    <SocketProvider>
      // Printable UI for the application
      <AudioRecorder sendFile={sendAudioFile} />
    </SocketProvider>
  );
}

export default App;