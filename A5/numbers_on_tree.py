def main():
    inp = input().split()
    H = int(inp[0])
    path = inp[1] if len(inp) > 1 else "" # no path should give root
    
    print(2**(H+1) - 2**(len(path)+1) + path_to_index(path) + 1)

def path_to_index(path: str):
    binary_str = ""
    for i in path:
        if i == 'L':
            binary_str += "1"
        else: 
            binary_str += "0"
    return int(binary_str, 2) if binary_str else 0
    
if __name__ == "__main__":
    main()