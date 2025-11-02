"""
NEO Logger - Comprehensive logging and monitoring system
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime
from logging.handlers import RotatingFileHandler
import json


class NEOLogger:
    """
    Advanced logging system for NEO with file and console output
    """
    
    _instances = {}
    
    def __new__(cls, name: str = "NEO"):
        """Singleton pattern per logger name"""
        if name not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[name] = instance
        return cls._instances[name]
    
    def __init__(self, name: str = "NEO", log_dir: Optional[Path] = None):
        """Initialize logger"""
        if hasattr(self, '_initialized'):
            return
            
        self.name = name
        self.log_dir = log_dir or Path("logs")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Prevent duplicate handlers
        if self.logger.handlers:
            return
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        
        # File handler (rotating)
        log_file = self.log_dir / f"{name.lower()}_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        
        # Add handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        
        self._initialized = True
    
    def debug(self, message: str, **kwargs):
        """Log debug message"""
        self.logger.debug(message, extra=kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info message"""
        self.logger.info(message, extra=kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message"""
        self.logger.warning(message, extra=kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message"""
        self.logger.error(message, extra=kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical message"""
        self.logger.critical(message, extra=kwargs)
    
    def exception(self, message: str, **kwargs):
        """Log exception with traceback"""
        self.logger.exception(message, extra=kwargs)
    
    def log_event(self, event_type: str, data: dict):
        """Log structured event"""
        event = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'data': data
        }
        self.info(f"EVENT: {json.dumps(event)}")
    
    def log_metric(self, metric_name: str, value: float, tags: dict = None):
        """Log metric for monitoring"""
        metric = {
            'timestamp': datetime.now().isoformat(),
            'metric': metric_name,
            'value': value,
            'tags': tags or {}
        }
        self.info(f"METRIC: {json.dumps(metric)}")


class PerformanceMonitor:
    """Monitor performance metrics"""
    
    def __init__(self, logger: NEOLogger):
        self.logger = logger
        self.metrics = {}
    
    def start_timer(self, operation: str):
        """Start timing an operation"""
        self.metrics[operation] = {
            'start_time': datetime.now(),
            'end_time': None,
            'duration': None
        }
    
    def stop_timer(self, operation: str):
        """Stop timing an operation"""
        if operation in self.metrics:
            self.metrics[operation]['end_time'] = datetime.now()
            self.metrics[operation]['duration'] = (
                self.metrics[operation]['end_time'] - 
                self.metrics[operation]['start_time']
            ).total_seconds()
            
            self.logger.log_metric(
                f"{operation}_duration",
                self.metrics[operation]['duration']
            )
    
    def get_metrics(self) -> dict:
        """Get all collected metrics"""
        return self.metrics.copy()


if __name__ == "__main__":
    # Test logger
    logger = NEOLogger("Test")
    logger.info("Logger initialized")
    logger.debug("Debug message")
    logger.warning("Warning message")
    logger.error("Error message")
    
    logger.log_event("test_event", {"key": "value"})
    logger.log_metric("test_metric", 42.5, {"tag": "test"})
