from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO
import openai
import os

openai.api_key = os.environ.get('OPENAI_API_KEY')

from google.cloud import speech_v1p1beta1 as speech


#This would require an audio stream chunked into parts to work most effectively, which would require changes based on the specific implementation of audio input.
def transcribe_audio_stream(stream):
    client = speech.SpeechClient()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_speaker_diarization=True,
        diarization_speaker_count=2,
    )

    requests = [
        speech.StreamingRecognizeRequest(audio_content=chunk)
        for chunk in stream
    ]

    responses = client.streaming_recognize(config, requests)

    for response in responses:
    	pass
        # Process responses


app = Flask(__name__, static_folder='talkasaurus-react/build')
socketio = SocketIO(app)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@socketio.on('message')
def handle_message(data):
    # Send the message to OpenAI's GPT4 model and produce a response
    response = generate_ai_response(data['message'])

    # Send the AI response back to the client
    socketio.emit('response', {'message': response})

def generate_ai_response(user_message): 
    response = openai.Completion.create(
        engine="text-davinci-003", 
        prompt=user_message, 
        max_tokens=150
    )
    return response['choices'][0]['text'].strip()


if __name__ == '__main__':
    socketio.run(app)