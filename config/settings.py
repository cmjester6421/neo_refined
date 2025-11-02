"""
NEO Configuration and Settings Management
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import json
import yaml
from dotenv import load_dotenv
from dataclasses import dataclass, asdict


@dataclass
class AIConfig:
    """AI Engine configuration"""
    model_path: str = "models/neo_ai_engine.pth"
    learning_rate: float = 0.001
    max_recursion_depth: int = 5
    confidence_threshold: float = 0.8


@dataclass
class SystemConfig:
    """System control configuration"""
    enable_shutdown: bool = False  # Safety: disabled by default
    enable_restart: bool = False
    max_retries: int = 3
    timeout: int = 30


@dataclass
class SecurityConfig:
    """Security configuration"""
    enable_port_scanning: bool = True
    max_scan_timeout: float = 2.0
    password_min_length: int = 8
    enable_vulnerability_scan: bool = True


@dataclass
class ResearchConfig:
    """Research configuration"""
    default_depth: str = "moderate"
    max_sources: int = 10
    cache_results: bool = True
    cache_ttl: int = 3600  # 1 hour


@dataclass
class TaskConfig:
    """Task automation configuration"""
    max_workers: int = 5
    max_retries: int = 3
    queue_size: int = 100


@dataclass
class NLPConfig:
    """NLP configuration"""
    confidence_threshold: float = 0.7
    max_context_messages: int = 10
    enable_sentiment_analysis: bool = True


@dataclass
class LoggingConfig:
    """Logging configuration"""
    log_level: str = "INFO"
    log_dir: str = "logs"
    max_log_size: int = 10485760  # 10MB
    backup_count: int = 5


class Settings:
    """
    NEO Settings Management
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize settings
        
        Args:
            config_file: Path to configuration file (YAML or JSON)
        """
        # Load environment variables
        load_dotenv()
        
        # Initialize configs with defaults
        self.ai = AIConfig()
        self.system = SystemConfig()
        self.security = SecurityConfig()
        self.research = ResearchConfig()
        self.task = TaskConfig()
        self.nlp = NLPConfig()
        self.logging = LoggingConfig()
        
        # General settings
        self.app_name = "NEO"
        self.app_version = "1.0.0"
        self.environment = os.getenv("NEO_ENV", "development")
        self.debug = os.getenv("NEO_DEBUG", "false").lower() == "true"
        
        # API keys (from environment variables)
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        
        # Paths
        self.base_dir = Path(os.getenv("NEO_BASE_DIR", os.getcwd()))
        self.data_dir = self.base_dir / "data"
        self.models_dir = self.base_dir / "models"
        self.logs_dir = self.base_dir / "logs"
        
        # Create directories
        self._create_directories()
        
        # Load from config file if provided
        if config_file:
            self.load_from_file(config_file)
    
    def _create_directories(self):
        """Create necessary directories"""
        for directory in [self.data_dir, self.models_dir, self.logs_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def load_from_file(self, config_file: str):
        """
        Load configuration from file
        
        Args:
            config_file: Path to config file (YAML or JSON)
        """
        config_path = Path(config_file)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_file}")
        
        # Load based on file extension
        if config_path.suffix in [".yaml", ".yml"]:
            with open(config_path, 'r') as f:
                config_data = yaml.safe_load(f)
        elif config_path.suffix == ".json":
            with open(config_path, 'r') as f:
                config_data = json.load(f)
        else:
            raise ValueError(f"Unsupported config file format: {config_path.suffix}")
        
        # Update configurations
        self._update_from_dict(config_data)
    
    def _update_from_dict(self, config_data: Dict[str, Any]):
        """Update configuration from dictionary"""
        if "ai" in config_data:
            for key, value in config_data["ai"].items():
                if hasattr(self.ai, key):
                    setattr(self.ai, key, value)
        
        if "system" in config_data:
            for key, value in config_data["system"].items():
                if hasattr(self.system, key):
                    setattr(self.system, key, value)
        
        if "security" in config_data:
            for key, value in config_data["security"].items():
                if hasattr(self.security, key):
                    setattr(self.security, key, value)
        
        if "research" in config_data:
            for key, value in config_data["research"].items():
                if hasattr(self.research, key):
                    setattr(self.research, key, value)
        
        if "task" in config_data:
            for key, value in config_data["task"].items():
                if hasattr(self.task, key):
                    setattr(self.task, key, value)
        
        if "nlp" in config_data:
            for key, value in config_data["nlp"].items():
                if hasattr(self.nlp, key):
                    setattr(self.nlp, key, value)
        
        if "logging" in config_data:
            for key, value in config_data["logging"].items():
                if hasattr(self.logging, key):
                    setattr(self.logging, key, value)
    
    def save_to_file(self, config_file: str, format: str = "yaml"):
        """
        Save configuration to file
        
        Args:
            config_file: Path to save config
            format: File format (yaml or json)
        """
        config_data = {
            "app_name": self.app_name,
            "app_version": self.app_version,
            "environment": self.environment,
            "ai": asdict(self.ai),
            "system": asdict(self.system),
            "security": asdict(self.security),
            "research": asdict(self.research),
            "task": asdict(self.task),
            "nlp": asdict(self.nlp),
            "logging": asdict(self.logging)
        }
        
        config_path = Path(config_file)
        
        if format == "yaml":
            with open(config_path, 'w') as f:
                yaml.dump(config_data, f, default_flow_style=False, indent=2)
        elif format == "json":
            with open(config_path, 'w') as f:
                json.dump(config_data, f, indent=2)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration as dictionary"""
        return {
            "app_name": self.app_name,
            "app_version": self.app_version,
            "environment": self.environment,
            "debug": self.debug,
            "ai": asdict(self.ai),
            "system": asdict(self.system),
            "security": asdict(self.security),
            "research": asdict(self.research),
            "task": asdict(self.task),
            "nlp": asdict(self.nlp),
            "logging": asdict(self.logging)
        }
    
    def validate(self) -> Dict[str, Any]:
        """Validate configuration"""
        issues = []
        
        # Validate AI config
        if self.ai.learning_rate <= 0 or self.ai.learning_rate > 1:
            issues.append("AI learning rate must be between 0 and 1")
        
        # Validate task config
        if self.task.max_workers < 1:
            issues.append("Task max_workers must be at least 1")
        
        # Validate paths
        if not self.base_dir.exists():
            issues.append(f"Base directory does not exist: {self.base_dir}")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues
        }


# Global settings instance
settings = Settings()


if __name__ == "__main__":
    # Test settings
    config = Settings()
    
    print(f"App: {config.app_name} v{config.app_version}")
    print(f"Environment: {config.environment}")
    print(f"Debug: {config.debug}")
    print(f"Base Dir: {config.base_dir}")
    
    # Validate
    validation = config.validate()
    print(f"Config valid: {validation['valid']}")
