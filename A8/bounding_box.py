import sys
from math import sin, cos, pi

def bounding_box(n, A, B, C):
    """
    Given 3 points and the number of vertices of a regular polygon, find the smallest bounding box area
    """
    # 1. find circumcenter (px, py) of A, B, C)
    #    -> use it to rotate to resolve all vertices
    # 2. for k in range(n), compute vertex k, track the min/max x and y
    # 3. return (maxx - minx) * (maxy - miny) = A    
    def circumcenter(a, b, c):
        d = 2*(a[0]*(b[1]-c[1]) + b[0]*(c[1]-a[1]) + c[0]*(a[1]-b[1]))
        sa, sb, sc = a[0]**2+a[1]**2, b[0]**2+b[1]**2, c[0]**2+c[1]**2
        ux = (sa*(b[1]-c[1]) + sb*(c[1]-a[1]) + sc*(a[1]-b[1])) / d
        uy = (sa*(c[0]-b[0]) + sb*(a[0]-c[0]) + sc*(b[0]-a[0])) / d
        return ux, uy
    
    px, py = circumcenter(A, B, C) # circumcenter of triangle formed by A, B, C
    # now rotate the triangle about k times
    def rotate(v, t):
        return (v[0]*cos(t) - v[1]*sin(t), v[0]*sin(t) + v[1]*cos(t))
    def rotate_about(p, c, t):
        d = rotate((p[0]-c[0], p[1]-c[1]), t)
        return (c[0]+d[0], c[1]+d[1])
    
    step = 2 * pi / n
    minx = miny = float('inf')
    maxx = maxy = float('-inf')
    for k in range(n):
        vx, vy = rotate_about(A, (px, py), k * step)
        minx = min(minx, vx)
        maxx = max(maxx, vx)
        miny = min(miny, vy)
        maxy = max(maxy, vy)
    
    return (maxx - minx) * (maxy - miny) # = A
    

def main():
    data = sys.stdin.read().split()
    i = 0
    result = []
    while i < len(data):
        n = int(data[i])
        i += 1
        if n == 0:
            break # dummy case, done
        x1, y1, x2, y2, x3, y3 = map(float, data[i:i+6])
        i+=6
        area = bounding_box(n, (x1, y1), (x2, y2), (x3, y3))
        result.append(f"{area:.10f}") # within 10 decimal places
    print("\n".join(result))

if __name__ == "__main__":
    main()