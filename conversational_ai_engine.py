#v1.0.0 Basic Conversation and User Adaptability Modules

import openai
import os
import sqlite3
from collections import Counter
import atexit
from textblob import TextBlob  # for rudimentary sentiment analysis and parts of speech tagging

openai.api_key = os.environ.get("OPENAI_API_KEY")

# a class to handle conversation sequencing, feedback, overlap, interruption 
class ConversationHandler:
    # TODO: Write appropriate methods here in order to
    #       track conversation sequencing, feedback, overlap, and interruptions, repairing mistakes in conversation
    #       and delegating parallel or background generative tasks as needed,
    #       working closely with the GPT-4 API and the Google APIs, and integrated with api_server.py
    def __init__(self, buffer_size=10):
        self.message_history = []
        self.buffer_size = buffer_size
        self.conn = sqlite3.connect('messages.db')
        self.cursor = self.conn.cursor()
        # Initialize message table if not exists
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS messages
                               (id INTEGER PRIMARY KEY, message TEXT)''')
        atexit.register(self._cleanup)

    def process(self, message):
        # Save the message into the database
        self.cursor.execute("INSERT INTO messages (message) VALUES (?)",
                            (message,))
        self.conn.commit()

        # If memory buffer is full, remove the oldest message
        if len(self.message_history) >= self.buffer_size:
            self.message_history.pop(0)

        self.message_history.append(message)
        return message

    def _cleanup(self):
        self.conn.close()


class UserAdaptability:
    # TODO: Write appropriate methods here that use self-referential prompt engineering with the GPT-4 API
    #       to detect the user's lexicon, syntax, overtones, and conversational patterns. Potentially use
    #       a mixture of the GPT-3.5 API, the GPT-4 API, and open-source models (e.g. Llama2, Siamese BERT, or FalconAI) to
    #       optimize cost. Adaptability should extend to explicit instructions from the user, e.g. "from now
    #       on, during every conversation, please remind me to stand up and stretch every 15 minutes, and 
    #       every hour, ask me if I had a drink of water recently."
    #       or, another example - "I'm curious about photonic computing. would you please keep tabs on it,
    #       and do research on it in the background, and once a month check in with me on what you're finding,
    #       and how to adapt your research for the next month?"
    #       Also, embed an implicit suggestion/reward mechanism by using sentiment analysis - again, to minimize
    #       costs, use some hybrid of GPT-3.5, GPT-4, and open-source models.
    #       utilizing prompt-engineering and the capabilities of GPT-4 is an excellent starting point for modeling the characteristics of the user's speech. Mapping the critical elements outlined above (such as stress/emphasis, speed of speech, morphological choices etc.) to structured data that the model can learn and infers from, will be valuable. 
    #       Just like a good listener in a conversation picks up on the other person's tone, mood, and speaking style unconsciously, developing a suite of such prompts for GPT-4 allows it to play different speech expert roles, synthesizing a much deeper understanding of the user's linguistics and conversation style.

    def __init__(self):
        # Storing user lexicon and mannerisms identified
        self.user_lexicon = set()
        self.user_mannerisms = Counter()
        self.user_sentiments = []
        self.pos_tags = Counter()
        self.conn = sqlite3.connect('user_adaptability.db')
        self.cursor = self.conn.cursor()
        # Initialize lexicon, mannerisms, sentiments and pos tags table if not exists
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS lexicon
                               (id INTEGER PRIMARY KEY, word TEXT)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS mannerisms
                               (id INTEGER PRIMARY KEY, mannerism TEXT, frequency INTEGER)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sentiments
                               (id INTEGER PRIMARY KEY, sentiment REAL)''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS pos_tags
                               (id INTEGER PRIMARY KEY, pos_tag TEXT, frequency INTEGER)''')
        atexit.register(self._cleanup)

    def adapt(self, message):
        # Assimilate unique words into user lexicon
        self.user_lexicon.update(set(word.lower() for word in message.split(' ')))
        # Add words to lexicon table
        for word in self.user_lexicon:
            self.cursor.execute("INSERT INTO lexicon (word) VALUES (?)",
                                (word,))       

        blob = TextBlob(message)
        # Update user's mannerisms and sentiments
        self.user_mannerisms.update(blob.word_counts)
        self.user_sentiments.append(blob.sentiment.polarity)
        self.pos_tags.update(tag for (word, tag) in blob.tags)
        # Add mannerisms, sentiments and pos tags to respective tables
        for mannerism, frequency in self.user_mannerisms.items():
            self.cursor.execute("INSERT INTO mannerisms (mannerism, frequency) VALUES (?, ?)",
                                (mannerism, frequency))
        for sentiment in self.user_sentiments:
            self.cursor.execute("INSERT INTO sentiments (sentiment) VALUES (?)",
                                (sentiment,))
        for pos_tag, frequency in self.pos_tags.items():
            self.cursor.execute("INSERT INTO pos_tags (pos_tag, frequency) VALUES (?, ?)",
                                (pos_tag, frequency))

        self.conn.commit()
        return message

    def generate_expert_prompts(self):
        # This method generates a range of expert prompts that will serve as basis to create an analytic view of user's speech
        role_system_prompt = {"role": "system", "content": "You are a chatbot designed to analyze and adapt to a user's language. Capabilities include phonetic, phonological, morphological, semantic, pragmatic, sociolinguistic, psycholinguistic, discourse, and orthographic analyses."}
        role_user_prompt = {"role": "user", "content": "Analyze my tone, mode of speech, emphasis, common phrases and topics, likes and dislikes, dialect, sentiment, and other mannerisms."}

        # Shaping assistant's role 
        role_assistant_prompts = [
            {"role": "assistant", "content": f"The user often uses the following words and phrases: {', '.join(self.user_lexicon)}."},
            {"role": "assistant", "content": f"The user displays a {self.determine_user_sentiment()} sentiment overall."},
            {"role": "assistant", "content": "The user's position towards politeness is being inferred from the frequency of markers like please, thank you, etc."},
            {"role": "assistant", "content": "The user has shown an interest in the following topics: ... ."},
            {"role": "assistant", "content": "The user displays the following discourse markers: ... ."},
            {"role": "assistant", "content": "The user's dialectical features include: ... ."},
            {"role": "assistant", "content": "The user seems to display orthographic features characteristic of this digital platform: ... ."}
        ]

        # Collating all prompts in a conversation format for more context
        expert_prompts = [
            role_system_prompt,
            role_user_prompt
        ]
        expert_prompts.extend(role_assistant_prompts)
        return expert_prompts

    def determine_user_sentiment(self):
        # Determining overall user sentiment (positive, negative, or neutral)
        average_sentiment_score = statistics.mean(self.user_sentiments) if self.user_sentiments else 0
        if average_sentiment_score > 0.05:
            return 'positive'
        elif average_sentiment_score < -0.05:
            return 'negative'
        else:
            return 'neutral'

    def _cleanup(self):
        self.conn.close()


# A context manager to easily begin and end a conversation
class ChatSession(ContextManager):
    pass


#the 10 human speech fields most relevant to TalkasaurusRex: 
#Phonetics, 
#Phonology,   
#Psycholinguistics, 
#Sociolinguistics,
#Morphology, Syntax, Semantics, Pragmatics, Discourse Analysis, Computational Linguistics


class PromptGenerator:
    def __init__(self, adaptability_module):
        self.adaptability_module = adaptability_module

    # Linguist: Focuses on the structure of language and syntax
    def linguist_view(self):
        # Example conversation prompt for linguist_view
        conversation = {
            'messages': [
                {"role": "system", "content": "You are a skilled linguist."},
                {"role": "user", "content": 'Analyze my style of speech.'},
                {"role": "assistant", "content": "The user often uses {0}.".format(', '.join(self.adaptability_module.user_lexicon))}
            ]
        }
        prompt = self._generate_prompt(conversation)  
        return prompt

    # Psycholinguist: Considers psychological factors in understanding language
    def psycholinguist_view(self):
        avg_sentiment = sum(self.adaptability_module.user_sentiments) / len(self.adaptability_module.user_sentiments) if self.adaptability_module.user_sentiments else 0
        sentiment_type = "positive" if avg_sentiment > 0 else "negative" if avg_sentiment < 0 else "neutral"
        # Example conversation prompt for psycholinguist_view
        conversation = {
            'messages': [
                {"role": "system", "content": "You are an experienced psycholinguist."},
                {"role": "user", "content": 'What does my language reveal about my mindset?'},
                {"role": "assistant", "content": f"The user usually uses {sentiment_type} language."}
            ]
        }
        prompt = self._generate_prompt(conversation)  
        return prompt

    # Sociolinguist: Explores social dimensions of language use
    def sociolinguist_view(self):
        # Here we assume the presence of a method that can infer social context from language use
        social_context = self.adaptability_module.infer_social_context()
        # Example conversation prompt for sociolinguist_view
        conversation = {
            'messages': [
                {"role": "system", "content": "You are a renowned sociolinguist."},
                {"role": "user", "content": 'What social context does my language suggest?'},
                {"role": "assistant", "content": f"The user's language suggests a {social_context} social context."}
            ]
        }
        prompt = self._generate_prompt(conversation)  
        return prompt

    # Phonetics: Examines the physical sounds of human speech
    def phonetic_view(self):
        message_phonetics = self.analyze_phonetics(self.adaptability_module.last_message)
        conversation = {
            'messages': [
                {"role": "system", "content": "You are a skilled phonetician."},
                {"role": "user", "content": 'What can you tell about the phonetics of my speech?'},
                {"role": "assistant", 
                "content": f"Your speech exhibits traits common in {message_phonetics} accents."}
            ]
        }
        prompt = self._generate_prompt(conversation)  
        return prompt

    # Phonologist
    def phonologist_view(self):
        message_phonology = self.analyze_phonology(self.adaptability_module.last_message) # assuming method for phonology analysis
        conversation = {
            'messages': [
                {"role": "system", "content": "You are a phonologist."},
                {"role": "user", "content": 'Can you analyze the phonology of my speech?'},
                {"role": "assistant", 
                "content": f"{message_phonology}"}
            ]
        }
        prompt = self._generate_prompt(conversation)  
        return prompt

    #...
    # replace the "..." with other expert views
    #...

    # Helper Function to generate a conversation prompt for the AI model
    def _generate_prompt(self, conversation):
        message = conversation['messages'][-1]['content']
        role = random.choice(["user", "assistant"])  # Need to model both 'user' and 'assistant' roles
        prompt = f"You are having a conversation where a user just said: '{message}'. As an {role}, what would you respond?"
        return prompt

#...
# In api_server.py's 'generate_ai_response' function, make use of these prompts
# prompt_generator = PromptGenerator(adaptability_module)
#linguist_prompt = prompt_generator.linguist_view()
#psycholinguist_prompt = prompt_generator.psycholinguist_view()
#sociolinguist_prompt = prompt_generator.sociolinguist_view()
# Generate ai response for each prompt and collectively analyze them
#linguist_response = openai.Completion.create(prompt=linguist_prompt)
#psycholinguist_response = openai.Completion.create(prompt=psycholinguist_prompt)
#sociolinguist_response = openai.Completion.create(prompt=sociolinguist_prompt)
# Analyze these results and craft appropriate assistant's response
#...
#By simulating various expert views, these prompts can help analyse the user's speech in a diverse and comprehensive manner. Also, the outputs can be used to custom shape how GPT-4 responds to the user.