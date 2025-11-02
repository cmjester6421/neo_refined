"""
Unit Tests for NEO Core AI Engine
"""

import unittest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.ai_engine import NEOAIEngine, DeepLearningModule, NeuroLearningModule
from src.core.ai_engine import RecursiveLearningModule, SmartThinkingModule


class TestNEOAIEngine(unittest.TestCase):
    """Test NEO AI Engine"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.engine = NEOAIEngine()
    
    def test_initialization(self):
        """Test engine initialization"""
        self.assertIsNotNone(self.engine)
        self.assertIsNotNone(self.engine.deep_learning)
        self.assertIsNotNone(self.engine.neuro_learning)
        self.assertIsNotNone(self.engine.recursive_learning)
        self.assertIsNotNone(self.engine.smart_thinking)
    
    def test_process_task(self):
        """Test task processing"""
        task = {
            'id': 'test_001',
            'type': 'analysis',
            'description': 'Test task',
            'data': [1, 2, 3, 4, 5]
        }
        
        result = self.engine.process_task(task)
        
        self.assertIsNotNone(result)
        self.assertIn('task_id', result)
        self.assertIn('confidence', result)
        self.assertIn('solution', result)
    
    def test_metrics(self):
        """Test metrics collection"""
        metrics = self.engine.get_metrics()
        
        self.assertIn('tasks_processed', metrics)
        self.assertIn('successful_predictions', metrics)
        self.assertIn('learning_iterations', metrics)


class TestSmartThinking(unittest.TestCase):
    """Test Smart Thinking Module"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.thinking = SmartThinkingModule()
    
    def test_analyze_problem(self):
        """Test problem analysis"""
        problem = "Write a function to calculate fibonacci numbers"
        analysis = self.thinking.analyze_problem(problem)
        
        self.assertIn('complexity', analysis)
        self.assertIn('required_skills', analysis)
        self.assertIn('approach', analysis)
    
    def test_make_decision(self):
        """Test decision making"""
        options = [
            {'option': 'A', 'cost': 0.8, 'speed': 0.6},
            {'option': 'B', 'cost': 0.6, 'speed': 0.9}
        ]
        criteria = {'cost': 0.5, 'speed': 0.5}
        
        decision = self.thinking.make_decision(options, criteria)
        
        self.assertIn('selected_option', decision)
        self.assertIn('score', decision)


if __name__ == '__main__':
    unittest.main()
