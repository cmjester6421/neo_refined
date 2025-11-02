"""
Task Automation Module
Efficient task scheduling, execution, and management
"""

import time
import threading
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import queue
import schedule

from src.utils.logger import NEOLogger


class TaskStatus(Enum):
    """Task status enumeration"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    SCHEDULED = "scheduled"


class TaskPriority(Enum):
    """Task priority levels"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Task:
    """Task definition"""
    id: str
    name: str
    function: Callable
    args: tuple = field(default_factory=tuple)
    kwargs: dict = field(default_factory=dict)
    priority: TaskPriority = TaskPriority.NORMAL
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Any = None
    error: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3


class TaskAutomation:
    """
    Advanced task automation and scheduling system
    """
    
    def __init__(self, max_workers: int = 5):
        self.logger = NEOLogger("TaskAutomation")
        self.logger.info(f"Task Automation initialized with {max_workers} workers")
        
        self.max_workers = max_workers
        self.task_queue = queue.PriorityQueue()
        self.tasks: Dict[str, Task] = {}
        self.scheduled_tasks: Dict[str, Dict] = {}
        
        self.is_running = False
        self.workers: List[threading.Thread] = []
        
        self._task_counter = 0
        self._lock = threading.Lock()
    
    def create_task(
        self,
        name: str,
        function: Callable,
        args: tuple = (),
        kwargs: dict = None,
        priority: TaskPriority = TaskPriority.NORMAL
    ) -> str:
        """
        Create a new task
        
        Args:
            name: Task name
            function: Function to execute
            args: Function arguments
            kwargs: Function keyword arguments
            priority: Task priority
        
        Returns:
            Task ID
        """
        with self._lock:
            self._task_counter += 1
            task_id = f"task_{self._task_counter}_{int(time.time())}"
        
        task = Task(
            id=task_id,
            name=name,
            function=function,
            args=args,
            kwargs=kwargs or {},
            priority=priority
        )
        
        self.tasks[task_id] = task
        
        self.logger.info(f"Created task: {task_id} ({name}) with priority {priority.name}")
        
        return task_id
    
    def submit_task(self, task_id: str) -> bool:
        """
        Submit task to execution queue
        
        Args:
            task_id: Task ID
        
        Returns:
            Success status
        """
        if task_id not in self.tasks:
            self.logger.error(f"Task not found: {task_id}")
            return False
        
        task = self.tasks[task_id]
        
        # Add to priority queue (lower priority value = higher priority)
        priority_value = -task.priority.value  # Negate for correct priority ordering
        self.task_queue.put((priority_value, task_id))
        
        self.logger.info(f"Submitted task: {task_id}")
        
        return True
    
    def execute_task(self, task_id: str) -> Any:
        """
        Execute a task immediately
        
        Args:
            task_id: Task ID
        
        Returns:
            Task result
        """
        if task_id not in self.tasks:
            self.logger.error(f"Task not found: {task_id}")
            return None
        
        task = self.tasks[task_id]
        
        return self._execute_task(task)
    
    def _execute_task(self, task: Task) -> Any:
        """Execute task with error handling and retries"""
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.now()
        
        self.logger.info(f"Executing task: {task.id} ({task.name})")
        
        try:
            result = task.function(*task.args, **task.kwargs)
            
            task.status = TaskStatus.COMPLETED
            task.result = result
            task.completed_at = datetime.now()
            
            duration = (task.completed_at - task.started_at).total_seconds()
            self.logger.info(f"Task completed: {task.id} in {duration:.2f}s")
            
            return result
        
        except Exception as e:
            self.logger.error(f"Task failed: {task.id} - {str(e)}")
            
            task.error = str(e)
            task.retry_count += 1
            
            # Retry logic
            if task.retry_count < task.max_retries:
                self.logger.info(f"Retrying task: {task.id} (attempt {task.retry_count + 1}/{task.max_retries})")
                time.sleep(2 ** task.retry_count)  # Exponential backoff
                return self._execute_task(task)
            else:
                task.status = TaskStatus.FAILED
                task.completed_at = datetime.now()
                return None
    
    def schedule_task(
        self,
        task_id: str,
        schedule_time: datetime = None,
        interval: timedelta = None,
        cron: str = None
    ) -> bool:
        """
        Schedule task for future execution
        
        Args:
            task_id: Task ID
            schedule_time: Specific time to execute
            interval: Recurring interval
            cron: Cron expression (simplified)
        
        Returns:
            Success status
        """
        if task_id not in self.tasks:
            self.logger.error(f"Task not found: {task_id}")
            return False
        
        task = self.tasks[task_id]
        task.status = TaskStatus.SCHEDULED
        
        schedule_info = {
            "task_id": task_id,
            "schedule_time": schedule_time,
            "interval": interval,
            "cron": cron
        }
        
        self.scheduled_tasks[task_id] = schedule_info
        
        self.logger.info(f"Scheduled task: {task_id}")
        
        return True
    
    def cancel_task(self, task_id: str) -> bool:
        """
        Cancel a task
        
        Args:
            task_id: Task ID
        
        Returns:
            Success status
        """
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        
        if task.status == TaskStatus.RUNNING:
            self.logger.warning(f"Cannot cancel running task: {task_id}")
            return False
        
        task.status = TaskStatus.CANCELLED
        
        # Remove from scheduled tasks
        if task_id in self.scheduled_tasks:
            del self.scheduled_tasks[task_id]
        
        self.logger.info(f"Cancelled task: {task_id}")
        
        return True
    
    def start_workers(self):
        """Start worker threads"""
        if self.is_running:
            self.logger.warning("Workers already running")
            return
        
        self.is_running = True
        
        for i in range(self.max_workers):
            worker = threading.Thread(target=self._worker, name=f"Worker-{i+1}", daemon=True)
            worker.start()
            self.workers.append(worker)
        
        self.logger.info(f"Started {self.max_workers} worker threads")
    
    def stop_workers(self):
        """Stop worker threads"""
        self.is_running = False
        
        self.logger.info("Stopping workers...")
        
        for worker in self.workers:
            worker.join(timeout=5)
        
        self.workers.clear()
        
        self.logger.info("Workers stopped")
    
    def _worker(self):
        """Worker thread function"""
        worker_name = threading.current_thread().name
        
        while self.is_running:
            try:
                # Get task from queue with timeout
                priority, task_id = self.task_queue.get(timeout=1)
                
                if task_id in self.tasks:
                    task = self.tasks[task_id]
                    self.logger.debug(f"{worker_name} executing task: {task_id}")
                    self._execute_task(task)
                
                self.task_queue.task_done()
            
            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"{worker_name} error: {e}")
    
    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Get task status
        
        Args:
            task_id: Task ID
        
        Returns:
            Task status dictionary
        """
        if task_id not in self.tasks:
            return None
        
        task = self.tasks[task_id]
        
        return {
            "id": task.id,
            "name": task.name,
            "status": task.status.value,
            "priority": task.priority.name,
            "created_at": task.created_at.isoformat(),
            "started_at": task.started_at.isoformat() if task.started_at else None,
            "completed_at": task.completed_at.isoformat() if task.completed_at else None,
            "retry_count": task.retry_count,
            "error": task.error
        }
    
    def get_all_tasks(self, status: Optional[TaskStatus] = None) -> List[Dict[str, Any]]:
        """
        Get all tasks, optionally filtered by status
        
        Args:
            status: Filter by status
        
        Returns:
            List of task status dictionaries
        """
        tasks = []
        
        for task_id, task in self.tasks.items():
            if status is None or task.status == status:
                task_info = self.get_task_status(task_id)
                if task_info:
                    tasks.append(task_info)
        
        return tasks
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get task execution statistics"""
        total_tasks = len(self.tasks)
        
        status_counts = {
            status.value: len([t for t in self.tasks.values() if t.status == status])
            for status in TaskStatus
        }
        
        completed_tasks = [t for t in self.tasks.values() if t.status == TaskStatus.COMPLETED]
        
        avg_duration = 0
        if completed_tasks:
            durations = [
                (t.completed_at - t.started_at).total_seconds()
                for t in completed_tasks if t.started_at and t.completed_at
            ]
            avg_duration = sum(durations) / len(durations) if durations else 0
        
        return {
            "total_tasks": total_tasks,
            "status_counts": status_counts,
            "queue_size": self.task_queue.qsize(),
            "active_workers": len([w for w in self.workers if w.is_alive()]),
            "average_duration": avg_duration,
            "scheduled_tasks": len(self.scheduled_tasks)
        }
    
    def create_workflow(self, name: str, task_chain: List[Dict[str, Any]]) -> str:
        """
        Create a workflow of dependent tasks
        
        Args:
            name: Workflow name
            task_chain: List of task definitions in order
        
        Returns:
            Workflow ID
        """
        self.logger.info(f"Creating workflow: {name} with {len(task_chain)} tasks")
        
        workflow_id = f"workflow_{int(time.time())}"
        task_ids = []
        
        for task_def in task_chain:
            task_id = self.create_task(
                name=task_def['name'],
                function=task_def['function'],
                args=task_def.get('args', ()),
                kwargs=task_def.get('kwargs', {}),
                priority=task_def.get('priority', TaskPriority.NORMAL)
            )
            task_ids.append(task_id)
        
        return workflow_id
    
    def execute_workflow(self, workflow_id: str, task_ids: List[str]) -> List[Any]:
        """
        Execute workflow tasks in sequence
        
        Args:
            workflow_id: Workflow ID
            task_ids: List of task IDs
        
        Returns:
            List of results
        """
        self.logger.info(f"Executing workflow: {workflow_id}")
        
        results = []
        
        for task_id in task_ids:
            result = self.execute_task(task_id)
            results.append(result)
            
            # If task failed, stop workflow
            if task_id in self.tasks and self.tasks[task_id].status == TaskStatus.FAILED:
                self.logger.error(f"Workflow {workflow_id} stopped due to task failure: {task_id}")
                break
        
        return results


if __name__ == "__main__":
    # Test task automation
    automation = TaskAutomation(max_workers=3)
    
    # Create test tasks
    def test_function(x, y):
        time.sleep(1)
        return x + y
    
    task1 = automation.create_task("Add Numbers", test_function, args=(5, 3), priority=TaskPriority.HIGH)
    task2 = automation.create_task("Another Task", test_function, args=(10, 20), priority=TaskPriority.NORMAL)
    
    # Start workers
    automation.start_workers()
    
    # Submit tasks
    automation.submit_task(task1)
    automation.submit_task(task2)
    
    # Wait a bit
    time.sleep(3)
    
    # Get statistics
    stats = automation.get_statistics()
    print(f"Statistics: {stats}")
    
    # Stop workers
    automation.stop_workers()
