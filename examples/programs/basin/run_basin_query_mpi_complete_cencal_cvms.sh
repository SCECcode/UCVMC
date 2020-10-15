#!/bin/bash
##
## example of running on usc/hpc cluster
##

if [ -z "$UCVM_INSTALL_PATH" ]; then
  echo "Need to set UCVM_INSTALL_PATH to run >" ${0##*/} 
  exit
fi

if ! [ -f "/usr/usc/openmpi/default/setup.sh" ]; then
## setup hpc mpi environment
  source /usr/usc/openmpi/default/setup.sh
  echo "Running on usc hpc cluster >" ${0##*/} 
fi

BIN_DIR=${UCVM_INSTALL_PATH}/bin
CONF_DIR=${UCVM_INSTALL_PATH}/conf

salloc --ntasks=2 --time=00:10:00 srun --ntasks=2 -v ${BIN_DIR}/basin_query_mpi_complete -b hpc_cencal_cvms_z2.5x.first,hpc_cencal_cvms_z2.5x.firstOrSecond,hpc_cencal_cvms_z2.5x.last,$hpc_cencal_cvms_z2.5x.secondOnly,hpc_cencal_cvms_z2.5x.threeLast -o hpc_cencal_cvms_z2.5x.result,hpc_cencal_cvms_z2.5x.meta.json -f ${CONF_DIR}/ucvm.conf -m cencal,cvms -i 20 -v 2500 -l 35,-122.5 -s 0.1 -x 16 -y 11 



