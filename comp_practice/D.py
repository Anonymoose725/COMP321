def main():
    n, x, m = map(int, input().split())
    on_clock = 0
    on_count = 0
    for _ in range(m):
        crate = int(input())
        if 1 <= crate < x:
            on_clock += 1
        else:
            on_count += 1

    print(min(on_clock, on_count))

if __name__ == "__main__":
    main()