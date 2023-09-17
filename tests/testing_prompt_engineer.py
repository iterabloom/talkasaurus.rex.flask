import unittest
from conversational_ai_engine import PromptEngineer
class TestPromptEngineer(unittest.TestCase):
  	def setUp(self):
    	self.prompt_engineer = PromptEngineer()

	  def test_pass_to_gpt4(self):
    	conversation_prompts = [
        	{"role": "system", "content": "You are an expert in Linguistics."},
    	    {"role": "user", "content": "Analyze the syntax and structure of my speech."},
    	    {"role": "assistant", "content": "The user converses in conversational English."}
    	]
    	generated_prompts = self.prompt_engineer._pass_to_gpt4(conversation_prompts)
    	self.assertIsInstance(generated_prompts, str)