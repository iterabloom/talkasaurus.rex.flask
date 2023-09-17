# talkasaurus.rex.flask

![a cartoon tyrannosaurus rex talks on an oversized 1980s-style telephone while stirring a cup of tea with a large aquamarine-colored spoon](talkosaurus-rex.png?raw=true "TalkasaurusRex")  

TalkasaurusRex is designed for naturally flowing conversation - adapting to and mirroring the user's communication style. It leverages Google's Speech-to-Text, Text-to-Speech APIs, alongside the GPT4-32k model, creating an interaction akin to conversing with another human.

## Table of Contents
* Features
* Current State
* Getting Started
* Prerequisites
* Installation
    * Cloning the Repository
    * Backend Setup
    * Frontend Setup
* Usage Instructions
    * Starting the Backend Server
    * Starting the Frontend Server
    * Accessing the Conversational AI
    * Example Conversation

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

### Prerequisites:
* To get the application up and running, make sure to have Python 3.x and NodeJS installed on your machine.

### Installation:

#### Cloning the repository:
1. Clone the repository using `git clone https://github.com/iterabloom/talkasaurus.rex.flask.git`

#### Backend Setup : (Recommended - For Full Backend setup only)
* To set the backend setup `launch the project in a devContainer` , or move forward with following steps for local setup.

2. Depending upon the preference:
    * Inside project's root directory open terminal and run `pip install -r requirements.txt` to install the Python requirements.
    * Run the backend sever by executing `python api_server.py`. The server starts up at `localhost:5000`.

#### Frontend Setup :
    Generally, setting up front end involves running a different server from that of backend tailered to aid front-end development (like immediate reflect of code changes and ability to easily consume APIs).

3. Within `talkasaurus-react/` directory run:
    * `npm install` to install dependent packages listed in `package.json` file. You must be in the same directory as `package.json file`.
    * `npm start` to start the frontend development server at `localhost:3000`.

### Usage Instructions

1. Start up backend by running ```bash python api_server.py```, this starts the backend server at [localhost:5000](http://localhost:5000).

2. Start up frontend development server by running `npm start`, this starts the server at [localhost:3000](http://localhost:3000)

3. Access the fully functioning conversational AI chat at [localhost:3000](http://localhost:3000) in your web browser.
                
## Example Conversation
A typical conversation looks something like this:
User: Hello, how was your day?
Bot: Hello! As an artificial intelligence, I don't experience days in the same way a human might, but thank you for asking! How may I assist you today?