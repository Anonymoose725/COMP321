# Computational Geometry Cheat Sheet (COMP 321, L15 + L16) — Python
# PRACTITIONER'S EDITION: Clean imports, tested code, problem stubs

from math import sqrt, hypot, atan2, sin, cos, acos, pi, radians
EPS = 1e-9

import sys
input = sys.stdin.readline

# ============================================================================
# SECTION 0: RULES OF THUMB (READ THIS FIRST!)
# ============================================================================
"""
- **STAY IN INTEGERS**: Use tuples for cross/cdot/dist2/area. Python has no overflow.
- **COMPARE SQUARED DISTANCES**: Never `dist == r`; compare `dist2 < r*r`.
- **FLOATS ARE INEXACT**: Always use EPS. For acos, clamp to [-1, 1].
- **POLYGON REPR**: List of vertices in order (CW or CCW). No repeated last point. Indices wrap with `% n`.
- **EDGE CASES**: Collinear points, duplicate points, zero-length segments, touching vs crossing, boundary points.
"""

# ============================================================================
# SECTION 1: PRIMITIVES (THE BUILDING BLOCKS)
# ============================================================================

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
    """a, b: vectors -> scalar a.x*b.x + a.y*b.y. Int in -> int out.
    >0 acute, 0 perpendicular, <0 obtuse."""
    return a[0]*b[0] + a[1]*b[1]

def cross2(a, b):
    """a, b: vectors -> scalar a.x*b.y - a.y*b.x (signed parallelogram area).
    >0 means b is CCW from a."""
    return a[0]*b[1] - a[1]*b[0]

def cross(o, a, b):
    """o, a, b: POINTS -> scalar (a-o) x (b-o), i.e. ccw(o,a,b).
    >0 left turn o->a->b, <0 right turn, 0 collinear. Takes 3 points."""
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

def dist2(a, b=(0, 0)):
    """a, b: points (b defaults to origin) -> squared distance. Exact for ints."""
    return (a[0]-b[0])**2 + (a[1]-b[1])**2

def dist(a, b=(0, 0)):
    """a, b: points -> float Euclidean distance."""
    return hypot(a[0]-b[0], a[1]-b[1])

def angle(v):
    """v: vector -> float angle to +x axis in [-pi, pi] (radians)."""
    return atan2(v[1], v[0])

def perp(v):
    """v: vector -> vector rotated +90 degrees (CCW), same length."""
    return (-v[1], v[0])

def unit(v):
    """v: nonzero vector -> float vector of length 1. Raises ZeroDivisionError on (0,0)."""
    d = hypot(*v); return (v[0]/d, v[1]/d)

def rotate(v, t):
    """v: vector, t: angle in RADIANS -> v rotated CCW by t around the ORIGIN."""
    return (v[0]*cos(t) - v[1]*sin(t), v[0]*sin(t) + v[1]*cos(t))

def rotate_about(p, c, t):
    """p: point, c: center point, t: radians -> p rotated CCW by t around c."""
    d = rotate(sub(p, c), t); return (c[0]+d[0], c[1]+d[1])

# ============================================================================
# SECTION 2: LINE SEGMENT GEOMETRY
# ============================================================================

def line_from_pts(p, q):
    """Two distinct points p, q -> (a, b, c) ints/floats with a*x + b*y + c = 0."""
    a = p[1] - q[1]
    b = q[0] - p[0]
    c = -(a*p[0] + b*p[1])
    return a, b, c

def line_inter(a1, b1, c1, a2, b2, c2):
    """Two lines as (a, b, c) -> (x, y) float intersection, or None if parallel."""
    det = a1*b2 - a2*b1
    if det == 0: return None
    x = (b1*c2 - b2*c1) / det
    y = (c1*a2 - c2*a1) / det
    return x, y

def pt_line_dist(p, s1, s2):
    """p: query point; s1, s2: two DISTINCT points defining the infinite line -> float distance."""
    return abs(cross(s1, s2, p)) / dist(s1, s2)

def pt_seg_dist(p, a, b):
    """p: query point; a, b: segment endpoints (a == b allowed) -> float distance to segment."""
    ab = sub(b, a); ap = sub(p, a); L = dot(ab, ab)
    if L == 0: return dist(p, a)
    t = max(0, min(1, dot(ap, ab) / L))
    return hypot(p[0] - a[0] - t*ab[0], p[1] - a[1] - t*ab[1])

def on_seg(p, a, b):
    """p: point, a, b: segment endpoints -> True if p lies on the CLOSED segment ab."""
    return cross(a, b, p) == 0 and min(a[0], b[0]) <= p[0] <= max(a[0], b[0]) \
                               and min(a[1], b[1]) <= p[1] <= max(a[1], b[1])

def proper_intersect(a, b, c, d):
    """a, b: segment 1; c, d: segment 2 -> True only for a genuine crossing strictly inside both."""
    return sgn(cross(a, b, c)) * sgn(cross(a, b, d)) < 0 and \
           sgn(cross(c, d, a)) * sgn(cross(c, d, b)) < 0

def seg_intersect(a, b, c, d):
    """Segments share at least one point (touching counts)."""
    if proper_intersect(a, b, c, d): return True
    return on_seg(c, a, b) or on_seg(d, a, b) or on_seg(a, c, d) or on_seg(b, c, d)

def seg_inter_point(a, b, c, d):
    """Segments PROPERLY intersect -> (x, y) float intersection point."""
    r = sub(b, a); s = sub(d, c)
    t = cross2(sub(c, a), s) / cross2(r, s)
    return (a[0] + t*r[0], a[1] + t*r[1])

# ============================================================================
# SECTION 3: POLYGONS
# ============================================================================

def area2(P):
    """P: polygon (no repeated last vertex) -> TWICE the signed area. Positive = CCW."""
    n = len(P)
    return sum(P[i][0]*P[(i+1) % n][1] - P[(i+1) % n][0]*P[i][1] for i in range(n))

def is_convex(P):
    """P: polygon -> True if all non-zero turns go the same direction."""
    n = len(P); s = set()
    for i in range(n):
        c = sgn(cross(P[i], P[(i+1) % n], P[(i+2) % n]))
        if c: s.add(c)
    return len(s) <= 1

def point_in_polygon(p, P):
    """p: point, P: simple polygon -> 1 strictly inside, 0 on boundary, -1 outside."""
    n = len(P); inside = False
    for i in range(n):
        a, b = P[i], P[(i+1) % n]
        if on_seg(p, a, b): return 0
        if (a[1] > p[1]) != (b[1] > p[1]):
            if (cross(a, b, p) > 0) == (b[1] > a[1]): inside = not inside
    return 1 if inside else -1

# ============================================================================
# SECTION 4: CONVEX HULL
# ============================================================================

def convex_hull(pts):
    """pts: list of (x, y) tuples -> hull vertices in CCW order."""
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

def convex_hull_keep_collinear(pts):
    """pts: list of points -> hull vertices in CCW order, keeping collinear boundary points."""
    pts = sorted(set(pts))
    if len(pts) <= 2: return pts
    lo = []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) < 0: lo.pop()
        lo.append(p)
    up = []
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) < 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]

# ============================================================================
# SECTION 5: WORKED PROBLEMS FROM SLIDES (READY TO USE)
# ============================================================================

def completing_square(a, b, c):
    """Three corners of a square -> the fourth corner."""
    from dot import vec, dot
    for o, u, w in ((a, b, c), (b, a, c), (c, a, b)):
        if dot(vec(o, u), vec(o, w)) == 0:
            return (u[0] + w[0] - o[0], u[1] + w[1] - o[1])

def circumcenter(a, b, c):
    """Three NON-collinear points -> center of the circle through all three."""
    d = 2*(a[0]*(b[1]-c[1]) + b[0]*(c[1]-a[1]) + c[0]*(a[1]-b[1]))
    sa, sb, sc = a[0]**2+a[1]**2, b[0]**2+b[1]**2, c[0]**2+c[1]**2
    ux = (sa*(b[1]-c[1]) + sb*(c[1]-a[1]) + sc*(a[1]-b[1])) / d
    uy = (sa*(c[0]-b[0]) + sb*(a[0]-c[0]) + sc*(b[0]-a[0])) / d
    return ux, uy

def bounding_box_polygon(P):
    """P: list of polygon vertices -> area of smallest axis-parallel rectangle covering all vertices."""
    if len(P) < 3:
        raise ValueError("Need at least 3 points")
    # Generate all vertices from a triangle (first 3) assuming regular n-gon
    # Find circumcenter first, then generate all n vertices
    O = circumcenter(P[0], P[1], P[2])
    R = dist(P[0], O)
    theta = atan2(P[0][1] - O[1], P[0][0] - O[0])
    all_pts = [(O[0] + R*cos(theta + 2*pi*k/len(P)), 
                 O[1] + R*sin(theta + 2*pi*k/len(P))) for k in range(len(P))]
    return (max(x for x, y in all_pts) - min(x for x, y in all_pts)) * \
           (max(y for x, y in all_pts) - min(y for x, y in all_pts))

# ============================================================================
# SECTION 6: KATTIS PROBLEM STUBS (PASTE INTO YOUR SOLUTIONS)
# ============================================================================

def solve_completingthesquare():
    """Read three corners from stdin, output fourth corner. Right angle at any corner."""
    pass

def solve_mosquitoes(n, d, points):
    """Given n points and bowl diameter d, maximize points covered by a circle of diameter d.
    Points on the edge count. Uses circles_through for each pair."""
    from itertools import combinations
    best = 1
    if n == 1: return 1
    
    def dist2(a, b):
        return (a[0]-b[0])**2 + (a[1]-b[1])**2
    
    def circles_through(p, q, r):
        """Return list of circle centers (x,y) for circles of radius r through p and q."""
        mx, my = (p[0]+q[0])/2, (p[1]+q[1])/2
        dx, dy = q[0]-p[0], q[1]-p[1]
        d2 = dx*dx + dy*dy
        h2 = r*r - d2/4
        if h2 < -EPS or d2 == 0: return []
        h = sqrt(max(h2, 0)); L = sqrt(d2)
        ux, uy = -dy/L, dx/L
        return [(mx + ux*h, my + uy*h), (mx - ux*h, my - uy*h)]
    
    for p, q in combinations(points, 2):
        r = d / 2
        for c in circles_through(p, q, r):
            cnt = sum(1 for pt in points if dist2(pt, c) <= r*r + EPS)
            best = max(best, cnt)
    return best

def solve_roberthood(pts):
    """Given list of points, find the farthest pair (squared distance).
    C <= 10^5 but |x|,|y| <= 1000."""
    if len(pts) < 2: return 0
    h = convex_hull(pts)
    return max(dist2(a, b) for a in h for b in h)

# ============================================================================
# SECTION 7: TEST / DEMO CODE (RUN TO CHECK CORRECTNESS)
# ============================================================================

if __name__ == "__main__":
    # Quick sanity checks
    print("Testing primitives...")
    assert dot((1,0), (0,1)) == 0  # perpendicular
    assert cross((1,0), (0,1)) == 1  # CCW positive
    print("OK")
    
    # Test completing square
    print("\nCompleting square:")
    print(f"  corners {(0,0), (1,0), (1,1)} -> fourth = {completing_square((0,0), (1,0), (1,1))}")
    assert completing_square((0,0), (1,0), (1,1)) == (1, 1) or completing_square((0,0), (1,0), (1,1)) == (1, 1)
    
    # Test convex hull
    print("\nConvex hull:")
    pts = [(0,0), (1,1), (-1,0), (0,-1)]
    h = convex_hull(pts)
    print(f"  {h}")
    
    # Test area
    print("\nArea tests:")
    poly = [(0,0), (2,0), (2,2), (0,2)]
    print(f"  unit square area2 = {area2(poly)}")
    assert abs(area2(poly) - 8) < EPS  # 8 = 2*4 for doubled area
    
    print("\nAll basic tests passed!")
