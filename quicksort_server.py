#server quicksort
import socket
from sorts import qsort,merge
import random ,math
from multiprocessing import Process, Manager ,Queue
import sys,os,time
n = 100000
cores = 4
#step 1 : divide your array in number pf cores

def quicksort_multi(array_portion):
        manager_list_pi.append(qsort(array_portion))

def merge_multi(list_left,list_right):
        manager_list_pi.append(merge(list_left,list_right))

random.seed(10)

array = [random.uniform(0,n) for i in range(0,n)]
#array = [12,34,123,11,67,35,85,10,24,2,43,35,52,15,57,456]
split_ratio = 7
split_index = (n*split_ratio)//10

array_pi = array[:split_index]
array_pc = array[split_index:]

#making the connection
addr_list = []                                             #list of client addresses

start_time = time.time()

HOST = ''
PORT = 50007
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)               #AF_INET is an address family where $
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)              # SOCK_STREAM > just a socket type
s.bind((HOST, PORT))

s.listen(1)                                        #Listens for (n) number of client connections
print('Waiting for client...')

conn, addr = s.accept()                                 #Accepts connection from client
print('Connected by', addr)
addr_list.append(addr)


#sending data to pc
arraystring = repr(array_pc)
conn.sendto(arraystring.encode('utf-8'),addr_list[0])
print('data sent to pc')
if cores > 1 :
    manager = Manager()
    manager_list_pi = manager.list()
    l1 = len(array_pi)

    print("length of the array in pi is ",l1)

    print('Starting %d-core process'%cores)
    start_time = time.time()

    # divide the list in number of parts equal to cores
    step = int( math.floor( n / cores ) )
    offset = 0
    p = []

    for n in range(0, cores):
        
        if n < cores - 1:
            #pass part of a list to a process

            proc = Process( target=quicksort_multi, args=( array_pi[n*step:(n+1)*step], ) )
        else:
            # get the remaining elements in the list
            proc = Process( target=quicksort_multi, args=( array_pi[n*step:], ) )

        p.append(proc)
      
    for proc in p:
        proc.start()
    for proc in p:
        proc.join()
    print("length of manager_list_pi",len(manager_list_pi))


    #write the code to receive the manager list from the pc and combine them _S
    print('receiving arrays from pc')
    received_string = ''
    while 1:
        data = conn.recv(2048)
        d = data.decode('utf-8')
        received_string += d
        #print(received_string)
        if ']]' in d:
            break
    print('arrays received from pc')


    arrays  = eval(received_string)
    #print(arrays)
    for array in arrays:
        manager_list_pi.append(array)
    #   print(array)

    print("length of manager list after receiving arrays from pc ",len(manager_list_pi))
    
    print('Performing final merge...')
    start_time_final_merge = time.time()
    p = []

    ''' For a core count greater than 2, we can use multiprocessing
    again to merge sublists in parallel '''
    if len(manager_list_pi) > 2:
        while len(manager_list_pi) > 0:
            ''' we remove sublists from the "manager_list_pi" list and pass it as input to the
            "merge_multi" wrapper function of "merge" '''
            proc = Process( target=merge_multi, args=(manager_list_pi.pop(0),manager_list_pi.pop(0)) )
            p.append(proc)
        # again starting and joining ( this seems like a pattern, doesn't it ... ? )
        for proc in p:
            proc.start()
        for proc in p:
            proc.join()
    # the last two sublists that needs to be merged
    array_pi  = merge(manager_list_pi[0], manager_list_pi[1])

    final_merge_time = time.time() - start_time_final_merge
    print('Final merge duration : ', final_merge_time)
    multi_core_time = time.time() - start_time

