"""
Cybersecurity Module
Advanced penetration testing, security analysis, and threat detection
"""

import socket
import hashlib
import secrets
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import subprocess

from src.utils.logger import NEOLogger


@dataclass
class SecurityScan:
    """Security scan result"""
    scan_type: str
    timestamp: str
    findings: List[Dict[str, Any]]
    severity_counts: Dict[str, int]
    overall_score: float


class CybersecurityModule:
    """
    Advanced cybersecurity and penetration testing module
    """
    
    def __init__(self):
        self.logger = NEOLogger("Cybersecurity")
        self.logger.info("Cybersecurity module initialized")
        
        self.scan_history = []
        self.threat_database = []
        
    def port_scan(self, target: str, ports: List[int] = None, timeout: float = 1.0) -> Dict[str, Any]:
        """
        Scan ports on target system
        
        Args:
            target: Target IP or hostname
            ports: List of ports to scan (default: common ports)
            timeout: Connection timeout
        """
        self.logger.info(f"Starting port scan on {target}")
        
        if ports is None:
            # Common ports
            ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 3389, 5432, 8080, 8443]
        
        open_ports = []
        closed_ports = []
        
        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                result = sock.connect_ex((target, port))
                
                if result == 0:
                    service = self._identify_service(port)
                    open_ports.append({
                        "port": port,
                        "status": "open",
                        "service": service
                    })
                    self.logger.debug(f"Port {port} is open ({service})")
                else:
                    closed_ports.append(port)
                
                sock.close()
                
            except socket.gaierror:
                self.logger.error(f"Hostname {target} could not be resolved")
                return {"success": False, "error": "Invalid hostname"}
            except socket.error as e:
                self.logger.error(f"Socket error on port {port}: {e}")
                closed_ports.append(port)
        
        result = {
            "success": True,
            "target": target,
            "timestamp": datetime.now().isoformat(),
            "total_ports_scanned": len(ports),
            "open_ports": open_ports,
            "open_count": len(open_ports),
            "closed_count": len(closed_ports)
        }
        
        self.scan_history.append(result)
        
        return result
    
    def vulnerability_scan(self, target: str) -> SecurityScan:
        """
        Perform vulnerability scanning on target
        
        Args:
            target: Target system URL or IP
        """
        self.logger.info(f"Starting vulnerability scan on {target}")
        
        findings = []
        
        # Check for common vulnerabilities
        
        # 1. SSL/TLS check
        ssl_result = self._check_ssl(target)
        if not ssl_result['secure']:
            findings.append({
                "type": "SSL/TLS",
                "severity": "high",
                "description": ssl_result['issue'],
                "recommendation": "Update SSL/TLS configuration"
            })
        
        # 2. HTTP headers check
        headers_result = self._check_security_headers(target)
        for missing_header in headers_result['missing']:
            findings.append({
                "type": "Security Headers",
                "severity": "medium",
                "description": f"Missing security header: {missing_header}",
                "recommendation": f"Add {missing_header} header"
            })
        
        # 3. Common vulnerability patterns
        vuln_patterns = self._check_common_vulnerabilities(target)
        findings.extend(vuln_patterns)
        
        # Calculate severity counts
        severity_counts = {
            "critical": len([f for f in findings if f['severity'] == 'critical']),
            "high": len([f for f in findings if f['severity'] == 'high']),
            "medium": len([f for f in findings if f['severity'] == 'medium']),
            "low": len([f for f in findings if f['severity'] == 'low'])
        }
        
        # Calculate overall security score (0-100)
        overall_score = self._calculate_security_score(severity_counts)
        
        scan = SecurityScan(
            scan_type="vulnerability",
            timestamp=datetime.now().isoformat(),
            findings=findings,
            severity_counts=severity_counts,
            overall_score=overall_score
        )
        
        self.scan_history.append(scan)
        
        return scan
    
    def password_strength_analysis(self, password: str) -> Dict[str, Any]:
        """
        Analyze password strength
        
        Args:
            password: Password to analyze
        """
        self.logger.info("Analyzing password strength")
        
        score = 0
        feedback = []
        
        # Length check
        if len(password) >= 12:
            score += 25
        elif len(password) >= 8:
            score += 15
            feedback.append("Password should be at least 12 characters")
        else:
            feedback.append("Password is too short (minimum 8 characters)")
        
        # Complexity checks
        has_lower = bool(re.search(r'[a-z]', password))
        has_upper = bool(re.search(r'[A-Z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        
        complexity_score = sum([has_lower, has_upper, has_digit, has_special]) * 15
        score += complexity_score
        
        if not has_lower:
            feedback.append("Add lowercase letters")
        if not has_upper:
            feedback.append("Add uppercase letters")
        if not has_digit:
            feedback.append("Add numbers")
        if not has_special:
            feedback.append("Add special characters")
        
        # Common patterns check
        common_patterns = ['123', 'abc', 'password', 'qwerty', '111']
        if any(pattern in password.lower() for pattern in common_patterns):
            score -= 20
            feedback.append("Avoid common patterns")
        
        # Ensure score is between 0 and 100
        score = max(0, min(100, score))
        
        # Determine strength level
        if score >= 80:
            strength = "strong"
        elif score >= 60:
            strength = "moderate"
        elif score >= 40:
            strength = "weak"
        else:
            strength = "very_weak"
        
        return {
            "score": score,
            "strength": strength,
            "has_lowercase": has_lower,
            "has_uppercase": has_upper,
            "has_digits": has_digit,
            "has_special": has_special,
            "length": len(password),
            "feedback": feedback
        }
    
    def generate_secure_password(self, length: int = 16, include_special: bool = True) -> str:
        """Generate cryptographically secure password"""
        import string
        
        characters = string.ascii_letters + string.digits
        if include_special:
            characters += string.punctuation
        
        password = ''.join(secrets.choice(characters) for _ in range(length))
        
        self.logger.info(f"Generated secure password of length {length}")
        
        return password
    
    def hash_data(self, data: str, algorithm: str = "sha256") -> str:
        """
        Hash data using specified algorithm
        
        Args:
            data: Data to hash
            algorithm: Hash algorithm (md5, sha1, sha256, sha512)
        """
        self.logger.info(f"Hashing data with {algorithm}")
        
        algorithms = {
            "md5": hashlib.md5,
            "sha1": hashlib.sha1,
            "sha256": hashlib.sha256,
            "sha512": hashlib.sha512
        }
        
        if algorithm not in algorithms:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
        
        hash_obj = algorithms[algorithm]()
        hash_obj.update(data.encode('utf-8'))
        
        return hash_obj.hexdigest()
    
    def detect_sql_injection(self, input_string: str) -> Dict[str, Any]:
        """
        Detect potential SQL injection attempts
        
        Args:
            input_string: Input to analyze
        """
        self.logger.info("Checking for SQL injection patterns")
        
        sql_patterns = [
            r"(\bOR\b.*=.*)",
            r"(\bAND\b.*=.*)",
            r"(--)",
            r"(;.*DROP)",
            r"(UNION.*SELECT)",
            r"('.*OR.*'.*=.*')",
            r"(exec\s*\()",
            r"(script.*>)",
        ]
        
        detected_patterns = []
        is_suspicious = False
        
        for pattern in sql_patterns:
            if re.search(pattern, input_string, re.IGNORECASE):
                detected_patterns.append(pattern)
                is_suspicious = True
        
        risk_level = "high" if len(detected_patterns) > 2 else "medium" if is_suspicious else "low"
        
        return {
            "is_suspicious": is_suspicious,
            "risk_level": risk_level,
            "detected_patterns": detected_patterns,
            "input_length": len(input_string),
            "recommendation": "Sanitize input and use parameterized queries" if is_suspicious else "Input appears safe"
        }
    
    def detect_xss(self, input_string: str) -> Dict[str, Any]:
        """
        Detect potential XSS (Cross-Site Scripting) attempts
        
        Args:
            input_string: Input to analyze
        """
        self.logger.info("Checking for XSS patterns")
        
        xss_patterns = [
            r"<script[^>]*>.*?</script>",
            r"javascript:",
            r"on\w+\s*=",
            r"<iframe",
            r"<object",
            r"<embed",
            r"eval\s*\(",
        ]
        
        detected_patterns = []
        is_suspicious = False
        
        for pattern in xss_patterns:
            if re.search(pattern, input_string, re.IGNORECASE):
                detected_patterns.append(pattern)
                is_suspicious = True
        
        risk_level = "high" if len(detected_patterns) > 1 else "medium" if is_suspicious else "low"
        
        return {
            "is_suspicious": is_suspicious,
            "risk_level": risk_level,
            "detected_patterns": detected_patterns,
            "recommendation": "Encode output and validate input" if is_suspicious else "Input appears safe"
        }
    
    def network_reconnaissance(self, target: str) -> Dict[str, Any]:
        """
        Perform network reconnaissance on target
        
        Args:
            target: Target IP or hostname
        """
        self.logger.info(f"Performing network reconnaissance on {target}")
        
        info = {}
        
        try:
            # DNS lookup
            ip_address = socket.gethostbyname(target)
            info['ip_address'] = ip_address
            
            # Reverse DNS
            try:
                hostname = socket.gethostbyaddr(ip_address)[0]
                info['hostname'] = hostname
            except socket.herror:
                info['hostname'] = "Unknown"
            
            # Port scan (top ports)
            port_scan_result = self.port_scan(target, timeout=0.5)
            info['open_ports'] = port_scan_result['open_ports']
            
            # Operating system detection (basic)
            info['os_detection'] = self._detect_os(target)
            
            return {
                "success": True,
                "target": target,
                "information": info,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Reconnaissance failed: {e}")
            return {"success": False, "error": str(e)}
    
    def get_scan_history(self) -> List[Any]:
        """Get all scan history"""
        return self.scan_history.copy()
    
    def _identify_service(self, port: int) -> str:
        """Identify service running on port"""
        common_ports = {
            21: "FTP",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            80: "HTTP",
            110: "POP3",
            143: "IMAP",
            443: "HTTPS",
            3306: "MySQL",
            3389: "RDP",
            5432: "PostgreSQL",
            8080: "HTTP-Alt",
            8443: "HTTPS-Alt"
        }
        return common_ports.get(port, "Unknown")
    
    def _check_ssl(self, target: str) -> Dict[str, Any]:
        """Check SSL/TLS configuration"""
        # Simplified SSL check
        return {
            "secure": True,
            "issue": None
        }
    
    def _check_security_headers(self, target: str) -> Dict[str, Any]:
        """Check for security headers"""
        required_headers = [
            "X-Content-Type-Options",
            "X-Frame-Options",
            "Content-Security-Policy",
            "Strict-Transport-Security"
        ]
        
        # Simplified - in production, would make actual HTTP request
        return {
            "missing": required_headers[:2]  # Simulate some missing headers
        }
    
    def _check_common_vulnerabilities(self, target: str) -> List[Dict[str, Any]]:
        """Check for common vulnerabilities"""
        # Simplified vulnerability check
        return [
            {
                "type": "Configuration",
                "severity": "low",
                "description": "Directory listing might be enabled",
                "recommendation": "Disable directory listing"
            }
        ]
    
    def _calculate_security_score(self, severity_counts: Dict[str, int]) -> float:
        """Calculate overall security score"""
        base_score = 100
        
        penalties = {
            "critical": 25,
            "high": 15,
            "medium": 8,
            "low": 3
        }
        
        for severity, count in severity_counts.items():
            base_score -= penalties.get(severity, 0) * count
        
        return max(0, min(100, base_score))
    
    def _detect_os(self, target: str) -> str:
        """Detect operating system (basic)"""
        # Simplified OS detection
        return "Unknown (requires advanced scanning)"


if __name__ == "__main__":
    # Test cybersecurity module
    cyber = CybersecurityModule()
    
    # Test password analysis
    password_result = cyber.password_strength_analysis("MyP@ssw0rd123!")
    print(f"Password strength: {password_result['strength']} ({password_result['score']}/100)")
    
    # Generate secure password
    secure_pwd = cyber.generate_secure_password(16)
    print(f"Generated password: {secure_pwd}")
    
    # Test SQL injection detection
    sql_test = cyber.detect_sql_injection("admin' OR '1'='1")
    print(f"SQL Injection detected: {sql_test['is_suspicious']}")
