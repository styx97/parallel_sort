import socket 
import MergeSort	#Imports mergesort functions 
import random 
import time 

#breaks down array into n sections where n is the number of processors 
def breakarray(array, n): 
	sectionlength = len(array)//n	
	result = [] 
	for i in range(n):
		if i < n - 1:
			result.append(array[i*sectionlength:(i+1)*sectionlength])
                                                        
		else:
			result.append(array[i*sectionlength:])

	return result

#Create an array to be sorted 
arraylength = 100000	#Length of array to be sorted 
print('Length of array is',arraylength)
array = list(range(arraylength))	#Creates array 
random.shuffle(array)	#Jumbles up array 


#Specify info on processors/computers 
#procno = int(sys.argv[1])	#number of processors 
procno = 4
print('Number of processors:', procno) 
procID = 0	#ID of this processor(server) 
addr_list = []	                                           #list of client addresses 


#Sets up network 
HOST = '' 
PORT = 50007 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)               #AF_INET is an address family where a pair(host,port) is used as the first argument to the socket object 
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)              # SOCK_STREAM > just a socket type 
s.bind((HOST, PORT)) 

s.listen(procno - 1)	                                   #Listens for (n) number of client connections 
print('Waiting for client...') 

for i in range(procno - 1):	                                #Connects to all clients
	# conn > new socket(uninheritable), object, addr > address
	conn, addr = s.accept()	                                #Accepts connection from client 
	print('Connected by', addr) 
	addr_list.append(addr)	                                 #Adds address to address list

#Start and time distributed computing sorting process	

start_time = time.time()	#Records start time 

sections = breakarray(array,procno)	#splits array into sections for every client 

for i in range(procno - 1):	#Converts array section into string to be sent

	arraystring = repr(sections[i+1]) 
	conn.sendto(arraystring.encode('utf-8'),addr_list[i])	#Sends array string 
	print('Data sent, sorting array...')

array = MergeSort.merge_sort(sections[procID])	#Sorts section and stores it in array 
print('Array sorted.')

for i in range(procno - 1):	#Receives sorted sections from each client

	arraystring = '' 
	print('Receiving data from clients...') 
	while 1:
		data = conn.recv(4096)	#Receives data in chunks 
		d = str(data)
		arraystring += d	#Adds data to array string 
		if ']' in d:	#When end of data is received	
			break
	print('Data received, merging arrays...')	
	array = MergeSort.merge(array, eval(arraystring))	#Merges current array with section from client	
	print('Arrays merged.')

conn.close() 
time_taken = time.time() - start_time	#Calculates and records time_taken 

print('Time taken to sort is ', time_taken, 'seconds.')	
