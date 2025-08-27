"""
Mixin pattern example demonstrating how to use mixins for modular functionality
that can be combined with various classes.
"""

from datetime import datetime
from typing import List, Dict, Any, Optional

class TimestampMixin:
    """Mixin that adds creation and modification time tracking."""
    
    def __init__(self):
        self._created_at = datetime.now()
        self._modified_at: Optional[datetime] = None

    def update_timestamp(self) -> None:
        """Update the modification timestamp."""
        self._modified_at = datetime.now()

    def get_timestamps(self) -> Dict[str, datetime]:
        """Get the creation and modification timestamps."""
        return {
            "created_at": self._created_at,
            "modified_at": self._modified_at
        }

class SerializableMixin:
    """Mixin that adds JSON serialization capabilities."""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert object attributes to a dictionary."""
        return {
            key: value for key, value in self.__dict__.items()
            if not key.startswith('_')
        }

    def from_dict(self, data: Dict[str, Any]) -> None:
        """Update object attributes from a dictionary."""
        for key, value in data.items():
            if not key.startswith('_'):
                setattr(self, key, value)
        if hasattr(self, 'update_timestamp'):
            self.update_timestamp()

class ValidationMixin:
    """Mixin that adds data validation capabilities."""
    
    def __init__(self):
        self._errors: List[str] = []

    def validate(self) -> bool:
        """
        Validate the object's attributes.
        Subclasses should override _validate() to implement specific validation.
        """
        self._errors = []
        return self._validate()

    def _validate(self) -> bool:
        """
        Protected method to be overridden by subclasses.
        Should populate self._errors list and return True if valid.
        """
        return True

    def get_validation_errors(self) -> List[str]:
        """Get the list of validation errors."""
        return self._errors.copy()

class User(TimestampMixin, SerializableMixin, ValidationMixin):
    """
    User class that demonstrates combining multiple mixins.
    Shows how mixins can work together to provide modular functionality.
    """
    def __init__(self, username: str, email: str):
        # Initialize all mixins
        TimestampMixin.__init__(self)
        ValidationMixin.__init__(self)
        
        self.username = username
        self.email = email

    def _validate(self) -> bool:
        """Implement custom validation logic."""
        is_valid = True
        
        if not self.username or len(self.username) < 3:
            self._errors.append("Username must be at least 3 characters long")
            is_valid = False
            
        if not self.email or '@' not in self.email:
            self._errors.append("Invalid email format")
            is_valid = False
            
        return is_valid

class Article(TimestampMixin, SerializableMixin):
    """
    Article class that demonstrates using a subset of available mixins.
    Shows how mixins allow flexible feature composition.
    """
    def __init__(self, title: str, content: str):
        TimestampMixin.__init__(self)
        self.title = title
        self.content = content

    def update_content(self, new_content: str) -> None:
        """Update article content and timestamp."""
        self.content = new_content
        self.update_timestamp()

def main():
    # Demonstrate User with all mixins
    print("\nUser Demo (with all mixins):")
    print("-" * 50)
    
    user = User("jo", "invalid-email")
    
    # Show validation
    print("Validation result:", user.validate())
    print("Validation errors:", user.get_validation_errors())
    
    # Show timestamps
    print("Initial timestamps:", {
        k: v.strftime("%Y-%m-%d %H:%M:%S") if v else None
        for k, v in user.get_timestamps().items()
    })
    
    # Show serialization
    user_data = user.to_dict()
    print("Serialized user:", user_data)
    
    # Update user and show timestamp changes
    user.username = "john_doe"
    user.email = "john@example.com"
    user.update_timestamp()
    
    print("\nAfter update:")
    print("Validation result:", user.validate())
    print("Validation errors:", user.get_validation_errors())
    print("Updated timestamps:", {
        k: v.strftime("%Y-%m-%d %H:%M:%S") if v else None
        for k, v in user.get_timestamps().items()
    })

    # Demonstrate Article with subset of mixins
    print("\nArticle Demo (with timestamp and serializable mixins):")
    print("-" * 50)
    
    article = Article("Python Mixins", "Initial content...")
    
    # Show timestamps
    print("Initial timestamps:", {
        k: v.strftime("%Y-%m-%d %H:%M:%S") if v else None
        for k, v in article.get_timestamps().items()
    })
    
    # Update content and show timestamp changes
    article.update_content("Updated content about Python mixins...")
    
    print("\nAfter update:")
    print("Updated timestamps:", {
        k: v.strftime("%Y-%m-%d %H:%M:%S") if v else None
        for k, v in article.get_timestamps().items()
    })
    
    # Show serialization
    print("Serialized article:", article.to_dict())

if __name__ == "__main__":
    main()
