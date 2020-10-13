#!/usr/bin/env sh

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

rm -rf ucvm2mesh_mpi ucvm.conf small-cvmsi.conf small_cvmsi.grid small_cvmsi.media

BIN_DIR=${UCVM_INSTALL_PATH}/bin
CONF_DIR=${UCVM_INSTALL_PATH}/conf
SCRATCH=./scratch

cp ${BIN_DIR}/ucvm2mesh_mpi .
cp ${CONF_DIR}/ucvm.conf .

sed 's ${CONF_DIR} '$CONF_DIR' ' small_cvmsi.conf_template | sed 's ${SCRATCH} '$SCRATCH' ' > small_cvmsi.conf


salloc -N 4 --ntasks=8 --time=00:30:00 srun --ntasks=8 -v --mpi=pmi2 ${BIN_DIR}/ucvm2mesh_mpi -f small_cvmsi.conf


