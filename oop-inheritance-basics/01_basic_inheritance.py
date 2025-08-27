"""
Basic inheritance example demonstrating a simple class hierarchy
with practical use cases in a shape calculation context.
"""

class Shape:
    """Base class for all shapes."""
    def __init__(self, color: str):
        self.color = color

    def area(self) -> float:
        """Calculate the area of the shape."""
        raise NotImplementedError("Subclasses must implement area()")

    def describe(self) -> str:
        """Return a description of the shape."""
        return f"A {self.color} shape"


class Rectangle(Shape):
    """A rectangle shape with width and height."""
    def __init__(self, width: float, height: float, color: str):
        super().__init__(color)  # Initialize the parent class
        self.width = width
        self.height = height

    def area(self) -> float:
        """Calculate the area of the rectangle."""
        return self.width * self.height

    def describe(self) -> str:
        """Return a description of the rectangle."""
        return (f"A {self.color} rectangle with width {self.width} "
                f"and height {self.height}")


class Square(Rectangle):
    """A square is a special case of a rectangle with equal sides."""
    def __init__(self, side: float, color: str):
        super().__init__(width=side, height=side, color=color)

    def describe(self) -> str:
        """Return a description of the square."""
        return f"A {self.color} square with side {self.width}"


def main():
    # Create instances of different shapes
    rectangle = Rectangle(width=5, height=3, color="blue")
    square = Square(side=4, color="red")

    # Demonstrate inheritance hierarchy
    print("\nShape Inheritance Example:")
    print("-" * 50)

    # Show that both shapes inherit from Shape
    print(f"Rectangle is a Shape? {isinstance(rectangle, Shape)}")
    print(f"Square is a Shape? {isinstance(square, Shape)}")
    print(f"Square is a Rectangle? {isinstance(square, Rectangle)}")

    # Demonstrate method inheritance and overriding
    print("\nShape Descriptions:")
    print("-" * 50)
    print(f"Rectangle: {rectangle.describe()}")
    print(f"Square: {square.describe()}")

    # Show area calculations
    print("\nArea Calculations:")
    print("-" * 50)
    print(f"Rectangle area: {rectangle.area()}")
    print(f"Square area: {square.area()}")

    # Demonstrate attribute inheritance
    print("\nColor Attributes:")
    print("-" * 50)
    print(f"Rectangle color: {rectangle.color}")
    print(f"Square color: {square.color}")


if __name__ == "__main__":
    main()
