#!/bin/bash
#download project files
wget https://github.com/vulix/gravity/archive/master.zip
unzip master
#download data files
wget 'http://de.iplantcollaborative.org/dl/d/0e0ab561-8281-4c6f-aa1e-1e4b4b35125e/gravity_data_ACIC_JKennedy.tgz'
tar -zxvf gravity_data_ACIC_JKennedy.tgz
chmod go+w -R gravity-master/
cd gravity-master
mkdir test
mkdir grav_pos
split -a4 -l $1 ../test1_density_grid.txt test/grid
split -a4 -l $2 ../test1_grav_pos.txt grav_pos/pos
set environmental variables
export PATH=~/cctools/bin:${PATH}
export PYTHONPATH=${PYTHONPATH}:~/cctools/lib/python2.6/site-packages
python wq.py
python merge.py $3 $4
rm grav*.txt
cd ..
chmod go-w -R gravity-master/
