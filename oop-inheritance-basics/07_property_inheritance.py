"""
Property inheritance example demonstrating how properties and descriptors
work with inheritance in Python.
"""

from typing import Any, Optional, Dict
from datetime import datetime

class ValidatedProperty:
    """
    A descriptor class that implements validation for a property.
    Demonstrates how descriptors can be used to create reusable property logic.
    """
    def __init__(self, validation_func, error_message: str):
        self.validation_func = validation_func
        self.error_message = error_message
        self.property_name = ''  # Will be set when the descriptor is assigned to a class

    def __set_name__(self, owner: Any, name: str):
        """Called when the descriptor is assigned to a class attribute."""
        self.property_name = name

    def __get__(self, instance: Any, owner: Any) -> Any:
        """Retrieve the property value."""
        if instance is None:
            return self
        return instance.__dict__.get(self.property_name)

    def __set__(self, instance: Any, value: Any):
        """Set and validate the property value."""
        if not self.validation_func(value):
            raise ValueError(f"{self.property_name}: {self.error_message}")
        instance.__dict__[self.property_name] = value

class TrackingDescriptor:
    """
    A descriptor that tracks when a property was last modified.
    Demonstrates descriptor inheritance and composition.
    """
    def __init__(self):
        self.property_name = ''
        self.tracker_name = ''

    def __set_name__(self, owner: Any, name: str):
        """Called when the descriptor is assigned to a class attribute."""
        self.property_name = name
        self.tracker_name = f"_{name}_last_modified"

    def __get__(self, instance: Any, owner: Any) -> Any:
        """Retrieve the property value."""
        if instance is None:
            return self
        return instance.__dict__.get(self.property_name)

    def __set__(self, instance: Any, value: Any):
        """Set the value and update the last modified timestamp."""
        instance.__dict__[self.property_name] = value
        instance.__dict__[self.tracker_name] = datetime.now()

class BaseProduct:
    """
    Base class demonstrating property definition and inheritance.
    """
    def __init__(self, name: str, price: float):
        self._name = name
        self._price = price

    @property
    def name(self) -> str:
        """Product name property."""
        return self._name

    @name.setter
    def name(self, value: str):
        if not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()

    @property
    def price(self) -> float:
        """Product price property."""
        return self._price

    @price.setter
    def price(self, value: float):
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = value

class DigitalProduct(BaseProduct):
    """
    Digital product class demonstrating property inheritance and extension.
    """
    # Using descriptors for new properties
    file_size = ValidatedProperty(
        lambda x: isinstance(x, int) and x > 0,
        "File size must be a positive integer"
    )
    download_url = ValidatedProperty(
        lambda x: isinstance(x, str) and x.startswith(('http://', 'https://')),
        "Download URL must be a valid HTTP(S) URL"
    )
    version = TrackingDescriptor()

    def __init__(self, name: str, price: float, file_size: int, download_url: str):
        super().__init__(name, price)
        self.file_size = file_size  # Uses ValidatedProperty
        self.download_url = download_url  # Uses ValidatedProperty
        self.version = "1.0"  # Uses TrackingDescriptor

    @property
    def price(self) -> float:
        """
        Override parent's price property to add digital discount.
        Demonstrates property override while using parent's validation.
        """
        base_price = super().price
        return base_price * 0.8  # 20% discount for digital products

def main():
    # Demonstrate basic property inheritance
    print("\nBasic Property Inheritance:")
    print("-" * 50)
    try:
        product = BaseProduct("Test Product", 10.0)
        print(f"Initial product name: {product.name}")
        product.name = "Updated Product"
        print(f"Updated product name: {product.name}")
        
        # Try invalid value
        product.name = ""
    except ValueError as e:
        print(f"Validation error: {e}")

    # Demonstrate digital product with descriptors
    print("\nDigital Product with Descriptors:")
    print("-" * 50)
    try:
        digital = DigitalProduct(
            name="Software Package",
            price=100.0,
            file_size=1024,
            download_url="https://example.com/download"
        )
        
        # Show inherited and overridden properties
        print(f"Name: {digital.name}")
        print(f"Original price: ${100.0:.2f}")
        print(f"Discounted price: ${digital.price:.2f}")
        print(f"File size: {digital.file_size}")
        print(f"Download URL: {digital.download_url}")
        print(f"Version: {digital.version}")
        
        # Demonstrate version tracking
        digital.version = "1.1"
        print(f"\nAfter version update:")
        print(f"Version: {digital.version}")
        print(f"Last modified: {digital.__dict__['_version_last_modified']}")

        # Try invalid values
        print("\nTrying invalid values:")
        digital.file_size = -100  # Should raise ValueError
    except ValueError as e:
        print(f"Validation error: {e}")

    try:
        digital.download_url = "ftp://invalid-url"  # Should raise ValueError
    except ValueError as e:
        print(f"Validation error: {e}")

if __name__ == "__main__":
    main()
