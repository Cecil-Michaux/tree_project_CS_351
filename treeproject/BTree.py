from IBTree import IbTree, IbTreeNode



class bTreeNode(IbTreeNode):
    def __init__(self, isleaf, parent = None, keys = [],):

        self._keys:list[str] = keys
        self._parent = parent

        self._children:list[bTreeNode] = []
        self._isleaf = isleaf
        self._keycount = len(self._keys) # cumulative count - num of keys in or below this node

    def have_key(self, key) -> bool:
        for item in self._keys:
            if key == item:
                return True
            
        return False

    def isleaf(self):
        return self._isleaf
    
    def set_leaf(self, isleaf:bool):
        self._isleaf = isleaf


    def compare(self, input, return_index = True):

        keys = self.get_keys()
        m = len(keys)

        for i in range(m):
            if input < keys[i]:
                if return_index == True:
                    return i
                else:
                    return keys[i]
                
        if return_index == True:
            return m
        else:
            return keys[i]
        
    def get_kids(self):
        return self._children

    def get_keys(self):
        return self._keys

    def add_key(self, new_key):
        n = len(self._keys)
        for i in range(n):
            if new_key <= self._keys[i]:
                self._keys.insert(i, new_key)
                return
        self._keys.insert(n, new_key)

    def set_keys(self, new_keys):
        self._keys = new_keys
    
    def clear_keys(self):
        self._keys = []

    def remove_key(self, key):
        self._keys.remove(key)
    
    def add_child(self, child):
        self._children.append(child)
        return self._children[-1]

    def remove_child(self, child):
        self._children.remove(child)
    
    def clear_kids(self):
        self._children = []
    
    def get_child(self, index):
        return self._children[index] 

    def verify(self):
        pass



class bTree(IbTree):
    def __init__(self, name, split_thresh):
        self._name:str = name
        self._root: bTreeNode = bTreeNode(True)
        self._split_thresh: int = split_thresh #max keys to store in 1 node



    def get_name(self):
        return self._name
    
    def insert(self, new_key, node = "Start"):

        if node == "Start":
            node = self._root
        
        node._keycount += 1
        
        if node.isleaf() == True:

            node.add_key(new_key)

            #print("Added key "+new_key)

            if len(node.get_keys()) > self._split_thresh:
                self.split(node)
        
        else:
            travel = node.get_child(node.compare(new_key))
            
            self.insert(new_key, travel)
        
    
    def group_insert(self, key_list): 
        for key in key_list:
            self.insert(key)

    def split(self, node:bTreeNode):
        #print("called split function")
        keys = node.get_keys()
        len_keys = len(keys)
        n = len_keys//2
        parent:bTreeNode = node._parent

        if parent == None:

            start, middle, end = keys[:n], keys[n], keys[n+1:]

            left = node.add_child(bTreeNode(True, node, start))
            right = node.add_child(bTreeNode(True, node, end))
            node.clear_keys()
            node.add_key(middle)
            node.set_leaf(False)
            return left, right
        
        elif len(parent.get_keys())< self._split_thresh:
            staying, leaving = keys[:n], keys[n:]

            node.set_keys(staying)

            parent.add_key(leaving.pop())
            parent.add_child(bTreeNode(True, parent, leaving))
        else:

            siblings = parent.get_kids()
            parent.clear_kids()
            left, right = self.split(parent)
            left.set_leaf(False)
            right.set_leaf(False)

            n = len(siblings)/2
            for i in range(len(siblings)):
                if i < n:
                    left.add_child(siblings[i])
                    siblings[i]._parent = left
                else:
                    right.add_child(siblings[i])
                    siblings[i]._parent = right
        



    
    def balance(self, node):
        pass

            
    def treeprint(self, node, layer):
        string = f"{node.get_keys()}"
        if node.isleaf():
            string += f'<> k={node._keycount}\n'
        else:
            string += f'k={node._keycount}\n'

        for kid in node.get_kids():
            string += layer *'    ' + f"{self.treeprint(kid, layer+1)}"

        return string


    def __repr__(self):
        
        return self.treeprint(self._root, layer = 1)

