#!/usr/bin/sh

if [ -z "$UCVM_INSTALL_PATH" ]; then
  echo "Need to set UCVM_INSTALL_PATH to run >" ${0##*/} 
  exit
fi

## setup mpi environment
source /usr/usc/openmpi/default/setup.sh

BIN_DIR=${UCVM_INSTALL_PATH}/bin
CONF_DIR=${UCVM_INSTALL_PATH}/conf
SCRATCH=./scratch

sed 's ${CONF_DIR} '$CONF_DIR' ' small_cvmsi.conf_template | sed 's ${SCRATCH} '$SCRATCH' ' > small_cvmsi.conf

salloc -N 4 --ntasks=8 --time=00:30:00 srun --ntasks=8 -v --mpi=pmi2 ${BIN_DIR}/ucvm2mesh-mpi -f small_cvmsi.conf


