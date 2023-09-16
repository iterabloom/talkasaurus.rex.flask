from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO
import openai
import os

# Pull the OpenAI API key from the environment variables
openai.api_key = os.environ.get('OPENAI_API_KEY')

from google.cloud import speech_v1p1beta1 as speech
from google.cloud import texttospeech
from queue import Queue
import base64

# BufferStream to handle audio buffering
class BufferStream(Queue):
    def __init__(self, buffer_size):
        # Initialise a Queue with a maximum buffer size
        super().__init__(maxsize=buffer_size)

    # read the audio from the Queue 
    def read(self):
        return self.get()

class BufferStream(Queue):
    # initialize the queue with the intended size
    def __init__(self, buffer_size):
        super().__init__(maxsize=buffer_size)

# Handle the transcription of the audio stream into text
def transcribe_audio_stream(stream):
    client = speech.SpeechClient()

    config=speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_speaker_diarization=True,
        diarization_speaker_count=2
    )

    stream_buffer = BufferStream(5)

    for chunk in stream:
        stream_buffer.put(chunk)
        if stream_buffer.full(): 
            # extract audio_content in chunks from buffer
            audio_content = stream_buffer.get_nowait() 
            request = speech.StreamingRecognizeRequest(audio_content=audio_content)
            
            # communicate with the API and get the response
            responses = client.streaming_recognize(config, [request])
            for response in responses:
                # TODO: implement the operation

# Produce speech audio from the text
def convert_text_to_speech(text: str):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code="en-US",
                                              ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    audio_data = response.audio_content

    # Emit the data directly to the frontend
    socketio.emit('response', {'audio_data': base64.b64encode(audio_data).decode()})

# Save the conversation
def storeConversationData(user_message, response):
    # TODO: implement the functionality

def generate_ai_response(user_message: str) -> str:   
    conversation = {
        'messages': [{"role": "user", "content": f"{user_message}"}]
    }

    response = openai.ChatCompletion.create(model="gpt-4", messages=conversation['messages'],
                                            max_tokens=150)
    return response['choices'][0]['message']['content']

app = Flask(__name__, static_folder='talkasaurus-react/build')
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@socketio.on('message')
def handle_message(data):
    user_message = data['message']
    response = generate_ai_response(user_message)

    # send back the responses and user message
    convert_text_to_speech(response)
    socketio.emit('response', {'response': response, 'message': user_message})

    # save the conversation
    storeConversationData(user_message, response)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)