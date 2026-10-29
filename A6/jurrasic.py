# minimum spanning tree problem
# nodes = the n DNA strings
# edges = every pair of strings, weight weight equal to number of differing positions

import sys

data = sys.stdin.read().split()
n, k = int(data[0]), int(data[1])
dna_strings = data[2:n+2] # n of them

MAX = float("inf")

included = [False] * n

best = [MAX] * n # best[x] = shortest distance from x to the tree
best[0] = 0
total = 0 # running minimum distance

edges = []
parent = [-1] * n

for _ in range(n):
    # pick the next node not included in the tree with closest distance
    u = -1
    for v in range(n):
        if not included[v] and (u == -1 or best[v] < best[u]): # not an included node and a min
            u = v
    # add u to tree
    included[u] = True
    total += best[u]
    
    if parent[u] != -1: # put on tree
        edges.append((parent[u], u))
    
    # relax distances because now more nodes can be closer
    for v in range(n):
        if not included[v]:
            d = sum(c1 != c2 for c1, c2 in zip(dna_strings[u], dna_strings[v])) # calculates distance by summing differences
            if d < best[v]:
                best[v] = d
                parent[v] = u

    # O(n^2) acceptable for 1 <= n <= 1000
    
evo_likely = [f"{a} {b}" for a, b in edges]
print(total)
print("\n".join(evo_likely))