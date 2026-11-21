# Computational Geometry Cheat Sheet (COMP 321, L15 + L16) — Python

Contents: 0 Rules of thumb · 1 Primitives · 2 Cross/dot meaning · 3 Lines · 4 Triangles · 5 Circles · 6 Polygons · 7 Segment intersection · 8 Convex hull · 9 Sweep line · 10 Kattis problems from the slides · 11 Edge-case checklist

All code below was run against brute-force checks. Points are tuples `(x, y)`; use **ints whenever the input is integer**.

---

## 0. Rules of thumb

- **Stay in integers** for ccw/cross/dot/area/dist². Python ints don't overflow, so you don't need the "multiply `sgn()`s to avoid overflow" trick from the slides, but it's harmless.
- **Compare `dist²`, not `dist`** (the slides' warning for circle in/out tests). Only call `sqrt` at the end.
- **Floats are not exact.** Compare with an epsilon: `abs(a-b) < 1e-9`. Only go to floats when you must (rotation, intersection points, circumcenters).
- Use `math.pi`, or `2*acos(0)`. Never type `3.14159`.
- Vertical lines have infinite slope, so avoid `y = mx + c`. Use `ax + by + c = 0` or two points.
- Polygons: list the vertices in order (CW or CCW). The slides repeat the first vertex as the last. In the code below the polygon is a list with **no** repeated last point, and indices wrap with `% n`.
- Geometry problems are mostly edge cases: collinear points, duplicate points, zero-length segments, touching vs crossing, a point exactly on the boundary.
- For fast input: `import sys; input = sys.stdin.readline`, or read everything with `sys.stdin.read().split()`.

---

## 1. Primitives

```python
from math import sqrt, hypot, atan2, sin, cos, acos, pi
EPS = 1e-9

# Conventions used by every helper in this sheet:
#   point   = (x, y) tuple of ints or floats
#   vector  = (dx, dy) tuple, same shape as a point; the vector a -> b is sub(b, a)
#   polygon = list of points in order, first vertex NOT repeated at the end
# To switch to a Point class or complex numbers, only the p[0] / p[1] accessors change.

def sgn(x):
    """x: number -> -1, 0 or 1."""
    return (x > 0) - (x < 0)

def add(a, b):
    """a, b: vectors/points -> vector (a.x+b.x, a.y+b.y)."""
    return (a[0]+b[0], a[1]+b[1])

def sub(a, b):
    """a, b: points -> vector a - b. The vector FROM a TO b is sub(b, a)."""
    return (a[0]-b[0], a[1]-b[1])

def mul(a, k):
    """a: vector, k: scalar -> vector scaled by k."""
    return (a[0]*k, a[1]*k)

def dot(a, b):
    """a, b: vectors -> scalar a.x*b.x + a.y*b.y. Int in -> int out. >0 acute, 0 perpendicular, <0 obtuse."""
    return a[0]*b[0] + a[1]*b[1]

def cross2(a, b):
    """a, b: vectors -> scalar a.x*b.y - a.y*b.x (signed parallelogram area). >0 means b is CCW from a."""
    return a[0]*b[1] - a[1]*b[0]

def cross(o, a, b):
    """o, a, b: POINTS -> scalar (a-o) x (b-o), i.e. the slides' ccw(o,a,b).
    >0 left turn o->a->b, <0 right turn, 0 collinear. Takes 3 points, NOT 2 vectors (use cross2 for that)."""
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

def dist2(a, b=(0, 0)):
    """a, b: points (b defaults to the origin, so dist2(v) is the squared norm of vector v) -> squared distance. Exact for ints."""
    return (a[0]-b[0])**2 + (a[1]-b[1])**2

def dist(a, b=(0, 0)):
    """a, b: points (b defaults to origin) -> float Euclidean distance."""
    return hypot(a[0]-b[0], a[1]-b[1])

def angle(v):
    """v: vector -> float angle to the +x axis in [-pi, pi] (radians)."""
    return atan2(v[1], v[0])

def perp(v):
    """v: vector -> vector rotated +90 degrees (CCW), same length. Stays int for int input."""
    return (-v[1], v[0])

def unit(v):
    """v: nonzero vector -> float vector of length 1. Floats only; raises ZeroDivisionError on (0,0)."""
    d = hypot(*v); return (v[0]/d, v[1]/d)

def rotate(v, t):
    """v: vector, t: angle in RADIANS -> v rotated CCW by t around the ORIGIN (floats).
    Negative t rotates clockwise. To rotate a point around another center, use rotate_about."""
    return (v[0]*cos(t) - v[1]*sin(t), v[0]*sin(t) + v[1]*cos(t))

def rotate_about(p, c, t):
    """p: point, c: center point, t: radians -> p rotated CCW by t around c (floats)."""
    d = rotate(sub(p, c), t); return (c[0]+d[0], c[1]+d[1])
```

**Complex-number alternative.** Python's `complex` is a free 2D point, and `abs(z)` is the norm.

```python
p = complex(3, 4)
abs(p)                          # 5.0 (distance from origin)
p * 1j                          # rotate +90 degrees
p * cmath.exp(1j * t)           # rotate CCW by t  (the slide's e^{i*theta} trick)
(a.conjugate() * b).imag        # cross(a, b)
(a.conjugate() * b).real        # dot(a, b)
```

Complex numbers use floats, so they are inexact for large integer coordinates. Prefer tuples for exact work.

**Vectors**

- A point `(x, y)` is the vector from the origin. Its norm is `sqrt(x²+y²)`.
- The vector from A to B is `B − A` (slide: `B = C − A`).
- Distance between points `a` and `b` is `|b − a|`. Example from the slide: `a=(4,2), b=(3,-1)` gives `3.16228`.

**Rotation matrix** (CCW by θ about the origin):

```
[x']   [cosθ  -sinθ] [x]
[y'] = [sinθ   cosθ] [y]
```

---

## 2. Dot and cross products (the two workhorses)

| | Formula | Algebraic | Meaning |
|---|---|---|---|
| **Dot** | `u·v = ‖u‖‖v‖cosθ` | `x0·x1 + y0·y1` | `>0` acute, `=0` perpendicular, `<0` obtuse. Projections, angles. |
| **Cross (2D scalar)** | `u×v = ‖u‖‖v‖sinθ` | `x0·y1 − y0·x1` | **Signed** area of the parallelogram. `½|u×v|` is the triangle area. |

**Sign of `cross(A, B, C) = (B−A) × (C−A)`.** This is the slides' `ccw(A,B,C)`:

| Value | Meaning |
|---|---|
| `> 0` | C is to the **left** of A→B. Turn A→B→C is **counterclockwise (left turn)**. |
| `< 0` | C is to the **right**. Clockwise (right turn). |
| `= 0` | **Collinear.** |

- The cross product is **signed**: `a×b = −(b×a)`. Order matters, and that is the useful part.
- Triangle area is `abs(cross(A,B,C)) / 2`. Keep the doubled area (an int) when possible: `area2 = abs(cross(A,B,C))`.
- Angle between vectors: `acos(dot(u,v) / (‖u‖‖v‖))`. Signed angle: `atan2(cross2(u,v), dot(u,v))`.
- Perpendicular check: `dot(u,v) == 0`. Parallel check: `cross2(u,v) == 0`.
- Collinear check for 3 points: `cross(A,B,C) == 0`.

> ⚠️ The L15 "Cross Product" slide writes `|u×v| < 0 iff θ < π`, which reads backwards. With the standard convention above, `u×v > 0` when v is CCW from u (0 < θ < π). Trust the `ccw(A,B,C) > 0 ⇒ left turn` slide, which agrees with this.

---

## 3. Lines

**Representations.**

- Slope-intercept: `y = mx + c`. Breaks on vertical lines.
- General form: `ax + by + c = 0`. Handles all lines.
- Two points `P1, P2`. Unique, and the most robust.

**Line through two points → `ax + by + c = 0`.**

```python
def line_from_pts(p, q):
    """Two distinct points p, q -> (a, b, c) ints/floats with a*x + b*y + c = 0 through both. Not normalized,
    so parallel/same-line tests must use cross-multiplication (see the notes above)."""
    a = p[1] - q[1]
    b = q[0] - p[0]
    c = -(a*p[0] + b*p[1])
    return a, b, c        # a*x + b*y + c = 0
```

(From the slides: `a·x1 + b·y1 + c = 0` and `a·x2 + b·y2 + c = 0`.)

**Comparing two lines** `(a1,b1,c1)`, `(a2,b2,c2)`:

- **Parallel** iff `a1*b2 == a2*b1`. The slide says "same a and b", which only holds after normalizing, so use the cross-multiplied test.
- **Same line** iff parallel and also `a1*c2 == a2*c1` and `b1*c2 == b2*c1`.
- Otherwise they intersect in exactly one point.

**Line–line intersection** (Cramer's rule, from the slide's derivation):

```python
def line_inter(a1, b1, c1, a2, b2, c2):
    """Two lines as (a, b, c) coefficients -> (x, y) float intersection point, or None if parallel/identical."""
    det = a1*b2 - a2*b1
    if det == 0: return None          # parallel or same line
    x = (b1*c2 - b2*c1) / det
    y = (c1*a2 - c2*a1) / det
    return x, y
```

**Point–line distance** (2 points `s1`, `s2` define the line; `p` is the query point). The slide shows two views: area = `½·b·d` and projecting `p − s1` onto the perpendicular of `s2 − s1`.

```
d = |(p − s1) × (s2 − s1)| / |s2 − s1|
```

```python
def pt_line_dist(p, s1, s2):
    """p: query point; s1, s2: two DISTINCT points defining the infinite line -> float distance from p to that line.
    (For a segment, use pt_seg_dist.)"""
    return abs(cross(s1, s2, p)) / dist(s1, s2)
```

**Side test.** `cross(s1, s2, p)` is `> 0` for left, `< 0` for right, `= 0` on the line (this is the slide "Use the cross product to determine sides").

**Projection / closest point on a segment** (extra, but very common):

```python
def pt_seg_dist(p, a, b):
    """p: query point; a, b: segment endpoints (a == b allowed) -> float distance from p to the closest point of the segment."""
    ab = sub(b, a); ap = sub(p, a); L = dot(ab, ab)
    if L == 0: return dist(p, a)                  # degenerate segment
    t = max(0, min(1, dot(ap, ab) / L))           # clamp the projection to [0, 1]
    return hypot(p[0] - a[0] - t*ab[0], p[1] - a[1] - t*ab[1])
```

---

## 4. Triangles

- Area: `½·base·height`, or `abs(cross(A,B,C))/2` (preferred).
- Heron: `s = (a+b+c)/2`, `A = sqrt(s(s−a)(s−b)(s−c))`.
- **Incircle** (circle inside the triangle):
  - Radius `r = A / s`, where `s` is the semi-perimeter.
  - Center is the intersection of the angle bisectors.
  - Direct formula: incenter `= (a·A_pt + b·B_pt + c·C_pt) / (a+b+c)`, where `a` is the length of the side opposite `A_pt` (a weighted average of the vertices by opposite side length).
- **Circumcircle** (circle through all 3 vertices):
  - Radius `R = a·b·c / (4A)`.
  - Center is the intersection of the perpendicular bisectors.

```python
def circumcenter(a, b, c):        # raises ZeroDivisionError if collinear
    """a, b, c: three NON-collinear points -> (x, y) float center of the circle through all three.
    Radius = dist(center, a). Raises ZeroDivisionError if the points are collinear."""
    d = 2*(a[0]*(b[1]-c[1]) + b[0]*(c[1]-a[1]) + c[0]*(a[1]-b[1]))
    sa, sb, sc = a[0]**2+a[1]**2, b[0]**2+b[1]**2, c[0]**2+c[1]**2
    ux = (sa*(b[1]-c[1]) + sb*(c[1]-a[1]) + sc*(a[1]-b[1])) / d
    uy = (sa*(c[0]-b[0]) + sb*(a[0]-c[0]) + sc*(b[0]-a[0])) / d
    return ux, uy
```

**Triangle toolbox** (from the "Triangle Basics" slide):

- Pythagoras: `a² + b² = h²`.
- `sinθ = opp/hyp`, `cosθ = adj/hyp`, `tanθ = opp/adj`.
- Law of sines: `a/sinα = b/sinβ = c/sinγ`.
- Law of cosines: `c² = a² + b² − 2ab·cosγ`.
- Law of tangents also appears on the slide. It is rarely needed.

---

## 5. Circles

- Circle with center `(a, b)` and radius `r`: all `(x, y)` with `(x−a)² + (y−b)² = r²`.
- Circumference `2πr`, area `πr²`. Diameter `2r`.
- Parts named in the slide: chord, arc, sector, segment.

**Point vs circle** (use d², never sqrt):

```python
def pt_vs_circle(p, c, r):
    """p: point, c: center point, r: radius (number) -> 'inside' | 'on' | 'outside'. Exact for ints;
    for float inputs replace == with abs(d2 - r*r) < EPS."""
    d2 = dist2(p, c)
    return 'inside' if d2 < r*r else ('on' if d2 == r*r else 'outside')   # ints; for floats use EPS
```

**Circles through two points with a given radius** (for the Mosquitoes problem, zero, one, or two solutions):

```python
def circles_through(p, q, r):
    """p, q: two points, r: radius (NOT diameter) -> list of 0, 1 or 2 float centers of circles of radius r passing
    through both p and q. Empty if p == q or the points are more than 2r apart."""
    mx, my = (p[0]+q[0])/2, (p[1]+q[1])/2
    dx, dy = q[0]-p[0], q[1]-p[1]
    d2 = dx*dx + dy*dy
    h2 = r*r - d2/4                     # (distance from midpoint to center)^2
    if h2 < -EPS or d2 == 0: return []  # too far apart, or same point
    h = sqrt(max(h2, 0)); L = sqrt(d2)
    ux, uy = -dy/L, dx/L                # unit normal to pq
    return [(mx + ux*h, my + uy*h), (mx - ux*h, my - uy*h)]   # one entry repeated if h == 0
```

**Circle–circle intersection (extra).**

- Let `d` be the distance between centers.
- No intersection if `d > r0 + r1` or `d < |r0 − r1|`.
- Tangent if `d == r0 + r1` or `d == |r0 − r1|`.
- Otherwise there are two points.

---

## 6. Polygons

**Representation.** A list of vertices in CW or CCW order. A *simple* polygon has no self-intersections. A *convex* polygon is a simple polygon where every line segment between two interior points stays inside it.

### 6.1 Signed area (shoelace formula)

```python
def area2(P):                           # twice the signed area, an exact int for int coordinates
    """P: polygon (list of points, no repeated last vertex) -> TWICE the signed area (an int for int points).
    Positive for CCW order, negative for CW. Real area = abs(area2(P)) / 2. Works for concave simple polygons."""
    n = len(P)
    return sum(P[i][0]*P[(i+1) % n][1] - P[(i+1) % n][0]*P[i][1] for i in range(n))
# area = abs(area2(P)) / 2
```

- **`area2 > 0` means CCW, `< 0` means CW.** This is the slide's "fun fact" for finding orientation.
- Why it works with concave polygons: fix a start point and sum the triangle areas (as cross products) of every adjacent pair. Area counted outside the polygon is subtracted again, thanks to the sign.
- Print `abs(area2(P)) / 2` (half-integers are exact: use `/2` or print `.1f`).
- This also solves the opening **quadrilateral area** problem for any simple quadrilateral, including the concave "hard case". Don't use base×height formulas. Trapezoid/kite/rhombus special cases are not needed.

### 6.2 Convexity test

A polygon is convex iff all turns have the same direction (all CW or all CCW). Zero turns mean collinear points.

```python
def is_convex(P):
    """P: polygon -> True if all non-zero turns go the same direction (collinear vertices are ignored).
    Does not check that P is simple."""
    n = len(P); s = set()
    for i in range(n):
        c = sgn(cross(P[i], P[(i+1) % n], P[(i+2) % n]))
        if c: s.add(c)
    return len(s) <= 1
```

(This checks turn directions only. A self-intersecting star can pass the turn test, so also require it to be simple if the problem allows non-simple input.)

### 6.3 Point on segment (needed for boundary cases)

```python
def on_seg(p, a, b):
    """p: point, a, b: segment endpoints -> True if p lies on the CLOSED segment ab (endpoints included). Exact for ints."""
    return cross(a, b, p) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) \
                               and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])
```

### 6.4 Point in polygon

**(a) Convex polygon, area method** (slide): the sum of the areas of the triangles (point, `P[i]`, `P[i+1]`) equals the polygon's area iff the point is inside or on the boundary. In integers: `sum(abs(cross(p, P[i], P[i+1]))) == abs(area2(P))`. This is O(n) and exact. It fails for concave polygons.

**(b) Convex polygon, ccw method.** For CCW order, the point is inside iff `cross(P[i], P[i+1], p) >= 0` for every edge (strict `> 0` excludes the boundary). With CW order, flip the signs. A binary search version exists for O(log n).

**(c) Any simple polygon: even-odd (ray casting) rule** (slide). Shoot a ray from the point. An odd number of boundary crossings means inside, even means outside. It does not matter which ray you pick. The edge cases are the "evil test cases": the ray hits a vertex, runs along an edge, or the point is on the boundary. The standard fix is to treat each edge as half-open (`a.y > p.y) != (b.y > p.y)`) so vertices are counted exactly once, and to test boundary points first.

```python
def point_in_polygon(p, P):
    """p: point, P: simple polygon (convex or concave, either orientation) -> 1 strictly inside, 0 on the boundary, -1 outside.
    Exact for int coordinates."""
    n = len(P); inside = False
    for i in range(n):
        a, b = P[i], P[(i+1) % n]
        if on_seg(p, a, b): return 0
        if (a[1] > p[1]) != (b[1] > p[1]):                 # edge straddles the horizontal line through p
            # p is to the left of the edge, as seen going upward, <=> the crossing is to the right of p
            if (cross(a, b, p) > 0) == (b[1] > a[1]): inside = not inside
    return 1 if inside else -1
```

**(d) Winding number / angle sum** (L16 slide): define `θ(p, a, b)` as the signed angle between `a−p` and `b−p`. Then `p` is inside `P = {q1..qk}` iff `Σ θ(p, q_i, q_{i+1}) = 2π` (left turns add, right turns subtract; the sum is 0 when outside). It works for convex and concave polygons.

```python
def winding_inside(p, P):          # floats! use a tolerance; handle on-boundary separately
    """p: point, P: simple polygon -> True if the signed angles sum to about 2*pi. Float-based; boundary points are
    ambiguous, so test on_seg first if the boundary matters."""
    s = 0.0; n = len(P)
    for i in range(n):
        u = sub(P[i], p); v = sub(P[(i+1) % n], p)
        s += atan2(cross2(u, v), dot(u, v))
    return abs(s) > pi             # |sum| is ~2*pi inside, ~0 outside
```

Use (c) when you want exactness and (d) only if you prefer the angle idea. (d) is O(n) but uses trig and floats.

---

## 7. Segment intersection

Given segments `AB` and `CD`. Notation: `ccw(A,B,C) = cross(A,B,C)`.

**Proper intersection** means they meet at a single point strictly inside both segments (a real crossing). Idea: from AB's point of view, C and D must be on opposite sides, and from CD's point of view A and B must also be on opposite sides:

```
ccw(A,B,C) * ccw(A,B,D) < 0   and   ccw(C,D,A) * ccw(C,D,B) < 0
```

(Use the product of the `sgn()`s to avoid overflow in C++. In Python you can multiply the raw values.)

```python
def proper_intersect(a, b, c, d):
    """a, b: endpoints of segment 1; c, d: endpoints of segment 2 -> True only for a genuine crossing strictly inside
    both segments. Touching endpoints and collinear overlaps return False."""
    return sgn(cross(a, b, c)) * sgn(cross(a, b, d)) < 0 and \
           sgn(cross(c, d, a)) * sgn(cross(c, d, b)) < 0
```

**Non-proper cases** (the slide: "very careful implementation is required"):

- A segment endpoint touches the other segment (T-junction or shared endpoint). One of the four ccw values is 0 **and** the point lies within the other segment's bounding box.
- All four ccw values are 0: the segments are **collinear**. They overlap iff their projections (intervals) overlap, i.e. the 1D check below. There are four overlap types in the slide, but they all reduce to an interval-overlap test.

```python
def seg_intersect(a, b, c, d):          # True if they share at least one point (touching counts)
    """a, b: segment 1 endpoints; c, d: segment 2 endpoints -> True if the segments share at least one point
    (proper crossings, endpoint touches and collinear overlaps all count)."""
    if proper_intersect(a, b, c, d): return True
    return on_seg(c, a, b) or on_seg(d, a, b) or on_seg(a, c, d) or on_seg(b, c, d)
```

The last line covers endpoint touches and collinear overlaps, because overlapping collinear segments always have at least one endpoint lying on the other segment.

**Intersection point of two segments.** After a proper intersection test, intersect the induced lines:

```python
def seg_inter_point(a, b, c, d):        # assumes the segments properly intersect
    """a, b / c, d: endpoints of two segments that PROPERLY intersect -> (x, y) float intersection point.
    Undefined (division by zero) if they are parallel, so test proper_intersect first."""
    r = sub(b, a); s = sub(d, c)
    t = cross2(sub(c, a), s) / cross2(r, s)
    return (a[0] + t*r[0], a[1] + t*r[1])
```

**Collinear interval overlap (1D)**: `max(lo1, lo2) <= min(hi1, hi2)`.

---

## 8. Convex hull

Smallest convex polygon containing all points ("elastic band"). The lecture's first idea assumed no three collinear points.

**Naive O(n³)**: `AB` is a hull edge iff `ccw(A,B,C)` has the same sign for every other point `C`. Record those edges, then walk them to recover the hull.

### Graham scan (slide, O(n log n))

1. The leftmost (lowest-x, then lowest-y) point `p0` must be on the hull. Make it the origin.
2. Sort the other points by angle around `p0`. The slide sorts by increasing `y/x` (angle).
3. Keep a stack `S = [p0]`. For each point `p` in order, **pop while the last two stack points and `p` do not make a left turn**: `while len(S) >= 2 and ccw(S[-2], S[-1], p) <= 0: S.pop()`. Then push `p`.
4. `S` is the hull in CCW order.

The slide's pseudocode divides by `x` (`p[1]/p[0]`). That breaks for points directly above `p0` (x = 0) and gives no tie-break for collinear points. Sort with the cross product instead (below). The slide's `<= 0` in the `while` drops collinear points on the hull boundary; use `< 0` to keep them.

```python
from functools import cmp_to_key

def graham(pts):
    """pts: list of points -> hull vertices in CCW order starting from the leftmost-lowest point. Collinear boundary
    points are dropped (change <= 0 to < 0 to keep them). Duplicates are removed first."""
    pts = list(set(pts))
    if len(pts) < 3: return sorted(pts)
    p0 = min(pts)                                   # leftmost, then lowest
    rest = [p for p in pts if p != p0]
    def cmp(a, b):
        c = cross(p0, a, b)
        if c: return -1 if c > 0 else 1             # smaller polar angle first
        return dist2(a, p0) - dist2(b, p0)          # collinear: closer first
    rest.sort(key=cmp_to_key(cmp))
    S = [p0]
    for p in rest:
        while len(S) >= 2 and cross(S[-2], S[-1], p) <= 0: S.pop()
        S.append(p)
    return S                                        # CCW hull, collinear boundary points removed
```

### Andrew's monotone chain (O(n log n), the easiest to get right, recommended)

```python
def convex_hull(pts):
    """pts: list of (x, y) tuples (ints or floats) -> hull vertices in CCW order, starting at the smallest (x, y).
    Collinear boundary points are dropped (use < 0 in both loops to keep them). Returns sorted unique points if
    fewer than 3 distinct points. Does not modify pts."""
    pts = sorted(set(pts))
    if len(pts) <= 2: return pts
    lo = []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    up = []
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]                        # CCW, starts at the lowest-x point
```

- Use `< 0` instead of `<= 0` in both loops to **keep collinear boundary points** (watch out for all-collinear input, which then gives duplicates).
- Hull size 1 or 2 (all points equal or collinear) needs special handling in many problems. Check what the problem asks.
- The hull perimeter is `sum(dist(h[i], h[(i+1) % len(h)]))`. The hull area is `abs(area2(h))/2`.

### Using the hull

- **Farthest pair of points** (the slide's *Robert Hood*): the farthest pair always consists of hull vertices. Compute the hull, then check all pairs on it. With `|x|,|y| ≤ 1000` the hull has at most ~4000 points, so O(h²) is fine. With a larger hull, use rotating calipers (O(h)).
- Smallest enclosing shapes, "is this point inside all points' hull", and similar problems usually start with the hull.

```python
def farthest_pair_d2(pts):
    """pts: list of points -> SQUARED distance of the farthest pair (take sqrt when printing). O(h^2) on the hull size."""
    h = convex_hull(pts)
    return max(dist2(a, b) for a in h for b in h)    # O(h^2)
```

---

## 9. Sweep line

**Idea.** Sweep a line across the plane while maintaining a data structure for what the line currently cuts. You only update at *interesting points* (events). Decide what the events are, sort them in sweep order, and process them one by one. This turns an infinite or continuous search space into a finite one. Graham scan is a radial sweep.

**General recipe**

1. Choose the events (rectangle left/right edges, points sorted by x, segment endpoints).
2. Sort events (careful with ties: decide whether inserts or removals happen first at equal coordinates).
3. Keep an active set (ordered by y, or a counter array).
4. At each event, update the active set and the answer.

### 9.1 Area of the union of rectangles (slide)

Events: left edge means insert, right edge means remove. Between two consecutive event x-values, the area added is `(covered length of y in the active set) × (Δx)`. Finding the union length of the active segments is the hard part. With coordinate compression and a count array it is O(n²) overall, which is fine for small n (a segment tree with a covered-length counter gives O(n log n)).

```python
def union_area(rects):                 # rects: (x1, y1, x2, y2), x1<x2, y1<y2
    """rects: list of (x1, y1, x2, y2) axis-aligned rectangles with x1 < x2, y1 < y2 -> total area covered by their
    union (overlaps counted once). O(n^2); fine for small n."""
    ev = []
    for x1, y1, x2, y2 in rects:
        ev.append((x1, 1, y1, y2)); ev.append((x2, -1, y1, y2))
    ev.sort()
    ys = sorted({y for r in rects for y in (r[1], r[3])})
    idx = {y: i for i, y in enumerate(ys)}
    cnt = [0] * (len(ys) - 1)          # cnt[i] = how many rectangles cover slab [ys[i], ys[i+1]]
    area = 0; prev = ev[0][0]
    for x, t, y1, y2 in ev:
        covered = sum(ys[i+1] - ys[i] for i in range(len(cnt)) if cnt[i] > 0)
        area += covered * (x - prev); prev = x
        for i in range(idx[y1], idx[y2]): cnt[i] += t
    return area
```

### 9.2 Closest pair of points in O(n log n) (slide)

**Sweep version (slide).**

- Sort points by x and sweep left to right.
- Keep `d`, the best distance so far, and an ordered set `D` (sorted by y) of the points within `d` to the left of the sweep line.
- At each new point `p`:
  1. Remove points more than `d` to the left from `D`.
  2. Look only at points in `D` with y within `[p.y − d, p.y + d]`. All points in that box are at least `d` apart from each other, so there are **at most 6** (a `d × 2d` rectangle holds at most six points that are pairwise ≥ d apart).
  3. Update `d` if a closer pair is found.
  4. Insert `p` into `D`.
- Python has no built-in ordered set. Use the divide-and-conquer version below, or keep a sorted list with `bisect` (insertion is O(n), usually fine).

**Divide and conquer version (same complexity, plain Python, tested).** Returns the **squared** distance of the closest pair:

```python
def closest_pair_d2(pts):
    """pts: list of at least 2 points -> SQUARED distance between the closest pair (0 if there are duplicates).
    Take sqrt yourself if you need the actual distance; recover the pair by tracking it alongside d."""
    pts = sorted(pts)                              # by x, then y
    def rec(l, r):
        if r - l <= 3:
            return min(dist2(pts[i], pts[j]) for i in range(l, r) for j in range(i+1, r))
        m = (l + r) // 2; mx = pts[m][0]
        d = min(rec(l, m), rec(m, r))
        strip = sorted((p for p in pts[l:r] if (p[0]-mx)**2 < d), key=lambda p: p[1])
        for i in range(len(strip)):
            for j in range(i+1, len(strip)):
                if (strip[j][1] - strip[i][1])**2 >= d: break      # at most ~6 iterations
                d = min(d, dist2(strip[i], strip[j]))
        return d
    return rec(0, len(pts))                        # needs >= 2 points; duplicates give 0
```

For large n you may hit Python's recursion limit or be slow. Only recursion depth `log n` is used here, so recursion is fine. Raise `sys.setrecursionlimit` only if you rewrite it more deeply.

### 9.3 Horizontal / vertical segment intersections (slide)

Report (or count) all intersections among horizontal and vertical segments. There are three event types: **start of a horizontal segment**, **end of a horizontal segment**, **a vertical segment**. The active set holds the y-values of the horizontal segments currently cut by the sweep line, sorted by y. For a vertical segment `x, [y1, y2]`, count or report the active horizontals with `y1 ≤ y ≤ y2`.

```python
from bisect import insort, bisect_left, bisect_right

def hv_intersections(H, V):                       # H: (y, x1, x2) with x1<=x2;  V: (x, y1, y2) with y1<=y2
    """H: list of horizontal segments (y, x1, x2) with x1 <= x2; V: list of vertical segments (x, y1, y2) with y1 <= y2
    -> number of (horizontal, vertical) pairs that intersect (touching counts)."""
    ev = []
    for y, x1, x2 in H: ev += [(x1, 0, y), (x2, 2, y)]    # 0 = add, 2 = remove (after queries at the same x)
    for x, y1, y2 in V: ev.append((x, 1, y1, y2))         # 1 = vertical query
    ev.sort()
    active, res = [], 0
    for e in ev:
        if e[1] == 0:   insort(active, e[2])
        elif e[1] == 2: active.pop(bisect_left(active, e[2]))
        else:           res += bisect_right(active, e[3]) - bisect_left(active, e[2])
    return res                                    # touching (endpoint) intersections are counted
```

(`insort` and `pop` on a list are O(n), so O(n²) worst case. Use a Fenwick tree over compressed y for a true O(n log n). The sorting of event types makes adds happen before queries and removals after, so touching intersections count.)

### 9.4 Lines in the plane (L16 "Planar Geo" break)

- `n` lines divide the plane into at most **`n(n+1)/2 + 1`** regions (all pairs intersect, no three through one point).
- To count regions: start with 1 region and add lines one at a time. The `k`-th line adds `(number of distinct intersection points it has with earlier lines) + 1` new regions. Parallel lines or concurrent lines reduce the count.

---

## 10. Kattis problems from the slides

**Completing the Square** (`completingthesquare`). Given three corners `p`, `q`, `0` of a square where the right angle is at the origin (isosceles right triangle): the fourth corner is `p + q`. In general, if the right angle is at corner `B` with neighbors `A` and `C`, then the fourth corner is `A + C − B`. First find which vertex has the right angle: it is the one where `dot(u, v) == 0` for the two edges leaving it.

```python
def fourth_corner(a, b, c):                      # one of the three is the right-angle corner
    """a, b, c: three corners of a square (the right angle is at one of them) -> the fourth corner as an (x, y) tuple."""
    for o, u, w in ((a, b, c), (b, a, c), (c, a, b)):
        if dot(sub(u, o), sub(w, o)) == 0:
            return (u[0] + w[0] - o[0], u[1] + w[1] - o[1])
```

**Mosquitoes** (`mosquitoes`; bowl of diameter `d`, `n ≤ 32` points, maximize the number covered, points on the edge count).

- Infinitely many bowl positions, but any optimal bowl can be slid until **at least two mosquitoes are on its edge** without losing any.
- So for every pair of points, build the (zero, one, or two) circles of radius `d/2` through them (`circles_through`) and count the points with `dist2(point, center) <= r² + eps`.
- If `n == 1` (or all points coincide), the answer is `1` (or `n`).
- The statement allows the diameter to grow by up to 1e-5 without changing the answer, so use a tolerance such as `r*r*(1+1e-9) + 1e-9` or similar.
- Complexity `O(n³)` with `n ≤ 32`, which is fine.

```python
def mosquitoes(pts, d):
    """pts: list of points, d: bowl DIAMETER -> maximum number of points that fit under/on a circle of diameter d."""
    r = d / 2; best = 1
    for i in range(len(pts)):
        for j in range(i+1, len(pts)):
            for c in circles_through(pts[i], pts[j], r):
                cnt = sum(1 for p in pts if dist2(p, c) <= r*r + 1e-7)
                best = max(best, cnt)
    return best
```

**Robert Hood** (`roberthood`; `C ≤ 10⁵` integer points, `|x|,|y| ≤ 1000`, find the farthest pair). Compute the convex hull, then try all pairs of hull points (at most ~4000, O(h²)). See `farthest_pair_d2` in section 8. Print `sqrt` of the answer.

---

## 11. Edge-case checklist

- Duplicate points (`set()` them before hulls, closest pair gives 0).
- All points collinear (hull is a segment, area is 0, `circumcenter` divides by 0).
- Fewer than 3 points for hull and polygon functions.
- Zero-length segments (`pt_seg_dist`, intersections).
- Segments that only touch at an endpoint vs cross properly. Decide which one the problem wants.
- Collinear overlapping segments (all four `cross` values are 0).
- Point exactly on a polygon edge or at a vertex. Ray casting needs the half-open `(a.y > p.y) != (b.y > p.y)` rule.
- Polygon given CW vs CCW. Take `abs()` of the area, and fix orientation if you need a specific one.
- Concave polygons: base×height or convex-only tests do not apply. Use the shoelace formula and ray casting.
- Float comparisons use `EPS`. Compare squared distances. Avoid `acos` outside `[-1, 1]` (clamp: `acos(max(-1, min(1, x)))`).
- Vertical and horizontal lines when using slope. Use `ax+by+c` instead.
- Output formatting: print with enough digits (`print(f"{ans:.6f}")`), and avoid printing `-0.000000` (add `+ 0.0` or check `abs(ans) < 1e-12`).

---

## Quick function index

| Need | Use |
|---|---|
| Turn direction / side of a line | `cross(A,B,C)` sign |
| Triangle or polygon area | `abs(area2(P))/2` |
| Polygon orientation | sign of `area2(P)` |
| Convex test | `is_convex(P)` |
| Point in convex polygon | ccw on all edges, or area sum |
| Point in any polygon | `point_in_polygon` (even-odd) |
| Segments cross / touch | `proper_intersect` / `seg_intersect` |
| Line-line intersection | `line_inter` |
| Distance point to line / segment | `pt_line_dist` / `pt_seg_dist` |
| Circle through 2 points, radius r | `circles_through` |
| Circle through 3 points | `circumcenter` + `R = abc/(4A)` |
| Convex hull | `convex_hull` (monotone chain) or `graham` |
| Farthest pair | hull, then all pairs |
| Closest pair | `closest_pair_d2` |
| Union of rectangles | `union_area` |
| H/V segment intersections | `hv_intersections` |
## Worked problem: Completing the Square

**Task:** three corners of a square are given (in any order); output the fourth.

**Math**

1. Three corners of a square form an isosceles right triangle. The right angle is at the corner `A` that sits between the other two points `B` and `C`.
2. Find `A` with the dot product: `(B - A) · (C - A) == 0` means the two vectors from `A` are perpendicular. Try each of the 3 points as the candidate; exactly one passes. (Integer inputs make `== 0` exact.)
   - Alternative: the longest squared side is the hypotenuse, and `A` is the point not on it.
3. The fourth corner is where you land after walking both neighbor vectors from `A`:

```
D = A + (B - A) + (C - A) = B + C - A
```

**Check (Sample 2):** `A = (1,0)`, `B = (0,0)`, `C = (1,1)` gives `D = (0,0) + (1,1) - (1,0) = (0,1)`.

```python
import sys

pts = []
for line in sys.stdin.read().strip().splitlines():
    x, y = map(int, line.split())
    pts.append((x, y))

def vec(p, q):  return (q[0] - p[0], q[1] - p[1])
def dot(u, v):  return u[0]*v[0] + u[1]*v[1]

for i in range(3):
    A, B, C = pts[i], pts[(i+1) % 3], pts[(i+2) % 3]
    if dot(vec(A, B), vec(A, C)) == 0:
        print(A[0] + (B[0]-A[0]) + (C[0]-A[0]),
              A[1] + (B[1]-A[1]) + (C[1]-A[1]))
        break
```

## 11. Worked problem: Bounding Box

**Task:** given `n` and 3 vertices of a regular `n`-gon, find the area of the smallest axis-parallel rectangle covering all `n` vertices.

**Math, step by step**

1. **All vertices lie on one circle** (a regular polygon is cyclic). Its center `P` is the polygon's center, i.e. the **circumcenter** of the 3 given points: equidistant from each of them.
2. **Find `P`.** Set `|P-A|² = |P-B|²`. Expanding `|P|² - 2P·A + |A|² = |P|² - 2P·B + |B|²`, the `|P|²` terms cancel, leaving a linear equation:

   ```
   2(B-A)·P = |B|² - |A|²
   ```

   Do the same with `C`. Write the two equations as `a1·px + b1·py = c1` and `a2·px + b2·py = c2`:

   ```
   a1 = 2(Bx-Ax)   b1 = 2(By-Ay)   c1 = Bx²+By² - Ax²-Ay²
   a2 = 2(Cx-Ax)   b2 = 2(Cy-Ay)   c2 = Cx²+Cy² - Ax²-Ay²
   ```

   Cramer's rule (a 2x2 determinant):

   ```
   D  = a1*b2 - a2*b1          # nonzero because the points aren't collinear
   px = (c1*b2 - c2*b1) / D
   py = (a1*c2 - a2*c1) / D
   ```

3. **Radius and starting angle** from vertex `A`: `r = |A - P|`, `θ = atan2(Ay - py, Ax - px)`.
4. **Generate all vertices.** Neighbors are `2π/n` apart around the circle (hexagon: 60°). Vertex `k`:

   ```
   (px + r·cos(θ + 2πk/n),  py + r·sin(θ + 2πk/n))     for k = 0 .. n-1
   ```

   Equivalent to rotating `A - P` by `2πk/n` (rotation matrix, section 8) and adding `P` back. The other two given points are produced automatically, so you never need to identify them.
5. **Bounding box.** The smallest axis-parallel rectangle runs from the smallest to largest `x` and `y` over all vertices:

   ```
   area = (max_x - min_x) * (max_y - min_y)
   ```

**Checks**

- Sample 1: points (10,0), (0,-10), (-10,0) give `P = (0,0)`, `r = 10`; with `n = 4` the vertices are (±10,0), (0,±10), so the box is 20 × 20 = **400**
- Sample 2 (`n = 6`) should print `1056.1719423660`
- Input ends with `n = 0`; read floats; print with ~10 decimals; answer needs absolute or relative error ≤ 1e-9
- `atan2`, `cos`, `sin` use radians; `2π = 2 * math.pi`

## 12. Trig and triangle reference

| Item | Formula |
|---|---|
| Pythagoras | `a² + b² = h²` |
| Trig ratios | `sin θ = opp/hyp`, `cos θ = adj/hyp`, `tan θ = opp/adj` |
| Law of sines | `a/sin α = b/sin β = c/sin γ` |
| Law of cosines | `c² = a² + b² - 2ab·cos γ` |
| Triangle area | `½·b·h`, or `½·\|u × v\|`, or Heron's formula |
| Circumradius | `R = abc / (4A)` |
| Inradius | `r = A / s`, `s = (a+b+c)/2` |
| Arc / sector (angle θ in radians) | arc length `r·θ`, sector area `½·r²·θ` |
| Inside / on / outside a circle | compare `d²` with `r²` (exact, no `sqrt`) |

**Bounding-box trick for any point set:** take min and max of `x` and `y` separately; no need to find "extreme points" as pairs.

## 13. Practical tips

- Use **integers** when you can; floats are inexact, so compare with a small epsilon (e.g. `1e-9`)
- Compare **squared** distances to avoid `sqrt`
- Treat vertical lines (infinite slope) separately, or use `ax + by + c = 0` form
- Wrap vertex indices with `% n` to close the polygon
- Check collinear, duplicate-point, and endpoint-touching cases explicitly
- Print floats with plenty of decimals, e.g. `f"{x:.10f}"`