"""
TODO: Some areas that should be tested include:
    - connection to the database
    - all routing functions (What happens if the function receives invalid input? What if there's a failure or error during the process? What if the database request fails? What is the response if the function handles
      the operation properly? )
    - chatbot conversation testing, i.e., send a series of messages, resp similar to user test cases.
"""

import unittest
from apiserver import generate_ai_response
class TestApiServer(unittest.TestCase):
  	def test_generate_ai_response(self):
        response = generate_ai_response("Hello, bot!")
        self.assertIsInstance(response, str)