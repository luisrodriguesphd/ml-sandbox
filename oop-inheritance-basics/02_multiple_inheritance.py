"""
Multiple inheritance example demonstrating method resolution order (MRO)
and common multiple inheritance patterns in Python.
"""

class PowerSource:
    """Base class for power-related functionality."""
    def __init__(self, power_type: str):
        self.power_type = power_type
        
    def get_power_info(self) -> str:
        """Return information about the power source."""
        return f"Powered by {self.power_type}"

class NetworkDevice:
    """Base class for network-related functionality."""
    def __init__(self, ip_address: str):
        self.ip_address = ip_address
        
    def get_network_info(self) -> str:
        """Return network-related information."""
        return f"Connected to network at {self.ip_address}"

    def status(self) -> str:
        """Get device status."""
        return "Network device is online"

class Storage:
    """Base class for storage-related functionality."""
    def __init__(self, capacity: int):
        self.capacity = capacity
        
    def get_storage_info(self) -> str:
        """Return storage-related information."""
        return f"Storage capacity: {self.capacity}GB"

    def status(self) -> str:
        """Get storage status."""
        return "Storage is available"

class SmartDevice(PowerSource, NetworkDevice, Storage):
    """
    A smart device that combines power, network, and storage capabilities.
    This demonstrates multiple inheritance and method resolution.
    """
    def __init__(self, name: str, power_type: str, ip_address: str, capacity: int):
        # Initialize all parent classes
        PowerSource.__init__(self, power_type)
        NetworkDevice.__init__(self, ip_address)
        Storage.__init__(self, capacity)
        self.name = name

    def status(self) -> str:
        """
        Get complete device status.
        This demonstrates how method resolution order affects inheritance.
        """
        # NetworkDevice.status() will be called because NetworkDevice
        # comes before Storage in the inheritance order
        return f"{self.name}: {super().status()}"

    def get_full_info(self) -> str:
        """Get complete information about the device."""
        return (f"{self.name}:\n"
                f"- {self.get_power_info()}\n"
                f"- {self.get_network_info()}\n"
                f"- {self.get_storage_info()}")

def main():
    # Create a smart device instance
    device = SmartDevice(
        name="Smart Hub",
        power_type="AC",
        ip_address="192.168.1.100",
        capacity=64
    )

    # Demonstrate method resolution order (MRO)
    print("\nClass Hierarchy and MRO:")
    print("-" * 50)
    print("Method Resolution Order:", [c.__name__ for c in SmartDevice.__mro__])
    print(f"SmartDevice inherits from PowerSource? {isinstance(device, PowerSource)}")
    print(f"SmartDevice inherits from NetworkDevice? {isinstance(device, NetworkDevice)}")
    print(f"SmartDevice inherits from Storage? {isinstance(device, Storage)}")

    # Show how methods from different parent classes are accessed
    print("\nAccessing Methods from Different Parents:")
    print("-" * 50)
    print("Power Info:", device.get_power_info())
    print("Network Info:", device.get_network_info())
    print("Storage Info:", device.get_storage_info())

    # Demonstrate method resolution for status()
    print("\nMethod Resolution for status():")
    print("-" * 50)
    print("Device Status:", device.status())
    print("(Notice that NetworkDevice.status() is used due to MRO)")

    # Show complete device information
    print("\nComplete Device Information:")
    print("-" * 50)
    print(device.get_full_info())

if __name__ == "__main__":
    main()
