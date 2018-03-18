# Distributed Merge 

## Distributing a sorting task from a raspberry pi to a computer.

Here , we have tried to sort an array of 50k floats by using all the cores of a connected pc. The result is then sent back to the pi and validated against sorting on a single core using the same algorithm (here, mergesort). 

First, connect your pc with the pi using an ethernet cable, and edit the eth0 connectivities. 

On your pi,write : 
  
     sudo ifconfig eth0 192.168.1.1 broadcast 192.168.1.255 netmask 255.255.255.0
and on your pc, write   
    
     sudo ifconfig eth0 192.168.1.2 broadcast 192.168.1.255 netmask 255.255.255.0

Then, run MergeServer.py from the raspberry and MergeClient.py from the pc. The MergeSort.py should obviously be in the same directory. 

For sorting 500000 randomly generated float values,the distributed sorting is about 5 times faster on average in the pi.
Tested in python3 with a Raspberry Pi 3 B2. 


In future, similar approaches can be taken where a task will be scheduled from a pi to a machine with larger computing power (such as a cluster of computers in a cloud) and the pi will just show the results. 


### Motivations 
The Cambridge tutorial on distributed computing - 
https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/distributed-computing/

George Psarakis's tutorial on multiprocessing - 
https://devopslog.wordpress.com/2012/04/15/mergesort-example-using-python-multiprocessing/
