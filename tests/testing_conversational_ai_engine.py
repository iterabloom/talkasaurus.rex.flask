import unittest
import sqlite3
from mock import patch
from conversational_ai_engine import ConversationHandler, UserAdaptability

#may need to mock external service calls?

# TODO: doesn't cover what happens when test_conversation_state_management receives 
#       the first 'Hello, bot.' message, following which 'Greeting' state ought to be invoked rather than 'initial' state

class TestConversationHandlerHSM(unittest.TestCase):
    #This is just an example. realistically, states would probably be represented by numbers or constant variables, 
    # and state transitions would likely be tested by a system function or by analyzing 
    # the actions that resulted from changing states. We are going to focus on covering all features, states, and possible paths.
    def setUp(self):
        self.conversation_handler = ConversationHandler()

    def test_conversation_state_management(self):
        self.conversation_handler.process("Hello, bot.")
        # Here we assert that our.state has transferred to an expected state
        self.assertEqual(self.conversation_handler.state, 'Greeting')
        
        self.conversation_handler.process("What's the weather?")
        self.assertEqual(self.conversation_handler.state, 'WeatherQuery')

        self.conversation_handler.process("Thank you.")
        self.assertEqual(self.conversation_handler.state, 'Closing')


class TestConversationHandler(unittest.TestCase):
    #a new test case test_overflow is added to test for overflow behaviour when the buffer size is exceeded.
    def setUp(self):
        self.conversation_handler = ConversationHandler(buffer_size=2)

    def test_process(self):
        processed_msg = self.conversation_handler.process('Hello')
        self.assertEqual(processed_msg, 'Hello')
        self.assertEqual(self.conversation_handler.message_history, ['Hello'])

    def test_overflow(self):
        self.conversation_handler.process('Hello')
        self.conversation_handler.process('How are you doing?')
        self.conversation_handler.process('Nice weather outside!')

        self.assertEqual(self.conversation_handler.message_history, ['How are you doing?', 'Nice weather outside!'])
        

class TestUserAdaptability(unittest.TestCase):
    #a new test case test_act_on_instructions is added to check whether instructions are being correctly acted upon.
    def setUp(self):
        self.user_adaptability = UserAdaptability()

    def test_adapt(self):
        self.user_adaptability.adapt('Hello')

        # Check lexicon
        self.assertIn('hello', self.user_adaptability.user_lexicon)

        # Check mannerisms
        self.assertIn('hello', self.user_adaptability.user_mannerisms)
        self.assertEqual(self.user_adaptability.user_mannerisms['hello'], 1)

        # Check sentiment
        self.assertEqual(sum(self.user_adaptability.user_sentiments)/len(self.user_adaptability.user_sentiments), 0.0)

        # Check tags
        self.assertIn('NN', self.user_adaptability.pos_tags)
        self.assertEqual(self.user_adaptability.pos_tags['NN'], 1)

    @patch('conversational_ai_engine.UserAdaptability.fetch_research_info')
    def test_act_on_instructions(self, mock_fetch_research_info):
        mock_fetch_research_info.return_value = 'Info about cats.'
        self.user_adaptability.cursor.execute("INSERT INTO user_tasks (task) VALUES ('Research about cats.')")
        self.user_adaptability.conn.commit()

        info = self.user_adaptability.act_on_instructions()

        self.assertEqual(info, 'Info about cats.')
        self.user_adaptability.cursor.execute("SELECT is_complete FROM user_tasks WHERE task = 'Research about cats.'")
        is_complete = self.user_adaptability.cursor.fetchall()[0][0]

        self.assertEqual(is_complete, 1)

if __name__ == '__main__':
    unittest.main()