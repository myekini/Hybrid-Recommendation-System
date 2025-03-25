################### String manipulations    ###########################

# reverse a string using direct method 
from unittest import result
def reverse_string(arr):
    char = ''
    for i in arr:
        char = i + char
    return char
        

# using stack logic
def  reverse_string_stack(arr):
    stack = []
    for i in arr:
        stack.append(i)
    char = ''
    while len(stack) > 0:
        char += stack.pop()
    return char


################### Removing duplicate from a list while maintaining order ###########################
def remove_duplicate(arr):
    seen = set()
    result = []
    
    for i in arr:
        if i not in seen:
            seen.add(i)
            result.append(i)
    return result

print(remove_duplicate([1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9]))



################### checking if a string is palindrome ###########################


def check_palindrome(arr):
    if arr == arr[::-1]:
        return True
    else:
        return False

print(check_palindrome('malayalam'))


################### finding the first non repeating character ###########################
from collections import Counter
def fnrp_check(arr):
    char_count = Counter(arr)
    if char_count:
        for i in arr:
            if char_count[i] == 1:
                return i


################ Sorting algorithms #####################

def sort_arr(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr


############   Merge sort #################

def merge_sort(arr):
    n = len(arr)
    
    #divide
    mid = len(arr) // 2
    
    left_arr = arr[:mid]
    right_arr = arr[mid:]
    
    #recursively sort them
    merge_sort(left_arr)
    merge_sort(right_arr)
    
    #conquer
    i = j = k = 0
    
    while i < len(left_arr) and j < len(right_arr):
        if left_arr[i] < right_arr[j]:
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j +=1
        
        k += 1
        
    while i < len(left_arr):
        arr[k] = left_arr[i]
        i += 1
        k += 1
    while j < len(right_arr):
        arr[k] = right_arr[j]
        j += 1
        k += 1
    return arr

print =(merge_sort([1, 5, 2, 4, 3, 6, 8, 7, 9]))




def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_arr = arr[:mid]
        right_arr = arr[mid:]

        merge_sort(left_arr)
        merge_sort(right_arr)

        i = j = k = 0

        while i < len(left_arr) and j < len(right_arr):
            if left_arr[i] < right_arr[j]:
                arr[k] = left_arr[i]
                i += 1
            else:
                arr[k] = right_arr[j]
                j += 1
            k += 1

        while i < len(left_arr):
            arr[k] = left_arr[i]
            i += 1
            k += 1
        while j < len(right_arr):
            arr[k] = right_arr[j]
            j += 1
            k += 1
    return arr