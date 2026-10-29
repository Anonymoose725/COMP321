# this is dijkstra's shortest path!
# rather than minimizing distances, we're maximizing factor products
# why? well 0.1 * 0.1 = 0.01 => smaller shrinking factor, the goal!
# so rather than use a min-heap prio queue, we'll use a max-heap prio queue
# relaxing is multiplication

import sys
import heapq # max heap


def solve(n, adj):
    # TODO 1: best = list of n floats, all 0.0, except best[0] = 1.0

    # TODO 2: heap = [(-1.0, 0)]
    #         heapq is a MIN-heap, so store the NEGATED size:
    #         the most negative value (= the largest size) comes out first.

    # TODO 3: while heap is non-empty:
    #   - pop (neg_size, u) with heapq.heappop, and set size = -neg_size
    #   - if size < best[u]: stale entry, continue
    #   - for (v, f) in adj[u]:
    #         candidate = best[u] * f
    #         if candidate > best[v]:
    #             best[v] = candidate
    #             heapq.heappush(heap, (-candidate, v))

    # TODO 4: return best[n - 1]
    return 0.0


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

        adj = [[] for _ in range(n)]

        for _ in range(m):
            x = int(data[pos])
            y = int(data[pos + 1])
            f = float(data[pos + 2])
            pos += 3
            # TODO 6: undirected graph, so append (y, f) to adj[x]
            #         AND (x, f) to adj[y]

        result = solve(n, adj)
        result.append(f"{result:.4f}")

    print("\n".join(result))


main()