import sys

def build_LPS(pattern):
    """Computes longest proper prefix <-> a suffix array"""
    m = len(pattern)
    pi = [0] * m
    longest = 0
    i = 1
    
    while i < m:
        if pattern[i] == pattern[longest]:
            longest += 1
            pi[i] = longest
            i += 1
        else:
            if longest != 0:
                # previous is best
                longest = pi[longest - 1]
            else:
                pi[i] = 0
                i += 1
                
    return pi


def kmp_find(pattern, text):
    m = len(pattern)
    n = len(text)
    
    if m == 0:
        return [0]
    if n < m:
        return []
    
    LPS = build_LPS(pattern)
    matches = [] # indices
    
    i = 0 # text
    j = 0 # pattern
    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1
        
        if j == m:
            # full match
            start = i - j
            matches.append(start)
            j = LPS[j-1] # fallback to last
        
        elif i < n and pattern[j] != text[i]:
            # break
            if j != 0:
                j = LPS[j-1]
            else:
                i += 1
    
    return matches

def main():
    data = [ln.rstrip() for ln in sys.stdin.read().split("\n")]
    while data and data[-1] == "": # leftovers from the last newline
        data.pop()

    out = []
    for i in range(0, len(data) - 1, 2):
        pattern, text = data[i], data[i + 1]
        out.append(" ".join(map(str, kmp_find(pattern, text))))

    print("\n".join(out) + "\n") # new lines . WHY IS THERE NO TEST NUMBER !!!
            
if __name__ == "__main__":
    main()