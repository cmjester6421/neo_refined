"""
System Control Module
Handles PC automation, shutdown, startup, and system operations
"""

import os
import platform
import psutil
import subprocess
from typing import Dict, List, Any, Optional
from datetime import datetime
import schedule
import time

from src.utils.logger import NEOLogger


class SystemControl:
    """
    Complete PC control and automation system
    """
    
    def __init__(self):
        self.logger = NEOLogger("SystemControl")
        self.platform = platform.system()
        self.logger.info(f"System Control initialized on {self.platform}")
        
        self.scheduled_tasks = []
        self.is_running = False
        
    def shutdown(self, delay: int = 0, force: bool = False) -> Dict[str, Any]:
        """
        Shutdown the system
        
        Args:
            delay: Delay in seconds before shutdown
            force: Force shutdown without saving
            
        Returns:
            Status dictionary
        """
        self.logger.warning(f"Initiating system shutdown (delay: {delay}s, force: {force})")
        
        try:
            if self.platform == "Windows":
                cmd = f"shutdown /s /t {delay}"
                if force:
                    cmd += " /f"
            elif self.platform in ["Linux", "Darwin"]:
                cmd = f"sudo shutdown -h +{delay//60}" if delay > 0 else "sudo shutdown -h now"
                if force:
                    cmd += " -f"
            else:
                return {"success": False, "error": "Unsupported platform"}
            
            # In production, this would execute:
            # subprocess.run(cmd, shell=True, check=True)
            
            self.logger.info("Shutdown command prepared (not executed in safe mode)")
            
            return {
                "success": True,
                "command": cmd,
                "platform": self.platform,
                "delay": delay,
                "message": "Shutdown scheduled (safe mode - not executed)"
            }
            
        except Exception as e:
            self.logger.error(f"Shutdown failed: {e}")
            return {"success": False, "error": str(e)}
    
    def restart(self, delay: int = 0) -> Dict[str, Any]:
        """Restart the system"""
        self.logger.warning(f"Initiating system restart (delay: {delay}s)")
        
        try:
            if self.platform == "Windows":
                cmd = f"shutdown /r /t {delay}"
            elif self.platform in ["Linux", "Darwin"]:
                cmd = f"sudo shutdown -r +{delay//60}" if delay > 0 else "sudo shutdown -r now"
            else:
                return {"success": False, "error": "Unsupported platform"}
            
            self.logger.info("Restart command prepared (not executed in safe mode)")
            
            return {
                "success": True,
                "command": cmd,
                "platform": self.platform,
                "message": "Restart scheduled (safe mode - not executed)"
            }
            
        except Exception as e:
            self.logger.error(f"Restart failed: {e}")
            return {"success": False, "error": str(e)}
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get comprehensive system information"""
        self.logger.info("Gathering system information")
        
        try:
            cpu_info = {
                "physical_cores": psutil.cpu_count(logical=False),
                "logical_cores": psutil.cpu_count(logical=True),
                "usage_percent": psutil.cpu_percent(interval=1),
                "frequency": psutil.cpu_freq()._asdict() if psutil.cpu_freq() else None
            }
            
            memory = psutil.virtual_memory()
            memory_info = {
                "total": memory.total,
                "available": memory.available,
                "used": memory.used,
                "percent": memory.percent
            }
            
            disk = psutil.disk_usage('/')
            disk_info = {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "percent": disk.percent
            }
            
            network = psutil.net_io_counters()
            network_info = {
                "bytes_sent": network.bytes_sent,
                "bytes_recv": network.bytes_recv,
                "packets_sent": network.packets_sent,
                "packets_recv": network.packets_recv
            }
            
            return {
                "platform": {
                    "system": platform.system(),
                    "release": platform.release(),
                    "version": platform.version(),
                    "machine": platform.machine(),
                    "processor": platform.processor()
                },
                "cpu": cpu_info,
                "memory": memory_info,
                "disk": disk_info,
                "network": network_info,
                "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get system info: {e}")
            return {"success": False, "error": str(e)}
    
    def get_running_processes(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get list of running processes"""
        self.logger.info(f"Fetching running processes (limit: {limit})")
        
        try:
            processes = []
            
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append({
                        "pid": proc.info['pid'],
                        "name": proc.info['name'],
                        "cpu_percent": proc.info['cpu_percent'],
                        "memory_percent": proc.info['memory_percent']
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Sort by CPU usage
            processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
            
            return processes[:limit]
            
        except Exception as e:
            self.logger.error(f"Failed to get processes: {e}")
            return []
    
    def kill_process(self, pid: int, force: bool = False) -> Dict[str, Any]:
        """Kill a process by PID"""
        self.logger.warning(f"Attempting to kill process {pid} (force: {force})")
        
        try:
            process = psutil.Process(pid)
            process_name = process.name()
            
            if force:
                process.kill()
            else:
                process.terminate()
            
            # Wait for process to terminate
            process.wait(timeout=5)
            
            self.logger.info(f"Process {pid} ({process_name}) terminated successfully")
            
            return {
                "success": True,
                "pid": pid,
                "name": process_name,
                "message": "Process terminated"
            }
            
        except psutil.NoSuchProcess:
            return {"success": False, "error": "Process not found"}
        except psutil.AccessDenied:
            return {"success": False, "error": "Access denied"}
        except Exception as e:
            self.logger.error(f"Failed to kill process: {e}")
            return {"success": False, "error": str(e)}
    
    def execute_command(self, command: str, shell: bool = True, timeout: int = 30) -> Dict[str, Any]:
        """Execute system command"""
        self.logger.info(f"Executing command: {command[:50]}...")
        
        try:
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "command": command
            }
            
        except subprocess.TimeoutExpired:
            self.logger.error(f"Command timed out after {timeout}s")
            return {"success": False, "error": "Command timeout"}
        except Exception as e:
            self.logger.error(f"Command execution failed: {e}")
            return {"success": False, "error": str(e)}
    
    def schedule_task(self, task_name: str, command: str, schedule_time: str) -> Dict[str, Any]:
        """
        Schedule a task to run at specific time
        
        Args:
            task_name: Name of the task
            command: Command to execute
            schedule_time: Time in format "HH:MM"
        """
        self.logger.info(f"Scheduling task '{task_name}' for {schedule_time}")
        
        try:
            # Schedule the task
            schedule.every().day.at(schedule_time).do(
                self.execute_command, 
                command=command
            ).tag(task_name)
            
            self.scheduled_tasks.append({
                "name": task_name,
                "command": command,
                "time": schedule_time,
                "status": "scheduled"
            })
            
            return {
                "success": True,
                "task_name": task_name,
                "scheduled_for": schedule_time,
                "message": "Task scheduled successfully"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to schedule task: {e}")
            return {"success": False, "error": str(e)}
    
    def get_scheduled_tasks(self) -> List[Dict[str, Any]]:
        """Get all scheduled tasks"""
        return self.scheduled_tasks.copy()
    
    def cancel_task(self, task_name: str) -> Dict[str, Any]:
        """Cancel a scheduled task"""
        self.logger.info(f"Cancelling task '{task_name}'")
        
        try:
            schedule.clear(task_name)
            
            # Remove from task list
            self.scheduled_tasks = [
                task for task in self.scheduled_tasks 
                if task['name'] != task_name
            ]
            
            return {
                "success": True,
                "task_name": task_name,
                "message": "Task cancelled"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to cancel task: {e}")
            return {"success": False, "error": str(e)}
    
    def run_scheduler(self):
        """Run the task scheduler (blocking)"""
        self.logger.info("Starting task scheduler")
        self.is_running = True
        
        while self.is_running:
            schedule.run_pending()
            time.sleep(1)
    
    def stop_scheduler(self):
        """Stop the task scheduler"""
        self.logger.info("Stopping task scheduler")
        self.is_running = False
    
    def monitor_resource(self, resource_type: str, threshold: float, callback=None) -> Dict[str, Any]:
        """
        Monitor system resource and trigger callback when threshold is exceeded
        
        Args:
            resource_type: 'cpu', 'memory', or 'disk'
            threshold: Threshold percentage (0-100)
            callback: Function to call when threshold is exceeded
        """
        self.logger.info(f"Monitoring {resource_type} with threshold {threshold}%")
        
        try:
            if resource_type == 'cpu':
                current = psutil.cpu_percent(interval=1)
            elif resource_type == 'memory':
                current = psutil.virtual_memory().percent
            elif resource_type == 'disk':
                current = psutil.disk_usage('/').percent
            else:
                return {"success": False, "error": "Invalid resource type"}
            
            exceeded = current > threshold
            
            if exceeded and callback:
                callback(resource_type, current, threshold)
            
            return {
                "success": True,
                "resource": resource_type,
                "current": current,
                "threshold": threshold,
                "exceeded": exceeded
            }
            
        except Exception as e:
            self.logger.error(f"Resource monitoring failed: {e}")
            return {"success": False, "error": str(e)}


if __name__ == "__main__":
    # Test system control
    control = SystemControl()
    
    # Get system info
    info = control.get_system_info()
    print(f"Platform: {info['platform']['system']}")
    print(f"CPU Usage: {info['cpu']['usage_percent']}%")
    print(f"Memory Usage: {info['memory']['percent']}%")
    
    # Get running processes
    processes = control.get_running_processes(5)
    print(f"\nTop 5 processes by CPU usage:")
    for proc in processes:
        print(f"  {proc['name']}: {proc['cpu_percent']}%")
