import sys
from pathlib import Path
import unittest
import tempfile
import json
import os

current_dir = Path(__file__).resolve().parent
src_dir = current_dir.parent / "src" / "prompt_registry"
sys.path.insert(0, str(src_dir))

from prompt_fetcher import PromptFetcher, PromptNotFoundError

class TestPromptRegistry(unittest.TestCase):
    
    def setUp(self):
        # Create a temporary registry for deterministic testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.registry_file = Path(self.temp_dir.name) / "test_prompts.json"
        
        self.test_data = {
            "test_prompt_v1": "Hello world from VTE",
            "test_prompt_v2": "Hello universe"
        }
        
        with open(self.registry_file, 'w') as f:
            json.dump(self.test_data, f)
            
        self.fetcher = PromptFetcher(registry_path=str(self.registry_file))
        
    def tearDown(self):
        self.temp_dir.cleanup()

    def test_fetch_existing_prompt(self):
        prompt = self.fetcher.get_prompt("test_prompt_v1")
        self.assertEqual(prompt, "Hello world from VTE")
        
    def test_missing_prompt_fails_closed(self):
        with self.assertRaises(PromptNotFoundError) as context:
            self.fetcher.get_prompt("rogue_ai_prompt_v99")
            
        self.assertIn("Determinism Error", str(context.exception))
        self.assertIn("rogue_ai_prompt_v99", str(context.exception))

if __name__ == '__main__':
    unittest.main()
