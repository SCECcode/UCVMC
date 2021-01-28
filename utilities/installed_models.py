#!/usr/bin/env python
# Generate a master mesh grid, out.grd, 
# and time the model population speed of the
# available crustal models 

from subprocess import call, Popen, PIPE, STDOUT
import sys
import os
import time

UCVM_CVMS = {"1d":"1D(1d)", \
             "1dgtl":"1D w/ Vs30 GTL(1dgtl)", \
             "bbp1d":"Broadband Northridge Region 1D Model(bbp1d)", \
             "cvms":"CVM-S4(cvms)", \
             "cvms5":"CVM-S4.26(cvms5)", \
             "cvmsi":"CVM-S4.26.M01(cvms426)", \
             "cca":"CCA 06(cca)", \
             "cs173":"CyperShake 17.3(cs173)", \
             "cs173h":"CyperShake 17.3 with San Joaquin and Santa Maria Basins data(cs173h)", \
             "cvmh":"CVM-H 15.1.1(cvmh1511)", \
             "albacore":"ALBACORE(albacore)", \
             "cencal":"USGS Bay Area Model(cencal)"}

# get installed models
mypath=os.environ.get('UCVM_INSTALL_PATH')
if(mypath == None) :
    print("Need to set UCVM_INSTALL_PATH to run > ucvm_models.py")
    exit(1)

CMD=mypath+"/bin/run_ucvm_query.sh"
proc = Popen([CMD, "-H"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
rawoutput = proc.communicate()[0]
output=rawoutput.decode()
lines = output.split("\n")
target_models=[]

## looking for
##          1d : crustal model
##       bbp1d : crustal model
##        cvmh : crustal model
for line in lines:
    if ": crustal model" in line :
        p = line.split(":")
        u = p[0].strip()
        keys=UCVM_CVMS.keys()
        if( u in keys ) :
          target_models.append(u.encode())
        else:
          pass
    else:
        pass

print(target_models)
