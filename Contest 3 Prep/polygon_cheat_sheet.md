# Polygon Geometry Cheat Sheet (COMP 321)

## 1. Definitions

| Term | Meaning |
|---|---|
| **Polygon** | Closed path of line segments; stored as a list of vertices in CW or CCW order |
| **Simple** | No edges cross each other (a bowtie is *not* simple) |
| **Convex** | Simple, and any segment between two points inside stays inside |
| **Concave** | Simple but not convex (has a "dent") |
| **Regular** | All sides equal, all angles equal (always convex; all vertices lie on one circle) |

## 2. Core primitives

```python
def dot(u, v):   return u[0]*v[0] + u[1]*v[1]
def cross(u, v): return u[0]*v[1] - u[1]*v[0]
def vec(p, q):   return (q[0]-p[0], q[1]-p[1])      # vector p -> q
def ccw(A, B, C): return cross(vec(A, B), vec(A, C)) 
```

| Operation | Formula | Tells you |
|---|---|---|
| Dot product | `x0*x1 + y0*y1 = \|u\|\|v\|cos θ` | `0` means perpendicular; angle via `acos`; projection |
| Cross product | `x0*y1 - y0*x1 = \|u\|\|v\|sin θ` | **Signed** area of the parallelogram |
| Triangle area | `abs(cross(u, v)) / 2` | Area of triangle formed by `u` and `v` |
| `ccw(A,B,C)` | `(B-A) × (C-A)` | `> 0` left turn, `< 0` right turn, `== 0` collinear |
| Squared distance | `dx*dx + dy*dy` | Exact for ints; compare `d²` with `r²` instead of using `sqrt` |

**Which side of a line?** For line through `s1, s2` and point `p`: `cross(s2-s1, p-s1)`  
`> 0` left, `< 0` right, `= 0` on the line.

**Point-line distance:** `abs(cross(p-s1, s2-s1)) / |s2-s1|`

Class:

```python
# Vector class (Python)
from math import sqrt, atan2, cos, sin

class Vec:
    def __init__(self, x=0, y=0):
        self.x, self.y = x, y

    def __add__(self, o):  return Vec(self.x + o.x, self.y + o.y)
    def __sub__(self, o):  return Vec(self.x - o.x, self.y - o.y)
    def __mul__(self, k):  return Vec(self.x * k, self.y * k)
    def __eq__(self, o):   return self.x == o.x and self.y == o.y
    def __repr__(self):    return f"({self.x}, {self.y})"

    def dot(self, o):      return self.x * o.x + self.y * o.y
    def cross(self, o):    return self.x * o.y - self.y * o.x
    def dist2(self):       return self.x * self.x + self.y * self.y   # exact for ints
    def dist(self):        return sqrt(self.dist2())
    def angle(self):       return atan2(self.y, self.x)               # in [-pi, pi]
    def perp(self):        return Vec(-self.y, self.x)                # rotate +90 degrees
    def rotate(self, a):   # CCW by a radians around the origin
        return Vec(self.x * cos(a) - self.y * sin(a),
                   self.x * sin(a) + self.y * cos(a))

def ccw(A, B, C):
    return (B - A).cross(C - A)    # > 0 left turn, < 0 right turn, 0 collinear
```

Example (Completing the Square, corner `A` with neighbors `B`, `C`):

```python
A, B, C = Vec(1, 0), Vec(0, 0), Vec(1, 1)
if (B - A).dot(C - A) == 0:        # perpendicular, so A is the corner
    print(A + (B - A) + (C - A))   # (0, 1)
```




## 3. Convexity test

Take `ccw` of every three consecutive vertices (wrapping around).

- All turns left **or** all turns right → **convex**
- Mixed signs → **concave**

```python
def is_convex(P):
    n = len(P)
    signs = set()
    for i in range(n):
        c = ccw(P[i], P[(i+1) % n], P[(i+2) % n])
        if c != 0:
            signs.add(c > 0)
    return len(signs) <= 1
```

## 4. Area: shoelace formula

```python
def signed_area(P):
    total = 0
    n = len(P)
    for i in range(n):
        x1, y1 = P[i]
        x2, y2 = P[(i+1) % n]       # wraps to close the polygon
        total += x1*y2 - x2*y1
    return total / 2
```

- **Positive** → vertices are counter-clockwise; **negative** → clockwise
- True area = `abs(signed_area(P))`
- Works for any simple polygon (triangles outside the shape cancel out because the cross product is signed)
- Check: square (0,0), (2,0), (2,2), (0,2) → terms 0+4+4+0 = 8 → area **4**

**Triangles:** `A = ½·b·h`, Heron: `s = (a+b+c)/2`, `A = √(s(s-a)(s-b)(s-c))`

## 5. Point in polygon

| Method | Works for | Idea |
|---|---|---|
| **Area sum** | Convex only | Sum areas of triangles (point + each adjacent vertex pair). Equal to polygon area ⇔ point inside |
| **Even-odd (ray casting)** | Any polygon | Cast a ray in any direction, count edge crossings. **Odd = inside**, even = outside |
| **Winding number** | Any polygon | Sum signed angles `P[i], pt, P[i+1]` (add left turns, subtract right turns). **2π = inside**, 0 = outside |

**Watch out (slide "Evil test cases"):** rays passing exactly through a vertex or along an edge, and points lying exactly on the boundary.

## 6. Segment-segment intersection

**Proper intersection** (cross strictly inside both segments), segments `AB` and `CD`:

```
ccw(A,B,C) * ccw(A,B,D) < 0   and   ccw(C,D,A) * ccw(C,D,B) < 0
```

Edge cases needing extra care:

- Intersect at an endpoint (a `ccw` is 0)
- Collinear: all four `ccw` values are 0 → reduces to checking whether two 1D intervals overlap (no overlap / interior overlap / shared endpoint / containment)
- If they intersect, the point comes from intersecting the two induced lines

**Line intersection** for `a1x + b1y + c1 = 0` and `a2x + b2y + c2 = 0`:

```
det = a1*b2 - a2*b1          # det == 0 → parallel
x = (b1*c2 - c1*b2) / det
```

## 7. Circles and regular polygons

| Item | Formula |
|---|---|
| Circle equation | `(x-a)² + (y-b)² = r²` |
| Circumference / area | `2πr`, `πr²` |
| Get π | `2 * acos(0)` (don't hard-code an approximation) |
| Circumradius of triangle | `R = abc / (4A)` |
| Circumcenter | Intersection of perpendicular bisectors |
| Inradius of triangle | `r = A / s` |
| Rotate point CCW by θ around origin | `(x cosθ - y sinθ, x sinθ + y cosθ)` |

**Regular n-gon from a center `P`, radius `r`, and one vertex angle `θ`:** vertex `k` is  
`(px + r·cos(θ + 2πk/n), py + r·sin(θ + 2πk/n))` for `k = 0..n-1`.

**Circumcenter from 3 points** (equidistant from A, B, C): solve the linear system  
`2(B-A)·P = |B|² - |A|²` and `2(C-A)·P = |C|² - |A|²` with Cramer's rule.

## 8. Practical tips

- Use **integers** when you can; floats are inexact, so compare with a small epsilon (e.g. `1e-9`)
- Compare **squared** distances to avoid `sqrt`
- Treat vertical lines (infinite slope) separately, or use `ax + by + c = 0` form
- Wrap vertex indices with `% n` to close the polygon
- Check collinear, duplicate-point, and endpoint-touching cases explicitly
- Print floats with plenty of decimals, e.g. `f"{x:.10f}"`
