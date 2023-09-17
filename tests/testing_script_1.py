import unittest
from flask_socketio import SocketIO, emit
from flask import Flask
from unittest.mock import Mock
import api_server
from conversational_ai_engine import ConversationHandler, UserAdaptability

# TODO: expand to cover more edge cases and functionalities
class TestApp(unittest.TestCase):
    def setUp(self):
        # Setup flask app
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app)
        self.client = self.app.test_client()

        # Setup chat handler and adaptability modules
        self.chat_handler = ConversationHandler()
        self.adaptability_module = UserAdaptability()

    def test_socket_connection(self):
        mock = Mock()
        self.socketio.on('connect', mock)
        self.socketio.test_client(self.app).emit('connect')
        assert mock.called

    def test_generate_ai_response(self):
        response = api_server.generate_ai_response('Hello Chatbot')
        self.assertIsNotNone(response)

    def test_converse_handler(self):
        test_msg = "Hello Chatbot"
        processed_msg = self.chat_handler.process(test_msg)
        self.assertEqual(processed_msg, test_msg)
        self.assertTrue(len(self.chat_handler.message_history) > 0)

    def test_user_adaptability(self):
        test_msg = "Hello Chatbot"
        adapted_msg = self.adaptability_module.adapt(test_msg)
        self.assertEqual(adapted_msg, test_msg)
        self.assertTrue(len(self.adaptability_module.user_lexicon) > 0)

if __name__ == '__main__':
    unittest.main()