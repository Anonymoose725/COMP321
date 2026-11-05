from collections import deque

class ACNode:
    def __init__(self):
        self.children = {}          # map: character -> next node
        self.fail: ACNode = None    # pointer to longest proper suffix
        self.output = []            # list of patterns ending at this character

class ACAutomaton:
    def __init__(self, patterns):
        self.root = ACNode()
        self.build_trie(patterns)
        self.build_fails()
        
    def build_trie(self, patterns):
        for p in patterns:
            if not p: # ignore
                continue
            cur = self.root
            for char in p:
                cur = cur.children.setdefault(char, ACNode())
            cur.output.append(p)

    def build_fails(self):
        # BFS from root, since we build layer-by-layer
        q: deque[ACNode] = deque()
        
        # root's children fail to root
        for child in self.root.children.values(): # key-value pairs
            child.fail = self.root
            q.append(child)
        
        while q: # not empty
            cur = q.popleft()
            
            for char, child in cur.children.items():
                fallback = cur.fail
                # follow upwards either until reaching a node with char or the root
                while fallback is not None and char not in fallback.children:
                    fallback = fallback.fail
                
                child.fail = fallback.children[char] if fallback else self.root # if we went up and hit nothing, fail to root
                child.output.extend(child.fail.output) # join
                
                q.append(child)
    
    def find(self, substr):
        cur = self.root
        
        for end_idx, char in enumerate(substr):
            while cur is not None and char not in cur.children:
                # fall back while not matching
                cur = cur.fail
            
            # try again at root if it didnt work
            if cur is None:
                cur = self.root
                continue
            
            cur = cur.children[char] # advance
            
            # yield => return for every iteration at current automaton state
            for p in cur.output:
                yield end_idx - len(p) + 1, p # end index - p.length + 1 = start index
        

def main():
    patterns = ["he", "she", "his", "hers"]
    text = "ushersandhis"
    
    automaton = ACAutomaton(patterns)
    
    print(f"Search for {patterns} in '{text}':")
    for start_idx, pattern in automaton.find(text):
        print(f"Found keyword '{pattern}' starting at index {start_idx}")
        
if __name__ == "__main__":
    main()