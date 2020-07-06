# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 17:39:38 2020

@author: Sanket Pandilwar
"""
import numpy as np
import time
import random
import matplotlib.pyplot as plt
import copy

# =============================================================================
# This funtion sorts the array using bubble sort with checks and returns time taken to sort the array in seconds
# =============================================================================

def bubble_sort(arr):
    start_time=time.time()
    size=len(arr)
    for i in range(size):
        check=False

        for j in range(size-i-1):
            if(arr[j]>arr[j+1]):
                arr[j],arr[j+1]=arr[j+1],arr[j]
                check=True

        if(check==False):
            break

    return time.time()-start_time

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

if __name__ == "__main__":
    n=[5000,10000,15000,20000,25000,30000]   

    plot_bubble_sort= {i:[] for i in range(1,6)} #This dict stores time taken to run input size for bubble sort
    plot_insertion_sort= {i:[] for i in range(1,6)} #This dict stores time taken to run input size for insertion sort

    for i in n:

#        Input 1
        bubble_sort_time=[]
        insertion_sort_time=[]
        for j in range(3):
            arr_1=np.random.randint(low=1,high=i+1,size=i)
            arr_2=copy.deepcopy(arr_1)
            bubble_sort_time.append(bubble_sort(arr_1))
            insertion_sort_time.append(insertion_sort(arr_2))

        plot_bubble_sort[1].append(sum(bubble_sort_time)/3)
        plot_insertion_sort[1].append(sum(insertion_sort_time)/3)
    
    plt.xlabel('Input Size')
    plt.ylabel('Overall Runtime')
    plt.title('Figure 1: Large random inputs')
    plt.grid('Yes')
    plt.plot(n, plot_bubble_sort[1],marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4, label='Bubble Sort')
    plt.plot(n, plot_insertion_sort[1],marker='o', markerfacecolor='orange', markersize=12, color='orange', linewidth=4, label='Insertion Sort')
    plt.legend()
    plt.savefig('Plot1.png')
    plt.show()

    for i in n:
#        Input 2
        bubble_sort_time=[]
        insertion_sort_time=[]
        for j in range(3):
            arr_1=sorted(np.random.randint(low=1,high=i+1,size=i))
            arr_2=copy.deepcopy(arr_1)
            bubble_sort_time.append(bubble_sort(arr_1))
            insertion_sort_time.append(insertion_sort(arr_2))

        plot_bubble_sort[2].append(sum(bubble_sort_time)/3)
        plot_insertion_sort[2].append(sum(insertion_sort_time)/3)

    plt.xlabel('Input Size')
    plt.ylabel('Overall Runtime')
    plt.title('Figure 2: Non-decreasing inputs')
    plt.plot(n, plot_bubble_sort[2],marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4, label='Bubble Sort')
    plt.plot(n, plot_insertion_sort[2],marker='o', markerfacecolor='orange', markersize=12, color='orange', linewidth=4, label='Insertion Sort')
    plt.legend()
    plt.grid('Yes')
    plt.savefig('Plot2.png')
    plt.show()

    for i in n:
#        Input 3
        bubble_sort_time=[]
        insertion_sort_time=[]
        for j in range(3):
            arr_1=sorted(np.random.randint(low=1,high=i+1,size=i))
            arr_2=copy.deepcopy(arr_1)
            bubble_sort_time.append(bubble_sort(arr_1))
            insertion_sort_time.append(insertion_sort(arr_2))

        plot_bubble_sort[3].append(sum(bubble_sort_time)/3)
        plot_insertion_sort[3].append(sum(insertion_sort_time)/3)

    plt.xlabel('Input Size')
    plt.ylabel('Overall Runtime')
    plt.title('Figure 3: Non-increasing inputs')
    plt.plot(n, plot_bubble_sort[3],marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4, label='Bubble Sort')
    plt.plot(n, plot_insertion_sort[3],marker='o', markerfacecolor='orange', markersize=12, color='orange', linewidth=4, label='Insertion Sort')
    plt.legend()
    plt.grid('Yes')
    plt.savefig('Plot3.png')
    plt.show()
    
    for i in n:
        
#        Input 4
        
        bubble_sort_time=[]
        insertion_sort_time=[]
        for j in range(3):
            arr_1=sorted(np.random.randint(low=1,high=i+1,size=i))
            arr_2=copy.deepcopy(arr_1)

            for k in range(50):
                a=random.randint(0,i-1)
                b=random.randint(0,i-1)
                arr_1[a],arr_1[b] = arr_1[b],arr_1[a]
                arr_2[a],arr_2[b] = arr_2[b],arr_2[a]
                
            bubble_sort_time.append(bubble_sort(arr_1))
            insertion_sort_time.append(insertion_sort(arr_2))

        plot_bubble_sort[4].append(sum(bubble_sort_time)/3)
        plot_insertion_sort[4].append(sum(insertion_sort_time)/3)

    plt.xlabel('Input Size')
    plt.ylabel('Overall Runtime')
    plt.title('Figure 4: Noisy non-decreasing inputs')
    plt.plot(n, plot_bubble_sort[4],marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4, label='Bubble Sort')
    plt.plot(n, plot_insertion_sort[4],marker='o', markerfacecolor='orange', markersize=12, color='orange', linewidth=4, label='Insertion Sort')
    plt.legend()
    plt.grid('Yes')
    plt.savefig('Plot4.png')
    plt.show()
    
#        Input 5
    bubble_sort_time=0
    insertion_sort_time=0
    for j in range(100000):
        arr_1=np.random.randint(low=1,high=51,size=50)
        arr_2=copy.deepcopy(arr_1)
        bubble_sort_time+=bubble_sort(arr_1)
        insertion_sort_time+=insertion_sort(arr_2)

    plot_bubble_sort[5].append(bubble_sort_time)
    plot_insertion_sort[5].append(insertion_sort_time)
    print(bubble_sort_time)
    print(insertion_sort_time)
    
    plt.xlabel('Input Size')
    plt.ylabel('Overall Runtime')
    plt.title('Figure 5: Small random inputs')
    plt.plot([1], plot_bubble_sort[5],marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4, label='Bubble Sort')
    plt.plot([1], plot_insertion_sort[5],marker='o', markerfacecolor='orange', markersize=12, color='orange', linewidth=4, label='Insertion Sort')
    plt.legend()
    plt.grid('Yes')
    plt.savefig('Plot5.png')
    plt.show()