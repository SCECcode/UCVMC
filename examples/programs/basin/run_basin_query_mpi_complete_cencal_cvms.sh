#!/bin/bash
##
## example of running on usc cluster
##

if [ -z "$UCVM_INSTALL_PATH" ]; then
  echo "Need to set UCVM_INSTALL_PATH to run >" ${0##*/} 
  exit
fi

if [ -f "/usr/usc/openmpi/default/setup.sh" ]; then
  source /usr/usc/openmpi/default/setup.sh
  echo "Running on usc hpc cluster >" ${0##*/} 
fi

BIN_DIR=${UCVM_INSTALL_PATH}/bin
CONF_DIR=${UCVM_INSTALL_PATH}/conf
TEST=basin_query_mpi_complete_cencal_cvms_z2.5x

salloc --ntasks=2 --time=00:10:00 srun --ntasks=2 -o ${TEST}.srun.out -v ${BIN_DIR}/basin_query_mpi_complete -b ${TEST}.first,${TEST}.firstOrSecond,${TEST}.last,${TEST}.secondOnly,${TEST}.threeLast -o ${TEST}.result,${TEST}.meta.json -f ${CONF_DIR}/ucvm.conf -m cencal,cvms -i 20 -v 2500 -l 35,-122.5 -s 0.1 -x 16 -y 11 



