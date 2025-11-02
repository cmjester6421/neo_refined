"""
Google Gemini AI Integration for NEO
Provides advanced AI capabilities using Google's Gemini models
"""

import os
from typing import Dict, List, Any, Optional, Generator
from dataclasses import dataclass
import json

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

from src.utils.logger import NEOLogger


@dataclass
class GeminiResponse:
    """Response from Gemini API"""
    text: str
    model: str
    finish_reason: str
    safety_ratings: List[Dict[str, Any]]
    usage_metadata: Optional[Dict[str, int]] = None


class GeminiIntegration:
    """
    Google Gemini AI Integration
    
    Provides access to Google's advanced Gemini models for:
    - Natural language understanding and generation
    - Code generation and analysis
    - Reasoning and problem-solving
    - Multi-turn conversations
    - Vision understanding (Gemini Pro Vision)
    """
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.0-flash"):
        """
        Initialize Gemini integration
        
        Args:
            api_key: Google API key (or set GEMINI_API_KEY env var)
            model_name: Gemini model to use (gemini-2.0-flash, gemini-2.5-pro, etc.)
        """
        self.logger = NEOLogger("GeminiAI")
        
        if not GEMINI_AVAILABLE:
            self.logger.error("google-generativeai package not installed")
            raise ImportError("Please install: pip install google-generativeai")
        
        # Get API key
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            self.logger.error("Gemini API key not found")
            raise ValueError("GEMINI_API_KEY environment variable not set")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)
        self.chat_history: List[Dict[str, str]] = []
        
        self.logger.info(f"Gemini integration initialized with model: {model_name}")
    
    def generate_text(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        top_p: float = 0.95,
        top_k: int = 40
    ) -> GeminiResponse:
        """
        Generate text using Gemini
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens to generate
            top_p: Top-p sampling parameter
            top_k: Top-k sampling parameter
            
        Returns:
            GeminiResponse object
        """
        try:
            self.logger.debug(f"Generating text with prompt length: {len(prompt)}")
            
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
                top_p=top_p,
                top_k=top_k
            )
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            # Extract response data
            result = GeminiResponse(
                text=response.text,
                model=self.model_name,
                finish_reason=response.candidates[0].finish_reason.name if response.candidates else "UNKNOWN",
                safety_ratings=[
                    {
                        "category": rating.category.name,
                        "probability": rating.probability.name
                    }
                    for rating in response.candidates[0].safety_ratings
                ] if response.candidates else [],
                usage_metadata={
                    "prompt_token_count": getattr(response.usage_metadata, 'prompt_token_count', 0),
                    "candidates_token_count": getattr(response.usage_metadata, 'candidates_token_count', 0),
                    "total_token_count": getattr(response.usage_metadata, 'total_token_count', 0)
                } if hasattr(response, 'usage_metadata') else None
            )
            
            self.logger.info(f"Generated {len(result.text)} characters")
            return result
            
        except Exception as e:
            self.logger.error(f"Error generating text: {e}")
            raise
    
    def generate_streaming(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> Generator[str, None, None]:
        """
        Generate text with streaming response
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens
            
        Yields:
            Text chunks as they are generated
        """
        try:
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens
            )
            
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config,
                stream=True
            )
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            self.logger.error(f"Error in streaming generation: {e}")
            raise
    
    def start_chat(self, history: Optional[List[Dict[str, str]]] = None):
        """
        Start a chat session
        
        Args:
            history: Optional chat history
            
        Returns:
            Chat session object
        """
        try:
            # Convert history to Gemini format
            gemini_history = []
            if history:
                for msg in history:
                    gemini_history.append({
                        "role": msg.get("role", "user"),
                        "parts": [msg.get("content", "")]
                    })
            
            chat = self.model.start_chat(history=gemini_history)
            self.logger.info("Chat session started")
            return chat
            
        except Exception as e:
            self.logger.error(f"Error starting chat: {e}")
            raise
    
    def chat(
        self,
        message: str,
        chat_session=None,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> GeminiResponse:
        """
        Send a message in a chat session
        
        Args:
            message: User message
            chat_session: Existing chat session (or creates new one)
            temperature: Sampling temperature
            max_tokens: Maximum tokens
            
        Returns:
            GeminiResponse object
        """
        try:
            if chat_session is None:
                chat_session = self.start_chat()
            
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens
            )
            
            response = chat_session.send_message(
                message,
                generation_config=generation_config
            )
            
            result = GeminiResponse(
                text=response.text,
                model=self.model_name,
                finish_reason=response.candidates[0].finish_reason.name if response.candidates else "UNKNOWN",
                safety_ratings=[
                    {
                        "category": rating.category.name,
                        "probability": rating.probability.name
                    }
                    for rating in response.candidates[0].safety_ratings
                ] if response.candidates else []
            )
            
            # Store in history
            self.chat_history.append({"role": "user", "content": message})
            self.chat_history.append({"role": "assistant", "content": result.text})
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error in chat: {e}")
            raise
    
    def analyze_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Analyze code using Gemini
        
        Args:
            code: Source code to analyze
            language: Programming language
            
        Returns:
            Analysis results
        """
        prompt = f"""Analyze the following {language} code and provide:
1. Code quality assessment
2. Potential bugs or issues
3. Performance optimization suggestions
4. Security concerns
5. Best practices recommendations

Code:
```{language}
{code}
```

Provide the analysis in JSON format with keys: quality_score, bugs, optimizations, security, recommendations"""
        
        try:
            response = self.generate_text(prompt, temperature=0.3)
            
            # Try to parse JSON from response
            try:
                # Extract JSON from markdown code blocks if present
                text = response.text
                if "```json" in text:
                    text = text.split("```json")[1].split("```")[0].strip()
                elif "```" in text:
                    text = text.split("```")[1].split("```")[0].strip()
                
                analysis = json.loads(text)
            except json.JSONDecodeError:
                # If not JSON, return structured response
                analysis = {
                    "raw_analysis": response.text,
                    "quality_score": None,
                    "bugs": [],
                    "optimizations": [],
                    "security": [],
                    "recommendations": []
                }
            
            self.logger.info(f"Code analysis completed for {len(code)} characters")
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error analyzing code: {e}")
            raise
    
    def solve_problem(self, problem: str, context: Optional[str] = None) -> str:
        """
        Use Gemini to solve a problem with reasoning
        
        Args:
            problem: Problem description
            context: Optional context
            
        Returns:
            Solution with reasoning
        """
        prompt = f"""Problem: {problem}

{f'Context: {context}' if context else ''}

Please provide a detailed solution with step-by-step reasoning. Think through the problem carefully and explain your approach."""
        
        try:
            response = self.generate_text(prompt, temperature=0.5)
            return response.text
            
        except Exception as e:
            self.logger.error(f"Error solving problem: {e}")
            raise
    
    def summarize_text(self, text: str, max_length: int = 200) -> str:
        """
        Summarize long text
        
        Args:
            text: Text to summarize
            max_length: Maximum summary length in words
            
        Returns:
            Summary
        """
        prompt = f"""Summarize the following text in {max_length} words or less:

{text}

Summary:"""
        
        try:
            response = self.generate_text(prompt, temperature=0.3, max_tokens=max_length * 2)
            return response.text.strip()
            
        except Exception as e:
            self.logger.error(f"Error summarizing text: {e}")
            raise
    
    def translate_text(self, text: str, target_language: str) -> str:
        """
        Translate text to target language
        
        Args:
            text: Text to translate
            target_language: Target language
            
        Returns:
            Translated text
        """
        prompt = f"""Translate the following text to {target_language}:

{text}

Translation:"""
        
        try:
            response = self.generate_text(prompt, temperature=0.3)
            return response.text.strip()
            
        except Exception as e:
            self.logger.error(f"Error translating text: {e}")
            raise
    
    def get_available_models(self) -> List[str]:
        """Get list of available Gemini models"""
        try:
            models = genai.list_models()
            model_names = [model.name for model in models if 'generateContent' in model.supported_generation_methods]
            self.logger.info(f"Found {len(model_names)} available models")
            return model_names
        except Exception as e:
            self.logger.error(f"Error listing models: {e}")
            return []
    
    def count_tokens(self, text: str) -> int:
        """
        Count tokens in text
        
        Args:
            text: Input text
            
        Returns:
            Token count
        """
        try:
            token_count = self.model.count_tokens(text)
            return token_count.total_tokens
        except Exception as e:
            self.logger.error(f"Error counting tokens: {e}")
            return 0
    
    def clear_history(self):
        """Clear chat history"""
        self.chat_history = []
        self.logger.info("Chat history cleared")
    
    def export_history(self, filepath: str):
        """
        Export chat history to file
        
        Args:
            filepath: Path to save history
        """
        try:
            with open(filepath, 'w') as f:
                json.dump(self.chat_history, f, indent=2)
            self.logger.info(f"History exported to {filepath}")
        except Exception as e:
            self.logger.error(f"Error exporting history: {e}")
            raise


# Convenience functions
def create_gemini_client(model: str = "gemini-2.0-flash") -> GeminiIntegration:
    """Create a Gemini client instance"""
    return GeminiIntegration(model_name=model)


def quick_generate(prompt: str, model: str = "gemini-2.0-flash") -> str:
    """Quick text generation"""
    client = create_gemini_client(model)
    response = client.generate_text(prompt)
    return response.text


def quick_chat(message: str, model: str = "gemini-2.0-flash") -> str:
    """Quick chat interaction"""
    client = create_gemini_client(model)
    chat = client.start_chat()
    response = client.chat(message, chat)
    return response.text
