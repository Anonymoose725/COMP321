# this is a trie problem, storing character by character
# traverse each char in the word
# if a node doesnt exist, create it
# when reaching final character, retrieve a counter
# increment counters every time a new word is inserted

class TrieNode:
    def __init__(self):
        self.children = {}
        self.count = 0
        
def bing():
    n = int(input())
    r = TrieNode()
    
    for _ in range(n):
        word = input().strip()
        node = r
        # traverse trie, creating missing nodes along the way
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
                
            node = node.children[char] # advance down
        
        # print its counter ie. number of previously inserted words with this prefix
        print(node.count)
        
        # insert it i.e. update all counters
        node = r
        for char in word:
            node = node.children[char]
            node.count += 1

if __name__ == "__main__":
    bing()