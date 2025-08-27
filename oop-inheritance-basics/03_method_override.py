"""
Method override example demonstrating how to properly override methods
and use super() to extend parent class functionality.
"""

class Employee:
    """Base class for all employees."""
    
    def __init__(self, name: str, id: str, base_salary: float):
        self.name = name
        self.id = id
        self.base_salary = base_salary

    def calculate_salary(self) -> float:
        """Calculate the employee's salary."""
        return self.base_salary

    def get_info(self) -> str:
        """Get employee information."""
        return (f"Employee ID: {self.id}\n"
                f"Name: {self.name}\n"
                f"Base Salary: ${self.base_salary:,.2f}")

class Manager(Employee):
    """Manager class with additional bonus calculation."""
    
    def __init__(self, name: str, id: str, base_salary: float, team_size: int):
        # Call parent's __init__ first
        super().__init__(name, id, base_salary)
        self.team_size = team_size

    def calculate_salary(self) -> float:
        """
        Override salary calculation to include management bonus.
        Demonstrates extending parent method using super().
        """
        # Get base salary from parent class
        base_salary = super().calculate_salary()
        # Add management bonus based on team size
        management_bonus = self.team_size * 1000
        return base_salary + management_bonus

    def get_info(self) -> str:
        """
        Override get_info to include manager-specific details.
        Demonstrates how to extend parent's method output.
        """
        # Get basic info from parent class
        basic_info = super().get_info()
        # Add manager-specific information
        return (f"{basic_info}\n"
                f"Team Size: {self.team_size}\n"
                f"Role: Manager")

class Developer(Employee):
    """Developer class with different bonus structure."""
    
    def __init__(self, name: str, id: str, base_salary: float, 
                 programming_languages: list[str]):
        super().__init__(name, id, base_salary)
        self.programming_languages = programming_languages

    def calculate_salary(self) -> float:
        """
        Override salary calculation for developers.
        Demonstrates completely replacing parent method.
        """
        # Developer salary includes language expertise bonus
        language_bonus = len(self.programming_languages) * 1500
        return self.base_salary + language_bonus

    def get_info(self) -> str:
        """
        Override get_info for developer-specific details.
        Demonstrates selective use of parent method content.
        """
        return (f"Developer ID: {self.id}\n"
                f"Name: {self.name}\n"
                f"Languages: {', '.join(self.programming_languages)}\n"
                f"Base Salary: ${self.base_salary:,.2f}\n"
                f"Role: Developer")

def main():
    # Create instances of different employee types
    manager = Manager(
        name="Alice Smith",
        id="M123",
        base_salary=80000,
        team_size=5
    )

    developer = Developer(
        name="Bob Jones",
        id="D456",
        base_salary=70000,
        programming_languages=["Python", "JavaScript", "Go"]
    )

    # Demonstrate different ways of using super() and method overriding
    print("\nEmployee Information:")
    print("-" * 50)
    print("Manager:")
    print(manager.get_info())
    print("\nDeveloper:")
    print(developer.get_info())

    # Show how salary calculations are overridden
    print("\nSalary Calculations:")
    print("-" * 50)
    print(f"Manager's Total Salary: ${manager.calculate_salary():,.2f}")
    print(f"Developer's Total Salary: ${developer.calculate_salary():,.2f}")

    # Demonstrate isinstance() with inheritance
    print("\nInheritance Checks:")
    print("-" * 50)
    print(f"Is manager an Employee? {isinstance(manager, Employee)}")
    print(f"Is developer an Employee? {isinstance(developer, Employee)}")
    print(f"Is manager a Developer? {isinstance(manager, Developer)}")

if __name__ == "__main__":
    main()
