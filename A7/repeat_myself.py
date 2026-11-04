import sys

def shortest_pattern(str):
    n = len(str)
    for p in range(1, n+1):
        valid = True
        for i in range(n): # brute force
            if str[i] != str[i % p]: # wraps to continue checking pattern
                valid = False
                break
            
        if valid:
            return p
    
data = sys.stdin.read().split("\n")
t = int(data[0])

for i in range(t):
    idx = i + 1 # offset from initial t collection
    str = data[idx] # ignore whitespace
    print(shortest_pattern(str))
