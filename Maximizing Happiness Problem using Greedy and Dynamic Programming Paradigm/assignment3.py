# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 23:12:25 2020

@author: Sanket Pandilwar
"""

import unittest

def best_share_sort(a,b):
    """
    For the best share sort, we are sorting after we calculate differenece between alice and bob's happiness, 
    hence we have time complexity of O(N logN + N)=> O(N logN).
    Since, I am using one list to save the difference, we have space compelxity of O(N)
    """
    size=len(a)
    best_share=[]
    for i in range(size):
        best_share.append((i,a[i]-b[i]))
    best_share=list(sorted(best_share,key=lambda i:i[1],reverse=True))
    return [tup[0] for tup in best_share[:size//2]]



def best_share_dp(a,b):
    """
    For best share dp method, I am creating array of (n+1) x (n+1) to store maximum happiness at each stage, 
    whose values will be used again and again. Hence I have space complexity of O((N+1)^2 + N/2)= O(N^2)
    For the time complexity, I have two for loops to calculate and memoize the happiness for all the items. 
    Hence I have a time complexity of O(C+N^2+N)=> O(N^2)
    """
    size=len(a)
    dp=[[0 for i in range(size+1)] for j in range(size+1)]
    
    for i in range(1,size+1):
        for j in range(i+1):
            if j==0:
                dp[i][j]=dp[i-1][j]+b[i-1]
                continue
            if i==j:
                dp[i][j]=dp[i-1][j-1]+a[i-1]
                continue
            dp[i][j]= max(a[i-1]+dp[i-1][j-1], b[i-1]+dp[i-1][j]) 
#    print(dp)
#    print(dp[size][size//2])
    best_dp=[]
    index=size//2
#    print(index)
    for i in range(size,0,-1):
        if (dp[i][index]-a[i-1] == dp[i-1][index-1]) and index>0:
            best_dp.append(i-1)
#            print(dp[i][index])
            index=index-1
#        print(dp[i][index])
#    print(best_dp)  
    return best_dp

#
class Tests(unittest.TestCase):
    def test_1(self):
        a = [10,20,30,40]
        b = [8,8,25,35]
        output = [[1,2],[1,3]] 
        self.assertIn(sorted(best_share_sort(a,b)),output,"Best share sort Failed")
        self.assertIn(sorted(best_share_dp(a,b)),output,"Best share DP Failed")
        
    def test_2(self):
        a = [10,20,30,40]
        b = [8,18,25,35]
        output = [[2,3]] 
        self.assertIn(sorted(best_share_sort(a,b)),output,"Best share sort Failed")
        self.assertIn(sorted(best_share_dp(a,b)),output,"Best share DP Failed")
        
    def test_3(self):
        a=[10,10,10,10]
        b = [8,18,25,35]
        output = [[0,1]] 
        self.assertIn(sorted(best_share_sort(a,b)),output,"Best share sort Failed")
        self.assertIn(sorted(best_share_dp(a,b)),output,"Best share DP Failed")
        
    def test_4(self):
        a=[10,10,10,10,10,10,10,10]
        b = [20,20,20,20,20,20,20,20]
        output = [[0,1,2,3],[1,2,3,4],[2,3,4,5],[4,5,6,7],[2,4,6,7]] 
        self.assertIn(sorted(best_share_sort(a,b)),output,"Best share sort Failed")
        self.assertIn(sorted(best_share_dp(a,b)),output,"Best share DP Failed")
        
    def test_5(self):
        a=[1,1,1,1,1,1]
        b = [1,1,1,1,1,1]
        output = [[0,1,2],[3,4,5],[1,2,3]] 
        self.assertIn(sorted(best_share_sort(a,b)),output,"Best share sort Failed")
        self.assertIn(sorted(best_share_dp(a,b)),output,"Best share DP Failed")
    
    def test_6(self):
        a=[]
        b = []
        output = [[]] 
        self.assertIn(sorted(best_share_sort(a,b)),output,"Best share sort Failed")
        self.assertIn(sorted(best_share_dp(a,b)),output,"Best share DP Failed")
        
    def test_7(self):
        a=[2,1]
        b = [1,2]
        output = [[0]] 
        self.assertIn(sorted(best_share_sort(a,b)),output,"Best share sort Failed")
        self.assertIn(sorted(best_share_dp(a,b)),output,"Best share DP Failed")


if __name__ == "__main__":
    unittest.main()
#    a=[10,10,10,10]
#    b = [8,18,25,35]
#    a=[1,1,1,1,1,1]
#    b = [1,1,1,1,1,1]
#    a=[10,20,30,40]
#    b=[8,18,25,35]  
#    a=[10,20,30,40]
#    b=[8,8,25,35]   
#    a=[10,10,10,10,10,10,10,10]
#    b = [20,20,20,20,20,20,20,20]
#    a=[]
#    b = [1,1,1]
#    a=[2,1]
#    b = [1,2]
    
#    if(len(a)==0 or len(b)==0 or len(a)!=len(b) or len(a)%2!=0 or len(b)%2!=0):
#        print("Empty Array!!")
#        
#    print(best_share_sort(a,b))
#    print(best_share_dp(a,b))