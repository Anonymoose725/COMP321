# we choose the smallest factors that multiply together to meet at X
# -> prime factors
from math import isqrt

def num_PF(n):
    """Count the number of prime factors of n, including duplicates"""
    PF = 2
    ans = 0
    while PF * PF <= n:
        while n % PF == 0:
            n //= PF; ans += 1
        PF += 1
    if n != 1: ans += 1
    return ans

def game(X: int):
    """
    Receives as input positive integer 10^3 <= X <= 10^9
    Returns integer k such that (Y_1+1)(Y_2+1)...(Y_k+1) = X with maximal points k
    """
    return num_PF(X)

def main():
    X = int(input())
    print(game(X))

if __name__ == "__main__":
    main()
