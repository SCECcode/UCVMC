#!/usr/bin/env sh
## 
## example of running on usc/hpc cluster
##

if [ -z "$UCVM_INSTALL_PATH" ]; then
  echo "Need to set UCVM_INSTALL_PATH to run >" ${0##*/} 
  exit
fi

if ! [ -f "/usr/usc/openmpi/default/setup.sh" ]; then
  echo "Need to be on usc hpc cluster to run >" ${0##*/} 
  exit
fi

## setup mpi environment
source /usr/usc/openmpi/default/setup.sh

BIN_DIR=${UCVM_INSTALL_PATH}/bin
CONF_DIR=${UCVM_INSTALL_PATH}/conf

salloc --ntasks=2 --time=00:10:00 srun --ntasks=2 -v --mpi=pmi2 ${BIN_DIR}/basin_query_mpi -b hpc_cvms5_z2.5.simple -f ${CONF_DIR}/ucvm.conf -m cvms5 -i 20 -v 2500 -l 35.0,-122.5 -s 0.1 -x 16 -y 11




