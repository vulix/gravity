import sys
import os
from work_queue import *
 
try:
    Q = WorkQueue(port = 20994)
    Q.specify_name("ACIC2013")
except:
    print "could not instantiate Work Queue master"
    sys.exit(1)
 
print "Listening on port %d." % Q.port
pos_num=int(sys.argv[1])
time_step=int(sys.argv[2])
path=os.getcwd()
output=[[0.0 for i in range(time_step+1)] for j in range(pos_num)]
for i in range(pos_num):
	output[i][0]=i+1
densitys=os.listdir(path+"/test")
densitys.sort()
grav_positions=os.listdir(path+"/grav_pos")
grav_positions.sort()
print "Running a checkpoint on the completion of all the tasks."
for i in range(len(densitys)):
    for j in range(len(grav_positions)):
        outfile = "grav"+str(i)+"_"+str(j)+".txt"
	if os.path.exists(outfile)==False:
            infile2 = path+"/grav_pos/"+grav_positions[j]
	    infile1 = path+"/test/"+densitys[i]
        #print infile
            command = "python grav.py %s %s > %s" % (infile1, infile2, outfile)
            T = Task(command)
 
            T.specify_file("grav.py", "grav.py", WORK_QUEUE_INPUT, cache = True)
            T.specify_file(infile1, infile1, WORK_QUEUE_INPUT, cache = True)
            T.specify_file(infile2, infile2, WORK_QUEUE_INPUT, cache = True)
            T.specify_file(outfile, outfile, WORK_QUEUE_OUTPUT, cache = False)
 
            taskid = Q.submit(T)
    
print "Waiting for tasks to complete, please submit workers to the queue if it's not empty."
while not Q.empty():
    T = Q.wait(5)
    if T:
        print "task (id# %d): %s (return result %s)" % (T.id, T.command, T.result)
        print T.output
print "done."

for i in range(len(densitys)):
    for j in range(len(grav_positions)):
        current="grav"+str(i)+"_"+str(j)+".txt"
        c=open(current,'r')
        print " curent process %s" % (current)
    	for line in c:
	    entry=[float(x) for x in line.split()]
	    output[int(entry[0])-1][int(entry[1])]=output[int(entry[0])-1][int(entry[1])]+entry[2]
        c.close()
f=open('result.txt','w')
for i in range(pos_num):
    a=" ".join(str(e) for e in output[i])
    f.write(a+'\n')
f.close()
