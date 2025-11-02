"""
Helper utilities for NEO
"""

import hashlib
import json
from typing import Any, Dict, List
from datetime import datetime
import re


def generate_id(prefix: str = "neo") -> str:
    """Generate unique ID"""
    timestamp = datetime.now().isoformat()
    hash_obj = hashlib.md5(timestamp.encode())
    return f"{prefix}_{hash_obj.hexdigest()[:12]}"


def sanitize_input(text: str) -> str:
    """Sanitize user input"""
    # Remove potentially harmful characters
    sanitized = re.sub(r'[<>\"\'&]', '', text)
    return sanitized.strip()


def validate_json(data: str) -> bool:
    """Validate JSON string"""
    try:
        json.loads(data)
        return True
    except (json.JSONDecodeError, TypeError):
        return False


def format_bytes(bytes_value: int) -> str:
    """Format bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"


def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """Deep merge two dictionaries"""
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    return result


def chunk_list(lst: List, chunk_size: int) -> List[List]:
    """Split list into chunks"""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


def safe_execute(func, *args, default=None, **kwargs):
    """Safely execute function with exception handling"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        print(f"Error executing {func.__name__}: {e}")
        return default


class Timer:
    """Context manager for timing operations"""
    
    def __init__(self, name: str = "Operation"):
        self.name = name
        self.start_time = None
        self.end_time = None
        
    def __enter__(self):
        self.start_time = datetime.now()
        return self
        
    def __exit__(self, *args):
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()
        print(f"{self.name} took {duration:.4f} seconds")
        
    @property
    def elapsed(self) -> float:
        """Get elapsed time in seconds"""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0
