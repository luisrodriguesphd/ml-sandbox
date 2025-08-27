"""
Interface and Protocol example demonstrating Python's structural subtyping
approach using the typing.Protocol class (Python 3.8+).
"""

from typing import Protocol, List, runtime_checkable
from datetime import datetime

@runtime_checkable
class Loggable(Protocol):
    """
    Protocol defining an interface for objects that can be logged.
    The @runtime_checkable decorator allows isinstance() checks.
    """
    def log_entry(self, message: str) -> None:
        """Log a message."""
        ...

    def get_log_history(self) -> List[str]:
        """Retrieve log history."""
        ...

@runtime_checkable
class Exportable(Protocol):
    """Protocol defining an interface for objects that can be exported."""
    def export_data(self) -> dict:
        """Export object data."""
        ...

class LogMixin:
    """
    A mixin class that implements the Loggable protocol.
    This can be inherited by classes that need logging functionality.
    """
    def __init__(self):
        self._log_history: List[str] = []

    def log_entry(self, message: str) -> None:
        """Implement the log_entry method required by Loggable."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._log_history.append(f"[{timestamp}] {message}")

    def get_log_history(self) -> List[str]:
        """Implement the get_log_history method required by Loggable."""
        return self._log_history.copy()

class User(LogMixin):
    """
    User class that implements both Loggable (via LogMixin) and Exportable protocols.
    Note: No explicit inheritance or interface declaration needed for Exportable.
    """
    def __init__(self, user_id: str, name: str):
        super().__init__()  # Initialize LogMixin
        self.user_id = user_id
        self.name = name
        self.log_entry(f"Created user {name}")

    def export_data(self) -> dict:
        """Implement the export_data method required by Exportable."""
        return {
            "user_id": self.user_id,
            "name": self.name,
            "log_history": self.get_log_history()
        }

class Task:
    """
    Task class that implements Exportable protocol without any inheritance.
    Demonstrates structural subtyping - it only needs to implement the required methods.
    """
    def __init__(self, task_id: str, description: str):
        self.task_id = task_id
        self.description = description
        self.completed = False

    def export_data(self) -> dict:
        """Implement the export_data method required by Exportable."""
        return {
            "task_id": self.task_id,
            "description": self.description,
            "completed": self.completed
        }

def process_logs(loggable: Loggable) -> None:
    """
    Function that works with any object implementing the Loggable protocol.
    Demonstrates how protocols enable duck typing with type hints.
    """
    loggable.log_entry("Processing started")
    print("Log History:")
    for entry in loggable.get_log_history():
        print(f"  {entry}")

def export_item(item: Exportable) -> None:
    """
    Function that works with any object implementing the Exportable protocol.
    """
    print(f"Exported data: {item.export_data()}")

def main():
    # Create instances
    user = User("U123", "Alice")
    task = Task("T456", "Complete project")

    # Demonstrate protocol usage
    print("\nProcessing Loggable Object:")
    print("-" * 50)
    process_logs(user)
    
    # This would fail type checking but works at runtime
    # process_logs(task)  # Task doesn't implement Loggable

    print("\nExporting Objects:")
    print("-" * 50)
    export_item(user)
    export_item(task)

    # Demonstrate runtime protocol checking
    print("\nRuntime Protocol Checks:")
    print("-" * 50)
    print(f"Is User Loggable? {isinstance(user, Loggable)}")
    print(f"Is User Exportable? {isinstance(user, Exportable)}")
    print(f"Is Task Loggable? {isinstance(task, Loggable)}")
    print(f"Is Task Exportable? {isinstance(task, Exportable)}")

    # Show protocol usage with additional logging
    print("\nAdditional Logging Demo:")
    print("-" * 50)
    user.log_entry("Updated user profile")
    user.log_entry("Changed password")
    process_logs(user)

if __name__ == "__main__":
    main()
