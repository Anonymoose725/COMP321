from math import hypot

def dist(a, b=(0, 0)):
    """a, b: points (b defaults to origin) -> float Euclidean distance."""
    return hypot(a[0]-b[0], a[1]-b[1])

def circumcenter(a, b, c):
    """a, b, c: three NON-collinear points -> (x, y) float center of the circle through all three.
    Radius = dist(center, a). Raises ZeroDivisionError if the points are collinear."""
    d = 2*(a[0]*(b[1]-c[1]) + b[0]*(c[1]-a[1]) + c[0]*(a[1]-b[1]))
    sa, sb, sc = a[0]**2+a[1]**2, b[0]**2+b[1]**2, c[0]**2+c[1]**2
    ux = (sa*(b[1]-c[1]) + sb*(c[1]-a[1]) + sc*(a[1]-b[1])) / d
    uy = (sa*(c[0]-b[0]) + sb*(a[0]-c[0]) + sc*(b[0]-a[0])) / d
    return ux, uy

def solve(A, B, C):
    # 1. build triangle ABC = AB, BC, CA
    AB = (B[0]-A[0], B[1]-A[1])
    BC = (C[0]-B[0], C[1]-B[1])
    CA = (A[0]-C[0], A[1]-C[1])
    
    # 2. resolve incenter I
    a = dist(B, C) # |BC|
    b = dist(C, A) # |CA|
    c = dist(A, B) # |AB|
    s = a + b + c
    I = ((a*A[0] + b*B[0] + c*C[0]) / s, (a*A[1] + b*B[1] + c*C[1]) / s)
    
    # 3. draw circumcircle O to place points
    O = circumcenter(A, B, C) # px, py
    R = dist(A, O)
    
    # 4. draw AM, BN, CP by using I as parametric line
    
    
    # 5. Find POIs by setting lines equal
    # 6. return dists between points

def main():
    bx, cx, cy = map(float, input().split())
    A, B, C = (0, 0), (bx, 0), (cx, cy)
    print(solve(A, B, C))    

if __name__ == "__main__":
    main()