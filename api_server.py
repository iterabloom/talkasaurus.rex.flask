# TODO: possibly store responses from the API and user input, in a way that preserves user privacy.
#       anonymize user data before storing, either by generalizing the context or 
#       hashing specifics relating to the user's identity.
#       These data could be used to analyze and tune the user's conversational style over time. 
#       it will be beneficial to implement Machine Learning models for user style adaptation. 
#       This could start as another microservice that processes the data and learns from it.
# TODO: As the user input and AI response data become large, establish a data archiving policy
# TODO: a new method/service needs to be defined to process and analyze the user’s conversation style
#       define classes or functions that utilise machine learning (either local or remote) to analyse user inputs for style, language syntax, and verbal patterns 

from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO
import openai
import os

# TODO: Make sure this key is correctly set and safely stored
openai.api_key = os.environ.get('OPENAI_API_KEY')

from google.cloud import speech_v1p1beta1 as speech
from google.cloud import texttospeech
from queue import Queue

def transcribe_audio_stream(stream):
    # TODO: add error handling blocks to handle potential failures during transcription process
    # Instantiate client
    client = speech.SpeechClient()

    # Set configuration
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_speaker_diarization=True,
        diarization_speaker_count=2,
    )

    # Create BufferStream instance
    stream_buffer = BufferStream(5)

    # Loop through audio stream
    for chunk in stream:
        # Add to stream buffer
        stream_buffer.put(chunk)
        
        # Sending chunks to transcribe
        if stream_buffer.full(): # Check if buffer reached the maximum size
            audio_content = stream_buffer.get_nowait() # Get the first element added to queue
            request = speech.StreamingRecognizeRequest(audio_content=audio_content) # Create the request
            responses = client.streaming_recognize(config, [request]) # Make the request

            # TODO Add processing logic for each response
            for response in responses:
                # TODO extract the transcribed text from each response and append it to a string that holds the entire transcription of the conversation



def convert_text_to_speech(text: str):
    # TODO: handle audio output interruptions. If the API encounters an error while synthesizing speech, the system should be able to retry the operation and/or handle it gracefully
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput({"text": text})

    # More voice settings can be added for better speech synthesis
    voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)

    # Audio config settings can be updated for better audio output
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    # Creating the speech synthesis response
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # TODO: completely rewrite below 3 lines to directly stream the audio to the frontend, eliminating the need to manage audio files
    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)
    print("Audio content written to file output.mp3")


def storeConversationData(user_message, response):
    # TODO implement this method with consideration to user privacy
    #      the user interaction data should be anonymized, persisted, and handled properly to ensure user’s privacy and efficient data management


app = Flask(__name__, static_folder='talkasaurus-react/build')
socketio = SocketIO(app)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@socketio.on('message')
def handle_message(data):
    user_message = data['message']
    # Generate AI response
    response = generate_ai_response(user_message)
    # Store user message and AI response
    storeConversationData(user_message, response)
    # Send the AI response back to the client
    socketio.emit('response', {'message': response})


def generate_ai_response(user_message: str) -> str: 
    # TODO: error handling if there's an issue with the GPT API call:
    #      implement a retry mechanism and
    #      implement a switch to a backup language model/ model provider

    # Add a dictionary for conversation history
    conversation = {
        'messages': [
            # TODO: append past user and ai messages to this list to maintain a history of the conversation.
            {"role": "user", "content": user_message}
        ]
    }
   
    try:
        response = openai.ChatCompletion.create(
          model="gpt-4-32k",
          messages=conversation['messages'],
          max_tokens=150
        )

        # Update conversation history
        conversation['messages'].append(
            {"role": "assistant",
             "content": response['choices'][0]['message']['content']}
        )
    except Exception as ex:
        # Handle exception
        print(f"Failed to generate response from GPT AI. Details: {str(ex)}")
        # Strategy to generate a backup text could be implemented here. E.g., pre-defined or simpler model outputs
        response = type(
            '', (), {
                'choices': [
                    type(
                        '', (), {
                            'message': type(
                                '', (), {'content': "Sorry, I am currently unable to generate a response"}
                            )
                        }
                    )
                ]
            }
        )

    return response['choices'][0]['message']['content']


if __name__ == '__main__':
    socketio.run(app)