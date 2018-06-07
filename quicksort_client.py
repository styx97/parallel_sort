import socket
from sorts import qsort,merge
import os, sys, time
import math, random
from multiprocessing import Process, Manager
 
cores = 4 # for quad core cpu
 
 
# a wrapper function which appends the result of "merge_sort" to the "manager_list"
def merge_sort_multi( list_part ):
    manager_list.append(qsort( list_part ) )
 
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
 
        data = s.recv(4096)     #Receives data in chunks
        #print data
        d = data.decode('utf-8')
        arraystring += d        #Adds data to array string
        if ']' in d:    #When end of data is received
 
                break
 
#eval turns the string into an array
array = eval(arraystring)
#print(array)

print('Data received, sorting array... ' )
#print("the received array is",array,type(array))
 
 
if len(array) > 0:

    manager = Manager()
    manager_list  = manager.list()
    l = len(array)

    print("length of the array is ",l)
    
    print('Starting %d-core process'%cores)
    start_time = time.time()

    # divide the list in number of parts equal to cores
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
    # this may look weird, but is the accepted syntax (ref to docs) 
    for proc in p:
        proc.start()
    for proc in p:
        proc.join()
    
    print("length of manager_list is",len(manager_list))    
    print("sending the arrays to pi")    
    pi_array = list(manager_list)
    arraystring = repr(pi_array)
    #print(arraystring)
    s.sendall(arraystring.encode('utf-8'))  #Sends array string
    print('Data sent.')
    #print('Performing final merge...')
    #start_time_final_merge = time.time()
    #p = []

    # ''' For a core count greater than 2, we can use multiprocessing
    # again to merge sublists in parallel '''
    # if len(manager_list) > 2:
    #     while len(manager_list) > 0:
    #         ''' we remove sublists from the "manager_list" list and pass it as input to the
    #         "merge_multi" wrapper function of "merge" '''
    #         proc = Process( target=merge_multi, args=(manager_list.pop(0),manager_list.pop(0)) )
    #         p.append(proc)
    #     # again starting and joining ( this seems like a pattern, doesn't it ... ? )
    #     for proc in p:
    #         proc.start()
    #     for proc in p:
    #         proc.join()
    # # the last two sublists that needs to be merged
    # array  = merge(manager_list[0], manager_list[1])

    #final_merge_time = time.time() - start_time_final_merge
    #print('Final merge duration : ', final_merge_time)
    multi_core_time = time.time() - start_time
    print("multi core time",multi_core_time)
    #print("the sorted array is ",array)
    #print('Array sorted, sending data...')
    #Converts array into string to be sent back to server
    
else:
    print("length of received part is zero, aborting ")
    
