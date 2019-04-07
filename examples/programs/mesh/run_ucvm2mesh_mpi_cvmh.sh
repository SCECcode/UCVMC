#!/usr/bin/sh

## setup mpi environment
source /usr/usc/openmpi/default/setup.sh

BIN_DIR=${UCVM_INSTALL_PATH}/bin
CONF_DIR=${UCVM_INSTALL_PATH}/conf
SCRATCH=./scratch

sed 's ${CONF_DIR} '$CONF_DIR' ' small_cvmsh.conf_template | sed 's ${SCRATCH} '$SCRATCH' ' > small_cvmsh.conf

salloc --ntasks=2 --time=00:10:00 srun --ntasks=2 -v --mpi=pmi2 ${BIN_DIR}/ucvm2mesh_mpi -f small_cvmsh.conf



