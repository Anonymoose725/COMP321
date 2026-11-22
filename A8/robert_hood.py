# complex hull
import sys
from functools import cmp_to_key
from math import sqrt

def dist2(a, b=(0, 0)):
    """points (b defaults to origin, so dist2(v) is the squared norm of v) -> squared distance. Exact for ints."""
    return (a[0]-b[0])**2 + (a[1]-b[1])**2

def cross(o, a, b):
    """POINTS -> (a-o) x (b-o) = the slides' ccw(o,a,b). >0 left turn o->a->b, <0 right turn, 0 collinear."""
    return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])

def robert(shots):
    # 1. form convex hull
    # graham scan
    pts = list(set(shots)) # remove duplicates
    if len(pts) == 2:
        return float(sqrt(dist2(pts[0], pts[1]))) # early exit
    
    p0 = min(pts)
    rest = [p for p in pts if p != p0]
    def cmp(a, b): # sort by cross product
        c = cross(p0, a, b)
        if c:
            return -1 if c > 0 else 1
        return dist2(a, p0) - dist2(b, p0) 
    rest.sort(key=cmp_to_key(cmp))
    S = [p0]
    for p in rest:
        while len(S) >= 2 and cross(S[-2], S[-1], p) <= 0: 
            S.pop() # pop while another outermost point exists
        S.append(p)
    # now S is convex hull from lower leftmost point, CCW
    
    # 2. compare all pairs in the hull
    best = 0
    for i, p1 in enumerate(S):
        for p2 in S[i+1:]: # distinct, so check forward only
            best = max(best, dist2(p1, p2))
    
    # 3. return farthest euclidean distance
    return sqrt(best)

def main():
    data = sys.stdin.read().split()
    c = int(data[0])
    i = 1
    shots = []
    for _ in range(c):
        x, y = int(data[i]), int(data[i+1])
        shots.append((x, y))
        i += 2

    result = robert(shots)
    print(f"{result:.9f}")
    
    
if __name__ == "__main__":
    main()