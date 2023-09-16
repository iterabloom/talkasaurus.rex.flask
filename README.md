# talkasaurus.rex.flask

![a cartoon tyrannosaurus rex talks on an oversized 1980s-style telephone while stirring a cup of tea with a large aquamarine-colored spoon](talkosaurus-rex.png?raw=true "TalkasaurusRex").  

TalkasaurusRex leverages speech-to-text, text-to-speech, and GPT4-32k to have natural conversations with users. The conversation experience is a prime focus, requiring it to be as close to conversing with another human as possible.

Further, the app logic needs to accommodate interjections and pause at appropriate times. Even listening for nonword vocalizations like "ummm", "hmm", or "ah" and allowing contemplative silences should be expected.

An exciting feature of TalkasaurusRex is to have the generated text sequences mirror or complement the user's diction, imagery, detail, language, syntax, rhythms, and patterns. To achieve this, thorough user feed-ins, training modules, and efficient design models are in progress, to understand the user’s style and substantive context simultaneously. Ideally, a Hierarchical State Machine (HSM) will be used for managing conversation complexity and handling various conversation states – with a future plan to use Petri nets for achieving parallel processing of the tasks.

Further, the integration of a "DevOpsBot" in the CI/CD pipeline, for continuously improving and developing TalkasaurusRex, will be built with human-in-the-loop circuit breakers. One strategy is to build specific flags or comment tags that trigger manual intervention in the deployment process. For example, a flag like `[manual_review]` could be used where the project grows in complexity - for reliable quality control.

The architecture of TalkasaurusRex has been designed with a flexible roadmap that allows for additions to states, transitions, and modules as needed – which is important for scaling.

So far, development has clustered into six main activities:

1. Setup – Env, Tech, and Overview
    Docker setup implemented for deployments across diverse environments
2. Speech-to-text
    Google’s Speech-to-Text API integration has been made
3. Text-to-speech
    Google's Text-to-Speech API integration helps users hear what the AI thinks
4. Conversational AI with GPT4-32k
5. Analyzing and Adapting to a user's style
    A roadmap has been outlined for a next milestone where TalkasaurusRex learns to capture user’s uniqueness and molds its language in the same style
6. DevOpsBot
    CI/CD pipelines setup using GitHub Actions has been mostly completed. The next step is further testing of this pipeline, plus putting the "Dev" in the DevOps and unleashing this bot's creativity
