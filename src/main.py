"""
NEO: Neural Executive Operator
Main Application Entry Point
"""

import sys
import json
import argparse
from typing import Dict, List, Any, Optional
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.ai_engine import NEOAIEngine
from src.modules.system_control import SystemControl
from src.modules.cybersecurity import CybersecurityModule
from src.modules.coding_assistant import CodingAssistant
from src.modules.research import ResearchModule
from src.modules.task_automation import TaskAutomation, TaskPriority
from src.modules.nlp_conversation import NLPConversation
from src.utils.logger import NEOLogger
from config.settings import settings


class NEOAssistant:
    """
    Main NEO Assistant - Integrates all modules and capabilities
    """
    
    def __init__(self):
        self.logger = NEOLogger("NEO")
        self.logger.info("=" * 60)
        self.logger.info(f"Initializing {settings.app_name} v{settings.app_version}")
        self.logger.info("=" * 60)
        
        # Initialize all modules
        self.logger.info("Loading AI Engine...")
        self.ai_engine = NEOAIEngine()
        
        self.logger.info("Loading System Control...")
        self.system_control = SystemControl()
        
        self.logger.info("Loading Cybersecurity Module...")
        self.cybersecurity = CybersecurityModule()
        
        self.logger.info("Loading Coding Assistant...")
        self.coding_assistant = CodingAssistant()
        
        self.logger.info("Loading Research Module...")
        self.research = ResearchModule()
        
        self.logger.info("Loading Task Automation...")
        self.task_automation = TaskAutomation(max_workers=settings.task.max_workers)
        
        self.logger.info("Loading NLP Conversation...")
        self.nlp = NLPConversation()
        
        # Create default conversation session
        self.current_session = self.nlp.create_conversation("default_user")
        
        self.logger.info("✓ All modules loaded successfully")
        self.logger.info("=" * 60)
    
    def process_command(self, command: str) -> Dict[str, Any]:
        """
        Process a command using AI and appropriate modules
        
        Args:
            command: User command
        
        Returns:
            Command result
        """
        self.logger.info(f"Processing command: {command[:50]}...")
        
        # Analyze command with NLP
        analysis = self.nlp.process_message(self.current_session, command, role="user")
        
        intent = analysis.get("intent", "unknown")
        entities = analysis.get("entities", {})
        
        self.logger.info(f"Detected intent: {intent} (confidence: {analysis['confidence']:.2f})")
        
        # Route to appropriate module based on intent
        result = None
        
        try:
            if intent == "system_control":
                result = self._handle_system_control(command, entities)
            
            elif intent == "security":
                result = self._handle_security(command, entities)
            
            elif intent == "code_request":
                result = self._handle_coding(command, entities)
            
            elif intent == "research":
                result = self._handle_research(command, entities)
            
            elif intent == "question":
                result = self._handle_question(command, entities)
            
            elif intent in ["greeting", "farewell", "help", "gratitude"]:
                result = {
                    "response": self.nlp.generate_response(self.current_session, command),
                    "type": "conversation"
                }
            
            else:
                # Use AI engine for general processing
                task_result = self.ai_engine.process_task({
                    "type": intent,
                    "description": command,
                    "data": entities
                })
                
                result = {
                    "response": f"Processed with AI engine (confidence: {task_result['confidence']:.2f})",
                    "ai_result": task_result,
                    "type": "ai_processing"
                }
        
        except Exception as e:
            self.logger.error(f"Error processing command: {e}")
            result = {
                "error": str(e),
                "type": "error"
            }
        
        return result
    
    def _handle_system_control(self, command: str, entities: Dict) -> Dict[str, Any]:
        """Handle system control commands"""
        command_lower = command.lower()
        
        if "system info" in command_lower or "system information" in command_lower:
            info = self.system_control.get_system_info()
            return {
                "type": "system_info",
                "data": info,
                "response": f"System: {info['platform']['system']} {info['platform']['release']}, CPU: {info['cpu']['usage_percent']}%, Memory: {info['memory']['percent']}%"
            }
        
        elif "processes" in command_lower:
            processes = self.system_control.get_running_processes(limit=10)
            return {
                "type": "processes",
                "data": processes,
                "response": f"Found {len(processes)} top processes"
            }
        
        elif "shutdown" in command_lower:
            if settings.system.enable_shutdown:
                result = self.system_control.shutdown(delay=10)
                return {
                    "type": "shutdown",
                    "data": result,
                    "response": "Shutdown initiated (safe mode - not executed)"
                }
            else:
                return {
                    "type": "shutdown",
                    "response": "Shutdown is disabled in configuration for safety"
                }
        
        else:
            return {
                "type": "system_control",
                "response": "Available system commands: system info, processes, shutdown (disabled by default)"
            }
    
    def _handle_security(self, command: str, entities: Dict) -> Dict[str, Any]:
        """Handle security commands"""
        command_lower = command.lower()
        
        if "password" in command_lower:
            if "generate" in command_lower:
                password = self.cybersecurity.generate_secure_password(16)
                return {
                    "type": "password_generation",
                    "password": password,
                    "response": f"Generated secure password: {password}"
                }
            elif "check" in command_lower or "analyze" in command_lower:
                # Extract password from entities or command
                password = entities.get("password", "example123")
                analysis = self.cybersecurity.password_strength_analysis(password)
                return {
                    "type": "password_analysis",
                    "data": analysis,
                    "response": f"Password strength: {analysis['strength']} (score: {analysis['score']}/100)"
                }
        
        elif "scan" in command_lower and "port" in command_lower:
            target = entities.get("url", ["localhost"])[0] if "url" in entities else "localhost"
            result = self.cybersecurity.port_scan(target)
            return {
                "type": "port_scan",
                "data": result,
                "response": f"Port scan completed: {result['open_count']} open ports found"
            }
        
        else:
            return {
                "type": "security",
                "response": "Available security commands: password generate, password check, port scan"
            }
    
    def _handle_coding(self, command: str, entities: Dict) -> Dict[str, Any]:
        """Handle coding requests"""
        command_lower = command.lower()
        
        if "analyze" in command_lower:
            # Simulate code analysis
            sample_code = "def hello():\n    print('Hello, World!')"
            analysis = self.coding_assistant.analyze_code(sample_code)
            return {
                "type": "code_analysis",
                "data": vars(analysis),
                "response": f"Code quality score: {analysis.quality_score}/100"
            }
        
        elif "debug" in command_lower:
            result = self.coding_assistant.debug_code(
                "print(x)",
                error_message="NameError: name 'x' is not defined"
            )
            return {
                "type": "code_debug",
                "data": result,
                "response": "Debug suggestions generated"
            }
        
        else:
            return {
                "type": "coding",
                "response": "I can help with: code analysis, debugging, optimization, and documentation"
            }
    
    def _handle_research(self, command: str, entities: Dict) -> Dict[str, Any]:
        """Handle research requests"""
        # Extract topic from command
        topic = command.replace("research", "").replace("find", "").replace("search", "").strip()
        
        if not topic:
            topic = "artificial intelligence"
        
        result = self.research.research_topic(topic, depth="moderate")
        
        return {
            "type": "research",
            "data": vars(result),
            "response": f"Research completed on '{result.query}' with {result.confidence} confidence. Found {len(result.sources)} sources."
        }
    
    def _handle_question(self, command: str, entities: Dict) -> Dict[str, Any]:
        """Handle general questions using Gemini AI"""
        # Try to use Gemini first for better responses
        if self.ai_engine.is_gemini_available():
            try:
                response = self.ai_engine.generate_response(
                    command,
                    use_ai=True,
                    temperature=0.7
                )
                return {
                    "type": "question",
                    "response": response,
                    "source": "gemini"
                }
            except Exception as e:
                self.logger.warning(f"Gemini fallback: {e}")
        
        # Fallback to local AI engine
        task_result = self.ai_engine.process_task({
            "type": "question",
            "description": command,
            "data": entities
        })
        
        response = self.nlp.generate_response(self.current_session, command)
        
        return {
            "type": "question",
            "response": response,
            "ai_analysis": task_result,
            "source": "local"
        }
    
    def interactive_mode(self):
        """Run NEO in interactive mode"""
        self.logger.info("Starting interactive mode...")
        print("\n" + "=" * 60)
        print(f"🔹 {settings.app_name} - Neural Executive Operator")
        print(f"Version: {settings.app_version}")
        
        # Show Gemini status
        if self.ai_engine.is_gemini_available():
            print("🤖 Gemini AI: Active")
        else:
            print("⚠️  Gemini AI: Not available (set GEMINI_API_KEY)")
        
        print("=" * 60)
        print("\nType 'help' for available commands, 'exit' to quit.")
        print("Special commands: /ai <query>, /code <code>, /solve <problem>\n")
        
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Check for exit
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("\nNEO: Goodbye! Have a great day!")
                    break
                
                # Handle special Gemini commands
                if user_input.startswith('/'):
                    result = self._handle_special_command(user_input)
                else:
                    # Process normal command
                    result = self.process_command(user_input)
                
                # Display response
                response = result.get("response", "Command processed")
                print(f"\nNEO: {response}\n")
                
            except KeyboardInterrupt:
                print("\n\nNEO: Interrupted. Goodbye!")
                break
            except Exception as e:
                self.logger.error(f"Error in interactive mode: {e}")
                print(f"\nNEO: An error occurred: {e}\n")
    
    def _handle_special_command(self, command: str) -> Dict[str, Any]:
        """Handle special slash commands for Gemini"""
        parts = command.split(maxsplit=1)
        cmd = parts[0].lower()
        query = parts[1] if len(parts) > 1 else ""
        
        if cmd == "/ai" and query:
            # Direct Gemini query
            response = self.ai_engine.generate_response(query, use_ai=True)
            return {"response": response, "type": "gemini_direct"}
        
        elif cmd == "/code" and query:
            # Code analysis with Gemini
            analysis = self.ai_engine.analyze_code_with_ai(query)
            if "error" in analysis:
                return {"response": analysis["error"], "type": "error"}
            return {
                "response": f"Code Analysis:\n{json.dumps(analysis, indent=2)}",
                "type": "code_analysis"
            }
        
        elif cmd == "/solve" and query:
            # Problem solving with Gemini
            solution = self.ai_engine.solve_with_ai(query)
            return {"response": solution, "type": "problem_solving"}
        
        elif cmd == "/summarize" and query:
            # Summarize text
            summary = self.ai_engine.summarize_with_ai(query)
            return {"response": f"Summary: {summary}", "type": "summarization"}
        
        elif cmd == "/translate" and query:
            # Translation (format: /translate <language> <text>)
            parts = query.split(maxsplit=1)
            if len(parts) == 2:
                lang, text = parts
                translation = self.ai_engine.translate_with_ai(text, lang)
                return {"response": f"Translation: {translation}", "type": "translation"}
            else:
                return {"response": "Usage: /translate <language> <text>", "type": "help"}
        
        elif cmd == "/models":
            # List available models
            models = self.ai_engine.get_gemini_models()
            return {
                "response": f"Available models:\n" + "\n".join(models) if models else "No models available",
                "type": "models"
            }
        
        elif cmd == "/help":
            help_text = """
Special Commands:
  /ai <query>              - Direct AI query with Gemini
  /code <code>             - Analyze code with AI
  /solve <problem>         - Solve a problem with AI reasoning
  /summarize <text>        - Summarize text
  /translate <lang> <text> - Translate text to target language
  /models                  - List available AI models
  /help                    - Show this help

Regular Commands:
  - Ask questions naturally
  - "show system info" - Get system information
  - "scan ports" - Security scan
  - "analyze code" - Code analysis
  - "research <topic>" - Research a topic
"""
            return {"response": help_text, "type": "help"}
        
        else:
            return {
                "response": "Unknown command. Type /help for available commands.",
                "type": "error"
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Get NEO status"""
        return {
            "name": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment,
            "modules": {
                "ai_engine": "active",
                "system_control": "active",
                "cybersecurity": "active",
                "coding_assistant": "active",
                "research": "active",
                "task_automation": "active",
                "nlp_conversation": "active"
            },
            "metrics": self.ai_engine.get_metrics(),
            "task_stats": self.task_automation.get_statistics()
        }


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="NEO: Neural Executive Operator - Advanced AI Assistant"
    )
    
    parser.add_argument(
        "--mode",
        choices=["interactive", "command", "server"],
        default="interactive",
        help="Operation mode"
    )
    
    parser.add_argument(
        "--command",
        type=str,
        help="Command to execute (for command mode)"
    )
    
    parser.add_argument(
        "--config",
        type=str,
        help="Path to configuration file"
    )
    
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version information"
    )
    
    args = parser.parse_args()
    
    # Show version
    if args.version:
        print(f"{settings.app_name} v{settings.app_version}")
        return
    
    # Load custom config if provided
    if args.config:
        settings.load_from_file(args.config)
    
    # Initialize NEO
    neo = NEOAssistant()
    
    # Run in specified mode
    if args.mode == "interactive":
        neo.interactive_mode()
    
    elif args.mode == "command":
        if not args.command:
            print("Error: --command required for command mode")
            return
        
        result = neo.process_command(args.command)
        print(result.get("response", "Command executed"))
    
    elif args.mode == "server":
        print("Server mode not yet implemented")
        # TODO: Implement FastAPI server mode
    
    else:
        print("Invalid mode")


if __name__ == "__main__":
    main()
