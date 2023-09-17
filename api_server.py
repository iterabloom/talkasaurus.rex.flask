import logging
from flask import Flask, send_from_directory
from flask_socketio import SocketIO
import openai
import os

# OpenAI api key
openai.api_key = os.environ.get('OPENAI_API_KEY')

from google.cloud import speech_v1p1beta1 as speech
from google.cloud import texttospeech
from queue import Queue
import base64
import time
from conversational_ai_engine import ConversationHandler, UserAdaptability

# Setting up logging
logging.basicConfig(level=logging.DEBUG)

# Instantiate chat manager and adaptability module
chat_handler = ConversationHandler()
adaptability_module = UserAdaptability()

class BufferStream(Queue):
    def __init__(self, buffer_max_size: int = 5):
        super().__init__(maxsize=buffer_max_size)

    def read(self):
        return self.get()

def transcribe_audio_stream(stream):
    client = speech.SpeechClient()
    config=speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_speaker_diarization=True,
        diarization_speaker_count=2
    )
    stream_buffer = BufferStream()

    for chunk in stream:
        stream_buffer.put(chunk)
        if stream_buffer.full():
            audio_content = stream_buffer.get_nowait() 
            request = speech.StreamingRecognizeRequest(audio_content=audio_content)
            responses = client.streaming_recognize(config, [request])
            for response in responses:
                print(response)
                
def convert_text_to_speech(text: str):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code="en-US",
                                              ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    audio_data = response.audio_content
    socketio.emit('response', {'audio_data': base64.b64encode(audio_data).decode()})

def storeConversationData(conversations):
    [print(f"User: {dialogue['User']}\nResponse: {dialogue['Response']}") for dialogue in conversations]

def generate_ai_response(user_message: str) -> str:   
    """ 
    Chat with OpenAI's GPT4-32k. 
    The conversation state is managed internally with the help of message history. 
    Each message object in the messages array has three properties: role, content, and filename.
    Increasing the max tokens increases response length up to a limit.
    """
    # Pass the user message through the chat manager and adaptability module
    processed_message = chat_handler.process(user_message)
    adapted_message = adaptability_module.adapt(processed_message)
    conversation = {
        'messages': [{"role": "user", "content": f"{adapted_message}"}]
    }
    
    attempts = 0

    while attempts < 5:
        try:
            response = openai.ChatCompletion.create(model="gpt-4-32k", messages=conversation['messages'], max_tokens=150) 
            # If the API call was successful then break out of the loop
            break
        except Exception as e:
            print(e)
            if attempts < 4:  # if fewer than 4 attempts have been made, retry
                wait_time = (2 ** attempts) + (random.randint(0, 1000) / 1000)
                print(f"Waiting for {wait_time} seconds.")
                time.sleep(wait_time)
                attempts += 1
                continue
            else:  # after 4 attempts, stop trying
                print("Unable to connect to the API after several attempts.")
                response = None
    return response['choices'][0]['message']['content'] if response else None

app = Flask(__name__, static_folder='talkasaurus-react/build')
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@socketio.on('message')
def handle_message(data):
    # Log that we received a new message
    logging.info("Received new user message.")
 
    dialogsCollection = []
    user_message = data['message']
    
    try:
        # Log when the AI has started processing a response
        logging.info("Starting to process user message.")
        
        response = generate_ai_response(user_message)
        
        # Log when the text to speech operation has started
        logging.info("Starting Text-to-Speech operation.")
        convert_text_to_speech(response)
        socketio.emit('response', {'response': response, 'message': user_message})
        
        dialogsCollection.append({
            "User": user_message,
            "Response": response
        })
        
    except Exception as e:
        logging.error(str(e), exc_info=True)

    logging.info("Finished processing current user message.")
    storeConversationData(dialogsCollection)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0"', port=int(os.getenv('PORT', 5000)))