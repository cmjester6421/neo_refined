"""
Coding Assistant Module
Code analysis, debugging, optimization, and best practices
"""

import ast
import re
import subprocess
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import json

from src.utils.logger import NEOLogger


@dataclass
class CodeAnalysis:
    """Code analysis result"""
    file_path: str
    language: str
    lines_of_code: int
    complexity: str
    issues: List[Dict[str, Any]]
    suggestions: List[str]
    quality_score: float


class CodingAssistant:
    """
    Advanced coding assistance with analysis, debugging, and optimization
    """
    
    def __init__(self):
        self.logger = NEOLogger("CodingAssistant")
        self.logger.info("Coding Assistant initialized")
        
        self.analysis_history = []
        
    def analyze_code(self, code: str, language: str = "python") -> CodeAnalysis:
        """
        Analyze code for quality, complexity, and issues
        
        Args:
            code: Source code to analyze
            language: Programming language
        """
        self.logger.info(f"Analyzing {language} code")
        
        if language.lower() == "python":
            return self._analyze_python(code)
        elif language.lower() in ["javascript", "js"]:
            return self._analyze_javascript(code)
        else:
            return self._generic_analysis(code, language)
    
    def _analyze_python(self, code: str) -> CodeAnalysis:
        """Analyze Python code"""
        issues = []
        suggestions = []
        
        # Count lines
        lines = code.split('\n')
        loc = len([line for line in lines if line.strip() and not line.strip().startswith('#')])
        
        # Try to parse the code
        try:
            tree = ast.parse(code)
            
            # Check for complexity
            complexity = self._calculate_complexity(tree)
            
            # Find potential issues
            issues.extend(self._find_python_issues(tree, code))
            
            # Generate suggestions
            suggestions.extend(self._generate_python_suggestions(tree, code))
            
        except SyntaxError as e:
            issues.append({
                "type": "syntax_error",
                "severity": "critical",
                "line": e.lineno,
                "message": str(e),
                "code": e.text
            })
            complexity = "unknown"
        
        # Calculate quality score
        quality_score = self._calculate_quality_score(loc, complexity, issues)
        
        analysis = CodeAnalysis(
            file_path="<string>",
            language="python",
            lines_of_code=loc,
            complexity=complexity,
            issues=issues,
            suggestions=suggestions,
            quality_score=quality_score
        )
        
        self.analysis_history.append(analysis)
        
        return analysis
    
    def _calculate_complexity(self, tree: ast.AST) -> str:
        """Calculate code complexity"""
        complexity_score = 0
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For)):
                complexity_score += 1
            elif isinstance(node, ast.FunctionDef):
                complexity_score += 2
            elif isinstance(node, ast.ClassDef):
                complexity_score += 3
        
        if complexity_score < 10:
            return "low"
        elif complexity_score < 30:
            return "moderate"
        else:
            return "high"
    
    def _find_python_issues(self, tree: ast.AST, code: str) -> List[Dict[str, Any]]:
        """Find potential issues in Python code"""
        issues = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check line length
            if len(line) > 120:
                issues.append({
                    "type": "style",
                    "severity": "low",
                    "line": i,
                    "message": "Line too long (>120 characters)",
                    "code": line[:50] + "..."
                })
            
            # Check for print statements (debugging)
            if re.search(r'\bprint\s*\(', line):
                issues.append({
                    "type": "code_smell",
                    "severity": "low",
                    "line": i,
                    "message": "Remove print statement in production code",
                    "code": line.strip()
                })
        
        # Check for empty except blocks
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler):
                if not node.body or (len(node.body) == 1 and isinstance(node.body[0], ast.Pass)):
                    issues.append({
                        "type": "bad_practice",
                        "severity": "medium",
                        "line": node.lineno,
                        "message": "Empty except block - handle exceptions properly",
                        "code": "except: pass"
                    })
        
        return issues
    
    def _generate_python_suggestions(self, tree: ast.AST, code: str) -> List[str]:
        """Generate suggestions for Python code improvement"""
        suggestions = []
        
        # Check for docstrings
        has_docstring = False
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if ast.get_docstring(node):
                    has_docstring = True
                    break
        
        if not has_docstring:
            suggestions.append("Add docstrings to functions and classes")
        
        # Check for type hints
        has_type_hints = False
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.returns or any(arg.annotation for arg in node.args.args):
                    has_type_hints = True
                    break
        
        if not has_type_hints:
            suggestions.append("Consider adding type hints for better code clarity")
        
        # Suggest using list comprehensions
        if 'for ' in code and 'append(' in code:
            suggestions.append("Consider using list comprehensions for better readability")
        
        return suggestions
    
    def _analyze_javascript(self, code: str) -> CodeAnalysis:
        """Analyze JavaScript code"""
        issues = []
        suggestions = []
        
        lines = code.split('\n')
        loc = len([line for line in lines if line.strip() and not line.strip().startswith('//')])
        
        # Basic JavaScript analysis
        for i, line in enumerate(lines, 1):
            # Check for var usage
            if re.search(r'\bvar\s+', line):
                issues.append({
                    "type": "bad_practice",
                    "severity": "low",
                    "line": i,
                    "message": "Use 'let' or 'const' instead of 'var'",
                    "code": line.strip()
                })
            
            # Check for == instead of ===
            if '==' in line and '===' not in line:
                issues.append({
                    "type": "bad_practice",
                    "severity": "medium",
                    "line": i,
                    "message": "Use '===' instead of '==' for comparison",
                    "code": line.strip()
                })
        
        suggestions.append("Use ESLint for comprehensive JavaScript linting")
        suggestions.append("Consider using TypeScript for type safety")
        
        quality_score = max(0, 100 - (len(issues) * 5))
        
        return CodeAnalysis(
            file_path="<string>",
            language="javascript",
            lines_of_code=loc,
            complexity="moderate",
            issues=issues,
            suggestions=suggestions,
            quality_score=quality_score
        )
    
    def _generic_analysis(self, code: str, language: str) -> CodeAnalysis:
        """Generic code analysis for any language"""
        lines = code.split('\n')
        loc = len([line for line in lines if line.strip()])
        
        return CodeAnalysis(
            file_path="<string>",
            language=language,
            lines_of_code=loc,
            complexity="unknown",
            issues=[],
            suggestions=[f"Use language-specific linters for {language}"],
            quality_score=70.0
        )
    
    def _calculate_quality_score(self, loc: int, complexity: str, issues: List[Dict]) -> float:
        """Calculate code quality score (0-100)"""
        base_score = 100
        
        # Penalize for issues
        severity_penalties = {
            "critical": 20,
            "high": 10,
            "medium": 5,
            "low": 2
        }
        
        for issue in issues:
            penalty = severity_penalties.get(issue['severity'], 5)
            base_score -= penalty
        
        # Adjust for complexity
        complexity_adjustments = {
            "low": 0,
            "moderate": -5,
            "high": -15,
            "unknown": -10
        }
        base_score += complexity_adjustments.get(complexity, 0)
        
        return max(0, min(100, base_score))
    
    def debug_code(self, code: str, error_message: str = None) -> Dict[str, Any]:
        """
        Debug code and provide solutions
        
        Args:
            code: Code with potential bugs
            error_message: Error message if available
        """
        self.logger.info("Debugging code")
        
        suggestions = []
        potential_fixes = []
        
        if error_message:
            # Analyze error message
            if "NameError" in error_message:
                suggestions.append("Check for undefined variables")
                potential_fixes.append("Ensure all variables are defined before use")
            
            elif "SyntaxError" in error_message:
                suggestions.append("Check syntax - missing colons, parentheses, or quotes")
                potential_fixes.append("Review Python syntax rules")
            
            elif "IndentationError" in error_message:
                suggestions.append("Fix indentation - use consistent spaces or tabs")
                potential_fixes.append("Use 4 spaces for indentation (PEP 8)")
            
            elif "TypeError" in error_message:
                suggestions.append("Check data types - incompatible type operation")
                potential_fixes.append("Verify function arguments and return types")
            
            elif "AttributeError" in error_message:
                suggestions.append("Object doesn't have the specified attribute")
                potential_fixes.append("Check object type and available methods")
        
        # Analyze code structure
        try:
            tree = ast.parse(code)
            
            # Check for common anti-patterns
            for node in ast.walk(tree):
                if isinstance(node, ast.ExceptHandler) and node.type is None:
                    suggestions.append("Avoid bare except clauses")
                    potential_fixes.append("Catch specific exceptions instead of generic Exception")
        
        except SyntaxError:
            suggestions.append("Fix syntax errors first")
        
        return {
            "error_message": error_message,
            "suggestions": suggestions,
            "potential_fixes": potential_fixes,
            "recommended_actions": [
                "Run code with debugger",
                "Add print statements to trace execution",
                "Check variable types and values"
            ]
        }
    
    def optimize_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        """
        Suggest code optimizations
        
        Args:
            code: Code to optimize
            language: Programming language
        """
        self.logger.info("Analyzing code for optimization opportunities")
        
        optimizations = []
        
        if language.lower() == "python":
            # Check for string concatenation in loops
            if re.search(r'for .+:\s*\w+\s*\+=\s*["\']', code):
                optimizations.append({
                    "type": "performance",
                    "issue": "String concatenation in loop",
                    "suggestion": "Use list and join() method instead",
                    "impact": "high"
                })
            
            # Check for list comprehensions opportunity
            if re.search(r'for .+:\s*\w+\.append\(', code):
                optimizations.append({
                    "type": "readability",
                    "issue": "Manual list building",
                    "suggestion": "Use list comprehension",
                    "impact": "medium"
                })
            
            # Check for dictionary.get() usage
            if 'if key in dict' in code.replace(' ', ''):
                optimizations.append({
                    "type": "best_practice",
                    "issue": "Manual key checking",
                    "suggestion": "Use dict.get(key, default) method",
                    "impact": "low"
                })
        
        return {
            "language": language,
            "optimizations": optimizations,
            "total_suggestions": len(optimizations),
            "estimated_improvement": "10-30% performance gain" if optimizations else "Code is already optimized"
        }
    
    def format_code(self, code: str, language: str = "python") -> str:
        """
        Format code according to best practices
        
        Args:
            code: Code to format
            language: Programming language
        """
        self.logger.info(f"Formatting {language} code")
        
        if language.lower() == "python":
            try:
                # Try to use black formatter (if available)
                import black
                formatted = black.format_str(code, mode=black.Mode())
                return formatted
            except ImportError:
                self.logger.warning("Black formatter not available, using basic formatting")
                # Basic formatting
                return self._basic_python_format(code)
        
        return code
    
    def _basic_python_format(self, code: str) -> str:
        """Basic Python code formatting"""
        lines = code.split('\n')
        formatted_lines = []
        
        for line in lines:
            # Remove trailing whitespace
            line = line.rstrip()
            
            # Ensure space after commas
            line = re.sub(r',(\S)', r', \1', line)
            
            formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)
    
    def generate_documentation(self, code: str, language: str = "python") -> str:
        """
        Generate documentation for code
        
        Args:
            code: Source code
            language: Programming language
        """
        self.logger.info("Generating code documentation")
        
        if language.lower() == "python":
            return self._generate_python_docs(code)
        
        return "# Documentation\n\nCode documentation generation is available for Python."
    
    def _generate_python_docs(self, code: str) -> str:
        """Generate Python documentation"""
        try:
            tree = ast.parse(code)
            docs = ["# Code Documentation\n"]
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    docs.append(f"\n## Function: `{node.name}`")
                    
                    # Arguments
                    args = [arg.arg for arg in node.args.args]
                    docs.append(f"**Arguments:** {', '.join(args) if args else 'None'}")
                    
                    # Docstring
                    docstring = ast.get_docstring(node)
                    if docstring:
                        docs.append(f"\n{docstring}")
                    else:
                        docs.append("\n*No documentation available*")
                
                elif isinstance(node, ast.ClassDef):
                    docs.append(f"\n## Class: `{node.name}`")
                    
                    docstring = ast.get_docstring(node)
                    if docstring:
                        docs.append(f"\n{docstring}")
                    else:
                        docs.append("\n*No documentation available*")
            
            return '\n'.join(docs)
        
        except SyntaxError:
            return "# Documentation\n\nUnable to parse code - contains syntax errors."
    
    def get_analysis_history(self) -> List[CodeAnalysis]:
        """Get all code analysis history"""
        return self.analysis_history.copy()


if __name__ == "__main__":
    # Test coding assistant
    assistant = CodingAssistant()
    
    # Test code analysis
    test_code = """
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total

print(calculate_sum([1, 2, 3, 4, 5]))
"""
    
    analysis = assistant.analyze_code(test_code)
    print(f"Quality Score: {analysis.quality_score}/100")
    print(f"Issues: {len(analysis.issues)}")
    print(f"Suggestions: {analysis.suggestions}")
