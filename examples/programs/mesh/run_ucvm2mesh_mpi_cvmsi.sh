#!/usr/bin/sh

## setup mpi environment
source /usr/usc/openmpi/default/setup.sh

BIN_DIR=${UCVM_INSTALL_PATH}/bin
CONF_DIR=${UCVM_INSTALL_PATH}/conf
SCRATCH=./scratch

sed 's ${CONF_DIR} '$CONF_DIR' ' small_cvmsi.conf_template | sed 's ${SCRATCH} '$SCRATCH' ' > small_cvmsi.conf

salloc --ntasks=4 --time=00:10:00 srun --ntasks=4 -v --mpi=pmi2 ${BIN_DIR}/ucvm2mesh_mpi -f small_cvmsi.conf



