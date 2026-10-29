# shortest path in a graph, unweighted
# why? DP at first, but that wont work because there is no obvious way to fill a DP table
# this is because there are cycles in the floor decisions
# problem has "states" and "moves"
    # state = current floor (ie. node)
    # move = a button that takes you to another floor (ie. edge)
    
# BFS finds the minimum distance <-> minimum number of button presses (moves)

from collections import deque

f, s, g, u, d = map(int, input().split())
# f: number of floors
# s: start floor
# g: goal floor
# u: distance traveled in terms of number of floors when pressing up
# d: distance traveled in terms of number of floors when pressing down

dist = [-1] * (f+1) # number of floors (1-indexed). dist[0] is unused
dist[s] = 0

queue = deque([s]) # enqueue start floor

while queue:
    x = queue.popleft()
    if x == g:
        break # done!
    
    for v in (x + u, x - d): # either up or down
        if 1 <= v <= f and dist[v] == -1: # bound next floor to possible floors
            # next unvisited floor
            dist[v] = dist[x] + 1
            queue.append(v)

print(dist[g] if dist[g] != -1 else "use the stairs")