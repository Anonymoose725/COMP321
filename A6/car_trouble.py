# ring around the inner city
# all roads within are one-ways (directed edges)
# given a street X
    # X is unreachable if it can't be accessed from the circumscribing road
    # X is trapped if it can't access the circumscribing road
    
# get adjacency list
# BFS from outer road to get set of unreachable roads
# BFS from outer road in reversed graph to get streets that trap
# print in order: trapped, then unreachable (no problems if empty)

import sys
from collections import defaultdict, deque

# collect variables
n = int(input())

ordered = []
adj = defaultdict(list)
reversed = defaultdict(list)

for _ in range(n):
    parts = list(map(int, input().split()))
    id, k = parts[0], parts[1]
    neighbours = parts[2:] # everything after k (k of them)
    
    ordered.append(id)
    for v in neighbours:
        adj[id].append(v)
        reversed[v].append(id) # reverse

        
outer = 0

def bfs(graph, start): # use for either direction!
    visited = {start}
    queue = deque([start])
    while queue:
        x = queue.popleft()
        for y in graph[x]:
            if y not in visited:
                visited.add(y)
                queue.append(y)
    return visited

reachable = bfs(adj, outer)
can_escape = bfs(reversed, outer)

trapped = [x for x in ordered if x not in can_escape]
unreachable = [x for x in ordered if x not in reachable]

if not trapped and not unreachable:
    print("NO PROBLEMS")
else: 
    for x in trapped:
        print(f"TRAPPED {x}")
    for x in unreachable:
        print(f"UNREACHABLE {x}")
        
