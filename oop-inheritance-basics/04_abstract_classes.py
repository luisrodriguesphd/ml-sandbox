"""
Abstract base class example demonstrating how to define and use abstract classes
and methods to enforce interfaces in Python.
"""

from abc import ABC, abstractmethod
from typing import List

class DataSource(ABC):
    """
    Abstract base class defining a common interface for data sources.
    ABC ensures this class cannot be instantiated directly.
    """
    
    @abstractmethod
    def connect(self) -> bool:
        """
        Establish connection to the data source.
        Must be implemented by concrete classes.
        """
        pass

    @abstractmethod
    def disconnect(self) -> bool:
        """
        Close connection to the data source.
        Must be implemented by concrete classes.
        """
        pass

    @abstractmethod
    def fetch_data(self) -> List[dict]:
        """
        Retrieve data from the source.
        Must be implemented by concrete classes.
        """
        pass

    def get_status(self) -> str:
        """
        Non-abstract method that can be inherited as-is.
        Concrete classes can still override if needed.
        """
        return "DataSource is ready"

class DatabaseSource(DataSource):
    """Concrete implementation of DataSource for database connections."""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.is_connected = False

    def connect(self) -> bool:
        """Implement abstract connect method."""
        print(f"Connecting to database: {self.connection_string}")
        self.is_connected = True
        return True

    def disconnect(self) -> bool:
        """Implement abstract disconnect method."""
        print("Disconnecting from database")
        self.is_connected = False
        return True

    def fetch_data(self) -> List[dict]:
        """Implement abstract fetch_data method."""
        if not self.is_connected:
            raise RuntimeError("Must connect before fetching data")
        return [
            {"id": 1, "name": "Sample Data 1"},
            {"id": 2, "name": "Sample Data 2"}
        ]

class APISource(DataSource):
    """Another concrete implementation of DataSource for API connections."""
    
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key
        self.is_connected = False

    def connect(self) -> bool:
        """Implement abstract connect method."""
        print(f"Connecting to API: {self.api_url}")
        self.is_connected = True
        return True

    def disconnect(self) -> bool:
        """Implement abstract disconnect method."""
        print("Disconnecting from API")
        self.is_connected = False
        return True

    def fetch_data(self) -> List[dict]:
        """Implement abstract fetch_data method."""
        if not self.is_connected:
            raise RuntimeError("Must connect before fetching data")
        return [
            {"id": 1, "data": "API Response 1"},
            {"id": 2, "data": "API Response 2"}
        ]

    def get_status(self) -> str:
        """Override the non-abstract method with custom implementation."""
        return f"APISource connected to {self.api_url}"

def process_data_source(source: DataSource):
    """
    Function demonstrating how abstract base classes enable polymorphism.
    Works with any class that properly implements the DataSource interface.
    """
    try:
        source.connect()
        data = source.fetch_data()
        print(f"Status: {source.get_status()}")
        print(f"Fetched data: {data}")
    finally:
        source.disconnect()

def main():
    # Demonstrate that abstract class cannot be instantiated
    print("\nTrying to instantiate abstract class:")
    print("-" * 50)
    try:
        data_source = DataSource()
    except TypeError as e:
        print(f"Error: {e}")

    # Show how concrete implementations work
    print("\nUsing DatabaseSource:")
    print("-" * 50)
    db_source = DatabaseSource("postgresql://localhost:5432/mydb")
    process_data_source(db_source)

    print("\nUsing APISource:")
    print("-" * 50)
    api_source = APISource("https://api.example.com", "secret-key")
    process_data_source(api_source)

    # Demonstrate isinstance checks with abstract classes
    print("\nType Checking:")
    print("-" * 50)
    print(f"Is DatabaseSource a DataSource? {isinstance(db_source, DataSource)}")
    print(f"Is APISource a DataSource? {isinstance(api_source, DataSource)}")
    print(f"Is APISource a DatabaseSource? {isinstance(api_source, DatabaseSource)}")

if __name__ == "__main__":
    main()
