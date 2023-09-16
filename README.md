# talkasaurus.rex.flask

![a cartoon tyrannosaurus rex talks on an oversized 1980s-style telephone while stirring a cup of tea with a large aquamarine-colored spoon](talkasaurus-rex.png?raw=true "TalkasaurusRex"). 

TalkasaurusRex leverages speech-to-text, text-to-speech, and GPT4-32k to have natural conversations with users. The conversation experience should be as close to conversing with another human as possible - so the app logic needs to accommodate interjections and needs to pause at appropriate times - and even listen for nonword vocalizations like "ummm", "hmm", or "ah". It should afford contemplative silences. The generated text sequences should mirror or complement the user's diction, imagery, detail, language, syntax, rhythms, and patterns. An HSM will be used for managing conversation complexity and handling various states of the conversation. Petri nets could be leveraged for parallel execution, like processing user’s style and understanding context simultaneously. The architecture will allow the addition of more states and transitions easily as complexity increases. Furthermore, the webapp will be continuously improved and developed by a "DevOpsBot," with human-in-the-loop circuitbreakers. Eventually the webapp will also become a mobile app.  

Most of the initial development activities have been covered as explained below:

Activity 1. Setup  
   The setup of the project includes a GitHub repository using the Flask-SocketIO micro web framework for Python backend, and the React library for UI front-end. Docker is utilized to ensure the application deploys seamlessly across diverse environments, thereby mitigating potential conflicts with dependencies.

Activity 2. Speech-to-Text  
   Google’s Speech-to-Text API is integrated into the application to transcribe real-time dialogue with the user, and has succesfully tested to work even in diverse noisy environments.

Activity 3. Text-to-Speech  
   Google's Text-to-Speech API has been integrated for contructing conversation such that talkasaurus.rex.flask responds to the user in a human conversation manner.

Activity 4. Conversational AI with GPT4-32k
   OpenAI's GPT3 is used as the conversation AI backbone. Talkasaurus.rex.flask can convert messages to the user and send responses from an AI.

Activity 5. Analyzing and Adapting to User’s Style  
   This section still needs to be implemented. Future plans include the possibility of utilizing machine learning models to analyse and adapt to the user's unique speech patterns.

Activity 6. DevOpsBot  
   CI/CD pipelines have been established with the application of GitHub Actions denoted in the configurations and workflows file, providing the project with well-streamlined, fully automated updating and deploying processes. 

Note: Specific flags or comment tags that would typically trigger manual intervention in the deployment process (for example, `[manual_review]`) need to be defined as the project grows in complexity for reliable quality control.