import unittest
from flask_socketio import SocketIO, emit
from flask import Flask
from unittest.mock import Mock
import api_server

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.socketio = SocketIO(self.app)
        self.client = self.app.test_client()

    def test_socket_connection(self):
        mock = Mock()
        self.socketio.on('connect', mock)
        self.socketio.test_client(self.app).emit('connect')
        assert mock.called

    def test_generate_ai_response(self):
        response = api_server.generate_ai_response('Hello')
        self.assertIsNotNone(response)

if __name__ == '__main__':
    unittest.main()