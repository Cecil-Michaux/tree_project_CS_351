from BTree import bTree, bTreeNode
keys = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S']
def btreetest():
    tree = bTree("test", 3)
    tree.group_insert(keys)
    #print(tree)
    print(tree)


if __name__ == "__main__":
    btreetest()
