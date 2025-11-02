"""
NEO AI Engine
Advanced AI system with deep learning, neuro learning, and recursive learning capabilities
"""

import torch
import torch.nn as nn
import numpy as np
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json
from pathlib import Path
import os

from src.utils.logger import NEOLogger

# Try to import Gemini
try:
    from src.core.gemini_integration import GeminiIntegration
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False


@dataclass
class LearningContext:
    """Context for learning operations"""
    task_type: str
    input_data: Any
    expected_output: Optional[Any] = None
    confidence_threshold: float = 0.8
    learning_rate: float = 0.001


class DeepLearningModule(nn.Module):
    """Deep learning neural network module"""
    
    def __init__(self, input_size: int = 512, hidden_size: int = 1024, output_size: int = 256):
        super(DeepLearningModule, self).__init__()
        self.logger = NEOLogger("DeepLearning")
        
        # Multi-layer neural network
        self.network = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_size, output_size),
            nn.Tanh()
        )
        
        self.optimizer = torch.optim.Adam(self.parameters(), lr=0.001)
        self.criterion = nn.MSELoss()
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass through the network"""
        return self.network(x)
    
    def learn(self, input_data: torch.Tensor, target: torch.Tensor) -> float:
        """Train the network on given data"""
        self.optimizer.zero_grad()
        output = self.forward(input_data)
        loss = self.criterion(output, target)
        loss.backward()
        self.optimizer.step()
        return loss.item()


class NeuroLearningModule:
    """Neuro-inspired learning with pattern recognition and adaptation"""
    
    def __init__(self):
        self.logger = NEOLogger("NeuroLearning")
        self.memory_bank = {}
        self.pattern_database = []
        self.adaptation_rate = 0.1
        
    def recognize_pattern(self, data: Any) -> Dict[str, Any]:
        """Recognize patterns in input data"""
        self.logger.info("Recognizing patterns in data")
        
        # Convert data to feature vector
        features = self._extract_features(data)
        
        # Find similar patterns
        matches = []
        for idx, pattern in enumerate(self.pattern_database):
            similarity = self._calculate_similarity(features, pattern['features'])
            if similarity > 0.7:
                matches.append({
                    'pattern_id': idx,
                    'similarity': similarity,
                    'metadata': pattern.get('metadata', {})
                })
        
        return {
            'matches': matches,
            'features': features,
            'is_new_pattern': len(matches) == 0
        }
    
    def adapt(self, feedback: Dict[str, Any]) -> None:
        """Adapt learning based on feedback"""
        self.logger.info("Adapting based on feedback")
        
        if feedback.get('is_correct'):
            # Reinforce successful patterns
            pattern_id = feedback.get('pattern_id')
            if pattern_id is not None and pattern_id < len(self.pattern_database):
                self.pattern_database[pattern_id]['confidence'] *= (1 + self.adaptation_rate)
        else:
            # Adjust unsuccessful patterns
            pattern_id = feedback.get('pattern_id')
            if pattern_id is not None and pattern_id < len(self.pattern_database):
                self.pattern_database[pattern_id]['confidence'] *= (1 - self.adaptation_rate)
    
    def store_pattern(self, data: Any, metadata: Dict = None) -> int:
        """Store new pattern in database"""
        features = self._extract_features(data)
        pattern = {
            'features': features,
            'metadata': metadata or {},
            'confidence': 1.0,
            'usage_count': 0
        }
        self.pattern_database.append(pattern)
        return len(self.pattern_database) - 1
    
    def _extract_features(self, data: Any) -> np.ndarray:
        """Extract feature vector from data"""
        # Simple feature extraction - can be enhanced
        if isinstance(data, str):
            # Text to feature vector
            return np.array([hash(data) % 1000 / 1000.0 for _ in range(64)])
        elif isinstance(data, (list, np.ndarray)):
            return np.array(data).flatten()[:64]
        else:
            return np.random.rand(64)
    
    def _calculate_similarity(self, features1: np.ndarray, features2: np.ndarray) -> float:
        """Calculate similarity between feature vectors"""
        # Cosine similarity
        dot_product = np.dot(features1, features2)
        norm1 = np.linalg.norm(features1)
        norm2 = np.linalg.norm(features2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)


class RecursiveLearningModule:
    """Recursive learning with self-improvement and iterative refinement"""
    
    def __init__(self):
        self.logger = NEOLogger("RecursiveLearning")
        self.learning_history = []
        self.max_recursion_depth = 5
        self.improvement_threshold = 0.05
        
    def recursive_solve(self, problem: Dict[str, Any], depth: int = 0) -> Dict[str, Any]:
        """Recursively solve a problem with self-improvement"""
        self.logger.info(f"Recursive solving at depth {depth}")
        
        if depth >= self.max_recursion_depth:
            self.logger.warning("Max recursion depth reached")
            return {'solution': None, 'confidence': 0.0, 'depth': depth}
        
        # Generate initial solution
        solution = self._generate_solution(problem)
        
        # Evaluate solution
        evaluation = self._evaluate_solution(solution, problem)
        
        # If solution is not good enough, recurse
        if evaluation['quality'] < 0.8 and depth < self.max_recursion_depth:
            # Refine problem based on current solution
            refined_problem = self._refine_problem(problem, solution, evaluation)
            
            # Recursive call
            better_solution = self.recursive_solve(refined_problem, depth + 1)
            
            # Choose better solution
            if better_solution['confidence'] > evaluation['quality']:
                solution = better_solution
                evaluation = {'quality': better_solution['confidence']}
        
        # Store learning
        self.learning_history.append({
            'problem': problem,
            'solution': solution,
            'evaluation': evaluation,
            'depth': depth
        })
        
        return {
            'solution': solution,
            'confidence': evaluation['quality'],
            'depth': depth,
            'iterations': len([h for h in self.learning_history if h['depth'] <= depth])
        }
    
    def learn_from_mistakes(self) -> List[Dict[str, Any]]:
        """Analyze learning history to identify improvement areas"""
        insights = []
        
        for entry in self.learning_history:
            if entry['evaluation']['quality'] < 0.6:
                insights.append({
                    'problem_type': entry['problem'].get('type'),
                    'failure_reason': 'Low quality solution',
                    'depth': entry['depth'],
                    'suggestion': 'Increase recursion depth or refine approach'
                })
        
        return insights
    
    def _generate_solution(self, problem: Dict[str, Any]) -> Any:
        """Generate a solution for the problem"""
        # Placeholder - implement actual problem-solving logic
        problem_type = problem.get('type', 'general')
        data = problem.get('data')
        
        return {
            'type': problem_type,
            'result': f"Solution for {problem_type}",
            'data': data
        }
    
    def _evaluate_solution(self, solution: Any, problem: Dict[str, Any]) -> Dict[str, float]:
        """Evaluate the quality of a solution"""
        # Placeholder evaluation - implement actual evaluation logic
        quality = np.random.uniform(0.5, 1.0)  # Simulated quality score
        
        return {
            'quality': quality,
            'accuracy': quality * 0.9,
            'efficiency': quality * 0.95
        }
    
    def _refine_problem(self, problem: Dict[str, Any], solution: Any, evaluation: Dict) -> Dict[str, Any]:
        """Refine problem definition based on previous solution"""
        refined = problem.copy()
        refined['refinement_level'] = refined.get('refinement_level', 0) + 1
        refined['previous_quality'] = evaluation['quality']
        
        return refined


class SmartThinkingModule:
    """Smart thinking and decision-making module"""
    
    def __init__(self):
        self.logger = NEOLogger("SmartThinking")
        self.decision_tree = {}
        self.context_memory = []
        
    def analyze_problem(self, problem: str, context: Dict = None) -> Dict[str, Any]:
        """Analyze a problem and determine best approach"""
        self.logger.info("Analyzing problem with smart thinking")
        
        analysis = {
            'problem': problem,
            'complexity': self._assess_complexity(problem),
            'required_skills': self._identify_required_skills(problem),
            'approach': self._determine_approach(problem),
            'estimated_steps': self._estimate_steps(problem),
            'confidence': 0.85
        }
        
        # Store context
        if context:
            self.context_memory.append({
                'problem': problem,
                'context': context,
                'analysis': analysis
            })
        
        return analysis
    
    def make_decision(self, options: List[Dict[str, Any]], criteria: Dict[str, float]) -> Dict[str, Any]:
        """Make intelligent decision based on options and criteria"""
        self.logger.info(f"Making decision from {len(options)} options")
        
        scored_options = []
        for option in options:
            score = self._calculate_option_score(option, criteria)
            scored_options.append({
                'option': option,
                'score': score
            })
        
        # Sort by score
        scored_options.sort(key=lambda x: x['score'], reverse=True)
        
        best_option = scored_options[0] if scored_options else None
        
        return {
            'selected_option': best_option['option'] if best_option else None,
            'score': best_option['score'] if best_option else 0.0,
            'alternatives': scored_options[1:4],  # Top 3 alternatives
            'reasoning': self._generate_reasoning(best_option, criteria) if best_option else "No valid options"
        }
    
    def _assess_complexity(self, problem: str) -> str:
        """Assess problem complexity"""
        length = len(problem.split())
        
        if length < 10:
            return "simple"
        elif length < 30:
            return "moderate"
        else:
            return "complex"
    
    def _identify_required_skills(self, problem: str) -> List[str]:
        """Identify skills required to solve the problem"""
        skills = []
        
        keywords = {
            'code': ['coding', 'development', 'debugging'],
            'security': ['cybersecurity', 'penetration testing'],
            'research': ['research', 'data collection'],
            'system': ['system control', 'automation'],
            'analysis': ['analysis', 'problem solving']
        }
        
        problem_lower = problem.lower()
        for category, terms in keywords.items():
            if any(term in problem_lower for term in terms):
                skills.append(category)
        
        return skills or ['general']
    
    def _determine_approach(self, problem: str) -> str:
        """Determine best approach for the problem"""
        skills = self._identify_required_skills(problem)
        
        if 'code' in skills:
            return "coding_assistant"
        elif 'security' in skills:
            return "cybersecurity"
        elif 'research' in skills:
            return "research"
        elif 'system' in skills:
            return "system_control"
        else:
            return "general_analysis"
    
    def _estimate_steps(self, problem: str) -> int:
        """Estimate number of steps required"""
        complexity = self._assess_complexity(problem)
        
        steps_map = {
            'simple': 3,
            'moderate': 7,
            'complex': 15
        }
        
        return steps_map.get(complexity, 5)
    
    def _calculate_option_score(self, option: Dict[str, Any], criteria: Dict[str, float]) -> float:
        """Calculate score for an option based on criteria"""
        total_score = 0.0
        total_weight = sum(criteria.values())
        
        for criterion, weight in criteria.items():
            option_value = option.get(criterion, 0.5)
            total_score += option_value * weight
        
        return total_score / total_weight if total_weight > 0 else 0.0
    
    def _generate_reasoning(self, selected_option: Dict, criteria: Dict) -> str:
        """Generate reasoning for the decision"""
        score = selected_option['score']
        return f"Selected option scored {score:.2f} based on weighted criteria evaluation"


class NEOAIEngine:
    """
    Main AI Engine for NEO
    Integrates deep learning, neuro learning, recursive learning, smart thinking, and Gemini AI
    """
    
    def __init__(
        self, 
        model_path: Optional[Path] = None,
        use_gemini: bool = True,
        gemini_model: str = "gemini-2.0-flash"
    ):
        self.logger = NEOLogger("NEOAIEngine")
        self.logger.info("Initializing NEO AI Engine")
        
        # Initialize all learning modules
        self.deep_learning = DeepLearningModule()
        self.neuro_learning = NeuroLearningModule()
        self.recursive_learning = RecursiveLearningModule()
        self.smart_thinking = SmartThinkingModule()
        
        # Initialize Gemini if available and requested
        self.gemini = None
        self.use_gemini = use_gemini
        if use_gemini and GEMINI_AVAILABLE:
            try:
                self.gemini = GeminiIntegration(model_name=gemini_model)
                self.logger.info(f"Gemini AI initialized with model: {gemini_model}")
            except Exception as e:
                self.logger.warning(f"Could not initialize Gemini: {e}")
                self.use_gemini = False
        elif use_gemini and not GEMINI_AVAILABLE:
            self.logger.warning("Gemini requested but not available")
            self.use_gemini = False
        
        # Model path for saving/loading
        self.model_path = model_path or Path("models/neo_ai_engine.pth")
        
        # Performance metrics
        self.metrics = {
            'tasks_processed': 0,
            'successful_predictions': 0,
            'learning_iterations': 0,
            'gemini_calls': 0
        }
        
        self.logger.info("NEO AI Engine initialized successfully")
    
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a task using integrated AI capabilities
        
        Args:
            task: Dictionary containing task information
            
        Returns:
            Dictionary with task results and metadata
        """
        self.logger.info(f"Processing task: {task.get('type', 'unknown')}")
        
        # Step 1: Smart thinking analysis
        analysis = self.smart_thinking.analyze_problem(
            task.get('description', ''),
            task.get('context')
        )
        
        # Step 2: Pattern recognition
        patterns = self.neuro_learning.recognize_pattern(task.get('data'))
        
        # Step 3: Recursive problem solving if needed
        if analysis['complexity'] in ['moderate', 'complex']:
            solution = self.recursive_learning.recursive_solve({
                'type': task.get('type'),
                'data': task.get('data'),
                'analysis': analysis
            })
        else:
            solution = {'solution': 'Direct solution', 'confidence': 0.9, 'depth': 0}
        
        # Update metrics
        self.metrics['tasks_processed'] += 1
        
        result = {
            'task_id': task.get('id'),
            'analysis': analysis,
            'patterns': patterns,
            'solution': solution,
            'confidence': solution['confidence'],
            'timestamp': self._get_timestamp()
        }
        
        self.logger.info(f"Task processed successfully with confidence {solution['confidence']:.2f}")
        
        return result
    
    def learn(self, training_data: List[Dict[str, Any]], epochs: int = 10) -> Dict[str, float]:
        """
        Train the AI engine on provided data
        
        Args:
            training_data: List of training examples
            epochs: Number of training epochs
            
        Returns:
            Training metrics
        """
        self.logger.info(f"Starting training on {len(training_data)} examples for {epochs} epochs")
        
        total_loss = 0.0
        
        for epoch in range(epochs):
            epoch_loss = 0.0
            
            for data in training_data:
                # Convert to tensor
                input_tensor = self._prepare_input(data['input'])
                target_tensor = self._prepare_target(data.get('target'))
                
                # Train deep learning module
                loss = self.deep_learning.learn(input_tensor, target_tensor)
                epoch_loss += loss
                
                # Store pattern in neuro learning
                self.neuro_learning.store_pattern(data['input'], data.get('metadata'))
            
            avg_loss = epoch_loss / len(training_data)
            total_loss += avg_loss
            
            self.logger.info(f"Epoch {epoch + 1}/{epochs} - Loss: {avg_loss:.4f}")
            
            self.metrics['learning_iterations'] += 1
        
        final_metrics = {
            'average_loss': total_loss / epochs,
            'epochs': epochs,
            'samples': len(training_data)
        }
        
        self.logger.info(f"Training completed. Average loss: {final_metrics['average_loss']:.4f}")
        
        return final_metrics
    
    def predict(self, input_data: Any) -> Dict[str, Any]:
        """
        Make prediction on input data
        
        Args:
            input_data: Input data for prediction
            
        Returns:
            Prediction results
        """
        self.logger.info("Making prediction")
        
        # Prepare input
        input_tensor = self._prepare_input(input_data)
        
        # Deep learning prediction
        with torch.no_grad():
            output = self.deep_learning(input_tensor)
        
        # Pattern matching
        patterns = self.neuro_learning.recognize_pattern(input_data)
        
        prediction = {
            'output': output.numpy(),
            'patterns': patterns,
            'confidence': self._calculate_confidence(output, patterns)
        }
        
        self.metrics['successful_predictions'] += 1
        
        return prediction
    
    def save_model(self, path: Optional[Path] = None) -> None:
        """Save the AI engine model"""
        save_path = path or self.model_path
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        state = {
            'deep_learning_state': self.deep_learning.state_dict(),
            'neuro_patterns': self.neuro_learning.pattern_database,
            'metrics': self.metrics
        }
        
        torch.save(state, save_path)
        self.logger.info(f"Model saved to {save_path}")
    
    def load_model(self, path: Optional[Path] = None) -> None:
        """Load the AI engine model"""
        load_path = path or self.model_path
        
        if not load_path.exists():
            self.logger.warning(f"Model file not found at {load_path}")
            return
        
        state = torch.load(load_path)
        
        self.deep_learning.load_state_dict(state['deep_learning_state'])
        self.neuro_learning.pattern_database = state['neuro_patterns']
        self.metrics = state['metrics']
        
        self.logger.info(f"Model loaded from {load_path}")
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        return self.metrics.copy()
    
    def _prepare_input(self, data: Any) -> torch.Tensor:
        """Prepare input data as tensor"""
        if isinstance(data, torch.Tensor):
            return data
        elif isinstance(data, np.ndarray):
            return torch.from_numpy(data).float()
        elif isinstance(data, list):
            return torch.tensor(data, dtype=torch.float32)
        else:
            # Default: create random tensor
            return torch.randn(1, 512)
    
    def _prepare_target(self, data: Any) -> torch.Tensor:
        """Prepare target data as tensor"""
        if data is None:
            return torch.randn(1, 256)
        return self._prepare_input(data)
    
    def _calculate_confidence(self, output: torch.Tensor, patterns: Dict) -> float:
        """Calculate prediction confidence"""
        # Combine neural network output variance and pattern matching
        output_confidence = 1.0 - output.std().item()
        pattern_confidence = len(patterns['matches']) / 10.0  # Normalize
        
        return (output_confidence + pattern_confidence) / 2.0
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    # Gemini-powered methods
    
    def generate_response(
        self, 
        prompt: str, 
        use_ai: bool = True,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> str:
        """
        Generate intelligent response using Gemini
        
        Args:
            prompt: Input prompt
            use_ai: Whether to use Gemini AI (falls back to basic if unavailable)
            temperature: Creativity level (0.0-1.0)
            max_tokens: Maximum response length
            
        Returns:
            Generated response
        """
        if use_ai and self.gemini:
            try:
                response = self.gemini.generate_text(
                    prompt, 
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                self.metrics['gemini_calls'] += 1
                return response.text
            except Exception as e:
                self.logger.error(f"Gemini generation error: {e}")
                return f"I'm processing your request locally. Please try again."
        else:
            return f"I understand you're asking about: {prompt[:100]}..."
    
    def chat_with_gemini(
        self, 
        message: str,
        context: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Chat with Gemini AI
        
        Args:
            message: User message
            context: Optional conversation context
            
        Returns:
            AI response
        """
        if not self.gemini:
            return "Gemini AI is not available. Please check your API key."
        
        try:
            chat_session = self.gemini.start_chat(context)
            response = self.gemini.chat(message, chat_session)
            self.metrics['gemini_calls'] += 1
            return response.text
        except Exception as e:
            self.logger.error(f"Gemini chat error: {e}")
            return f"Sorry, I encountered an error: {e}"
    
    def analyze_code_with_ai(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Analyze code using Gemini AI
        
        Args:
            code: Source code
            language: Programming language
            
        Returns:
            Detailed code analysis
        """
        if not self.gemini:
            return {
                "error": "Gemini AI not available",
                "quality_score": None
            }
        
        try:
            analysis = self.gemini.analyze_code(code, language)
            self.metrics['gemini_calls'] += 1
            return analysis
        except Exception as e:
            self.logger.error(f"Code analysis error: {e}")
            return {"error": str(e)}
    
    def solve_with_ai(self, problem: str, context: Optional[str] = None) -> str:
        """
        Solve a problem using Gemini's reasoning
        
        Args:
            problem: Problem description
            context: Optional context
            
        Returns:
            Solution with reasoning
        """
        if not self.gemini:
            # Use local recursive learning as fallback
            problem_dict = {
                'description': problem,
                'complexity': 'moderate',
                'context': context or {}
            }
            result = self.recursive_learning.solve(problem_dict)
            return str(result.get('solution', 'No solution found'))
        
        try:
            solution = self.gemini.solve_problem(problem, context)
            self.metrics['gemini_calls'] += 1
            return solution
        except Exception as e:
            self.logger.error(f"Problem solving error: {e}")
            return f"Error solving problem: {e}"
    
    def summarize_with_ai(self, text: str, max_length: int = 200) -> str:
        """
        Summarize text using Gemini
        
        Args:
            text: Text to summarize
            max_length: Maximum summary length
            
        Returns:
            Summary
        """
        if not self.gemini:
            # Basic summarization
            return text[:max_length] + "..." if len(text) > max_length else text
        
        try:
            summary = self.gemini.summarize_text(text, max_length)
            self.metrics['gemini_calls'] += 1
            return summary
        except Exception as e:
            self.logger.error(f"Summarization error: {e}")
            return text[:max_length] + "..."
    
    def translate_with_ai(self, text: str, target_language: str) -> str:
        """
        Translate text using Gemini
        
        Args:
            text: Text to translate
            target_language: Target language
            
        Returns:
            Translated text
        """
        if not self.gemini:
            return f"Translation not available. Original: {text}"
        
        try:
            translation = self.gemini.translate_text(text, target_language)
            self.metrics['gemini_calls'] += 1
            return translation
        except Exception as e:
            self.logger.error(f"Translation error: {e}")
            return text
    
    def is_gemini_available(self) -> bool:
        """Check if Gemini AI is available"""
        return self.gemini is not None
    
    def get_gemini_models(self) -> List[str]:
        """Get available Gemini models"""
        if not self.gemini:
            return []
        return self.gemini.get_available_models()
    
    def switch_gemini_model(self, model_name: str) -> bool:
        """
        Switch to a different Gemini model
        
        Args:
            model_name: Model name (e.g., 'gemini-pro', 'gemini-pro-vision')
            
        Returns:
            Success status
        """
        if not GEMINI_AVAILABLE:
            return False
        
        try:
            self.gemini = GeminiIntegration(model_name=model_name)
            self.logger.info(f"Switched to Gemini model: {model_name}")
            return True
        except Exception as e:
            self.logger.error(f"Error switching model: {e}")
            return False


if __name__ == "__main__":
    # Test the AI Engine
    engine = NEOAIEngine()
    
    # Test task processing
    task = {
        'id': 'test_001',
        'type': 'analysis',
        'description': 'Analyze system performance',
        'data': [1, 2, 3, 4, 5],
        'context': {'priority': 'high'}
    }
    
    result = engine.process_task(task)
    print(f"Task processed: {result['confidence']:.2f} confidence")
    
    # Test prediction
    prediction = engine.predict([1.0, 2.0, 3.0])
    print(f"Prediction confidence: {prediction['confidence']:.2f}")
