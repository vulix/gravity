#!/usr/bin/python
from work_queue import *
import sys
path=sys.argv[1] 
try:
    Q = WorkQueue(port = 20994)
    Q.specify_name("ACIC2013")
except:
    print "could not instantiate Work Queue master"
    sys.exit(1)
 
print "Listening on port %d." % Q.port
densitys=os.listdir(path+"/test")
densitys.sort()
grav_positions=os.listdir(path+"/grav_pos")
grav_positions.sort()
print "total density_grids %d " %(len(densitys))
print "Total positions %d" % (len(grav_positions))
#print densitys
#print grav_positions
print "Open a new terminal window to submit workers."
print "Please add cctools directory to your path in the new terminal."
print "submit workers to this queue with -> torque_submit_workers -t 300 servername 20994 100."
for i in range(len(densitys)):
    for j in range(len(grav_positions)):
        outfile = "grav"+str(i)+"_"+str(j)+".txt"
        infile2 = path+"/grav_pos/"+grav_positions[j]
	infile1 = path+"/test/"+densitys[i]
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
