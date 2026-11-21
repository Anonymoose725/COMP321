from dataclasses import dataclass
from math import sqrt, atan2, sin, cos
def sgn(x): return (x > 0) - (x < 0)
@dataclass(order=True, frozen=True)
class Point:
# Use int for exact geometry, float for fractional coordinates.
# Uncomment marked methods ONLY when using float coordinates.
    x: int = 0
    y: int = 0
    def __add__(self, p): return Point(self.x+p.x, self.y+p.y)
    def __sub__(self, p): return Point(self.x-p.x, self.y-p.y)
    def __mul__(self, d): return Point(self.x*d, self.y*d)
    def dot(self, p): return self.x*p.x + self.y*p.y
    def cross(self, a, b=None):
        return self.x*a.y - self.y*a.x if b is None else (a-self).cross(b-self)
    def dist2(self): return self.x**2 + self.y**2
    def dist(self): return sqrt(self.dist2())
    def angle(self): return atan2(self.y, self.x)
    def perp(self): return Point(-self.y, self.x)
    # def __truediv__(self, d): return Point(self.x/d, self.y/d)
    # def unit(self): return self / self.dist()
    # def normal(self): return self.perp().unit()
    # def rotate(self, a):
    # return Point(self.x*cos(a)-self.y*sin(a),
    # self.x*sin(a)+self.y*cos(a))
    def __str__(self): return f"({self.x},{self.y})"