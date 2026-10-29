# this is dijkstra's shortest path!
# rather than minimizing distances, we're maximizing factor products
# why? well 0.1 * 0.1 = 0.01 => smaller shrinking factor, the goal!
# so rather than use a min-heap prio queue, we'll use a max-heap prio queue
# relaxing is multiplication

import sys
import heapq # max heap


def get_shorty(n, adj):
    # TODO 1: best = list of n floats, all 0.0, except best[0] = 1.0
    best = [0.0] * n
    best[0] = 1.0 # full size initially

    pq = [(-1.0, 0)] # negate to make a max heap. grabbing minimum grabs -(maximum)
    heapq.heapify(pq) # turns the list pq into a max heap
    
    # TODO 3: while heap is non-empty:
    #   - pop (neg_size, u) with heapq.heappop, and set size = -neg_size
    #   - if size < best[u]: stale entry, continue
    #   - for (v, f) in adj[u]:
    #         candidate = best[u] * f
    #         if candidate > best[v]:
    #             best[v] = candidate
    #             heapq.heappush(heap, (-candidate, v))

    while pq:
        size_neg, u = heapq.heappop(pq) # greedy choice
        size = -size_neg
        if size < best[u]: continue # ignore
        
        for (v, f) in adj[u]: # v neighbours, relaxing
            cur = best[u] * f
            if cur > best[v]:
                best[v] = cur
                heapq.heappush(pq, (-cur, v))

    return best[n-1]


def main():
    data = sys.stdin.read().split()
    pos = 0
    result = []

    while True:
        n = int(data[pos])
        m = int(data[pos + 1])
        pos += 2
        if n == 0 and m == 0: # indicates final test, not to be processed
            break

        adj = [[] for _ in range(n)] # n "intersections" ie nodes

        for _ in range(m):
            x = int(data[pos])
            y = int(data[pos + 1])
            f = float(data[pos + 2])
            pos += 3

            adj[x].append((y, f))
            adj[y].append((x, f)) # undirected so we take both

        best = get_shorty(n, adj)
        result.append(f"{best:.4f}")

    print("\n".join(result))

main()