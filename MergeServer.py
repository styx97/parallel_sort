import socket 
from MergeSort import merge,merge_sort	#Imports mergesort functions 
import random 
import time 
 
def findarray(s):
	start = s.index('[')
	end = s.index(']')
	arr =  s[start+1:end].split(', ')
	return list(map(int,arr))
 
#Create an array to be sorted 
l = 50000
 
 
#print('List length : ', l)
 
# create an unsorted list with random numbers
 
array  = [random.uniform(0, l) for n in range(0, l)] 
print("list length: ",len(array))
 
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
 
arraystring = repr(array) 
#print("the data sent is",arraystring)
conn.sendto(arraystring.encode('utf-8'),addr_list[0])	#Sends array string 
print('Data sent, sorting array...')
 
 
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
 
time_taken = time.time() - start_time	#Calculates and records time_taken 
print('Time taken for multi core sort', time_taken, 'seconds.')	
 
check_sort = time.time()
 
#array_received = eval(arraystring[2:])
#print(findarray(arraystring))
 
sorted_here = merge_sort(array)
 
#evaluating if it's correct by running the sort on a single core 
 
print("Sort truth evaluation: ",sorted_here == eval(arraystring))
single_core = time.time() - check_sort
print("time taken for single core operation: ",single_core)
 
file = open('test_results.txt','a')
file.write("/n") 
file.write("length of list is: %d ,single core time is: %f  ,multi core time is: %f " % (l,single_core,time_taken)) 
file.write("/n")
file.write("time gain : %f" % (single_core/time_taken))
 
file.close() 
 
 
 
 
 
 
