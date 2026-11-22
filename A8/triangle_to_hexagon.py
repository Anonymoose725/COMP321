from math import hypot

def cross(u, v): 
    return u[0]*v[1] - u[1]*v[0]

def sub(p, q): 
    return (p[0]-q[0], p[1]-q[1])

def dot(u, v): 
    return u[0]*v[0] + u[1]*v[1]

def dist(a, b=(0, 0)):
    """a, b: points (b defaults to origin) -> float Euclidean distance."""
    return hypot(a[0]-b[0], a[1]-b[1])

def circumcenter(a, b, c):
    """a, b, c: three NON-collinear points -> (x, y) float center of the circle through all three.
    Radius = dist(center, a). Raises ZeroDivisionError if the points are collinear."""
    d = 2*(a[0]*(b[1]-c[1]) + b[0]*(c[1]-a[1]) + c[0]*(a[1]-b[1]))
    sa, sb, sc = a[0]**2 +a[1]**2, b[0]**2+b[1]**2, c[0]**2+c[1]**2
    ux = (sa*(b[1]-c[1]) + sb*(c[1]-a[1]) + sc*(a[1]-b[1])) / d
    uy = (sa*(c[0]-b[0]) + sb*(a[0]-c[0]) + sc*(b[0]-a[0])) / d
    return ux, uy

def second_point(P, I, O):
    d = sub(I, P) # d gives direction of ray travelling through I
    t = -2 * dot(d, sub(P, O)) / dot(d, d) # parametric form!
    return (P[0] + t*d[0], P[1] + t*d[1]) # P + td

def intersect(p1, p2, q1, q2):
    """p1->p2, q1->q2, returns (x,y) point of intersection"""
    r, s = sub(p2, p1), sub(q2, q1)
    t = cross(sub(q1, p1), s) / cross(r, s)
    return (p1[0] + t*r[0], p1[1] + t*r[1])

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
    M, N, P = second_point(A, I, O), second_point(B, I, O), second_point(C, I, O)
    
    # 5. Find POIs
    E = intersect(A, B, N, P)
    F = intersect(A, C, N, P)
    G = intersect(A, C, N, M)
    H = intersect(B, C, N, M)
    J = intersect(B, C, M, P)
    K = intersect(B, A, M, P)
    
    # 6. return dists between points
    return [dist(E, F), dist(F, G), dist(G, H), dist(H, J), dist(J, K), dist(K, E)]

def main():
    bx, cx, cy = map(float, input().split())
    A, B, C = (0, 0), (bx, 0), (cx, cy)
    lengths = solve(A, B, C)
    result = [f"{l:.6f}" for l in lengths]
    print(" ".join(result))

if __name__ == "__main__":
    main()