import socket 
import MergeSort 

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
        d =  str(data) 
        arraystring += d        #Adds data to array string 
        if ']' in d:    #When end of data is received

                break

#eval turns the string into an array
array = eval(arraystring)       
print('Data received, sorting array... ' )


#Sorts the array which it is allocated 
array = MergeSort.merge_sort(array) 
print('Array sorted, sending data...') 


#Converts array into string to be sent back to server 
arraystring = repr(array) 
s.sendall(arraystring.encode('utf-8'))   #Sends array string 
print('Data sent.')

s.close()
