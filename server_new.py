import socket 
from MergeSort import merge,merge_sort	#Imports mergesort functions 
import random 
import time 
from multiprocessing import Process,Manager

# a wrapper function which appends the result of "merge_sort" to the "manager_list"
def merge_sort_multi( list_part ):
    manager_list.append( merge_sort( list_part ) )
 
# a wrapper function which appends the result of "merge" to the "manager_list"
def merge_multi( list_part_left, list_part_right ):
    manager_list.append( merge(list_part_left, list_part_right ) )
  
#Create an array to be sorted 
l = 50000
cores = 4 # number of cores in rpi3b2
# ratio in which the data will be split between pi and the pc
split_ratio = 1     # a number between 1 to 5
split_index = (l*split_ratio)//5
# create an unsorted list with random numbers
array  = [random.uniform(0, l) for n in range(0, l)] 
print("list length: ",len(array))
 
array_pi = array[:split_index]
array_pc = array[split_index:]

addr_list = []	                                           #list of client addresses 
 
start_time = time.time()
#Sets up network 
HOST = '' 
PORT = 50007 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)               #AF_INET is an address family where a pair(host,port) is used as the first argument to the socket object 
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)              # SOCK_STREAM > just a socket type 
s.bind((HOST, PORT)) 
 
s.listen(1)	                                   #Listens for (n) number of client connections 
print('Waiting for client...') 
 
	                                #Connects to all clients
# conn > new socket(uninheritable), object, addr > address
conn, addr = s.accept()	                                #Accepts connection from client 
print('Connected by', addr) 
addr_list.append(addr)	                                 #Adds address to address list
#print("addr_list > " ,addr_list)
#Start and time distributed computing sorting process	
 
start_time = time.time()	#Records start time 
 
arraystring = repr(array_pc) 
#print("the data sent is",arraystring)
conn.sendto(arraystring.encode('utf-8'),addr_list[0])	#Sends array string 
print('Data sent, sorting array...')

***
if cores > 1:
 
        manager = Manager()
        manager_list  = manager.list()
        l1 = len(array_pi)
 	
        print("length of the array in pi is ",l1)
        
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
 
                proc = Process( target=merge_sort_multi, args=( array_pi[n*step:(n+1)*step], ) )
            else:
                # get the remaining elements in the list
                proc = Process( target=merge_sort_multi, args=( array_pi[n*step:], ) )
 
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
        # the last two sublists that needs to be merged
        array_pi  = merge(manager_list[0], manager_list[1])
 
        final_merge_time = time.time() - start_time_final_merge
        print('Final merge duration : ', final_merge_time)
        multi_core_time = time.time() - start_time
        print("multi core time",multi_core_time)
       

arraystring = '' 
print('Receiving data from client...') 
while 1:
	data = conn.recv(4096)	#Receives data in chunks 
	d = data.decode('utf-8')
 
	arraystring += d	#Adds data to array string 
	if ']' in d:	#When end of data is received	
		break
print("data received from client")
conn.close() 
 
 
array_received = eval(arraystring)
final_array = merge(array_received,array_pi)


time_taken = time.time() - start_time	#Calculates and records time_taken 
print('Time taken for multi core sort', time_taken, 'seconds.')	


 
check_sort = time.time()

 
sorted_here = merge_sort(array)
 
#evaluating if it's correct by running the sort on a single core 
 
print("Sort truth evaluation: ",sorted_here == final_array)
single_core = time.time() - check_sort
print("time taken for single core operation: ",single_core)

 
file = open('test_results.txt','a')
file.write("/n") 
file.write("length of list is: %d ,single core time is: %f  ,multi core time is: %f " % (l,single_core,time_taken)) 
file.write("/n")
file.write("time gain : %f" % (single_core/time_taken))
 
file.close() 
 
 
 
 
 
 
