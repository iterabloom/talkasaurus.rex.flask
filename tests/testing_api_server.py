import unittest
from apiserver import generate_ai_response
class TestApiServer(unittest.TestCase):
  	def test_generate_ai_response(self):
        response = generate_ai_response("Hello, bot!")
        self.assertIsInstance(response, str)