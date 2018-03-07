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
# a = [1,23,212,286]
# b = [12,102,115,421]

def binary_find(array,element):
    n = len(array)
    start,end = 0,n
    if element > array[-1] :
        return n
    elif element < array[0] :
        return 0
    else :

        while (end-start > 1):
            #print(start,end)
            mid  = (start + end)//2
            if element == array[mid]:
                return mid
            if element > array[mid]:
                start = mid
            else :
                end = mid

        return start + 1

#print(binary_find(a,2))


def merge_parallel(a,b):

  jointarray = [0]*(len(a)+len(b))

  for i in range(len(a)):
      index = i + binary_find(b,a[i])
      #print(a[i],index)
      jointarray[index] = a[i]

  for i in range(len(b)):
      index = i + binary_find(a,b[i])
      #print(b[i],index)
      jointarray[index] = b[i]


  return jointarray

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

# array = [1,34,45,12,65,9,56]
# print(merge_sort(array))
