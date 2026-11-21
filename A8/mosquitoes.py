import sys
import itertools
from math import sqrt

def mosquitoes(n, d, points):
    # the best bowl is on the edge of two mosquitoes (min)
    # for any pair of mosquitoes, either 0, 1, or 2 such circles
    # for every two points, construct the circle passing through them of radius d
    # then see how many points lie within
    if n == 1:
        return 1
    
    r = d / 2
    best = 1
    
    def circles_through(p, q, r):
        mx, my = (p[0]+q[0])/2, (p[1]+q[1])/2
        dx, dy = q[0]-p[0], q[1]-p[1]
        d2 = dx*dx + dy*dy
        h2 = r*r -d2/4
        if h2 < -1e-5 or d2 == 0: return []
        h = sqrt(max(h2, 0)); L = sqrt(d2)
        ux, uy = -dy/L, dx/L
        return [(mx + ux*h, my + uy*h), (mx - ux*h, my - uy*h)]

    def dist2(a, b):
        return (a[0]-b[0])**2 + (a[1]-b[1])**2
    
    # loop over pairs
    for p, q in itertools.combinations(points, 2):
        for circle in circles_through(p, q, r):
            # count how many of all the points are within the circle
            count = 0
            for pt in points:
                if dist2(pt, circle) <= r*r + 1e-5: # within or on circle
                    count += 1
            best = max(best, count)
            
    return int(best)

def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    i = 1
    result = []
    for _ in range(t):
        n, d = int(data[i]), float(data[i+1])
        i += 2
        points = []
        for _ in range(n):
            x, y = float(data[i]), float(data[i+1])
            points.append((x, y))
            i += 2
    
        result.append(str(mosquitoes(n, d, points)))
    
    print("\n".join(result))
    
if __name__ == "__main__":
    main()