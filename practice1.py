import random
import time 
random.seed(10)


array = [random.randint(0,1000000) for i in range(0,1000000)]
array1 = array[:]

def partition(array,begin,end):         # sorting in place 
    partitionIndex = begin
    pivot = end-1
    for i in range(begin,end-1):
        if array[i] <= array[end-1]:
            array[i],array[partitionIndex] = array[partitionIndex],array[i]
            partitionIndex += 1
    
    array[pivot],array[partitionIndex] = array[partitionIndex],array[pivot]     
    return partitionIndex

def quicksort(array,begin,end):
    if  end > begin :
        partitionIndex = partition(array,begin,end) 
        quicksort(array,begin,partitionIndex)
        quicksort(array,partitionIndex+1,end)

def qsort(array):            #using a three way partitioning 
    less = []
    greater = []
    equal = []

    if len(array) > 1:
        #pivot = random.choice(array)
        pivot = array[0]
        for x in array:
            if x> pivot:
                greater.append(x)
            elif x == pivot:
                equal.append(x)
            elif x < pivot:
                less.append(x)
        return qsort(less) + equal + qsort(greater)
    else : 
        return array                    

def merge(left,right):
    #merges 2 sorted lists together

    result = []
    i, j = 0, 0

    #Goes through both lists
    while i < len(left) and j < len(right):
        #Adds smaller element of the lists to the final list
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result += left[i:]
    result += right[j:]
    #print(result)

    return result

def merge_sort(lst):

    #if there's only 1 element, no need to sort
    if len(lst) < 2:
        return lst
    #breaks down list into 2 halves
    middle = len(lst)//2

    #recursively splits and sorts each half
    left = merge_sort(lst[:middle])
    right = merge_sort(lst[middle:])

    #merges both sorted lists together
    return merge(left, right)



# t1 = time.time()

# quicksort(array,0,len(array))


# t2  = time.time()

# qsort(array1)

# t3 =  time.time()

# print("first sort time ",t2-t1)
# print("second sort time ",t3-t2)
