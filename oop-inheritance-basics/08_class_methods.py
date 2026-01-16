"""
Class methods example demonstrating @classmethod decorator usage,
alternative constructors, and class method inheritance.
"""

from datetime import datetime
from typing import Dict, Any


class BankAccount:
    """Base class for bank accounts with class-level tracking."""
    
    # Class attribute to track total accounts created
    total_accounts = 0
    interest_rate = 0.02  # Default 2% interest
    
    def __init__(self, account_number: str, holder_name: str, balance: float):
        self.account_number = account_number
        self.holder_name = holder_name
        self.balance = balance
        self.created_at = datetime.now()
        
        # Increment class-level counter
        BankAccount.total_accounts += 1
    
    @classmethod
    def get_total_accounts(cls) -> int:
        """
        Class method to get total number of accounts created.
        Uses cls parameter instead of self.
        
        NOTE: This method is for illustration. You could also access
        the class attribute directly: BankAccount.total_accounts
        
        Use a class method when you need:
        - Additional logic/validation before returning the value
        - To maintain encapsulation (hide implementation details)
        - Consistent API across different account types via inheritance
        """
        return cls.total_accounts
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BankAccount':
        """
        Alternative constructor using class method.
        Creates a BankAccount instance from a dictionary.
        """
        return cls(
            account_number=data['account_number'],
            holder_name=data['holder_name'],
            balance=data.get('balance', 0.0)
        )
    
    @classmethod
    def set_interest_rate(cls, rate: float) -> None:
        """
        Class method to modify class attribute.
        Affects all instances of the class.
        """
        cls.interest_rate = rate
    
    def calculate_interest(self) -> float:
        """Instance method that uses class attribute."""
        return self.balance * self.interest_rate
    
    def get_info(self) -> str:
        """Get account information."""
        return (f"Account: {self.account_number}\n"
                f"Holder: {self.holder_name}\n"
                f"Balance: ${self.balance:,.2f}\n"
                f"Interest Rate: {self.interest_rate * 100}%")


class SavingsAccount(BankAccount):
    """Savings account with higher interest rate."""
    
    interest_rate = 0.04  # 4% interest for savings
    minimum_balance = 100.0
    
    def __init__(self, account_number: str, holder_name: str, 
                 balance: float, withdrawal_limit: int = 3):
        super().__init__(account_number, holder_name, balance)
        self.withdrawal_limit = withdrawal_limit
        self.withdrawals_this_month = 0
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SavingsAccount':
        """
        Override parent's class method for SavingsAccount-specific creation.
        Demonstrates class method inheritance and overriding.
        """
        return cls(
            account_number=data['account_number'],
            holder_name=data['holder_name'],
            balance=data.get('balance', cls.minimum_balance),
            withdrawal_limit=data.get('withdrawal_limit', 3)
        )
    
    @classmethod
    def get_minimum_balance(cls) -> float:
        """
        Additional class method specific to SavingsAccount.
        """
        return cls.minimum_balance
    
    def get_info(self) -> str:
        """Override to include savings-specific information."""
        basic_info = super().get_info()
        return (f"{basic_info}\n"
                f"Account Type: Savings\n"
                f"Withdrawal Limit: {self.withdrawal_limit}/month\n"
                f"Withdrawals Used: {self.withdrawals_this_month}")


class CheckingAccount(BankAccount):
    """Checking account with overdraft protection."""
    
    interest_rate = 0.01  # 1% interest for checking
    
    def __init__(self, account_number: str, holder_name: str, 
                 balance: float, overdraft_limit: float = 500.0):
        super().__init__(account_number, holder_name, balance)
        self.overdraft_limit = overdraft_limit
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CheckingAccount':
        """
        Override parent's class method for CheckingAccount-specific creation.
        """
        return cls(
            account_number=data['account_number'],
            holder_name=data['holder_name'],
            balance=data.get('balance', 0.0),
            overdraft_limit=data.get('overdraft_limit', 500.0)
        )
    
    def get_info(self) -> str:
        """Override to include checking-specific information."""
        basic_info = super().get_info()
        return (f"{basic_info}\n"
                f"Account Type: Checking\n"
                f"Overdraft Limit: ${self.overdraft_limit:,.2f}")


def main():
    print("\nClass Methods Example:")
    print("=" * 60)
    
    # Creating instances normally
    print("\n1. Creating Accounts Normally:")
    print("-" * 60)
    account1 = BankAccount("ACC001", "John Doe", 1000.0)
    print(f"Created: {account1.holder_name}")
    print(f"Total accounts (via method): {BankAccount.get_total_accounts()}")
    print(f"Total accounts (direct access): {BankAccount.total_accounts}")
    
    # Using class method as alternative constructor
    print("\n2. Using Class Method as Alternative Constructor:")
    print("-" * 60)
    savings_data = {
        'account_number': 'SAV001',
        'holder_name': 'Jane Smith',
        'balance': 1000.0,
        'withdrawal_limit': 5
    }
    savings = SavingsAccount.from_dict(savings_data)
    print(f"Created from dict: {savings.holder_name}")
    print(f"Total accounts: {BankAccount.get_total_accounts()}")
    
    checking_data = {
        'account_number': 'CHK001',
        'holder_name': 'Bob Johnson',
        'balance': 1000.0,
        'overdraft_limit': 500.0
    }
    checking = CheckingAccount.from_dict(checking_data)
    print(f"Created from dict: {checking.holder_name}")
    print(f"Total accounts: {BankAccount.get_total_accounts()}")
    
    # Demonstrating class method inheritance
    print("\n3. Class Method Inheritance:")
    print("-" * 60)
    print(f"Base class interest rate: {BankAccount.interest_rate * 100}%")
    print(f"Savings interest rate: {SavingsAccount.interest_rate * 100}%")
    print(f"Checking interest rate: {CheckingAccount.interest_rate * 100}%")
    
    # Show different interest calculations
    print("\n4. Interest Calculations (using class attributes):")
    print("-" * 60)
    print(f"Account1 interest: ${account1.calculate_interest():,.2f}")
    print(f"Savings interest: ${savings.calculate_interest():,.2f}")
    print(f"Checking interest: ${checking.calculate_interest():,.2f}")
    
    # Modifying class attribute with class method
    print("\n5. Modifying Class Attribute via Class Method:")
    print("-" * 60)
    print("Setting new base interest rate to 3%...")
    BankAccount.set_interest_rate(0.03)
    print(f"New account1 interest: ${account1.calculate_interest():,.2f}")
    print(f"Savings still uses its own rate: ${savings.calculate_interest():,.2f}")
    
    # Accessing class-specific class methods
    print("\n6. Class-Specific Class Methods:")
    print("-" * 60)
    print(f"Savings minimum balance: ${SavingsAccount.get_minimum_balance():,.2f}")
    
    # Display full account information
    print("\n7. Full Account Information:")
    print("-" * 60)
    print("\nSavings Account:")
    print(savings.get_info())
    print("\nChecking Account:")
    print(checking.get_info())
    
    # Summary
    print("\n8. Summary:")
    print("-" * 60)
    print(f"Total accounts created: {BankAccount.get_total_accounts()}")
    print("\nKey Points Demonstrated:")
    print("  • @classmethod decorator for class-level operations")
    print("  • cls parameter (vs self for instance methods)")
    print("  • Class methods as alternative constructors")
    print("  • Class method inheritance and overriding")
    print("  • Class attributes shared across instances")
    print("  • Class methods modifying class state")
    print("\nNote: Class attributes can be accessed directly (e.g., BankAccount.total_accounts)")
    print("      Class methods are most useful for alternative constructors and operations")
    print("      that require logic, not just simple attribute access.")


if __name__ == "__main__":
    main()
