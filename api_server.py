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

# [Transition] Transcribe the audio stream into text
def transcribe_audio_stream(stream):
    client = speech.SpeechClient()

    # [New] Recognize multiple languages and dialects, and don't ignore non-word sounds
    config=speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,sample_rate_hertz=16000,language_code="en-US",enable_speaker_diarization=True,diarization_speaker_count=2)
    stream_buffer = BufferStream(5)

    for chunk in stream:
        stream_buffer.put(chunk)
        
        if stream_buffer.full(): 
            audio_content = stream_buffer.get_nowait() 
            request = speech.StreamingRecognizeRequest(audio_content=audio_content) 
            responses = client.streaming_recognize(config, [request]) 

            for response in responses:
                pass # replace with the real operation 

# [Transition] Produce speech audio from the text
# TODO clarify in comments how this function gets invoked (or if invocation is missing, create it)
def convert_text_to_speech(text: str):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    # Instead of writing to a file, emit the data directly to the frontend
    audio_data = response.audio_content
    socketio.emit('response', {'audio_data': base64.b64encode(audio_data).decode()})


def storeConversationData(user_message, response):
    pass # ToDo: implement functionality

def generate_ai_response(user_message: str) -> str: 
    conversation = {
        'messages': [
            {"role": "user", "content": user_message}
        ]
    }
   
    response = openai.ChatCompletion.create(model="gpt-4", messages=conversation['messages'], max_tokens=150)
    return response['choices'][0]['message']['content']

app = Flask(__name__, static_folder='talkasaurus-react/build')
socketio = SocketIO(app)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@socketio.on('message')
def handle_message(data):
    user_message = data['message']
    response = generate_ai_response(user_message)

    # [New] Send back the response and user message to the client
    socketio.emit('response', {'response': response, 'message': user_message})

    # [Transition] Store the conversation
    storeConversationData(user_message, response)

if __name__ == '__main__':
    socketio.run(app)