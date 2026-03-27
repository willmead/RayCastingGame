import math
from numbers import Number


type Radians = int | float 


def sign(x: Number) -> int:
    return int(math.copysign(1, x))


class Vector:

    def __init__(self, x: Number, y: Number) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: Vector) -> Vector:
        return Vector(self.x - other.x, self.y - other.y)
    
    def __mul__(self, multiplier: Number | Vector):
        if isinstance(multiplier, Number):
            return Vector(self.x * multiplier, self.y * multiplier)
        if isinstance(multiplier, Vector):
            # N.B. This is the Hadamard product (element-wise) not dot product
            return Vector(self.x * multiplier.x, self.y * multiplier.y)
        return NotImplemented
    
    def __truediv__(self, divisor: Number):
        if divisor == 0:
            return Vector(1e30, 1e30)
        return Vector(self.x / divisor, self.y / divisor)
    
    def __rtruediv__(self, dividend: Number):
        x = dividend / self.x if self.x != 0 else 1e30
        y = dividend / self.y if self.y != 0 else 1e30
        return Vector(x, y)
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"
    
    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"
    
    @property
    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)
    
    @property
    def perpendicular(self) -> Vector:
        """returns a unit vector perpendicular to the current vector"""
        perpendicular_vector = Vector(self.y, -1 * self.x)
        return perpendicular_vector / perpendicular_vector.magnitude
    
    def rotate(self, angle: Radians) -> None:
        new_x = self.x * math.cos(angle) - self.y * math.sin(angle)
        new_y = self.x * math.sin(angle) + self.y * math.cos(angle)
        self.x = new_x
        self.y = new_y

    def apply(self, function: callable) -> Vector:
        return Vector(function(self.x), function(self.y))