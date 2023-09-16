import logo from './logo.svg';
import './App.css';
import axios from 'axios';
import AudioRecorder from 'react-audio-recorder';
import { SocketProvider, useSocket } from './SocketContextPanel'; // import the SocketProvider and useSocket hook

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

  const socket = useSocket();

  useEffect(() => {
    socket.on("response", (res) => {
      const audioBlob = new Blob([base64ToUint8Array(res.audio_data)], { type: 'audio/mpeg' });
      const url = URL.createObjectURL(audioBlob);
    
      const audio = new Audio(url);
      audio.play();
    });
  }, [socket]);

  const base64ToUint8Array = (base64) => {
    const binary_string = atob(base64);
    const len = binary_string.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
        bytes[i] = binary_string.charCodeAt(i);
    }
    return bytes;
  }

  return (
    <SocketProvider>
      <AudioRecorder sendFile={sendAudioFile} />
    </SocketProvider>
  );
}

export default App;