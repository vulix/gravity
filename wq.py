#!/usr/bin/python
 
from work_queue import *
import sys
 
try:
    Q = WorkQueue(port = 9014)
    Q.specify_name("ACIC2013")
except:
    print "could not instantiate Work Queue master"
    sys.exit(1)
 
print "Listening on port %d." % Q.port
densitys=os.listdir('/N/u/xiaoliu/test')
densitys.sort()
grav_positions=os.listdir('/N/u/xiaoliu/grav_pos')
grav_positions.sort()
print "total density_grids %d " %(len(densitys))
print "Total positions %d" % (len(grav_positions))
#print densitys
#print grav_positions
print "working on Jeff's project."
for i in range(len(densitys)):
    for j in range(len(grav_positions)):
        outfile = "grav"+str(i)+"_"+str(j)+".txt"
        infile2 = "/N/u/xiaoliu/grav_pos/"+grav_positions[j]
	infile1 = "/N/u/xiaoliu/test/"+densitys[i]
        #print infile
        command = "python grav.py %s %s > %s" % (infile1, infile2, outfile)
        T = Task(command)
 
        T.specify_file("grav.py", "grav.py", WORK_QUEUE_INPUT, cache = True)
        T.specify_file(infile1, infile1, WORK_QUEUE_INPUT, cache = False)
        T.specify_file(infile2, infile2, WORK_QUEUE_INPUT, cache = False)
        T.specify_file(outfile, outfile, WORK_QUEUE_OUTPUT, cache = False)
 
        taskid = Q.submit(T)
    
print "done."
 
print "Waiting for tasks to complete..."
while not Q.empty():
    T = Q.wait(5)
    if T:
        print "task (id# %d): %s (return result %s)" % (T.id, T.command, T.result)
        print T.output
print "done."