# Computational Geometry Cheat Sheet (COMP 321, L15 + L16): Python

Contents: 0 Rules · 1 Primitives · 2 Dot/cross · 3 Lines · 4 Triangles · 5 Circles · 6 Polygons · 7 Segment intersection · 8 Convex hull · 9 Sweep line · 10 Kattis worked problems · 11 Edge cases · Index

Points are tuples `(x, y)`; use **ints whenever the input is integer**. All code was run against brute-force checks or the Kattis samples.

---

## 0. Rules of thumb

- **Stay in integers** for ccw/cross/dot/area/dist². Python ints don't overflow, so the slides' "multiply `sgn()`s" trick is unnecessary (but harmless).
- **Compare `dist²`, not `dist`** (circle in/out tests). Call `sqrt` only at the end.
- **Floats are inexact.** Compare with `abs(a-b) < 1e-9`. Go to floats only when you must (rotation, intersection points, circumcenters).
- Use `math.pi` (or `2*acos(0)`), never `3.14159`. Trig functions take radians.
- Vertical lines have infinite slope: avoid `y = mx + c`. Use `ax + by + c = 0` or two points / point + direction.
- Polygons: vertices in order (CW or CCW), first vertex **not** repeated at the end here (the slides repeat it); wrap indices with `% n`.
- Geometry is mostly edge cases (section 11).
- Fast input: `import sys; input = sys.stdin.readline`, or `sys.stdin.read().split()`.
- Print with plenty of decimals, e.g. `f"{x:.10f}"`.

---

## 1. Primitives

```python
from math import sqrt, hypot, atan2, sin, cos, acos, pi
EPS = 1e-9

# point = (x, y); vector = (dx, dy) (same shape); the vector a -> b is sub(b, a)
# polygon = list of points in order, first vertex NOT repeated

def sgn(x):
    """number -> -1, 0 or 1."""
    return (x > 0) - (x < 0)

def add(a, b):
    """vectors -> a + b."""
    return (a[0]+b[0], a[1]+b[1])

def sub(a, b):
    """points -> vector a - b. The vector FROM a TO b is sub(b, a)."""
    return (a[0]-b[0], a[1]-b[1])

def mul(a, k):
    """vector, scalar -> vector scaled by k."""
    return (a[0]*k, a[1]*k)

def dot(a, b):
    """vectors -> a.x*b.x + a.y*b.y (int in, int out). >0 acute, 0 perpendicular, <0 obtuse."""
    return a[0]*b[0] + a[1]*b[1]

def cross2(a, b):
    """VECTORS -> a.x*b.y - a.y*b.x (signed parallelogram area). >0 means b is CCW from a."""
    return a[0]*b[1] - a[1]*b[0]

def cross(o, a, b):
    """POINTS -> (a-o) x (b-o) = the slides' ccw(o,a,b). >0 left turn o->a->b, <0 right turn, 0 collinear.
    Three points, NOT two vectors (use cross2 for that)."""
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

def dist2(a, b=(0, 0)):
    """points (b defaults to origin, so dist2(v) is the squared norm of v) -> squared distance. Exact for ints."""
    return (a[0]-b[0])**2 + (a[1]-b[1])**2

def dist(a, b=(0, 0)):
    """points (b defaults to origin) -> float distance."""
    return hypot(a[0]-b[0], a[1]-b[1])

def angle(v):
    """vector -> angle to the +x axis in [-pi, pi]."""
    return atan2(v[1], v[0])

def perp(v):
    """vector -> rotated +90 degrees (CCW), same length; stays int for int input."""
    return (-v[1], v[0])

def unit(v):
    """nonzero vector -> float vector of length 1 (ZeroDivisionError on (0,0))."""
    d = hypot(*v); return (v[0]/d, v[1]/d)

def rotate(v, t):
    """vector, t in RADIANS -> v rotated CCW by t around the ORIGIN (floats). Negative t = clockwise."""
    return (v[0]*cos(t) - v[1]*sin(t), v[0]*sin(t) + v[1]*cos(t))

def rotate_about(p, c, t):
    """point, center, radians -> p rotated CCW by t around c (floats)."""
    d = rotate(sub(p, c), t); return (c[0]+d[0], c[1]+d[1])
```

**Complex-number alternative.** `complex` is a free 2D point; `abs(z)` is the norm. Floats, so inexact for large integer coordinates: prefer tuples for exact work.

```python
import cmath
p = complex(3, 4)
abs(p)                          # 5.0 (distance from origin)
p * 1j                          # rotate +90 degrees
p * cmath.exp(1j * t)           # rotate CCW by t (the slide's e^{i*theta} trick)
(a.conjugate() * b).imag        # cross(a, b)
(a.conjugate() * b).real        # dot(a, b)
```

**Vectors**

- A point `(x, y)` is the vector from the origin; its norm is `sqrt(x²+y²)`.
- The vector from A to B is `B − A`. Distance between `a`, `b` is `|b − a|` (slide: `a=(4,2), b=(3,-1)` gives `3.16228`).
- Rotation matrix (CCW by θ about the origin): `x' = x·cosθ − y·sinθ`, `y' = x·sinθ + y·cosθ`.

---

## 2. Dot and cross products

| | Formula | Algebraic | Meaning |
|---|---|---|---|
| **Dot** | `u·v = ‖u‖‖v‖cosθ` | `x0·x1 + y0·y1` | `>0` acute, `=0` perpendicular, `<0` obtuse. Projections, angles. |
| **Cross (2D scalar)** | `u×v = ‖u‖‖v‖sinθ` | `x0·y1 − y0·x1` | **Signed** parallelogram area; `½|u×v|` is the triangle area. |

**Sign of `cross(A, B, C) = (B−A) × (C−A)`** (the slides' `ccw`):

| Value | Meaning |
|---|---|
| `> 0` | C is **left** of A→B: counterclockwise (left turn) |
| `< 0` | C is **right**: clockwise (right turn) |
| `= 0` | **Collinear** |

- Signed: `a×b = −(b×a)`. Order matters, and that is the useful part.
- Triangle area `= abs(cross(A,B,C)) / 2`; keep the int `area2 = abs(cross(A,B,C))` when possible.
- Angle between vectors: `acos(dot(u,v) / (‖u‖‖v‖))`. Signed angle: `atan2(cross2(u,v), dot(u,v))`.
- Perpendicular: `dot(u,v) == 0`. Parallel: `cross2(u,v) == 0`. Collinear points: `cross(A,B,C) == 0`.
- **Algebra trick:** `cross2(v, v) = 0` and cross is linear. Crossing both sides of an equation with a vector eliminates the unknown multiple of that vector (this is how line intersection in section 3 is derived).

---

## 3. Lines

**Representations.** Slope-intercept `y = mx + c` (breaks on vertical lines); general `ax + by + c = 0` (handles all lines); two points `P1, P2` (unique, most robust); **point + direction** `p + t·d` (parametric: `t=0` is `p`, `t=1` is `p+d`).

**Line through two points → `ax + by + c = 0`** (slides: `a·x1 + b·y1 + c = 0` and `a·x2 + b·y2 + c = 0`):

```python
def line_from_pts(p, q):
    """Two distinct points -> (a, b, c) with a*x + b*y + c = 0 through both. Not normalized, so
    parallel/same-line tests must use cross-multiplication (below)."""
    a = p[1] - q[1]
    b = q[0] - p[0]
    c = -(a*p[0] + b*p[1])
    return a, b, c
```

**Comparing lines** `(a1,b1,c1)`, `(a2,b2,c2)`:

- **Parallel** iff `a1*b2 == a2*b1` (the slide's "same a and b" only holds after normalizing, so cross-multiply).
- **Same line** iff parallel and `a1*c2 == a2*c1` and `b1*c2 == b2*c1`.
- Otherwise exactly one intersection.

**Line–line intersection, `ax+by+c` form** (Cramer's rule from the slide):

```python
def line_inter(a1, b1, c1, a2, b2, c2):
    """Two lines as (a, b, c) -> (x, y) float intersection, or None if parallel/identical."""
    det = a1*b2 - a2*b1
    if det == 0: return None
    return (b1*c2 - b2*c1) / det, (c1*a2 - c2*a1) / det
```

**Line–line intersection, two points per line** (parametric; works on **infinite lines**, and also gives the point for two segments once `proper_intersect` passed):

Lines `p1 + t·r` and `q1 + u·s` with `r = p2−p1`, `s = q2−q1`. Setting them equal and crossing both sides with `s` (kills `u`) gives `t = cross2(q1−p1, s) / cross2(r, s)`.

```python
def line_inter_pts(p1, p2, q1, q2):
    """Line through p1,p2 and line through q1,q2 -> (x, y) float intersection.
    ZeroDivisionError if parallel (cross2(r, s) == 0)."""
    r, s = sub(p2, p1), sub(q2, q1)
    t = cross2(sub(q1, p1), s) / cross2(r, s)
    return (p1[0] + t*r[0], p1[1] + t*r[1])
```

**Point–line distance** (2 points `s1`, `s2` define the line). Slide views: area `½·b·d`, or projecting `p − s1` onto the perpendicular of `s2 − s1`. `d = |(p − s1) × (s2 − s1)| / |s2 − s1|`:

```python
def pt_line_dist(p, s1, s2):
    """p; s1, s2 DISTINCT points on the infinite line -> float distance (segments: pt_seg_dist)."""
    return abs(cross(s1, s2, p)) / dist(s1, s2)
```

**Side test.** `cross(s1, s2, p)`: `> 0` left, `< 0` right, `= 0` on the line.

**Closest point on a segment:**

```python
def pt_seg_dist(p, a, b):
    """p; segment a-b (a == b allowed) -> float distance from p to the closest point of the segment."""
    ab = sub(b, a); ap = sub(p, a); L = dot(ab, ab)
    if L == 0: return dist(p, a)
    t = max(0, min(1, dot(ap, ab) / L))           # clamp projection to [0, 1]
    return hypot(p[0] - a[0] - t*ab[0], p[1] - a[1] - t*ab[1])
```

---

## 4. Triangles

- Area: `½·base·height`, or `abs(cross(A,B,C))/2` (preferred). Heron: `s=(a+b+c)/2`, `Area = sqrt(s(s−a)(s−b)(s−c))`.
- **Incircle** (inside). Radius `r = Area / s`. Center = intersection of the angle bisectors:
  `I = (a·A + b·B + c·C) / (a+b+c)`, where `a = |BC|` is the side **opposite** `A` (etc.). Each vertex is weighted by its opposite side. `I` is always inside the triangle.
- **Circumcircle** (through all 3 vertices). Radius `R = abc / (4·Area)`. Center = intersection of the perpendicular bisectors.
- Pythagoras `a² + b² = h²`; `sinθ = opp/hyp`, `cosθ = adj/hyp`, `tanθ = opp/adj`.
- Law of sines `a/sinα = b/sinβ = c/sinγ`; law of cosines `c² = a² + b² − 2ab·cosγ`; law of tangents (slide, rarely needed).

```python
def incenter(A, B, C):
    """Three non-collinear points -> (x, y) float incenter."""
    a, b, c = dist(B, C), dist(C, A), dist(A, B)
    s = a + b + c
    return ((a*A[0] + b*B[0] + c*C[0]) / s, (a*A[1] + b*B[1] + c*C[1]) / s)

def circumcenter(a, b, c):
    """Three NON-collinear points -> (x, y) float center of the circle through all three.
    Radius = dist(center, a). ZeroDivisionError if collinear."""
    d = 2*(a[0]*(b[1]-c[1]) + b[0]*(c[1]-a[1]) + c[0]*(a[1]-b[1]))
    sa, sb, sc = a[0]**2+a[1]**2, b[0]**2+b[1]**2, c[0]**2+c[1]**2
    ux = (sa*(b[1]-c[1]) + sb*(c[1]-a[1]) + sc*(a[1]-b[1])) / d
    uy = (sa*(c[0]-b[0]) + sb*(a[0]-c[0]) + sc*(b[0]-a[0])) / d
    return ux, uy
```

(Careful: the parameters of `circumcenter` are points named `a, b, c`; side lengths `a, b, c` in `incenter` are different things.)

---

## 5. Circles

- Center `(a, b)`, radius `r`: all `(x, y)` with `(x−a)² + (y−b)² = r²`. Circumference `2πr`, area `πr²`, diameter `2r`.
- Arc length `r·θ`, sector area `½·r²·θ` (θ in radians). Named parts: chord, arc, sector, segment.

**Point vs circle** (use d², never sqrt):

```python
def pt_vs_circle(p, c, r):
    """point, center, radius -> 'inside' | 'on' | 'outside'. Exact for ints; for floats replace == with abs(d2 - r*r) < EPS."""
    d2 = dist2(p, c)
    return 'inside' if d2 < r*r else ('on' if d2 == r*r else 'outside')
```

**Second intersection of a line with a circle.** Point `P` is ON the circle (center `O`), the line is `X(t) = P + t·d` (e.g. `d = I − P`). On the circle iff `|P − O + t·d|² = R²`. Expand and use `|P−O|² = R²`:
`2t·d·(P−O) + t²·|d|² = 0`, i.e. `t·(2·d·(P−O) + t·|d|²) = 0`. Root `t = 0` is `P` itself; the other root is `t = −2·d·(P−O) / |d|²`.

```python
def second_hit(p, q, o):
    """p ON the circle with center o; q any other point on the line through p
    -> the line's other intersection with the circle (floats)."""
    d = sub(q, p)
    t = -2 * dot(d, sub(p, o)) / dot(d, d)
    return (p[0] + t*d[0], p[1] + t*d[1])
```

Sanity check: unit circle at the origin, `p=(1,0)`, `q=(0,0)` gives `t=2`, point `(-1, 0)` (antipode). Verify with `dist(second_hit(...), o) == dist(p, o)`.

**Circles through two points with a given radius** (Mosquitoes: zero, one, or two solutions):

```python
def circles_through(p, q, r, tol=EPS):
    """p, q; r = RADIUS (not diameter) -> list of 0, 1 or 2 float centers of radius-r circles through both.
    Empty if p == q or the points are more than 2r apart (beyond tol)."""
    mx, my = (p[0]+q[0])/2, (p[1]+q[1])/2
    dx, dy = q[0]-p[0], q[1]-p[1]
    d2 = dx*dx + dy*dy
    h2 = r*r - d2/4                     # (distance from midpoint to center)^2
    if h2 < -tol or d2 == 0: return []
    h = sqrt(max(h2, 0)); L = sqrt(d2)
    ux, uy = -dy/L, dx/L                # unit normal to pq
    return [(mx + ux*h, my + uy*h), (mx - ux*h, my - uy*h)]   # same point twice if h == 0
```

**Circle–circle intersection.** `d` = distance between centers. None if `d > r0 + r1` or `d < |r0 − r1|`; tangent if `d == r0 + r1` or `d == |r0 − r1|`; otherwise two points.

---

## 6. Polygons

A *simple* polygon has no self-intersections; a *convex* polygon keeps every segment between two interior points inside it.

### 6.1 Signed area (shoelace)

```python
def area2(P):
    """Polygon -> TWICE the signed area (exact int for int points). >0 CCW, <0 CW.
    Real area = abs(area2(P)) / 2. Works for concave simple polygons."""
    n = len(P)
    return sum(P[i][0]*P[(i+1) % n][1] - P[(i+1) % n][0]*P[i][1] for i in range(n))
```

- `area2 > 0` means CCW (the slide's fun fact for orientation).
- Why it works for concave polygons: fix a start point and sum signed triangle areas of adjacent pairs; area counted outside is subtracted by the sign.
- Half-integers print exactly with `/2` or `.1f`.
- Solves the **quadrilateral area** problem for any simple quadrilateral, including the concave hard case. No base×height special cases (trapezoid, kite, rhombus) needed.

### 6.2 Convexity test

Convex iff all turns have the same direction; zero turns are collinear points.

```python
def is_convex(P):
    """True if all non-zero turns go the same direction (collinear vertices ignored). Does NOT check simplicity:
    a self-intersecting star can pass, so also require simple if the problem allows non-simple input."""
    n = len(P); s = set()
    for i in range(n):
        c = sgn(cross(P[i], P[(i+1) % n], P[(i+2) % n]))
        if c: s.add(c)
    return len(s) <= 1
```

### 6.3 Point on segment

```python
def on_seg(p, a, b):
    """True if p lies on the CLOSED segment ab (endpoints included). Exact for ints."""
    return cross(a, b, p) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) \
                               and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])
```

### 6.4 Point in polygon

- **(a) Convex, area method** (slide): the triangles (p, `P[i]`, `P[i+1]`) sum to the polygon's area iff p is inside or on the boundary: `sum(abs(cross(p, P[i], P[i+1]))) == abs(area2(P))`. O(n), exact, convex only.
- **(b) Convex, ccw method:** for CCW order, inside iff `cross(P[i], P[i+1], p) >= 0` for every edge (strict `> 0` excludes the boundary); flip signs for CW. A binary-search version gives O(log n).
- **(c) Any simple polygon, even-odd (ray casting)** (slide): shoot any ray; odd crossings = inside. Evil cases: ray hits a vertex, runs along an edge, or p is on the boundary. Fix: treat each edge as half-open, `(a.y > p.y) != (b.y > p.y)`, so a vertex counts once, and test boundary points first.

```python
def point_in_polygon(p, P):
    """Simple polygon (convex or concave, either orientation) -> 1 strictly inside, 0 on boundary, -1 outside.
    Exact for int coordinates."""
    n = len(P); inside = False
    for i in range(n):
        a, b = P[i], P[(i+1) % n]
        if on_seg(p, a, b): return 0
        if (a[1] > p[1]) != (b[1] > p[1]):             # edge straddles the horizontal line through p
            if (cross(a, b, p) > 0) == (b[1] > a[1]): inside = not inside   # crossing is to the right of p
    return 1 if inside else -1
```

- **(d) Winding number / angle sum** (L16): `p` is inside iff `Σ θ(p, q_i, q_{i+1}) = 2π` (signed angles between `a−p` and `b−p`; left turns add, right turns subtract; 0 when outside). Works for convex and concave, but uses trig and floats: use (c) for exactness.

```python
def winding_inside(p, P):
    """Float-based; boundary points are ambiguous, so test on_seg first if the boundary matters."""
    s = 0.0; n = len(P)
    for i in range(n):
        u = sub(P[i], p); v = sub(P[(i+1) % n], p)
        s += atan2(cross2(u, v), dot(u, v))
    return abs(s) > pi             # |sum| ~ 2*pi inside, ~ 0 outside
```

---

## 7. Segment intersection

Segments `AB` and `CD`. **Proper intersection** = one point strictly inside both (a real crossing): C, D on opposite sides of AB **and** A, B on opposite sides of CD.

```python
def proper_intersect(a, b, c, d):
    """True only for a genuine crossing strictly inside both segments. Touching endpoints and collinear overlaps -> False."""
    return sgn(cross(a, b, c)) * sgn(cross(a, b, d)) < 0 and \
           sgn(cross(c, d, a)) * sgn(cross(c, d, b)) < 0

def seg_intersect(a, b, c, d):
    """True if the segments share at least one point (crossing, endpoint touch, collinear overlap)."""
    if proper_intersect(a, b, c, d): return True
    return on_seg(c, a, b) or on_seg(d, a, b) or on_seg(a, c, d) or on_seg(b, c, d)
```

**Non-proper cases** (the slide: "very careful implementation is required"): an endpoint touches the other segment (one ccw value is 0 **and** the point is within the other's bounding box), or all four ccw values are 0 (**collinear**: overlap iff the 1D intervals overlap, `max(lo1, lo2) <= min(hi1, hi2)`). Overlapping collinear segments always have an endpoint on the other, which is why `seg_intersect` covers them.

**Intersection point:** after `proper_intersect` passes, use `line_inter_pts(a, b, c, d)` from section 3.

---

## 8. Convex hull

Smallest convex polygon containing all points ("elastic band"). **Naive O(n³):** `AB` is a hull edge iff `ccw(A,B,C)` has the same sign for every other `C`; collect edges and walk them (assumes no three collinear).

### Andrew's monotone chain (O(n log n), easiest, recommended)

```python
def convex_hull(pts):
    """List of (x, y) -> hull vertices CCW starting at the smallest (x, y). Collinear boundary points dropped
    (use < 0 in both loops to keep them; all-collinear input then gives duplicates). < 3 distinct points -> sorted unique points."""
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
    return lo[:-1] + up[:-1]
```

### Graham scan (slide, O(n log n))

1. Leftmost (lowest-x, then lowest-y) point `p0` is on the hull; make it the origin.
2. Sort the others by angle around `p0` (the slide sorts by increasing `y/x`).
3. Stack `S = [p0]`; for each `p` pop while the last two and `p` are not a left turn (`ccw(S[-2], S[-1], p) <= 0`), then push `p`.
4. `S` is the hull in CCW order.

```python
from functools import cmp_to_key

def graham(pts):
    """List of points -> hull CCW from the leftmost-lowest point; collinear boundary points dropped; duplicates removed."""
    pts = list(set(pts))
    if len(pts) < 3: return sorted(pts)
    p0 = min(pts)
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
    return S
```

### Using the hull

- Perimeter `sum(dist(h[i], h[(i+1) % len(h)]))`; area `abs(area2(h))/2`. Hull of size 1 or 2 (all equal or collinear) needs special handling in many problems.
- **Farthest pair** (slide *Robert Hood*): always two hull vertices. With `|x|,|y| ≤ 1000` the hull has at most ~4000 points, so O(h²) is fine (larger: rotating calipers, O(h)).
- Smallest enclosing shapes and "inside the hull of all points" problems usually start with the hull.

```python
def farthest_pair_d2(pts):
    """List of points -> SQUARED distance of the farthest pair (sqrt when printing). O(h^2) on the hull size."""
    h = convex_hull(pts)
    return max(dist2(a, b) for a in h for b in h)
```

---

## 9. Sweep line

**Idea.** Sweep a line across the plane, keeping a structure for what it currently cuts; update only at *events*. Decide the events, sort them in sweep order, process one by one: this turns a continuous search space into a finite one. (Graham scan is a radial sweep.)

**Recipe:** 1) choose events (rectangle left/right edges, points by x, segment endpoints); 2) sort, deciding whether inserts or removals go first on ties; 3) keep an active set (ordered by y, or a counter array); 4) update the set and the answer at each event.

### 9.1 Area of the union of rectangles (slide)

Left edge = insert, right edge = remove. Between consecutive event x-values add `(covered y-length) × Δx`. Coordinate compression with a count array is O(n²) (fine for small n); a segment tree with a covered-length counter gives O(n log n).

```python
def union_area(rects):                 # rects: (x1, y1, x2, y2), x1<x2, y1<y2
    """Total area covered by the union (overlaps counted once). O(n^2)."""
    ev = []
    for x1, y1, x2, y2 in rects:
        ev.append((x1, 1, y1, y2)); ev.append((x2, -1, y1, y2))
    ev.sort()
    ys = sorted({y for r in rects for y in (r[1], r[3])})
    idx = {y: i for i, y in enumerate(ys)}
    cnt = [0] * (len(ys) - 1)          # cnt[i] = rectangles covering slab [ys[i], ys[i+1]]
    area = 0; prev = ev[0][0]
    for x, t, y1, y2 in ev:
        covered = sum(ys[i+1] - ys[i] for i in range(len(cnt)) if cnt[i] > 0)
        area += covered * (x - prev); prev = x
        for i in range(idx[y1], idx[y2]): cnt[i] += t
    return area
```

### 9.2 Closest pair in O(n log n) (slide)

**Sweep version.** Sort by x, sweep left to right. Keep `d` (best so far) and an ordered set `D` (by y) of points within `d` to the left. For each new `p`: (1) drop points more than `d` to the left; (2) check only points in `D` with y in `[p.y − d, p.y + d]`, at most **6** (a `d × 2d` box holds at most six points pairwise ≥ d apart); (3) update `d`; (4) insert `p`. Python has no ordered set: use the divide-and-conquer version, or a `bisect` sorted list (O(n) insertion, usually fine).

```python
def closest_pair_d2(pts):
    """List of >= 2 points -> SQUARED distance of the closest pair (0 with duplicates). Track the pair alongside d if needed."""
    pts = sorted(pts)                              # by x, then y
    def rec(l, r):
        if r - l <= 3:
            return min(dist2(pts[i], pts[j]) for i in range(l, r) for j in range(i+1, r))
        m = (l + r) // 2; mx = pts[m][0]
        d = min(rec(l, m), rec(m, r))
        strip = sorted((p for p in pts[l:r] if (p[0]-mx)**2 < d), key=lambda p: p[1])
        for i in range(len(strip)):
            for j in range(i+1, len(strip)):
                if (strip[j][1] - strip[i][1])**2 >= d: break      # ~6 iterations at most
                d = min(d, dist2(strip[i], strip[j]))
        return d
    return rec(0, len(pts))
```

Recursion depth is only `log n`, so no recursion-limit problem.

### 9.3 Horizontal / vertical segment intersections (slide)

Events: **start of a horizontal**, **end of a horizontal**, **a vertical**. The active set holds the y-values of horizontals currently cut, sorted. For a vertical `x, [y1, y2]` count or report active `y` with `y1 ≤ y ≤ y2`. Adds happen before queries and removals after, so touching counts.

```python
from bisect import insort, bisect_left, bisect_right

def hv_intersections(H, V):         # H: (y, x1, x2) with x1<=x2;  V: (x, y1, y2) with y1<=y2
    """Number of (horizontal, vertical) pairs that intersect (touching counts)."""
    ev = []
    for y, x1, x2 in H: ev += [(x1, 0, y), (x2, 2, y)]    # 0 = add, 2 = remove (after queries at the same x)
    for x, y1, y2 in V: ev.append((x, 1, y1, y2))         # 1 = vertical query
    ev.sort()
    active, res = [], 0
    for e in ev:
        if e[1] == 0:   insort(active, e[2])
        elif e[1] == 2: active.pop(bisect_left(active, e[2]))
        else:           res += bisect_right(active, e[3]) - bisect_left(active, e[2])
    return res
```

(`insort`/`pop` on a list are O(n), so O(n²) worst case; use a Fenwick tree over compressed y for true O(n log n).)

### 9.4 Lines in the plane (L16 "Planar Geo" break)

`n` lines divide the plane into at most **`n(n+1)/2 + 1`** regions (all pairs intersect, no three concurrent). To count: start with 1 region and add lines one by one; the `k`-th line adds `(distinct intersection points with earlier lines) + 1` regions. Parallel or concurrent lines reduce the count.

---

## 10. Kattis worked problems

### Completing the Square (`completingthesquare`)

Three corners of a square (any order); output the fourth.

1. The three corners form an isosceles right triangle; the right angle is at the corner `A` between the other two (`B`, `C`).
2. Find `A`: `dot(B − A, C − A) == 0` (exact for ints); try each of the 3 points, exactly one passes. (Alternative: the longest squared side is the hypotenuse; `A` is the point not on it.)
3. `D = A + (B − A) + (C − A) = B + C − A`.

Check (Sample 2): `A=(1,0)`, `B=(0,0)`, `C=(1,1)` gives `D=(0,1)`.

```python
import sys
pts = [tuple(map(int, l.split())) for l in sys.stdin.read().strip().splitlines()]
for i in range(3):
    A, B, C = pts[i], pts[(i+1) % 3], pts[(i+2) % 3]
    if dot(sub(B, A), sub(C, A)) == 0:
        print(B[0] + C[0] - A[0], B[1] + C[1] - A[1])
        break
```

### Bounding Box

Given `n` and 3 vertices of a regular `n`-gon, output the area of the smallest axis-parallel rectangle covering all vertices.

1. A regular polygon is cyclic: its center `P` is the **circumcenter** of the 3 given points (`circumcenter` from section 4 returns it).
2. Derivation of `P`: `|P−A|² = |P−B|²`; the `|P|²` terms cancel, leaving the linear `2(B−A)·P = |B|² − |A|²`. Same with `C`: `a1·px + b1·py = c1`, `a2·px + b2·py = c2`, with `a1=2(Bx−Ax)`, `b1=2(By−Ay)`, `c1=Bx²+By²−Ax²−Ay²` (and likewise `a2,b2,c2` with `C`). Cramer: `D = a1*b2 − a2*b1` (nonzero: not collinear), `px = (c1*b2 − c2*b1)/D`, `py = (a1*c2 − a2*c1)/D`.
3. `r = |A − P|`, `θ = atan2(Ay − py, Ax − px)`.
4. Vertex `k = 0..n−1`: `(px + r·cos(θ + 2πk/n), py + r·sin(θ + 2πk/n))` (equivalently `rotate(A − P, 2πk/n) + P`). The other two given points appear automatically.
5. Bounding box for any point set: min and max of `x` and `y` separately; `area = (max_x − min_x)·(max_y − min_y)`.

Checks: Sample 1 `(10,0), (0,-10), (-10,0)` gives `P=(0,0)`, `r=10`, `n=4`, box 20×20 = **400**. Sample 2 (`n=6`) prints `1056.1719423660`. Input ends with `n = 0`; read floats; print ~10 decimals (tolerance 1e-9).

### Mosquitoes (`mosquitoes`)

Bowl of diameter `d`, `n ≤ 32` points, maximize the number covered (points on the edge count).

- Any optimal bowl can be slid until **at least two mosquitoes are on its edge** without losing any. So for every pair, build the (0, 1 or 2) circles of radius `d/2` through them (`circles_through`) and count points with `dist2(point, center) <= r*r + tol`. If `n == 1` the answer is `1`. O(n³), fine for `n ≤ 32`.
- The statement allows the diameter to vary by up to 1e-5 without changing the answer, so tolerances of about `1e-5` to `1e-7` are used (also pass the same `tol` to `circles_through`).

```python
import sys, itertools

def mosquitoes(n, d, points):
    if n == 1: return 1
    r = d / 2; best = 1
    for p, q in itertools.combinations(points, 2):
        for c in circles_through(p, q, r, tol=1e-5):
            cnt = sum(1 for pt in points if dist2(pt, c) <= r*r + 1e-5)
            best = max(best, cnt)
    return best

def main():
    data = sys.stdin.read().split()
    t = int(data[0]); i = 1; out = []
    for _ in range(t):
        n, d = int(data[i]), float(data[i+1]); i += 2
        points = []
        for _ in range(n):
            points.append((float(data[i]), float(data[i+1]))); i += 2
        out.append(str(mosquitoes(n, d, points)))
    print("\n".join(out))
```

### Robert Hood (`roberthood`)

`C ≤ 10⁵` integer points, `|x|,|y| ≤ 1000`, find the farthest pair: convex hull, then all hull pairs (`farthest_pair_d2`, section 8). Print `sqrt` of the answer.

### Triangle To Hexagon (`triangle2hexagon`, 2017 GNY Regional)

Input `Bx Cx Cy` with `A=(0,0)`, `B=(Bx,0)`, `C=(Cx,Cy)`. `I` = incenter. `M, N, P` = second intersections of lines `AI, BI, CI` with the circumcircle. `E,F` = `NP` ∩ `AB`, `AC`; `G,H` = `MN` ∩ `AC`, `BC`; `J,K` = `MP` ∩ `BC`, `AB`. Output `|EF|, |FG|, |GH|, |HJ|, |JK|, |KE|`.

1. `I = incenter(A, B, C)`; `O = circumcenter(A, B, C)` (the center point, not the radius).
2. `M = second_hit(A, I, O)`, `N = second_hit(B, I, O)`, `P = second_hit(C, I, O)`.
3. Six points with `line_inter_pts` (infinite lines, no segment logic needed), then six consecutive distances (wrap with `% 6`).

```python
def solve(A, B, C):
    I = incenter(A, B, C); O = circumcenter(A, B, C)
    M, N, P = second_hit(A, I, O), second_hit(B, I, O), second_hit(C, I, O)
    E = line_inter_pts(N, P, A, B); F = line_inter_pts(N, P, A, C)
    G = line_inter_pts(M, N, A, C); H = line_inter_pts(M, N, B, C)
    J = line_inter_pts(M, P, B, C); K = line_inter_pts(M, P, A, B)
    pts = [E, F, G, H, J, K]
    return [dist(pts[i], pts[(i+1) % 6]) for i in range(6)]

bx, cx, cy = map(float, input().split())
print(" ".join(f"{x:.9f}" for x in solve((0, 0), (bx, 0), (cx, cy))))
```

Sample `3 2.5 3` gives `0.999173 1.533202 0.995436 0.929975 1.185867 0.904840` (all 3 samples verified). If wrong, check `dist(M, O) ≈ dist(A, O)` for `M, N, P` first. The statement guarantees `|EF|+|GH|+|JK| ≤ |KE|+|FG|+|HJ|`, a handy self-check.

---

## 11. Edge-case checklist

- Duplicate points (`set()` before hulls; closest pair gives 0). Fewer than 3 points for hull/polygon functions.
- All points collinear (hull is a segment, area is 0, `circumcenter` divides by 0). Zero-length segments (`pt_seg_dist`, intersections).
- Segments touching at an endpoint vs crossing properly (decide which the problem wants); collinear overlaps (all four `cross` values 0).
- Point exactly on a polygon edge or vertex; ray casting needs the half-open `(a.y > p.y) != (b.y > p.y)` rule.
- Polygon CW vs CCW: take `abs()` of the area, and fix orientation if a specific one is needed.
- Concave polygons: base×height and convex-only tests don't apply; use shoelace and ray casting.
- Parallel lines: `line_inter_pts` / `line_inter` divide by zero or return `None`.
- Floats: compare with `EPS`, compare squared distances, clamp `acos` input (`acos(max(-1, min(1, x)))`).
- Vertical/horizontal lines with slope form: use `ax+by+c` or two points.
- Output: enough digits (`f"{ans:.6f}"` or more); avoid `-0.000000` (add `+ 0.0` or check `abs(ans) < 1e-12`).

---

## Quick function index

| Need | Use |
|---|---|
| Turn direction / side of a line | `cross(A,B,C)` sign |
| Triangle or polygon area | `abs(area2(P))/2` |
| Polygon orientation | sign of `area2(P)` |
| Convex test | `is_convex(P)` |
| Point in convex / any polygon | ccw on all edges or area sum / `point_in_polygon` |
| Segments cross / touch | `proper_intersect` / `seg_intersect` |
| Line-line intersection | `line_inter_pts` (2 points each) / `line_inter` (`ax+by+c`) |
| Distance point to line / segment | `pt_line_dist` / `pt_seg_dist` |
| Incenter / circumcenter | `incenter` / `circumcenter` (radius `R = abc/(4·Area)`, `r = Area/s`) |
| Line meets circle again | `second_hit` |
| Circle through 2 points, radius r | `circles_through` |
| Convex hull | `convex_hull` (monotone chain) or `graham` |
| Farthest / closest pair | hull + all pairs / `closest_pair_d2` |
| Union of rectangles | `union_area` |
| H/V segment intersections | `hv_intersections` |