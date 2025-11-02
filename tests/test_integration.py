"""
Integration Tests for NEO
"""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.main import NEOAssistant


class TestNEOIntegration(unittest.TestCase):
    """Integration tests for NEO Assistant"""
    
    def setUp(self):
        """Set up NEO instance"""
        self.neo = NEOAssistant()
    
    def test_initialization(self):
        """Test NEO initialization"""
        self.assertIsNotNone(self.neo)
        self.assertIsNotNone(self.neo.ai_engine)
        self.assertIsNotNone(self.neo.nlp)
    
    def test_process_command(self):
        """Test command processing"""
        result = self.neo.process_command("Hello NEO")
        
        self.assertIsNotNone(result)
        self.assertIn('response', result)
    
    def test_system_info_command(self):
        """Test system info command"""
        result = self.neo.process_command("Show me system information")
        
        self.assertIsNotNone(result)
    
    def test_get_status(self):
        """Test status retrieval"""
        status = self.neo.get_status()
        
        self.assertIn('name', status)
        self.assertIn('version', status)
        self.assertIn('modules', status)


if __name__ == '__main__':
    unittest.main()
