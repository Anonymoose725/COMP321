import sys

class DSU:
    """Disjoint Union-Find, for naturally joining initially islanded users into groups"""
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
    
    def find(self, x):
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        
        # path compression
        while self.parent[x] != root:
            self.parent[x], x = root, self.parent[x]
        
        return root

    def union(self, a, b):
        roota, rootb = self.find(a), self.find(b)
        if roota == rootb:
            return # same DSU
        if self.size[roota] < self.size[rootb]:
            roota, rootb = rootb, roota
        # attach smaller set under larger one
        self.parent[rootb] = roota
        self.size[roota] += self.size[rootb]
 
def next_random(r, a, b, c): 
    return (r * a + b) % c
        
def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        
        n, r, a, b, c = map(int, line.split())
        groups = DSU(n)
        
        for i in range(n):
            while(True):
                r = next_random(r, a, b, c)
                x = r % n
                r = next_random(r, a, b, c)
                y = r % n
                if x != y:
                    break
            
            # start a chat between persons x and y, if they are not already chatting
            groups.union(x, y)
            
        count = {}
        for i in range(n):
            if groups.find(i) == i:
                s = groups.size[i] # size of group i
                count[s] = count.get(s, 0) + 1
        
        out = []
        for size in sorted(count, reverse=True):
            c = count[size]
            out.append(str(size) if c == 1 else f"{size}x{c}")

        print(sum(count.values()), *out) # out if applicable only
    
if __name__ == "__main__":
    main()