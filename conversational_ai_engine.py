#v1.0.0 Basic Conversation and User Adaptability Modules

import re
from collections import defaultdict

# a class to handle conversation sequencing, feedback, overlap, interruption 
class ConversationHandler:

    def __init__(self):
        pass

    # TODO: Write appropriate methods here in order to
    # 		track conversation sequencing, feedback, overlap, and interruptions, repairing mistakes in conversation
    #		and delegating parallel or background generative tasks as needed,
    # 		working closely with the GPT-4 API and the Google APIs, and integrated with api_server.py

# a class to handle user adaptability
class UserAdaptability:

    def __init__(self):
        pass

    # TODO: Write appropriate methods here that use self-referential prompt engineering with the GPT-4 API
    # 		to detect the user's lexicon, syntax, overtones, and conversational patterns. Potentially use
    #		a mixture of the GPT-3.5 API, the GPT-4 API, and open-source models (e.g. Llama2, Siamese BERT, or FalconAI) to
    #		optimize cost. Adaptability should extend to explicit instructions from the user, e.g. "from now
    #		on, during every conversation, please remind me to stand up and stretch every 15 minutes, and 
    #		every hour, ask me if I had a drink of water recently."
    #		or, another example - "I'm curious about photonic computing. would you please keep tabs on it,
    #		and do research on it in the background, and once a month check in with me on what you're finding,
    #		and how to adapt your research for the next month?"
    #		Also, embed an implicit suggestion/reward mechanism by using sentiment analysis - again, to minimize
    #		costs, use some hybrid of GPT-3.5, GPT-4, and open-source models.

# a context manager to easily begin and end a conversation
class ChatSession(ContextManager):
    pass