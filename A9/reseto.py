from math import isqrt

def primes(n, k) -> list[int]: # roughly O(Nlog(log(N))
    count = 0
    crossed_out = [False] * (n+1)
    
    for p in range(2, n+1):
        if not crossed_out[p]:
            for multiple in range(p, n+1, p): # start at p instead of p*p so p itself is crossed out
                if not crossed_out[multiple]:
                    # cross out
                    crossed_out[multiple] = True
                    count += 1
                    # check if kth cross
                    if count == k:
                        return multiple
                
    return -1 # something went wrong!

def main():
    n, k = map(int, input().split())
    print(primes(n, k))
    
if __name__ == "__main__":
    main()