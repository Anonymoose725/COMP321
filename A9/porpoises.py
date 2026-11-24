import sys

def fib(n, mod=None): # uses matrix equivalences
    """O(log n) fast doubling -> (F_n, F_{n+1}). Pass mod for large n."""
    def _helper(k: int, mod=None) -> tuple[int, int]:
        if k == 0: return (0, 1)
        a, b = _helper(k >> 1, mod)
        c = a * (2 * b - a)
        d = a * a + b * b
        if mod: c %= mod; d %= mod
        return (d, c + d) if (k & 1) else (c, d)
    return _helper(n, mod)[0]

def main():
    data = sys.stdin.read().split()
    P = int(data[0])
    i = 2
    years = []
    for _ in range(P):
        years.append(int(data[i]))
        i += 2
    
    for i, yr in enumerate(years):
        print(f"{i+1} {fib(yr, mod=10**9)}")
    
if __name__ == "__main__":
    main()