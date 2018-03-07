# mergesort using just 1 core 
import MergeSort	#Imports mergesort functions 
import random 
import time 

#Create an array to be sorted 
arraylength = 1000000	#Length of array to be sorted 
print('Length of array is', arraylength) 
array = list(range(arraylength))	#Creates array 
random.shuffle(array)	#Jumbles up array 

#Sort and time sorting process 
start_time = time.time()	#Records start time 
print('Sorting array...') 
array = MergeSort.merge_sort(array)	#Sorts array 
print('Array sorted.') 
time_taken = time.time() - start_time	#Calculates and records time_taken 

print('Time taken to sort is ', time_taken, 'seconds.')
