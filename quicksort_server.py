#server quicksort
import socket
from sorts import qsort,merge
import random ,math
from multiprocessing import Process, Manager ,Queue
import sys,os,time
n = 1000000
cores = 4
#step 1 : divide your array in number pf cores

def quicksort_multi(array_portion):
        manager_list_pi.append(qsort(array_portion))

def merge_multi(list_left,list_right):
        manager_list_pi.append(merge(list_left,list_right))

random.seed(10)

array = [random.uniform(0,n) for i in range(0,n)]
#array = [12,34,123,11,67,35,85,10,24,2,43,35,52,15,57,456]
split_ratio = 3
split_index = (n*split_ratio)//10

array_pi = array[:split_index]
array_pc = array[split_index:]
#print(array_pi)
#making the connection
addr_list = []                                             #list of client addresses



HOST = ''
PORT = 50007
if len(array_pc) > 0:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)               #AF_INET is an address family where a pair(host,port) is used as the first argument to the socket object
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)              # SOCK_STREAM > just a socket type
    s.bind((HOST, PORT))

    s.listen(1)                                        #Listens for (n) number of client connections
    print('Waiting for client...')

    conn, addr = s.accept()                                 #Accepts connection from client
    print('Connected by', addr)
    addr_list.append(addr)


    start_time = time.time()

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
    step = int( math.floor( l1 / cores ) )
    offset = 0
    p = []

    for n in range(0, cores):
        ''' we create a new Process object and assign the "merge_sort_multi" function to it,
        using as input a sublist '''
        if n < cores - 1:
            #pass part of a list to a process

            proc = Process( target=quicksort_multi, args=( array_pi[n*step:(n+1)*step], ) )
        else:
            # get the remaining elements in the list
            proc = Process( target=quicksort_multi, args=( array_pi[n*step:], ) )

        p.append(proc)

    ''' http://docs.python.org/library/multiprocessing.html#multiprocessing.Process.start &
    http://docs.python.org/library/multiprocessing.html#multiprocessing.Process.join each Process '''
    for proc in p:
        proc.start()
    for proc in p:
        proc.join()
    print("length of manager_list_pi",len(manager_list_pi))


    #write the code to receive the manager list from the pc and combine them _S
    if len(array_pc)>0 :
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
        for arr in arrays:
            manager_list_pi.append(arr)
    #   print(array)

    print("length of manager list after receiving arrays from pc ",len(manager_list_pi))
    #for elem in manager_list_pi:
    #    print(elem)



    print('Performing final merge...')
    start_time_final_merge = time.time()
    p = []

    ''' For a core count greater than 2, we can use multiprocessing
    again to merge sublists in parallel '''
    if len(manager_list_pi) > 2:
        while len(manager_list_pi) > 0:
            #print("length of manager list is ",len(manager_list_pi))
            #print(manager_list_pi)
            ''' we remove sublists from the "manager_list_pi" list and pass it as input to the
            "merge_multi" wrapper function of "merge" '''
            proc = Process( target=merge_multi, args=(manager_list_pi.pop(0),manager_list_pi.pop(0)) )
            p.append(proc)
        #print(p)
        # again starting and joining ( this seems like a pattern, doesn't it ... ? )
        for proc in p:
            proc.start()
        for proc in p:
            proc.join()
    # the last two sublists that needs to be merged
    p = []

    #print(manager_list_pi)
    #if len(manager_list_pi) > 2:
    #    while len(manager_list_pi) > 0:
    #        #print("length of manager list is ",len(manager_list_pi))
    #        #print(manager_list_pi)
    #        proc = Process( target=merge_multi, args=(manager_list_pi.pop(0),manager_list_pi.pop(0)) )
    #        p.append(proc)
    #    #print(p)
    #    # again starting and joining ( this seems like a pattern, doesn't it ... ? )
    #    for proc in p:
    #        proc.start()
    #    for proc in p:
    #        proc.join()
    #print(manager_list_pi)

    array_pi  = merge(merge(manager_list_pi[0], manager_list_pi[3]),merge(manager_list_pi[1],manager_list_pi[2]))
    #array_pi = merge(manager_list_pi[0],manager_list_pi[1])
    final_merge_time = time.time() - start_time_final_merge
    print('Final merge duration : ', final_merge_time)
    multi_core_time = time.time() - start_time
    print("multi core time",multi_core_time)
    print(array_pi==sorted(array))
    #print(sorted(array))


    """   for storing the results
    with open('quick_results.txt','a') as file:
        line1 = "  length of array:  " + str(n)
        line2 = '  pi : pc ratio >  ' +  str(split_ratio) + " : " + str(10 - split_ratio)
        line3 = "  total time taken : " + str(multi_core_time)
        line4 = "  sort truth verification " + str(array_pi == sorted(array))
        file.writelines([line1,line2,line3,line4] """
