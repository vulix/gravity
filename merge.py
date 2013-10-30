import sys
import os

pos_num=int(sys.argv[2])
time_step=int(sys.argv[3])
path=sys.argv[1]
output=[[0.0 for i in range(time_step+1)] for j in range(pos_num)]
for i in range(pos_num):
	output[i][0]=i+1
densitys=os.listdir(path+"/test")
densitys.sort()
grav_positions=os.listdir(path+"/grav_pos")
grav_positions.sort()
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
    print a
    f.write(a+'\n')
f.close()
