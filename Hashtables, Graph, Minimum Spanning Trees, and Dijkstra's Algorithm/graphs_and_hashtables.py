import unittest
from typing import TypeVar, Generic, List, Tuple, Optional, Callable
K = TypeVar('K')
V = TypeVar('V')


class HashTable(Generic[K, V]):
    """
    A HashTable which maps keys of type K to values of type V
    """

    def __init__(self, get_hash: Callable[[K], int], capacity=4):
        self.elements: List[List[Tuple[K, V]]] = [[] for _ in range(capacity)]  # Sets initial capacity
        self._size = 0  # The number of entries
        self.get_hash = get_hash  # hash function
        

    def double_capacity(self):
        """ Doubles the capacity """
        new_capacity = len(self.elements) * 2
        new_size=0
        new_list: List[List[Tuple[K, V]]] = [[] for _ in range(new_capacity)]
  
        for ele in self.elements:
            if len(ele)==0:
                continue
            for kv in ele:
                index=self.get_hash(kv[0]) % new_capacity
                new_list[index].append((kv))
                new_size+=1
        
        self.elements = new_list  
        self._size=new_size
        
        ...

    def __setitem__(self, key: K, value: V):
        """ Maps the key to the value. If the key already exists, replaces its value with the new one """

        index = self.get_hash(key) % len(self.elements)
        temp=self.__getitem__(key)
        if temp is None:
            if(self._size+1 > len(self.elements)/2):
                self.double_capacity()
            index = self.get_hash(key) % len(self.elements)
            self.elements[index].append((key,value))
            self._size+=1
        else:
            for kv in self.elements[index]:
                if kv[0] == key:
                    ind=self.elements[index].index(kv)
                    self.elements[index].remove(kv)
                    self.elements[index].insert(ind,(key,value))              
        return
        ...

    def delete(self, key: K):
        """ Deletes the key from the HashTable. :raise: an exception when the key doesn't exist  """
        temp=self.__getitem__(key)
        if temp is None:
            raise Exception ("key doesn't exists")
        else:
            index = self.get_hash(key) % len(self.elements)
            for kv in self.elements[index]:
                if kv[0] == key:
                    self.elements[index].remove(kv)
            self._size-=1

    # Allows one to use square brackets: hash_table[key].
    # Check https://docs.python.org/3/reference/datamodel.html#object.__getitem__
    def __getitem__(self, key: K) -> Optional[V]:
        """ :return: value corresponding to the key. Returns None if the key doesn't exist """
        index=self.get_hash(key) % len(self.elements)
        temp=self.elements[index]
        if len(temp)==0:
            return None
        else:
            for kv in temp:
                if(kv[0]==key):
                    return kv[1]
        ...

    def keys(self) -> List[K]:
        """ Returns all existing keys """
        keylist=[]
        for ele in self.elements:
            for kv in ele:
                keylist.append(kv[0])          
        return keylist
        ...

    def size(self):
        """ Returns the number of entries. Must take O(1) time """
        return self._size
        ...


class DisjointSetUnion:
    def __init__(self):
        self.parent: HashTable[int, int] = HashTable(lambda u: u)
        self.size: HashTable[int, int] = HashTable(lambda u: u)

    def create_set(self, u: int):
        """ Creates a set consisting of a single element u """
        self.parent[u] = u
        self.size[u] = 1

    def find_set(self, u: int) -> int:
        """
        Returns an element representing a set containing u.
        For all elements from the set, find_set returns the same item
        """
        v = self.parent[u]
        if v == u:
            return u
        root = self.find_set(v)
        self.parent[u] = root
        return root

    def union(self, u: int, v: int):
        """
        Merge sets containing u and v
        Now all elements from these sets have the same representative
        """
        pu = self.find_set(u)
        pv = self.find_set(v)
        if self.size[pu] > self.size[pv]:
            self.parent[pv] = pu
            self.size[pu] = self.size[pu] + self.size[pv]
        else:
            self.parent[pu] = pv
            self.size[pv] = self.size[pu] + self.size[pv]


class Graph:
    def __init__(self):
        # Map from vertices to adjacency HashTables
        self.g: HashTable[int, HashTable[int, int]] = HashTable(lambda u: u)

    def create_edge(self, u: int, v: int, w: int):
        temp_u=self.g.__getitem__(u)
        temp_v=self.g.__getitem__(v)

        if(temp_u is None):
            raise Exception ("Vertex U doesn't Exists")
        if(temp_v is None):
            raise Exception ("Vertex V doesn't Exists")
        if(w<0):
            raise Exception ("Weight less than zero")
        if(self.has_edge(u,v)):
            raise Exception ("Edge Already Exists")
            
        temp_u.__setitem__(v,w)
        temp_v.__setitem__(u,w)
        ...

    def delete_edge(self, u: int, v: int):
        temp_u=self.g.__getitem__(u)
        temp_v=self.g.__getitem__(v)
        if(self.has_edge(u,v) == False):
            raise Exception ("Edge doesn't Exists")
        
        temp_u.delete(v)
        temp_v.delete(u)
        ...

    def has_edge(self, u: int, v: int) -> bool:
        temp=self.g.__getitem__(u)
        if v in temp.keys():
            return True
        else:
            return False
        ...

    def create_vertex(self, u: int):
        temp=self.g.__getitem__(u)
        if temp is None:
            self.g.__setitem__(u,HashTable(lambda u: u))
        else:
            raise Exception ("Vertex Already Exists")
        ...

    def delete_vertex(self, u: int):
            
        u_neighbours=self.neighbours(u)
        for neigh in u_neighbours:
            temp=neigh.__getitem__(u)
            if temp is not None:
                neigh.delete(u)
        
        self.g.delete(u)
    
        ...

    def degree(self, u: int) -> int:
        temp=self.g.__getitem__(u)
        if temp is not None:
            return temp.size()
        else:
            raise Exception ("Vertex doesn't Exists")    
        ...

    def neighbors(self, u: int) -> list:
        temp=self.g.__getitem__(u)
        if temp is not None:
            return temp.keys()
        else:
            raise Exception ("Vertex doesn't Exists")
        ...

    def mst(self) -> List[Tuple[int, int]]:
        all_valid_edges=[]
        for vertex in self.g.keys():
            temp=self.g.__getitem__(vertex)
            if temp is None:
                continue
            else:
                for ele in temp.keys():
                    temp_ele=temp.__getitem__(ele)
                    if(temp_ele is None):
                        continue
                    else:
                        all_valid_edges.append((vertex,ele,temp_ele))
                        self.delete_edge(vertex,ele)
#        print(all_valid_edges)
        
#        sort ascending based on weights
        all_valid_edges.sort(key = lambda x: x[2])
        
        #initialize
        d=DisjointSetUnion()
        unique_vertex=[]
        for each_edge in all_valid_edges:
            if each_edge[0] not in unique_vertex:
#                print("vb", each_edge[0])
                #create normal set
                d.create_set(each_edge[0])
                unique_vertex.append(each_edge[0])
            if each_edge[1] not in unique_vertex:
#                print("vb2", each_edge[1])
                d.create_set(each_edge[1])
                unique_vertex.append(each_edge[1])
#       create mst list
        mst_list=[]

        for each_edge in all_valid_edges:
            find_a=d.find_set(each_edge[0])
            find_b=d.find_set(each_edge[1])
#            print(find_a,find_b)
            if(find_a==find_b): # if they are in same set, then cycle will form hence skipping loop
                continue
            else:
                mst_list.append((each_edge[0],each_edge[1]))
                d.union(find_a,find_b)
           
        return mst_list
        ...

    def shortest_path(self, u: int, v: int) -> List[int]:
        
#        visited for explored vertex and unvisited for not yet explored vertex
        visited=set()
        unvisited=[]
        
#        initialize distnaces of all to some max value
        shortest_distance_list=[9999999] * (len(self.g.keys()))

#        this list is to get parent of vertices
        parent=self.g.keys()
#        print(parent)
        
#        to maintain mapping of all the vertices
        all_keys_mapping=self.g.keys()
#        print(all_keys_mapping)
        
#        set start vertex distance to zero
        shortest_distance_list[parent.index(u)]=0
        
        unvisited.append(u)
        while(len(unvisited)!=0):#explore all vertices
            current_vertex=unvisited.pop(0)
            temp=self.g.__getitem__(current_vertex)
            
            visited.add(current_vertex)

            for neigh in temp.keys():#iterate over all neighbours of current vertex
                w = temp.__getitem__(neigh)
#                This is Relaxation step given in lectures
                if (shortest_distance_list[all_keys_mapping.index(neigh)] > w + shortest_distance_list[all_keys_mapping.index(current_vertex)]):
                    shortest_distance_list[all_keys_mapping.index(neigh)] = w + shortest_distance_list[all_keys_mapping.index(current_vertex)]
                    unvisited.append(neigh)
                    parent[all_keys_mapping.index(neigh)]=current_vertex
                    visited.add(neigh)
        
        print("Shortest distance from", u, "to",v, "is:", shortest_distance_list[all_keys_mapping.index(v)])

#        Backtracking from target to source to get shortest path
        temp=v
        shortest_path_list=[v]
        while(temp!=u):
            
            temp=parent[all_keys_mapping.index(temp)]
            shortest_path_list.append(temp)
        
        return shortest_path_list[::-1]

class Test(unittest.TestCase):
    ...


if __name__ == '__main__':
    unittest.main()
    
    print("=========================Hashtable Implementation=============================")
    
    ht=HashTable(lambda u: u)
    print("Size:",ht.size())
    ht.__setitem__(1,111)
    ht.__setitem__(5,121)
    print("List:",ht.elements)
    ht.__setitem__(9,131)
    ht.__setitem__(1,131)
    ht.__setitem__(5,13431)
    ht.__setitem__(9,134)
    ht.__setitem__(8,34)
    ht.__setitem__(9,34)
    ht.__setitem__(100,100)
    ht.__setitem__(101,100)
    ht.delete(5)
    print("List:",ht.elements)
    print("Size:",ht.size())
    
    
    print("================================================================================")
    
    print("=========================Graph Implementation==================================")
    graph= Graph()
    graph.create_vertex(5)
    graph.create_vertex(6)
    graph.create_vertex(10)
    print(graph.g.keys())
    print(graph.has_edge(5,10))
    
    graph.create_edge(5,10,10)
    graph.create_edge(6,10,1)
    
    print(graph.neighbors(10))
    print(graph.degree(5))
    print(graph.has_edge(5,10))
    
    print(graph.neighbors(10))
    print(graph.has_edge(5,10))
    
    print("================================================================================")

    print("=============================Shortest Path Implementation=======================")
    graph= Graph()
    graph.create_vertex(0)
    graph.create_vertex(1)
    graph.create_vertex(2)
    graph.create_vertex(3)
    graph.create_vertex(4)
    graph.create_vertex(5)
    graph.create_vertex(6)
    graph.create_vertex(7)
    graph.create_vertex(8)
    
    graph.create_edge(0,1,4)
    graph.create_edge(0,7,8)    
    graph.create_edge(1,2,8)
    graph.create_edge(7,8,7)
    graph.create_edge(7,6,1) 
    graph.create_edge(2,8,2)
    
    graph.create_edge(2,5,4)
    graph.create_edge(2,3,7)
    
    graph.create_edge(8,6,6)
    graph.create_edge(6,5,2)
    
    graph.create_edge(3,5,14) 
    graph.create_edge(3,4,9)
    
    graph.create_edge(5,4,10)
    
    print("Path From 0 to 6:", graph.shortest_path(0,6))
    
    print("================================================================================")
    
    print("========================MST Implementation=================================")
    print("MST is:",graph.mst())
    