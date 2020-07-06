import numpy as np
import time
import random
import matplotlib.pyplot as plt
import copy
import sys
import threading
#References: https://arxiv.org/pdf/1412.0193.pdf
#References: https://codeblab.com/wp-content/uploads/2009/09/DualPivotQuicksort.pdf

# =============================================================================
# This function sorts the array using insertion sort and returns time taken to sort the array in seconds
# =============================================================================
def insertion_sort(arr):
    start_time=time.time()
    size=len(arr)
    for i in range(1,size):
        key=arr[i]
        j=i-1
        while(j>=0 and key < arr[j]):
            arr[j+1]=arr[j]
            j-=1
        arr[j+1]=key

    return time.time()-start_time


# =============================================================================
# This function internally calls the randomized quick sort and returns time taken for the algorithm to run
# =============================================================================
def quicksort(arr):
    start_time=time.time()
    lo=0
    hi=len(arr)-1
    randomized_quicksort(arr,lo,hi)
    return time.time()-start_time


# =============================================================================
# This function sorts the array using randomized quick sort
# =============================================================================  
def randomized_quicksort(arr,lo,hi):
    if(lo<hi):
        q=randomized_partition(arr,lo,hi)
        randomized_quicksort(arr,lo,q-1)
        randomized_quicksort(arr,q+1,hi)

# =============================================================================
# This function generates a random pivot in lo and hi range
# =============================================================================      
def randomized_partition(arr,lo,hi):
    pivot=random.randint(lo,hi)
    arr[hi],arr[pivot]=arr[pivot],arr[hi]
    return partition(arr,lo,hi)

# =============================================================================
# This function rearranges the subarray in place
# =============================================================================
def partition(arr,lo,hi):
    pivot=arr[hi]
    i=lo-1
    for j in range(lo,hi):
        if arr[j]<=pivot:
            i+=1
            arr[i],arr[j]=arr[j],arr[i]
    arr[i+1],arr[hi]=arr[hi],arr[i+1]
    return i+1 #this returns partitioned index
        
   
# =============================================================================
# This function sorts the array using dual pivot randomized quick sort algorithms and returns time taken to sort the array in seconds
# =============================================================================
def dual_pivot_randomized_quicksort(arr):
    start_time=time.time()
    lo=0
    hi=len(arr)-1
    dual_quicksort(arr,lo,hi)
    return time.time()-start_time

# =============================================================================
# This function sorts the array using dual pivot randomized quick sort
# ============================================================================= 
def dual_quicksort(arr,lo,hi):
    if(lo<hi):
        p1,p2=dual_randomized_partition(arr,lo,hi)
        dual_quicksort(arr,lo,p1-1)
        dual_quicksort(arr,p1+1,p2-1)
        dual_quicksort(arr,p2+1,hi)
        
# =============================================================================
# This function rearranges the subarray in place and also returns partition index
# =============================================================================     
def dual_randomized_partition(arr,lo,hi):
    if(lo>=hi):
        return
    #generating two random pivot indexes
    pivot1=random.randint(lo,hi)
    pivot2=random.randint(lo,hi)
    
    #if they are same, randomize again to get different indexes
    while(pivot1==pivot2):
        pivot1=random.randint(lo,hi)
    #if pivot1 index is greater, swap them
    if(pivot1>pivot2):
        pivot1,pivot2=pivot2,pivot1
    
    pivot1_value=arr[pivot1]
    pivot2_value=arr[pivot2]
    
    #if pivot1 value is greater, swap them
    if(pivot1_value>pivot2_value):
        arr[pivot1],arr[pivot2]=arr[pivot2],arr[pivot1]
        pivot1_value=arr[pivot1]
        pivot2_value=arr[pivot2]
    
    #swapping pivots with lo and high
    arr[pivot1],arr[lo]=arr[lo],arr[pivot1]
    arr[pivot2],arr[hi]=arr[hi],arr[pivot2]
    
    #initializing necessary indexes 
    l=lo+1
    g=hi-1
    k=l
    p=arr[lo]
    q=arr[hi]
    
    
    if(p>q):
        arr[lo],arr[hi]=arr[hi],arr[lo]
        p=arr[lo]
        q=arr[hi]
    
    while(k<=g):
        if arr[k]< p:
            arr[k],arr[l]=arr[l],arr[k]
            l+=1
        elif(arr[k]>=q):
                while(arr[g] > q and k<g):
                    g-=1
                arr[k],arr[g]=arr[g],arr[k]
                g-=1
                if(arr[k]<p):
                    arr[k],arr[l]=arr[l],arr[k]
                    l+=1
        k+=1
    
    l-=1
    g+=1
    arr[l],arr[lo]=arr[lo],arr[l]
    arr[g],arr[hi]=arr[hi],arr[g]
    #returning the partitioned index
    return (l,g)
            
# =============================================================================
# This function has all the main function calls and it also plots the graph
# =============================================================================       
def run(): 
    sys.setrecursionlimit(50000)
    n=[5000,10000,15000,20000,25000,30000]   
    
    plot_insertion_sort= {i:[] for i in range(1,6)} #This dict stores time taken to run input size for insertion sort
    plot_quick_sort= {i:[] for i in range(1,6)} #This dict stores time taken to run input size for randomized quick sort
    plot_dual_pivot_quick_sort= {i:[] for i in range(1,6)} #This dict stores time taken to run input size for dual pivot randomized quick sort
     
    for i in n:
#        Input 1        
        insertion_sort_time=[]
        quick_sort_time=[]
        dual_pivot_quick_sort_time=[]
        for j in range(3):
            arr_1=np.random.randint(low=1,high=i+1,size=i)
            arr_2=copy.deepcopy(arr_1) # deepcopy is used to make a copy of data, since all algorithms are in place, we can not use same array for each sorting technique
            arr_3=copy.deepcopy(arr_1)
            insertion_sort_time.append(insertion_sort(arr_1))
            quick_sort_time.append(quicksort(arr_2))
            dual_pivot_quick_sort_time.append(dual_pivot_randomized_quicksort(arr_3))

        plot_insertion_sort[1].append(sum(insertion_sort_time)/3)
        plot_quick_sort[1].append(sum(quick_sort_time)/3)
        plot_dual_pivot_quick_sort[1].append(sum(dual_pivot_quick_sort_time)/3)
    
    plt.xlabel('Input Size')
    plt.ylabel('Overall Runtime')
    plt.title('Figure 1: Large random inputs')
    plt.grid('Yes')
    plt.plot(n, plot_insertion_sort[1],marker='o', markerfacecolor='orange', markersize=12, color='orange', linewidth=4, label='Insertion Sort')
    plt.plot(n, plot_quick_sort[1],marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4, label='Randomized Quick Sort')
    plt.plot(n, plot_dual_pivot_quick_sort[1],marker='o', markerfacecolor='green', markersize=12, color='green', linewidth=4, label='Dual Pivot Randomized Quick Sort')
    plt.legend()
    plt.savefig('Plot1.png')
    plt.show()

    for i in n:
#        Input 2
        insertion_sort_time=[]
        quick_sort_time=[]
        dual_pivot_quick_sort_time=[]
        for j in range(3):
            arr_1=sorted(np.random.randint(low=1,high=i+1,size=i))
            arr_2=copy.deepcopy(arr_1)
            arr_3=copy.deepcopy(arr_1)
            insertion_sort_time.append(insertion_sort(arr_1))
            quick_sort_time.append(quicksort(arr_2))
            dual_pivot_quick_sort_time.append(dual_pivot_randomized_quicksort(arr_3))

        plot_insertion_sort[2].append(sum(insertion_sort_time)/3)
        plot_quick_sort[2].append(sum(quick_sort_time)/3)
        plot_dual_pivot_quick_sort[2].append(sum(dual_pivot_quick_sort_time)/3)

    plt.xlabel('Input Size')
    plt.ylabel('Overall Runtime')
    plt.title('Figure 2: Non-decreasing inputs')
    plt.plot(n, plot_insertion_sort[2],marker='o', markerfacecolor='orange', markersize=12, color='orange', linewidth=4, label='Insertion Sort')
    plt.plot(n, plot_quick_sort[2],marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4, label='Randomized Quick Sort')
    plt.plot(n, plot_dual_pivot_quick_sort[2],marker='o', markerfacecolor='green', markersize=12, color='green', linewidth=4, label='Dual Pivot Randomized Quick Sort')
    plt.legend()
    plt.grid('Yes')
    plt.savefig('Plot2.png')
    plt.show()

    for i in n:
#        Input 3
        insertion_sort_time=[]
        quick_sort_time=[]
        dual_pivot_quick_sort_time=[]
        for j in range(3):
            arr_1=sorted(np.random.randint(low=1,high=i+1,size=i),reverse=True)
            arr_2=copy.deepcopy(arr_1)
            arr_3=copy.deepcopy(arr_1)
            insertion_sort_time.append(insertion_sort(arr_1))
            quick_sort_time.append(quicksort(arr_2))
            dual_pivot_quick_sort_time.append(dual_pivot_randomized_quicksort(arr_3))

        plot_insertion_sort[3].append(sum(insertion_sort_time)/3)
        plot_quick_sort[3].append(sum(quick_sort_time)/3)
        plot_dual_pivot_quick_sort[3].append(sum(dual_pivot_quick_sort_time)/3)

    plt.xlabel('Input Size')
    plt.ylabel('Overall Runtime')
    plt.title('Figure 3: Non-increasing inputs')
    plt.plot(n, plot_insertion_sort[3],marker='o', markerfacecolor='orange', markersize=12, color='orange', linewidth=4, label='Insertion Sort')
    plt.plot(n, plot_quick_sort[3],marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4, label='Randomized Quick Sort')
    plt.plot(n, plot_dual_pivot_quick_sort[3],marker='o', markerfacecolor='green', markersize=12, color='green', linewidth=4, label='Dual Pivot Randomized Quick Sort')
    plt.legend()
    plt.grid('Yes')
    plt.savefig('Plot3.png')
    plt.show()
    
    for i in n:       
#        Input 4       
        insertion_sort_time=[]
        quick_sort_time=[]
        dual_pivot_quick_sort_time=[]
        for j in range(3):
            arr_1=sorted(np.random.randint(low=1,high=i+1,size=i))
            arr_2=copy.deepcopy(arr_1)
            arr_3=copy.deepcopy(arr_1)

            for k in range(50):
                a=random.randint(0,i-1)
                b=random.randint(0,i-1)
                arr_1[a],arr_1[b] = arr_1[b],arr_1[a]
                arr_2[a],arr_2[b] = arr_2[b],arr_2[a]
                arr_3[a],arr_3[b] = arr_3[b],arr_3[a]
                
            insertion_sort_time.append(insertion_sort(arr_1))
            quick_sort_time.append(quicksort(arr_2))
            dual_pivot_quick_sort_time.append(dual_pivot_randomized_quicksort(arr_3))

        plot_insertion_sort[4].append(sum(insertion_sort_time)/3)
        plot_quick_sort[4].append(sum(quick_sort_time)/3)
        plot_dual_pivot_quick_sort[4].append(sum(dual_pivot_quick_sort_time)/3)

    plt.xlabel('Input Size')
    plt.ylabel('Overall Runtime')
    plt.title('Figure 4: Noisy non-decreasing inputs')
    plt.plot(n, plot_insertion_sort[4],marker='o', markerfacecolor='orange', markersize=12, color='orange', linewidth=4, label='Insertion Sort')
    plt.plot(n, plot_quick_sort[4],marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4, label='Randomized Quick Sort')
    plt.plot(n, plot_dual_pivot_quick_sort[4],marker='o', markerfacecolor='green', markersize=12, color='green', linewidth=4, label='Dual Pivot Randomized Quick Sort')
    plt.legend()
    plt.grid('Yes')
    plt.savefig('Plot4.png')
    plt.show()
     
    
    for i in n:
#        Input 5
        insertion_sort_time=[]
        quick_sort_time=[]
        dual_pivot_quick_sort_time=[]
        for j in range(3):
            arr_1=[1]*i
            arr_2=[1]*i
            arr_3=[1]*i
            insertion_sort_time.append(insertion_sort(arr_1))
            quick_sort_time.append(quicksort(arr_2))
            dual_pivot_quick_sort_time.append(dual_pivot_randomized_quicksort(arr_3))

        plot_insertion_sort[5].append(sum(insertion_sort_time)/3)
        plot_quick_sort[5].append(sum(quick_sort_time)/3)
        plot_dual_pivot_quick_sort[5].append(sum(dual_pivot_quick_sort_time)/3)

    plt.xlabel('Input Size')
    plt.ylabel('Overall Runtime')
    plt.title('Figure 5: Constant-value input')
    plt.plot(n, plot_insertion_sort[5],marker='o', markerfacecolor='orange', markersize=12, color='orange', linewidth=4, label='Insertion Sort')
    plt.plot(n, plot_quick_sort[5],marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4, label='Randomized Quick Sort')
    plt.plot(n, plot_dual_pivot_quick_sort[5],marker='o', markerfacecolor='green', markersize=12, color='green', linewidth=4, label='Dual Pivot Randomized Quick Sort')
    plt.legend()
    plt.grid('Yes')
    plt.savefig('Plot5.png')
    plt.show()    
    
    
#        Input 6
    insertion_sort_time=0
    quick_sort_time=0
    dual_pivot_quick_sort_time=0
    for j in range(100000):
        arr_1=np.random.randint(low=1,high=51,size=50)
        arr_2=copy.deepcopy(arr_1)
        arr_3=copy.deepcopy(arr_1)
        insertion_sort_time+=insertion_sort(arr_1)
        quick_sort_time+=quicksort(arr_2)
        dual_pivot_quick_sort_time+=dual_pivot_randomized_quicksort(arr_3)
    
    print("Insertion Sort Time:",insertion_sort_time)
    print("Quick Sort Time:",quick_sort_time)
    print("Dual Pivot Quick Sort Time:",dual_pivot_quick_sort_time)



threading . stack_size ( int (1e8 ))
t = threading . Thread ( target = run)
t. start ()
t. join () 