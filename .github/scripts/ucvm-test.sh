#!/bin/bash

source $UCVM_INSTALL_PATH/conf/ucvm_env.sh
cd $UCVM_INSTALL_PATH/tests
./run-testing | tee result.txt

p=`grep -c FAIL result.txt` 

if [ $p != 0 ]; then
   echo "something wrong.."
   exit 1 
else
   echo "okay"
   exit 0
fi
