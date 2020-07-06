from __future__ import annotations

from typing import Optional, List


class Node:
    def __init__(self, data):
        """
        Creates a node without children or parent
        :param data: the value stored in the node
        """
        self.data = data
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
        self.parent: Optional[Node] = None
        self.size = 1

    @staticmethod
    def get_size(node: Optional[Node]):
        """
        :param node: (possibly None) node
        :return: Size of the node. When the node is None, returns 0.
        """
        return 0 if node is None else node.size

    def fix_size(self):
        """
        Fixes node size based on sizes of its children
        """
        self.size = 1 + Node.get_size(self.left) + Node.get_size(self.right)

class TreeArray:
    """
    Efficient variable-size arrays implemented using tree
    """
    def __init__(self):
        self.root: Optional[Node] = None

    
    def size(self):
        """
        :return: The total number of elements
        Time Complexity: O(1)
        """
        return Node.get_size(self.root)

    def find(self, i: int) -> Node:
        """
        :param i: An index of a node to find
        :return: A node in the the tree with index i
        :raises IndexError if index is out of bounds
        Average Case Time Complexity: O(log N)
        Worst Case Time Complexity: O(N)
        """
        temp=self.root
        if(i>Node.get_size(temp)-1):
            raise IndexError
        while(1):
            if(i<Node.get_size(temp.left)):
                temp=temp.left
            elif(i==Node.get_size(temp.left)):
                return temp
            elif(i>Node.get_size(temp.left)):
                i=i-Node.get_size(temp.left)-1
                temp=temp.right
            else:
                pass
        return
        
    def get(self, i: int):
        """
        :param i: Index where the element is inserted
        :return: A value at index i
        :raises IndexError if index is out of bounds
        Average Case Time Complexity: O(log N) because of find function
        Worst Case Time Complexity: O(N) because of find function
        """
        return self.find(i).data

    def set(self, i: int, x):
        """
        Changes value at index i to x
        :param i: Index of the modified value
        :param x: The new value
        :raises IndexError if index is out of bounds
        Average Case Time Complexity: O(log N) because of find function
        Worst Case Time Complexity: O(N) because of find function        
        """
        if(i>Node.get_size(self.root)-1):
            raise IndexError
            
        self.find(i).data=x

    def fix_sizes(self, node: Node):
        """
        Fixes sizes of all nodes on the path between this node and the root of the tree
        :param node: Starting node
        Average Case Time Complexity: O(log N)
        Worst Case Time Complexity: O(N)
        """
        #Traverse from current node to root using parent pointer and update size
        while(node):
            Node.fix_size(node)
#            node.size = 1 + Node.get_size(node.left) + Node.get_size(node.right)
            node=node.parent
            
    def insert(self, i: int, x):
        """
        Insert value x into position i
        :param i: Index where the element is inserted
        :param x: The inserted value
        :raises IndexError if index is out of bounds
        Average Case Time Complexity: O(log N)
        Worst Case Time Complexity: O(N)
        """
        insert_node=Node(x)
        current_node=None
        
        #if index greater than size, raise index error
        if(i>Node.get_size(self.root)):
            raise IndexError
            
        #initial insert
        if(self.root is None):
            self.root=Node(x)
            return
        
        #if inserting at index 0, then insert at left most 
        temp=self.root
        if(i==0):
            while(temp.left):
                temp=temp.left
            temp.left=insert_node
            insert_node.parent=temp
            self.fix_sizes(insert_node)
            return
        
        #allow append at the end, hence last_index+1 insertion allowed
        if(i==Node.get_size(self.root)):
                temp=self.find(i-1)
                temp.right=insert_node
                insert_node.parent=temp
                self.fix_sizes(insert_node) 
                return
        
        #if in between index, then find i-1 node and put the element to right if right is null else put at leftmost of right
        current_node=self.find(i-1)
        if(current_node.right):
            current_node=current_node.right
            while(current_node.left):
                current_node=current_node.left
            current_node.left=insert_node
            insert_node.parent=current_node
            self.fix_sizes(insert_node)
        else:
            current_node.right=insert_node
            insert_node.parent=current_node
            self.fix_sizes(insert_node)
       
#Reference: https://www.geeksforgeeks.org/inorder-successor-in-binary-search-tree/
    def minValue(self,node): 
        current = node 
        # loop down to find the leftmost leaf 
        while(current is not None): 
            if current.left is None: 
                break
            current = current.left 
      
        return current

#Reference: https://www.geeksforgeeks.org/inorder-successor-in-binary-search-tree/    
    def inOrderSuccessor(self, n): 
        if n.right is not None: 
            return self.minValue(n.right)
        
        p = n.parent 
        while( p is not None): 
            if n != p.right : 
                break 
            n = p  
            p = p.parent 
        return p
    
    def remove(self, i: int):
        """
        Removes an element at index i
        :param i: Index of the removed element
        :raises IndexError if index is out of bounds
        Average Case Time Complexity: O(log N)
        Worst Case Time Complexity: O(N)
        """
        temp=self.root
        if(i>Node.get_size(temp)-1):
            raise IndexError
        
        del_node=self.find(i)
        
        if(del_node.parent is None):
            parent_node=None
        else:
            parent_node=del_node.parent
                    
        # Node at leaf
        if(del_node.left is None and del_node.right is None):
            if parent_node is not None:
                if (parent_node.left==del_node):
                    parent_node.left=None
                else:
                    parent_node.right=None
            else:
                self.root = None
            self.fix_sizes(parent_node)
            return
        
        
        #Node having only one child (left or right)
        if (del_node.left is not None and del_node.right is None) or (del_node.right is not None and del_node.left is None):
            if del_node.left is not None:
                child_node = del_node.left
            else:
                child_node = del_node.right

            if parent_node is not None:
                if parent_node.left == del_node:
                    parent_node.left = child_node
                else:
                    parent_node.right = child_node
            else:
                self.root = child_node
            child_node.parent = parent_node
            self.fix_sizes(parent_node)
            return
        
        # Node having both children
        if(del_node.left is not None and del_node.right is not None):
            succ=self.inOrderSuccessor(del_node.right)
            if(parent_node is None):
                self.root=succ
            elif(parent_node.left ==del_node):
                parent_node.left=succ
            else:
                parent_node.right=succ
            succ.left=del_node.left
            temp=del_node.right
            self.fix_sizes(temp)
        
                
    def inorder(self) -> List:
        """
        :return: Elements in inorder. Should return an array represented by the tree
        Worst Case Time Complexity: O(N) since it visits all the nodes
        """       
        stack=[]
        values=[]
        temp=self.root
        while True:
            while temp:
                stack.append(temp)
                temp = temp.left
            if not stack:
                return values
            node = stack.pop()
            values.append(node.data)
            temp = node.right
        
        return
    
# =============================================================================
#     Alternatively:
#         stack=[]
#         current=self.root
#         l=[]
#         while(1):
#             
#             if(current!=None):
#                 stack.append(current)
#                 current=current.left
#         
#             elif(current==None and len(stack)>0):
#                 temp=stack.pop()
#                 l.append(temp.data)
#                 current=temp.right
#             
#             else:
#                 break
#         return l
# =============================================================================

            
tree=TreeArray()
print("Initial Insert:")
tree.insert(0,1)
print(tree.inorder())

print("Inserting value 2 at the beginning:")
tree.insert(0,2)
print(tree.inorder())

print("Inserting value 3 at index 1 i.e in between:")
tree.insert(1,3)
print(tree.inorder())

print("Appending value 10 at the end:")
tree.insert(3,10)
print(tree.inorder())

print("Size of tree:")
print(tree.size())

print("Removing node at in between index 1:")
tree.remove(1)
print(tree.inorder())

print("Removing node at first index:")
tree.remove(0)
print(tree.inorder())

print("Removing node at last index:")
tree.remove(1)
print(tree.inorder())

#tree.insert(0,11)
#tree.insert(2,8)
#print(tree.inorder())
#tree.remove(2)
#tree.insert(3,9)
#tree.insert(3,6)
#print(tree.inorder())
#
#tree.insert(3,100)
#tree.insert(3,200)
#tree.insert(6,6)
#print(tree.inorder())
#tree.insert(0,9)
#tree.insert(1,5)
#tree.insert(2,8)
#tree.insert(3,3)
#tree.insert(4,1)
#tree.insert(5,2)
#tree.insert(1,3)
#tree.insert(1,3)
#tree.insert(1,4)
#tree.remove(0)
#tree.remove(2)
#print(tree.inorder())