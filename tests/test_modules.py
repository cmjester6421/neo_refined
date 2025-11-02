"""
Unit Tests for NEO Modules
"""

import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.modules.system_control import SystemControl
from src.modules.cybersecurity import CybersecurityModule
from src.modules.coding_assistant import CodingAssistant
from src.modules.research import ResearchModule
from src.modules.task_automation import TaskAutomation, TaskPriority
from src.modules.nlp_conversation import NLPConversation


class TestSystemControl(unittest.TestCase):
    """Test System Control Module"""
    
    def setUp(self):
        self.control = SystemControl()
    
    def test_get_system_info(self):
        """Test system info retrieval"""
        info = self.control.get_system_info()
        
        self.assertIn('platform', info)
        self.assertIn('cpu', info)
        self.assertIn('memory', info)


class TestCybersecurity(unittest.TestCase):
    """Test Cybersecurity Module"""
    
    def setUp(self):
        self.cyber = CybersecurityModule()
    
    def test_password_strength(self):
        """Test password strength analysis"""
        result = self.cyber.password_strength_analysis("MyP@ssw0rd123!")
        
        self.assertIn('score', result)
        self.assertIn('strength', result)
        self.assertGreater(result['score'], 50)
    
    def test_generate_password(self):
        """Test password generation"""
        password = self.cyber.generate_secure_password(16)
        
        self.assertEqual(len(password), 16)


class TestCodingAssistant(unittest.TestCase):
    """Test Coding Assistant Module"""
    
    def setUp(self):
        self.assistant = CodingAssistant()
    
    def test_analyze_code(self):
        """Test code analysis"""
        code = "def hello():\n    print('Hello')"
        analysis = self.assistant.analyze_code(code)
        
        self.assertIsNotNone(analysis)
        self.assertEqual(analysis.language, "python")
        self.assertGreater(analysis.quality_score, 0)


class TestResearch(unittest.TestCase):
    """Test Research Module"""
    
    def setUp(self):
        self.research = ResearchModule()
    
    def test_research_topic(self):
        """Test topic research"""
        result = self.research.research_topic("python programming", depth="quick")
        
        self.assertIsNotNone(result)
        self.assertGreater(len(result.sources), 0)
        self.assertGreater(result.confidence, 0)


class TestTaskAutomation(unittest.TestCase):
    """Test Task Automation Module"""
    
    def setUp(self):
        self.automation = TaskAutomation(max_workers=2)
    
    def test_create_task(self):
        """Test task creation"""
        def sample_task():
            return "result"
        
        task_id = self.automation.create_task("Test Task", sample_task)
        
        self.assertIsNotNone(task_id)
        self.assertIn(task_id, self.automation.tasks)


class TestNLPConversation(unittest.TestCase):
    """Test NLP Conversation Module"""
    
    def setUp(self):
        self.nlp = NLPConversation()
    
    def test_create_conversation(self):
        """Test conversation creation"""
        session_id = self.nlp.create_conversation("test_user")
        
        self.assertIsNotNone(session_id)
        self.assertIn(session_id, self.nlp.conversations)
    
    def test_detect_intent(self):
        """Test intent detection"""
        intent, confidence = self.nlp.detect_intent("Hello, how are you?")
        
        self.assertEqual(intent, "greeting")
        self.assertGreater(confidence, 0)


if __name__ == '__main__':
    unittest.main()
