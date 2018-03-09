import socket 
import MergeSort 
import os, sys, time
import math, random
from multiprocessing import Process, Manager

cores = 4 # for quad core cpu 


# a wrapper function which appends the result of "merge_sort" to the "manager_list" 
def merge_sort_multi( list_part ):
    manager_list.append( merge_sort( list_part ) )

# a wrapper function which appends the result of "merge" to the "manager_list"                               
def merge_multi( list_part_left, list_part_right ):
    manager_list.append( merge(list_part_left, list_part_right ) )


HOST = '192.168.1.1' 
PORT = 50007 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s.connect((HOST, PORT)) 


#Receives arraystring in chunks 
arraystring = '' 
print('Receiving data...' )
while 1:

	data = s.recv(4096)	#Receives data in chunks 
	#print data 
	arraystring += data	#Adds data to array string 
	if ']' in data:	#When end of data is received

		break

#eval turns the string into an array
array = eval(arraystring)	
print('Data received, sorting array... ' )

if cores > 1:
        l = len(array)
        ''' we collect the list element count and the time taken
        for each of the procedures in a file '''
        #f = open('mergesort-'+str(cores)+'.dat', 'a')
        print('Starting %d-core process'%cores)
        start_time = time.time()
        
        # divide the list in "cores" parts
        step = int( math.floor( l / cores ) )
        offset = 0
        p = []
        
        for n in range(0, cores):
            ''' we create a new Process object and assign the "merge_sort_multi" function to it,
            using as input a sublist '''
            if n < cores - 1:
                #pass part of a list to a process 
                
                proc = Process( target=merge_sort_multi, args=( array[n*step:(n+1)*step], ) )
            else:
                # get the remaining elements in the list
                proc = Process( target=merge_sort_multi, args=( array[n*step:], ) )
            
            p.append(proc)

        ''' http://docs.python.org/library/multiprocessing.html#multiprocessing.Process.start &
        http://docs.python.org/library/multiprocessing.html#multiprocessing.Process.join each Process '''
        for proc in p:
            proc.start()
        for proc in p:
            proc.join()
        print('Performing final merge...')
        start_time_final_merge = time.time()
        p = []
        
        ''' For a core count greater than 2, we can use multiprocessing
        again to merge sublists in parallel '''
        if len(manager_list) > 2:
            while len(manager_list) > 0:
                ''' we remove sublists from the "manager_list" list and pass it as input to the
                "merge_multi" wrapper function of "merge" '''
                proc = Process( target=merge_multi, args=(manager_list.pop(0),manager_list.pop(0)) )
                p.append(proc)
            # again starting and joining ( this seems like a pattern, doesn't it ... ? )
            for proc in p:
                proc.start()
            for proc in p:
                proc.join()
        
        # finally we have 2 sublists which need to be merged
        array  = merge(manager_list[0], manager_list[1])
        
        # final_merge_time = time.time() - start_time_final_merge
        # print 'Final merge duration : ', final_merge_time
        # multi_core_time = time.time() - start_time
        # # of course we double-check that we did everything right
        
        # print 'Sorted arrays equal : ', (a == single)
        # print '%d-Core ended: %4.6f sec'%(cores, multi_core_time)
          


#Sorts the array which it is allocated 
#array = MergeSort.mergesort(array) 
#print('Array sorted, sending data...') 


#Converts array into string to be sent back to server 
arraystring = repr(array) 
s.sendall(arraystring)	#Sends array string 
print('Data sent.') 

s.close()
