#!/bin/bash
#download project files
git clone git://github.com/vulix/gravity.git work-queue
#download data files
wget 'http://de.iplantcollaborative.org/dl/d/0e0ab561-8281-4c6f-aa1e-1e4b4b35125e/gravity_data_ACIC_JKennedy.tgz'
tar -zxvf gravity_data_ACIC_JKennedy.tgz
mkdir test
mkdir grav_pos
split -a4 -l $1 test1_density_grid.txt test/grid
split -a4 -l $2 test1_grav_pos.txt grav_pos/pos
#set environmental variables
export PATH=~/cctools/bin:${PATH}
export PYTHONPATH=${PYTHONPATH}:~/cctools/lib/python2.6/site-packages
cd work-queue
python wq.py
python merge.py $3 $4
rm grav*.txt
  
