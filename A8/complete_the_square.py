import sys

points = []
for line in sys.stdin.read().strip().splitlines():
    x, y = map(int, line.split())
    points.append((x, y))

def vec(p, q):
    return (q[0] - p[0], q[1] - p[1])

# find which point is between the other two
# find by checking right angle
def dot(u, v):
    return u[0]*v[0] + u[1] * v[1]

corner = None
for i in range(3):
    A = points[i]
    B = points[(i+1) % 3] # cycle around
    C = points[(i+2) % 3]
    
    if dot(vec(A, B), vec(A, C)) == 0:
        # perpendicular => corner
        corner = A
        points = (B, C)
        break

# compute P + Q
P = vec(corner, points[0])
Q = vec(corner, points[1])

x = corner[0] + P[0] + Q[0]
y = corner[1] + P[1] + Q[1]
print(x, y)