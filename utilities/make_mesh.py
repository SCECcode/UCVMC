#!/usr/bin/env python2
import sys
import os
import time

# Generate the master out.grid

#
# make out.grd
cmd="./makegrid.sh"
os.system(cmd)
print cmd
#
# Call each of the installed crustal models and time how
# long it takes to populate the models
#
#
# model bbp1d
#
start = time.time()
model_string = "bbp1d"
cmd="../bin/ucvm_query -f ../conf/ucvm.conf -m %s < ../utilities/out.grd > mesh_%s.out"%(model_string,model_string)
print cmd
os.system(cmd)
end = time.time()
print "Mesh extraction for model %s : %d seconds"%(model_string,(end-start))
#
#
# model 1d
#
start = time.time()
model_string = "1d"
cmd="../bin/ucvm_query -f ../conf/ucvm.conf -m %s < ../utilities/out.grd > mesh_%s.out"%(model_string,model_string)
print cmd
os.system(cmd)
end = time.time()
print "Mesh extraction for model %s : %d seconds"%(model_string,(end-start))
#
# model CVM-S4
#
start = time.time()
model_string = "cvms"
cmd="../bin/ucvm_query -f ../conf/ucvm.conf -m %s < ../utilities/out.grd > mesh_%s.out"%(model_string,model_string)
print cmd
os.system(cmd)
end = time.time()
print "Mesh extraction for model %s : %d seconds"%(model_string,(end-start))
#
# model CVM-S4.26
#
start = time.time()
model_string = "cvms5"
cmd="../bin/ucvm_query -f ../conf/ucvm.conf -m %s < ../utilities/out.grd > mesh_%s.out"%(model_string,model_string)
print cmd
os.system(cmd)
end = time.time()
print "Mesh extraction for model %s : %d seconds"%(model_string,(end-start))
#
# model CVM-S4.26.M01
#
start = time.time()
model_string = "cvmsi"
cmd="../bin/ucvm_query -f ../conf/ucvm.conf -m %s < ../utilities/out.grd > mesh_%s.out"%(model_string,model_string)
print cmd
os.system(cmd)
end = time.time()
print "Mesh extraction for model %s : %d seconds"%(model_string,(end-start))
#
# model CVM-H v15.1
#
start = time.time()
model_string = "cvmh"
cmd="../bin/ucvm_query -f ../conf/ucvm.conf -m %s < ../utilities/out.grd > mesh_%s.out"%(model_string,model_string)
print cmd
os.system(cmd)
end = time.time()
print "Mesh extraction for model %s : %d seconds"%(model_string,(end-start))
#
# model cencal
#
start = time.time()
model_string = "cencal"
cmd="../bin/ucvm_query -f ../conf/ucvm.conf -m %s < ../utilities/out.grd > mesh_%s.out"%(model_string,model_string)
print cmd
os.system(cmd)
end = time.time()
print "Mesh extraction for model %s : %d seconds"%(model_string,(end-start))
sys.exit(0)
#
# model cca
#
start = time.time()
model_string = "cca"
cmd="../bin/ucvm_query -f ../conf/ucvm.conf -m %s < ../utilities/out.grd > mesh_%s.out"%(model_string,model_string)
print cmd
os.system(cmd)
end = time.time()
print "Mesh extraction for model %s : %d seconds"%(model_string,(end-start))
sys.exit(0)
