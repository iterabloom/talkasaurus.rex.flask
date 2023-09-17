# talkasaurus.rex.flask

![a cartoon tyrannosaurus rex talks on an oversized 1980s-style telephone while stirring a cup of tea with a large aquamarine-colored spoon](talkosaurus-rex.png?raw=true "TalkasaurusRex")  

TalkasaurusRex is designed for naturally flowing conversation - adapting to and mirroring the user's communication style. It leverages Google's Speech-to-Text, Text-to-Speech APIs, alongside the GPT4-32k model, creating an interaction akin to conversing with another human.

## Features
- Gestures like Interjections, Nonword Vocalizations: The app can catch and react appropriately to "ummm", "hmm", "ah", and pauses in conversation to create a very human-like interaction.
- Adapting To User Style: It aims to mirror or complement the user's diction, imagery, language, syntax, and conversational patterns.
- Hierarchical State Machine (HSM): Intended for complex conversation and state management; plans are to use Petri nets for task parallelism.
- DevOpsBot: A presence within the system for improvements, featuring mechanisms for human-in-the-loop interventions when complexity rises, for instance deploying a segment of code marked with `[manual_review]`.

## Current State
1. Setup & Overview: Env, Tech enabled with Docker for diverse deployments
2. Speech-to-Text Integration: Google’s Speech-to-Text API
3. Text-to-Speech Integration: Google’s Text-to-Speech API
4. Conversational AI Integration: GPT4-32k for natural conversation experience
5. Analyzing & Adapting User Style: A roadmap outlined to enhance user-language molding  
6. DevOpsBot Initiation: CI/CD pipelines setup using GitHub Actions.

## Getting Started
1. Clone the repository.
2. You will need Python 3.x and NodeJS installed on your machine.
3. Install the Python requirements with `pip install -r requirements.txt`.
4. Run `npm install` in the `talkasaurus-react/` directory.
5. Start the backend server with `python api_server.py`. The server will start on localhost:5000.
6. Start the frontend server by running `npm start` in the `talkasaurus-react/` directory. The server will start on localhost:3000.
7. Access the conversational AI via http://localhost:3000 in your web browser.

## Example Conversation
A typical conversation looks something like this:
User: Hello, how was your day?
Bot: Hello! As an artificial intelligence, I don't experience days in the same way a human might, but thank you for asking! How may I assist you today?