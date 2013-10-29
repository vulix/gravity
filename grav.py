#!/usr/bin/python
import sys
from math import sqrt, pow

def calc_prism( dx, dy, dz, dxMid, dyMid, dzMid, Hfin, posX, posY, posZ):
    #print    dx, dy, dz, dxMid, dyMid, dzMid, Hfin, posX, posY, posZ
    import math
    GAMMA=6.67e-8
    RHO=1

    x = [ dxMid - dx/2 - posX, dxMid + dx/2 - posX ]
    y = [ dyMid - dy/2 - posY, dyMid + dy/2 - posY ]
    z = [ dzMid - dz/2 - posZ, dzMid + dz/2 - posZ ]

    gsum = 0;
    for i in range(2):
        for ii in range(2):
            for iii in range(2):
                rf = math.sqrt((math.pow(x[i],2) + math.pow(y[ii],2) + math.pow(z[iii],2)))
                gsum += math.pow(-1,(i+ii+iii+3))*(x[i]*math.log(y[ii] + rf) + y[ii] * math.log(x[i]+rf) -z[iii]*math.atan(x[i]*y[ii]/z[iii]/rf))

    return GAMMA * Hfin * RHO * 1e8 * gsum

def calc_pointmass( Hfin , dzMid, posZ, dx, dy, dz, rad):
#    print  Hfin , dzMid, posZ, dx, dy, dz, rad 
    return -6.67e-8 * Hfin * 1e8 * dx * dy * dz * (dzMid-posZ)/rad**3

def calc_macmillan( Hfin, dxMid, dyMid, dzMid, posX, posY, posZ, dx, dy, dz, rad):
    #print Hfin, dxMid, dyMid, dzMid, posX, posY, posZ, dx, dy, dz, rad
    alfa = 2*dx**2 - dy**2 - dz**2
    beta = -dx**2 + 2*dy**2 - dz**2
    ome = -dx**2 - dy**2 + 2*dz**2
    abg = alfa * (dxMid-posX)**2 + beta * (dyMid-posY)**2 + ome * (dzMid-posZ)**2

    tm1 = (dzMid-posZ) / rad**3
    tm2 = 5 * (dzMid - posZ) * abg / 24 / rad**7
    tm3 = -ome * (dzMid - posZ) / 24 / rad**5

    return -6.67e-8 * Hfin * 1e8 * dx * dy * dz * (tm1 + tm2 + tm3)


dx, dy, dz = (10., 10., .1)

grav_pos = []
density_grid = []
r2exac = 10.
r2macm = 81.

# read density grid
fid = open(sys.argv[1],'r')
for line in fid:
    density_grid.append([float(x) for x in line.split()])
fid.close()

# read gravimeter positions
fid = open(sys.argv[2],'r')
for line in fid:
    grav_pos.append([float(x) for x in line.split()])
fid.close()
g, g_out  = ([],[])

#fid = open(sys.argv[2]+'.out','w')
old_time_step = 1
for gp in grav_pos:
    g_sum = 0
    g_out =  []   
    for prism in density_grid:
        time_step = prism[0]

        # there's a better way to do this
        if time_step != old_time_step:
            g_out.append([gp[0],old_time_step, g_sum])
            g_sum = 0;
            old_time_step = time_step
        
        dxMid = prism[1]
        dyMid = prism[2]
        dzMid = prism[3]
	hfin  = prism[4]
       
        # Calculate the distance to the mass to determine which formula to use
        rad = sqrt((dxMid-gp[1])**2 + 
                   (dyMid-gp[2])**2 +
                   (dzMid-gp[3])**2)
        r2  = rad**2
        dr2 = dx**2 + dy**2 + dz**2
        f2  = r2 / dr2
        #f2 = 1 
	if f2 <= r2exac: 
            #print 'prism'
            g_prism = calc_prism(dx, dy, dz,
                             dxMid, dyMid, dzMid,
                             hfin,
                             gp[1],gp[2],gp[3])
        elif f2 >= r2macm:
            #print ' mac'
            g_prism = calc_pointmass( hfin, dzMid, gp[3], dx, dy, dz, rad)
        else:
            #print 'pm'
            g_prism = calc_macmillan( hfin, dxMid, dyMid, dzMid, 
                                      gp[1], gp[2], gp[3],
                                      dx, dy, dz, rad)
        #g.append(g_prism)
        g_sum += g_prism
    # add final time step
    g_out.append([gp[0],time_step, g_sum])
    for line in g_out:
        print "%d %d %f"%(int(line[0]),int(line[1]),line[2])

