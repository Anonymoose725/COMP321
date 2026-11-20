import math
from math import gcd

n = int(input())

# compute block
i = math.isqrt((8 * n + 1) - 1) // 2
while i * (i+1) // 2 < n:
    i+=1
while i > 1 and i * (i-1) // 2 >= n:
    i-=1

# compute offset
j = n - i * (i-1) // 2 - 1

if j == 0:
    print(i)
else:
    g = gcd(i, j)
    print(f"{i} {j // g}/{i // g}")

